from langchain_community.document_loaders import PDFPlumberLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains import RetrievalQA



# Load the PDF
# loader = PDFPlumberLoader("11pests1disease.pdf")
loader = PDFPlumberLoader("sandbox/หน้าที่คนประจำเรือ.pdf")
docs = loader.load()

# Instantiate the embedding model
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

# Define the prompt
prompt = """
1. Use the following pieces of context to answer the question at the end.
2. If you don't know the answer, just say that "I don't know" but don't make up an answer on your own.
3. Try to answer in Thai language.

Context: {context}

Question: {question}

Helpful Answer:"""

QA_CHAIN_PROMPT = PromptTemplate.from_template(prompt)

llm_chain = LLMChain(
    llm=llm,
    prompt=QA_CHAIN_PROMPT,
    callbacks=None,
    verbose=True)

document_prompt = PromptTemplate(
    input_variables=["page_content", "source"],
    template="Context:\ncontent:{page_content}\nsource:{source}",
)

combine_documents_chain = StuffDocumentsChain(
    llm_chain=llm_chain,
    document_variable_name="context",
    document_prompt=document_prompt,
    callbacks=None)

qa = RetrievalQA(
    combine_documents_chain=combine_documents_chain,
    verbose=True,
    retriever=retriever,
    return_source_documents=True)


# print(qa("How does plant respond to disease?")["result"])
print(qa("ความรับผิดชอบของ นายเรือ Captain or Master ตอบคำถามแยกเป็น ข้อๆ")["result"])
