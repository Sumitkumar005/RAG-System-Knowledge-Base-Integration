import streamlit as st
from preprocessors import process_uploaded_files
from vector_store import create_vector_store, load_vector_store
from conversational_chain import get_conversational_chain
import os

# Load and render HTML content
vector_store =  None
conversation_chain = None


# Streamlit UI
st.title("RAG System: Knowledge Base Integration")
st.sidebar.title("Upload Files")

# File Upload
uploaded_files = st.sidebar.file_uploader(
    "Upload files for processing",
    type=["pdf", "docx", "txt", "csv", "json", "png", "jpg", "jpeg", "mp3", "wav", "mp4", "avi", "mkv"],
    accept_multiple_files=True
)

if st.sidebar.button("Process Files"):
    if uploaded_files:
        with st.spinner("Processing files..."):
            text_chunks = process_uploaded_files(uploaded_files)
            create_vector_store(text_chunks)
            st.success("Files processed and vector store updated!")
    else:
        st.warning("Please upload at least one file.")

# Query Interface
st.header("Ask a Question")
question = st.text_input("Enter your query:")

if st.button("Get Answer"):
    if question:
        try:
            with st.spinner("Querying..."):
                chain = get_conversational_chain()
                response = chain({"question": question}, return_only_outputs=True)
                st.write("**Answer:**", response["output_text"])
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a question.")
