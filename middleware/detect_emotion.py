import pickle
import threading
from time import sleep

from flask_socketio import SocketIO
from opencv.utils import resize_image, get_face_landmarks
import cv2


class EmotionDetector:
    def __init__(self, frontend_socket: SocketIO):
        self.model = None
        self.frontend_socket = frontend_socket

        self.load_model('middleware/opencv/model')
        self.emotions = ['😡', '😃', '😐', '😮']

    def load_model(self, path):
        with open(path, 'rb') as f:
            self.model = pickle.load(f)

    def from_camera(self):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        while ret:
            ret, frame = cap.read()
            emotion = self.detect_emotion(frame)
            self.frontend_socket.emit('emotion', emotion)
            sleep(1)

    def detect_emotion(self, frame: cv2.typing.MatLike):
        frame = resize_image(frame, 200, 292)
        face_landmarks = get_face_landmarks(
            frame, draw=False, static_image_mode=False)

        if not face_landmarks:
            return None

        output = self.model.predict([face_landmarks])

        return self.emotions[int(output[0])]

    def start_detection_thread(self):
        detection_thread = threading.Thread(target=self.from_camera)
        detection_thread.daemon = True
        detection_thread.start()
