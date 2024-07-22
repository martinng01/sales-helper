"""
Facilitates communication between the react front-end and the WhisperLive backend.

Handles data transformation. RAG.
"""

import json
from multiprocessing import Process
import threading
import eventlet
import uuid


if eventlet:
    eventlet.monkey_patch()
    from detect_emotion import EmotionDetector
    from transcript_processor import TranscriptProcessor
    from flask_cors import CORS
    from flask_socketio import SocketIO
    from flask import Flask
    from websocket import WebSocketApp, ABNF


class MiddlewareServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'secret!'
        CORS(self.app)

        self.frontend_socket = SocketIO(
            self.app, cors_allowed_origins="*")
        self.backend_socket = WebSocketApp(
            'ws://0.0.0.0:9090',
            on_open=self.backend_on_open,
            on_message=self.backend_on_message,
            on_error=self.backend_on_error
        )

        self.setup_frontend_routes()

        self.transcript_processor = TranscriptProcessor(self.frontend_socket)
        self.emotion_detector = EmotionDetector(self.frontend_socket)

        self.emotion_detector.start_detection_thread()

    def setup_frontend_routes(self):
        @self.frontend_socket.on('connect')
        def handle_connect():
            print("New client connected", flush=True)

        @self.frontend_socket.on('audio')
        def on_audio_chunk(data):
            """
            Receives audio data from the front-end and forwards it to the WhisperLive backend.
            """
            if self.backend_socket.sock and self.backend_socket.sock.connected:
                self.backend_socket.send(data, ABNF.OPCODE_BINARY)

        @self.frontend_socket.on('video')
        def on_video_chunk(data):
            """
            Receives video data from the front-end and forwards it to emotion detection.
            """
            print(data)

    def backend_on_open(self, ws):
        """
        Sets up a client connection to the WhisperLive backend.
        """

        print("Connected to WhisperLive", flush=True)
        ws.send(json.dumps({
            "uid": str(uuid.uuid4()),
            "language": 'en',
            "task": 'transcribe',
            "model": 'small',
            "use_vad": True
        }))

    def backend_on_message(self, ws, message):
        """
        Receives messages from the WhisperLive backend and forwards them to the front-end.
        """
        message_json = json.loads(message)
        if 'message' in message_json:
            print(message_json['message'])
        elif 'segments' in message_json:
            text = ''
            for segment in json.loads(message)['segments']:
                text += segment['text']
            self.frontend_socket.emit('transcript', text)
            self.transcript_processor.add_transcript(text)
        else:
            print(message_json)

    def backend_on_error(self, ws, error):
        print(f"WebSocket error: {error}", flush=True)

    def run(self):
        frontend_socket_thread = threading.Thread(
            target=self.frontend_socket.run, kwargs={'app': self.app, 'host': '0.0.0.0', 'port': 8765})
        frontend_socket_thread.daemon = True
        frontend_socket_thread.start()

        backend_socket_thread = threading.Thread(
            target=self.backend_socket.run_forever)
        backend_socket_thread.daemon = True
        backend_socket_thread.start()

        frontend_socket_thread.join()
        backend_socket_thread.join()

        frontend_socket_thread.join()
        backend_socket_thread.join()


if __name__ == '__main__':
    server = MiddlewareServer()
    server.run()
