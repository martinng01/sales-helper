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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app)


def on_open(ws):
    print("Connected to WhisperLive", flush=True)
    uid = str(uuid.uuid4())
    ws.send(json.dumps(
        {
            "uid": uid,
            "language": 'en',
            "task": 'transcribe',
            "model": 'small',
            "use_vad": True
        }
    ))


def on_message(ws, message):
    print(message, flush=True)


frontend_socket = SocketIO(app, cors_allowed_origins="*")
whisperlive_socket = WebSocketApp(
    "ws://0.0.0.0:9090", on_open=lambda ws: on_open(ws), on_message=lambda ws, message: on_message(ws, message), on_error=lambda ws, error: print(error))


@frontend_socket.on('connect')
def handle_connect():
    print("New client connected", flush=True)


@frontend_socket.on('message event')
def handle_message_from_process_text_file(message):
    print(message)
    frontend_socket.emit('message', message)


@frontend_socket.on('audio')  # TODO: not receiving audio
def on_audio_chunk(data):
    try:
        if whisperlive_socket.sock and whisperlive_socket.sock.connected:
            whisperlive_socket.send(data, ABNF.OPCODE_BINARY)
        else:
            print("WebSocket connection is closed", flush=True)
    except Exception as e:
        print(f"Failed to send data: {e}", flush=True)


# @frontend_socket.on('disconnect')
# def handle_disconnect():
#     global thread_stop_event
#     thread_stop_event.set()
#     print("Client disconnected")


if __name__ == '__main__':
    frontend_socket_thread = threading.Thread(
        target=frontend_socket.run, kwargs={'app': app, 'host': '0.0.0.0', 'port': 8765})
    frontend_socket_thread.daemon = True
    frontend_socket_thread.start()
    # frontend_socket.run(app, host='0.0.0.0', port=8765)

    whisperlive_socket_thread = threading.Thread(
        target=whisperlive_socket.run_forever)
    whisperlive_socket_thread.daemon = True
    whisperlive_socket_thread.start()

    frontend_socket_thread.join()
    whisperlive_socket_thread.join()
