import collections
import queue
import threading

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

            if score < threshold:
                return

            result = self.rag.rag(doc.page_content)
            self.frontend_socket.emit('rag', result)

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
