import faiss
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from your_config import OPENAI_API_KEY
import os
from langchain.vectorstores import FAISS
import shutil
import logging
import time

def create_vector_store(text_chunks):
    try:
        logging.info("Creating vector store...")
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        vector_store = FAISS.from_texts(text_chunks, embeddings)
        vector_store.save_local("vector_store")
        logging.info("Vector store created and saved successfully.")
        return vector_store
    except Exception as e:
        logging.error(f"Error creating vector store: {e}")
        raise

def load_vector_store():
    try:
        if not os.path.exists('vector_store'):
            raise Exception("Vector store not found or corrupted. Please reprocess your files.")
        
        logging.info("Loading vector store...")
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        vector_store = FAISS.load_local("vector_store", embeddings)
        logging.info("Vector store loaded successfully.")
        return vector_store
    except Exception as e:
        logging.error(f"Failed to load vector store: {str(e)}")
        raise