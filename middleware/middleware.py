"""
Facilitates communication between the react front-end and the WhisperLive backend.

Handles data transformation. RAG.
"""

import json
import threading
import eventlet
import uuid

if eventlet:
    eventlet.monkey_patch()
    from flask_cors import CORS
    from flask_socketio import SocketIO
    from flask import Flask
    from websocket import WebSocketApp, ABNF


class MiddlewareServer:
    def __init__(self, frontend_host='0.0.0.0', frontend_port=8765, backend_url='ws://0.0.0.0:9090'):
        self.frontend_host = frontend_host
        self.frontend_port = frontend_port
        self.backend_url = backend_url

        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'secret!'
        CORS(self.app)

        self.frontend_socket = SocketIO(self.app, cors_allowed_origins="*")
        self.backend_socket = WebSocketApp(
            'ws://0.0.0.0:9090',
            on_open=self.backend_on_open,
            on_message=self.backend_on_message,
            on_error=self.backend_on_error
        )

        self.setup_frontend_routes()

    def setup_frontend_routes(self):
        @self.frontend_socket.on('connect')
        def handle_connect():
            print("New client connected", flush=True)

        @self.frontend_socket.on('audio')
        def on_audio_chunk(data):
            """
            Receives audio data from the front-end and forwards it to the WhisperLive backend.
            """
            try:
                if self.backend_socket.sock and self.backend_socket.sock.connected:
                    self.backend_socket.send(data, ABNF.OPCODE_BINARY)
                else:
                    print("WebSocket connection is closed", flush=True)
            except Exception as e:
                print(f"Failed to send data: {e}", flush=True)

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

        print(message, flush=True)
        self.frontend_socket.emit('transcript', message)

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


if __name__ == '__main__':
    server = MiddlewareServer()
    server.run()
