import numpy as np
import json
import os

DATA_FILE = "data.json"

# Load data safely
if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []
else:
    data = []

embeddings = [np.array(item["embedding"]) for item in data]
documents = [item["text"] for item in data]

def save_data():
    data = [
        {
            "text": documents[i],
            "embedding": embeddings[i].tolist()
        }
        for i in range(len(documents))
    ]

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_embedding(embedding, text):
    embeddings.append(embedding)
    documents.append(text)
    save_data()
    print("Data saved! Total documents:", len(documents))

def search(query_embedding):
    similarities = []

    for emb in embeddings:
        denom = (np.linalg.norm(query_embedding) * np.linalg.norm(emb))
        if denom == 0:
            sim = 0
        else:
            sim = np.dot(query_embedding, emb) / denom

        similarities.append(sim)

    if not similarities:
        return "No documents yet"

    best_index = np.argmax(similarities)
    return documents[best_index]

def get_all_data():
    return [
        {
            "text": documents[i],
            "embedding": embeddings[i].tolist()
        }
        for i in range(len(documents))
    ]