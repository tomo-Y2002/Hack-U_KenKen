from django.shortcuts import render
from django.http import HttpResponse,StreamingHttpResponse,JsonResponse
from django.views.decorators import gzip
from django.views.decorators.clickjacking import xframe_options_exempt
import cv2
import numpy as np
from HACKU.settings import BASE_DIR
from collections import deque
from hoyou.models import Person, Record, Shuttai
import time
from django.utils.timezone import now
import copy
import base64
from django.core.files.base import ContentFile
from video2vec import HumanInFrame, video2vec
import hoyou.views
from hoyou import functions
import itertools
from django.shortcuts import redirect

buffer = deque(maxlen=1000)
flag = None
count = 0
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        global buffer
        global flag
        global count
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        buffer.append(image)
        count += 1
        if(flag == "main" and count%60 == 0 and len(buffer) > 120):
            frames = copy.copy(list(itertools.islice(buffer, len(buffer)-120, len(buffer)-1)))
            if(HumanInFrame.HumanInFrame(frames[60])):
                flag = "processing"
                fps = 30
                h, w = frames[0].shape[:2]
                fmt = cv2.VideoWriter_fourcc('a', 'v', 'c', '1')
                writer = cv2.VideoWriter(str(BASE_DIR)+"/media/test/myvid.mp4", fmt, fps, (w, h), 0)
                for frame in frames:
                    writer.write(frame)
                writer.release()
                vector = video2vec.video2vec("C:/Users/denjo/Hack-U_KenKen/HACKU/media/test/myvid.mp4", "C:/Users/denjo/Hack-U_KenKen/HACKU/video2vec/model_0.832.pth")
                id = functions.inner_product(vector)
                person=Person.objects.get(id=id)
                newest=Record.objects.filter(person=person)
                if(not newest.exists()):
                    shuttai = Shuttai.shukkin if newest.last().shuttai == Shuttai.taikin else Shuttai.taikin if newest.last().shuttai == Shuttai.shukkin else Shuttai.shukkin
                else:
                    shuttai = Shuttai.shukkin
                functions.create_record(id, shuttai)
                flag = "main"
                buffer.clear()
                count = 0
        return jpeg.tobytes()

def gen(camera):
    global flag
    while True:
        if(flag == "processing"):
            yield 0
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def index(request):
    global buffer
    if(len(buffer)):
        if request.method == "POST":
            if "savefig" in request.POST:
                cv2.imwrite(str(BASE_DIR)+"/media/test/myfig.jpg", buffer[-1])
            if "savevid" in request.POST:
                frames = copy.copy(buffer)
                fps = 30
                h, w = frames[0].shape[:2]
                fmt = cv2.VideoWriter_fourcc('a', 'v', 'c', '1')
                writer = cv2.VideoWriter(str(BASE_DIR)+"/media/test/myvid.mp4", fmt, fps, (w, h), 0)
                for frame in frames:
                    writer.write(frame)
                writer.release()
    buffer.clear()
    return render(request ,'index.html')

@ gzip.gzip_page
@ xframe_options_exempt
def capture(request):
    return StreamingHttpResponse(gen(VideoCamera()),content_type='multipart/x-mixed-replace; boundary=frame')

@ xframe_options_exempt
def test_flag(request):
    def event_stream():
        global flag
        while True:
            current_time = now().strftime("%Y-%m-%d %H:%M:%S")
            if(now().second < 30):  
                flag = True
                yield f"data: {current_time}\n\n"  # リアルタイムデータをストリームとして送信
            else:
                flag = False
                yield ""
            time.sleep(1)  # 1秒ごとに更新

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    return response

def test_register(request):
    global flag
    print("pushed")
    if(flag):
        return HttpResponse("ok")
    else:
        return index(request)
    
def hoyou_register(request):
    global buffer
    global flag
    global count
    flag = "hoyou_register"
    if request.method == "POST":
        if "next" in request.POST:
            frames = copy.copy(buffer)
            fps = 30
            h, w = frames[0].shape[:2]
            fmt = cv2.VideoWriter_fourcc('a', 'v', 'c', '1')
            writer = cv2.VideoWriter(str(BASE_DIR)+"/media/test/myvid.mp4", fmt, fps, (w, h), 0)
            for frame in frames:
                writer.write(frame)
            writer.release()
            vector = video2vec.video2vec("C:/Users/denjo/Hack-U_KenKen/HACKU/media/test/myvid.mp4", "C:/Users/denjo/Hack-U_KenKen/HACKU/video2vec/model_0.832.pth")
            binary_data = request.session["image"]  # クライアントからのデータを取得
            image_data = base64.b64decode(binary_data.split(',')[1])  # Data URIをデコード
            image = ContentFile(image_data, name=request.session["family_name"]+request.session["first_name"]+request.session["birthday"]+'.jpg')
            Person.objects.create(family_name=request.session["family_name"], first_name=request.session["first_name"], email=request.session["email"], birthday=request.session["birthday"], image=image, vector=vector)
            buffer.clear()
            return redirect('home')
            # else:
            #     return redirect('camera:hoyou_register')
    buffer.clear()
    count = 0
    return render(request, "register_vector.html")

def ajax_recieve(request):
    for key, value in request.POST.items():
        request.session[key] = value
    return JsonResponse({"result":"ok"})

def main(request):
    global buffer
    global flag
    global count
    flag = "main"
    
    buffer.clear()
    count = 0
    return render(request, "main.html")

def test():
    video2vec.video2vec("C:/Users/denjo/Hack-U_KenKen/HACKU/media/test/myvid.mp4", "C:/Users/denjo/Hack-U_KenKen/HACKU/video2vec/model_0.832.pth")