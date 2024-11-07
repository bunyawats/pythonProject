# app/main.py
from fastapi import FastAPI
from app.routes import example_route
from app.routes import item_route

app = FastAPI()

# Register routes
app.include_router(example_route.router)
app.include_router(item_route.router)

@app.get("/")
def read_root():
    return {"message": "Hello, this is a simple REST Microservice with FastAPI"}
