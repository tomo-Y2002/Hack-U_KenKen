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

buffer = deque([], maxlen=100)
flag = False
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

def gen(camera):
    while True:
        frame = camera.get_frame()
        buffer.append(frame)
        if(len(buffer) == 100):
            flag = True
            HttpResponse("Hello, World")
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def tm():
    while True:
        yield str(time.time_ns())

def index(request):
    if(len(buffer)):
        if request.method == "POST":
            if "start" in request.POST:
                frame = np.frombuffer(buffer.pop(), np.uint8)
                jpeg = cv2.imdecode(frame, cv2.IMREAD_UNCHANGED)
                cv2.imwrite(str(BASE_DIR)+"/media/test/myjpeg.jpg", jpeg)
    if(len(buffer) >= 99):
        return render(request ,'index.html', context={"persons":Person.objects.all()})
    else:
        return render(request ,'index.html')

@ gzip.gzip_page
@ xframe_options_exempt
def capture(request):
    return StreamingHttpResponse(gen(VideoCamera()),content_type='multipart/x-mixed-replace; boundary=frame')

@ xframe_options_exempt
def test_flag(request):
    def event_stream():
        while True:
            current_time = now().strftime("%Y-%m-%d %H:%M:%S")
            yield f"data: {current_time}\n\n"  # リアルタイムデータをストリームとして送信
            time.sleep(1)  # 1秒ごとに更新

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    return response

def test_register(request):
    print("pushed")
    return index(request)
    # return HttpResponse("ok")