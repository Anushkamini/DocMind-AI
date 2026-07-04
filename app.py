from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import shutil
import os

from embed import get_embedding
from vector_db import add_embedding, search, get_all_data

app = FastAPI()

# Ensure uploads folder exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Frontend
@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html") as f:
        return f.read()

# Upload API
@app.post("/upload")
async def upload_file(file: UploadFile):

    path = f"uploads/{file.filename}"

    # Save file
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Read content (text files only)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    # AI processing
    embedding = get_embedding(text)
    add_embedding(embedding, text)

    return {"status": "Document stored successfully!!"}


# Query API
class Query(BaseModel):
    question: str

@app.post("/query")
def query(data: Query):
    query_embedding = get_embedding(data.question)
    result = search(query_embedding)
    return {"answer": result}


# Text embedding API
class TextData(BaseModel):
    text: str

@app.post("/embed")
def embed_text(data: TextData):
    embedding = get_embedding(data.text)
    add_embedding(embedding, data.text)
    return {"status": "Text embedded and stored successfully !!"}


# Get stored data
@app.get("/data")
def get_data():
    return get_all_data()