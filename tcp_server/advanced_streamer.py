from flask import Flask, Response
try:
    import cv3 as cv
except  ImportError:
    import cv2 as cv
from gevent.wsgi import WSGIServer


class Singleton(type):
    _class_instanciated = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._class_instanciated:
            cls._class_instanciated[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._class_instanciated[cls]


class Video():
    __metaclass__ = Singleton

    def __init__(self):
        self.cap = cv.VideoCapture(0)

    def read_video_frame(self):
        ret, frame = self.cap.read()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        return gray.tobytes()


app = Flask(__name__)


def event_genertor(video):
    while True:
        frame = video.read_video_frame()
        data = frame  +  b'\r\n\r\n'
        yield data


@app.route('/stream')
def video():
    return Response(
        event_genertor(Video()),
        mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.debug = True
    host = "0.0.0.0"
    port = 5000
    server = WSGIServer((host, port), app)
    server.serve_forever()
