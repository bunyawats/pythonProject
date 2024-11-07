 
pip install fastapi uvicorn   
pip install langchain psycopg2-binary pgvector psycopg2 transformers  
pip install torch  
pip install -U langchain-community 
pip install langchain-huggingface
pip install langchain_ollama
pip install langchain==0.1.14
pip install langchain-experimental==0.0.56
pip install langchain-community==0.0.31
pip install faiss-cpu==1.8.0
pip install pdfplumber==0.11.0
pip install gradio==4.25.0
brew install huggingface-cli


pip install langchain
pip install langchain-experimental
pip install langchain-community
pip install faiss-cpu
pip install pdfplumber
pip install gradio


pip install -U "huggingface_hub[cli]"
huggingface-cli --help

Your token has been saved to /Users/bunyawatsingchai/.cache/huggingface/token


pip install --upgrade pip


uvicorn app.main:app --reload

curl http://127.0.0.1:8000/items/1


curl -X 'POST' \
  'http://127.0.0.1:8000/items/123' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
        "name": "Sample Item",
        "description": "A sample item description",
        "price": 12.99,
        "quantity": 5
      }'


curl -X 'POST' \
  'http://127.0.0.1:8000/items/123' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'api_key: your-expected-api-key' \
  -d '{
        "name": "Sample Item",
        "description": "A sample item description",
        "price": 12.99,
        "quantity": 5
      }'

CREATE EXTENSION vector;

CREATE TABLE embeddings (
    id SERIAL PRIMARY KEY,
    text TEXT,
    embedding VECTOR(768) -- Adjust dimension based on the embedding model used
);
