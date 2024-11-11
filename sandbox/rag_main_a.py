from langchain_community.document_loaders import PDFPlumberLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaLLM
from langchain import hub
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import PromptTemplate


# Load the PDF
# loader = PDFPlumberLoader("11pests1disease.pdf")
loader = PDFPlumberLoader("หน้าที่คนประจำเรือ.pdf")

docs = loader.load()

# embedding_model_name = "all-MiniLM-L6-v2"
embedding_model_name = "intfloat/multilingual-e5-large"

# Instantiate the embedding model
embedder = HuggingFaceEmbeddings(model_name=embedding_model_name)

# Split into chunks
text_splitter = SemanticChunker(embedder)
documents = text_splitter.split_documents(docs)

# Create the vector store and fill it with embeddings
vector = FAISS.from_documents(documents, embedder)


retriever = vector.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# Define llm
llm = OllamaLLM(model="llama3")

# Prompt
# prompt = hub.pull("rlm/rag-prompt")

prompt = """
1. Use the following pieces of context to answer the question at the end. 
2. If you don't know the answer, just say that "I don't know" but don't make up an answer on your own.
3. Try to answer in Thai language.

Context: {context}

Question: {question}

Helpful Answer:"""

QA_CHAIN_PROMPT = PromptTemplate.from_template(prompt)

# Post-processing
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | QA_CHAIN_PROMPT
    | llm
    | StrOutputParser()
)

# Question
ans = rag_chain.invoke("ความรับผิดชอบของ นายเรือ Captain or Master ตอบคำถามแยกเป็น ข้อๆ")
print(ans)