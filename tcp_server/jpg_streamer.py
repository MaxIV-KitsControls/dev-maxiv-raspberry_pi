""" Flask server example to display RPI camera under serveral webbrowser """

from flask import Flask, Response

try:
    import cv3 as cv
except ImportError:
    import cv2 as cv
from gevent.pypwsgi import WSGIServer
from gevent.queue import Queue
import gevent
from time import time
from weakref import WeakSet
import logging

# Setup logger
logger = logging.getLogger(__name__)

# Setup list for client queues
listeners = WeakSet()

# Flask application
app = Flask(__name__)


class TimeIt:
    """ Context manager to time excecution """

    def __init__(self, prefix=""):
        self.prefix = prefix

    def __enter__(self):
        self.ref = time()

    def __exit__(self, *arg):
        logger.debug("{}:{}s".format(self.prefix, time() - self.ref))


class Singleton(type):
    """ Singleton metaclass implementation """

    _cls = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._cls:
            cls._cls[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._cls[cls]


class Video:
    """ Manage the video capture """

    __metaclass__ = Singleton

    def __init__(self):
        # Setup open CV capture
        self.cap = cv.VideoCapture(0)
        # Define resolution
        # TODO: Make resolustion configurable ?
        self.cap.set(3, 1920.0)
        self.cap.set(4, 1080.0)

    def read_video_frame(self):
        with TimeIt("Video::read_video_frame"):
            ret, frame = self.cap.read()
            # Encode frame to jpg
            img = cv.imencode(".jpg", frame)
            return img[1].tobytes()


def video_capture():
    """ A continious video acquisition"""
    video_cap = Video()
    while True:
        # Get frame only when client
        if len(listeners):
            frame = video_cap.read_video_frame()
            # Send the video frame to all clients
            for q in listeners:
                q.put(frame)
        # Force sleep time to manage other client.
        # TODO: make it configurable ?
        gevent.sleep(0.1)


def event_genertor(queue, q_id):
    """ Handle one client connection """
    while True:
        with TimeIt("Queue {}:: Wait for data".format(q_id)):
            # Wait for video acquisition
            frame = queue.get()
        # Publish a video a frame.
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
        )


@app.route("/stream")
def video():
    logger.info("New client connection.")
    queue = Queue()
    listeners.add(queue)
    logger.info("{} client listining".format(len(listeners)))
    return Response(
        event_genertor(queue, len(listeners)),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


def main():
    logging.basicConfig(level=logging.DEBUG)
    global app
    app.debug = True
    host = "0.0.0.0"
    port = 5000
    server = WSGIServer((host, port), app)
    # Schedule the acquistion greenlet
    gevent.spawn(video_capture)
    server.serve_forever()


if __name__ == "__main__":
    main()
