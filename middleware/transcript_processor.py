import collections
import json
import queue
import threading
import uuid

from flask_socketio import SocketIO
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from rag import RAG
import nltk


class TranscriptProcessor:
    def __init__(self, frontend_socket: SocketIO):
        self.frontend_socket = frontend_socket
        self.rag = RAG()
        self.memory = collections.deque()
        self.prev_doc = None
        self.topics_db = Chroma(
            collection_name='topics',
            embedding_function=HuggingFaceEmbeddings(
                model_name='all-MiniLM-L6-v2'),
            persist_directory='middleware/vectordb/chroma_db'
        )
        self.query_queue = queue.Queue()
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._process_queue)
        self.thread.start()

    def _process_queue(self):
        while not self.stop_event.is_set():
            try:
                transcript = self.query_queue.get(
                    timeout=5)  # Adjust timeout as needed
                self.process_transcript(transcript)
                self.query_queue.task_done()
            except queue.Empty:
                continue

    def process_transcript(self, transcript):
        """
        Determines if transcript should be sent to RAG.
        """
        threshold = 0.5

        sentences = nltk.sent_tokenize(transcript)
        for sentence in sentences:
            if sentence in self.memory:
                continue

            self.memory.append(sentence)
            doc, score = self.topics_db.similarity_search_with_relevance_scores(
                sentence, k=1)[0]
            print(f'sentence={sentence}, score={score}')

            # If the similarity score is below the threshold, skip
            if score < threshold:
                return

            # If question to be answered is the same as the previous one, skip
            if self.prev_doc and doc == self.prev_doc:
                continue
            self.prev_doc = doc

            result = self.rag.rag(sentence)
            self.frontend_socket.emit('rag', json.dumps({
                'id': str(uuid.uuid4()),
                'text': result,
                'transcript': sentence
            }))

    def add_transcript(self, transcript):
        """
        Adds a transcript to the processing queue.
        """
        self.query_queue.put(transcript)

    def stop(self):
        """
        Stops the background thread and waits for it to finish.
        """
        self.stop_event.set()
        self.thread.join()
