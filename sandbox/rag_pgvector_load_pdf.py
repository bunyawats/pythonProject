from langchain_community.document_loaders import PDFPlumberLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_postgres.vectorstores import PGVector
from langchain_huggingface import HuggingFaceEmbeddings
from sqlalchemy import URL
from sqlalchemy import create_engine

embedding_model_name = "intfloat/multilingual-e5-large"
embedder = HuggingFaceEmbeddings(model_name=embedding_model_name)
collection_name = "my_docs"
url_object = URL.create(
    "postgresql+psycopg",
    username="gouser",
    password="A1u$35#24",  # plain (unescaped) text
    host="localhost",
    database="go",
)
engine = create_engine(url_object)
vector_store = PGVector(
    embeddings=embedder,
    collection_name=collection_name,
    use_jsonb=True,
    connection=engine,
)

# Load the PDF
loader = PDFPlumberLoader("หน้าที่คนประจำเรือ.pdf")
docs = loader.load()
# Split into chunks
text_splitter = SemanticChunker(embedder)
documents = text_splitter.split_documents(docs)

vector_store.delete_collection()
vector_store.create_collection()

vector_store.add_documents(documents)
