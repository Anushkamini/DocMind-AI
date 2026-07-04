from transformers import AutoTokenizer, AutoModel
import torch

# Load model once
model_name = "jinaai/jina-embeddings-v2-base-en"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    
    # Mean pooling
    embedding = outputs.last_hidden_state.mean(dim=1)
    
    return embedding.detach().numpy()[0]