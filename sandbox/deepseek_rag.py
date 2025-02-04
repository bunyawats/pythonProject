import logging
import os
from typing import List

import psutil
from dotenv import load_dotenv
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_ollama.llms import OllamaLLM
from langchain_text_splitters import RecursiveCharacterTextSplitter

pathDir = os.path.join(os.getcwd(), ".env")
load_dotenv(pathDir)
huggingfacehub_api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

class RAGPipeline:
    def __init__(self, model_name: str = "llama2:7b-chat-q4", max_memory_gb: float = 3.0):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.check_system_memory(max_memory_gb)

        # Load the language model (LLM)
        self.llm = OllamaLLM(model=model_name)

        # Initialize embeddings using a lightweight model
        self.embeddings = HuggingFaceEndpointEmbeddings(
            model="intfloat/multilingual-e5-large",
            model_kwargs={'device': 'cpu'},  # Use CPU for efficiency
            huggingfacehub_api_token=huggingfacehub_api_token,
        )

        # Define the prompt template
        self.prompt = ChatPromptTemplate.from_template("""
        Answer the question based only on the following context. 
        Translated into Thai
        Be concise. If you cannot find the answer in the context, say "I cannot answer this based on the provided context."

        Context: {context}
        Question: {question}
        Answer: """)


    def check_system_memory(self, max_memory_gb: float):
        available_memory = psutil.virtual_memory().available / (1024 ** 3)
        self.logger.info(f"Available system memory: {available_memory:.1f} GB")
        if available_memory < max_memory_gb:
            self.logger.warning("Memory is below recommended threshold.")

    def load_and_split_documents(self, file_path: str) -> List[Document]:
        loader = PDFPlumberLoader(file_path)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len,
            add_start_index=True,
        )
        splits = text_splitter.split_documents(documents)
        self.logger.info(f"Created {len(splits)} document chunks")
        return splits

    def create_vectorstore(self, documents: List[Document]) -> FAISS:
        batch_size = 32
        vectorstore = FAISS.from_documents(documents[:batch_size], self.embeddings)

        for i in range(batch_size, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            vectorstore.add_documents(batch)
            self.logger.info(f"Processed batch {i // batch_size + 1}")
        return vectorstore

    def setup_rag_chain(self, vectorstore: FAISS, documents: List[Document]):
        retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 2, "fetch_k": 3})

        def format_docs(docs):
            print(docs)
            return "\n\n".join(doc.page_content for doc in documents)

        rag_chain = (
                {"context": retriever | format_docs, "question": RunnablePassthrough()}
                | self.prompt
                | self.llm
                | StrOutputParser()
        )
        return rag_chain

    def query(self, chain, question: str) -> str:
        memory_usage = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        self.logger.info(f"Memory usage: {memory_usage:.1f} MB")
        return chain.invoke(question)


def main():
    rag = RAGPipeline(model_name="deepseek-r1:8b", max_memory_gb=3.0)

    documents = rag.load_and_split_documents("หน้าที่คนประจำเรือ.pdf")
    vectorstore = rag.create_vectorstore(documents)
    chain = rag.setup_rag_chain(vectorstore, documents)

    question = "หน้าที่ กับตันเรือ ('Thai wen bu shi Zhong wen')"
    response = rag.query(chain, question)
    print(f"Question: {question}\nAnswer: {response}")


if __name__ == "__main__":
    main()
