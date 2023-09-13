from django.shortcuts import render
from django.http import HttpResponse,StreamingHttpResponse
from django.views.decorators import gzip
from django.views.decorators.clickjacking import xframe_options_exempt
import cv2
import numpy as np
import io
from HACKU.settings import BASE_DIR
from collections import deque
from hoyou.models import Person
import time
from django.utils.timezone import now
import copy

buffer = deque(maxlen=1000)
flag = False
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        global buffer
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        buffer.append(image)
        return jpeg.tobytes()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def tm():
    while True:
        yield str(time.time_ns())

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
                fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                writer = cv2.VideoWriter(str(BASE_DIR)+"/media/test/myvid.mp4", fmt, fps, (w, h), 0)
                for frame in frames:
                    writer.write(frame)
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