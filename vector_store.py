import faiss
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from config import OPENAI_API_KEY

def create_vector_store(text_chunks):
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vector_store = FAISS.from_texts(text_chunks, embeddings)
    vector_store.save_local("vector_store")
    return vector_store

def load_vector_store():
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    return FAISS.load_local("vector_store", embeddings)

import shutil

def load_vector_store():
    import os
    if not os.path.exists('vector_store'):
        raise Exception("Vector store not found or corrupted. Please reprocess your files.")
    
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    return FAISS.load_local("vector_store", embeddings)
"""
import faiss
from openai.embeddings_utils import get_embedding
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

class VectorStore:
    def __init__(self):
        self.index = faiss.IndexFlatL2(512)  # Assuming 512-dimensional embeddings
        self.data = []

    def add_data(self, content, metadata=None):
        embedding = get_embedding(content, "text-embedding-ada-002")  # Text embeddings
        self.index.add([embedding])
        self.data.append({"content": content, "metadata": metadata})

    def add_image(self, image_file):
        model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        image = Image.open(image_file).convert("RGB")
        inputs = processor(images=image, return_tensors="pt")
        embedding = model.get_image_features(**inputs).detach().numpy()
        self.index.add(embedding)

    def search(self, query, top_k=5):
        embedding = get_embedding(query, "text-embedding-ada-002")
        distances, indices = self.index.search([embedding], top_k)
        return [self.data[idx] for idx in indices[0]]
"""