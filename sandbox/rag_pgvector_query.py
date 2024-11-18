from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain_postgres.vectorstores import PGVector
from langchain_huggingface import HuggingFaceEmbeddings
from sqlalchemy import URL
from sqlalchemy import create_engine

embedding_model_name = "intfloat/multilingual-e5-large"
# embedding_model_name = "scb10x/typhoon-7b"
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

retriever = vector_store.as_retriever(
    # search_type="mmr",
    # search_kwargs={"k": 2, "fetch_k": 2, "lambda_mult": 0.5},
)

# Define llm
llm = OllamaLLM(model="llama3")

prompt = """
1. Use the following pieces of context to answer the question at the end. 
2. If you don't know the answer, just say that "I don't know" but don't make up an answer on your own.
3. Please answer the question in Thai language.

Context: {context}

Question: {question}

Helpful Answer:"""

QA_CHAIN_PROMPT = PromptTemplate.from_template(prompt)


# Post-processing
def format_docs(docs):
    context = "\n\n".join(doc.page_content for doc in docs)
    print(context)
    print("\n" + ("-" * 100))
    return context


# Chain
rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | QA_CHAIN_PROMPT
        | llm
        | StrOutputParser()
)

# question = "ความรับผิดชอบของ นายเรือ Captain or Master ตอบคำถามแยกเป็น ข้อๆ"
question = "แสดง สารบัญ ของเอกสารนี้"

for x in range(3):
    print("\n" + str(x) + ")  " + ("%" * 100))
    ans = rag_chain.invoke(question)
    print(ans)
