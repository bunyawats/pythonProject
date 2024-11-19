from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector
from sqlalchemy import URL, create_engine


def create_pgvector_store(embedder):

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

    return vector_store

# embedding_model_name = "scb10x/typhoon-7b"
embedding_model_name = "intfloat/multilingual-e5-large"
embedder = HuggingFaceEmbeddings(model_name=embedding_model_name)
