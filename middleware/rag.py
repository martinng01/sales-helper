import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from openai import OpenAI
from prompts import RAG_PROMPT, QUESTION_PROMPT

load_dotenv(override=True)


class RAG:
    def __init__(self):
        self.openai_client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.db = Chroma(
            collection_name='ads',
            embedding_function=HuggingFaceEmbeddings(
                model_name='all-MiniLM-L6-v2'),
            persist_directory='middleware/chroma_db'
        )

    def rag(self, transcript):
        """
        Generates a response to the user query based on the audio transcript.
        """

        k = 2

        question = self.transcript_to_question(transcript)
        docs = self.retrieve_documents(question, k)

        prompt = RAG_PROMPT.format(
            context_str='\n'.join([doc.page_content for doc in docs]),
            query_str=question
        )

        result = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return result.choices[0].message.content

    def transcript_to_question(self, transcript):
        """
        Generates a question to send to the RAG model based on the audio transcript.
        """

        prompt = QUESTION_PROMPT.format(transcript=transcript)

        query_completion = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        query_result = query_completion.choices[0].message.content
        return query_result

    def retrieve_documents(self, query, k):
        """
        Retrieves the top k most relevant documents from the Qdrant index based on the query.
        """

        return self.db.as_retriever(
            search_type="similarity", search_kwargs={"k": k}).invoke(query)


rag = RAG()
print(rag.rag('How to advertise on TikTok?'))
