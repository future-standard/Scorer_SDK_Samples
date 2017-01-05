import zmq
import cv2
import time
import threading
import pickle

#ZMQ scoket String
web_socket1      = "ipc://@/scorer/web-sdk1"
web_socket2      = "ipc://@/scorer/web-sdk2"
web_socket3      = "ipc://@/scorer/web-sdk3"
web_socket4      = "ipc://@/scorer/web-sdk4"

class Camera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread

    def __init__(self, index):
        #ZMQ
        if index == 1:
            self.web_socket = web_socket1
        elif index == 2:
            self.web_socket = web_socket2
        elif index == 3:
            self.web_socket = web_socket3
        elif index == 4:
            self.web_socket = web_socket4
        else:
            self.web_socket= ""

        ctx = zmq.Context()
        self.web_sock = ctx.socket(zmq.SUB)
        self.web_sock.setsockopt_string(zmq.SUBSCRIBE, '')
        self.web_sock.setsockopt(zmq.RCVHWM, 1)
        self.web_sock.connect(self.web_socket)

    def initialize(self):
        if Camera.thread is None:
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread, args=(self,))
            Camera.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        self.initialize()
        return self.frame

    @classmethod
    def _thread(cls, self):
        while True:
            serialized = self.web_sock.recv()
            cvdata = pickle.loads(serialized)
            if cvdata == None:
                continue

            ret, jpeg = cv2.imencode('.jpg', cvdata)
            cls.frame=jpeg.tostring()
        cls.thread = None
