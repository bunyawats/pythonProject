from langchain_community.document_loaders import PDFPlumberLoader
from langchain_experimental.text_splitter import SemanticChunker

from sandbox.rag_pgvector_store import create_pgvector_store, embedder

vector_store = create_pgvector_store(embedder)

# Load the PDF
loader = PDFPlumberLoader("หน้าที่คนประจำเรือ.pdf")
docs = loader.load()
# Split into chunks
text_splitter = SemanticChunker(embedder, breakpoint_threshold_type="interquartile")
documents = text_splitter.split_documents(docs)
for document in documents:
    print("\n"+("-"*100))
    print(document.page_content)


vector_store.delete_collection()
vector_store.create_collection()
vector_store.add_documents(documents)
