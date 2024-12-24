import streamlit as st
from preprocessors import process_uploaded_files
from vector_store import create_vector_store, load_vector_store
from conversational_chain import get_conversational_chain
import os
import tempfile
import whisper 
import ffmpeg 
from PIL import Image
import cv2
import io

vector_store =  None
conversation_chain = None

st.title("RAG System: Knowledge Base Integration")
st.sidebar.title("Upload Files")
import whisper

def transcribe_audio(uploaded_file):
    audio_file = uploaded_file.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
        temp_audio_file.write(audio_file)
        temp_audio_file_path = temp_audio_file.name

    model = whisper.load_model("base")  
    
    result = model.transcribe(temp_audio_file_path)
    
    os.remove(temp_audio_file_path)
    
    return result["text"]
def extract_image_features(uploaded_file):
    image_file = uploaded_file.read()
    image = Image.open(io.BytesIO(image_file))
    
    image_width, image_height = image.size
    image_format = image.format  
    
    image_features = {
        "width": image_width,
        "height": image_height,
        "format": image_format
    }
    import whisper
def transcribe_video(uploaded_file):
    with tempfile.TemporaryDirectory() as tmpdir:
        video_file = uploaded_file.read()
        input_video = tempfile.NamedTemporaryFile(delete=False, dir=tmpdir)
        input_video.write(video_file)
        input_video.close()
        
        audio_file = os.path.join(tmpdir, "extracted_audio.wav")
        ffmpeg.input(input_video.name).output(audio_file).run()
        model = whisper.load_model("base")  
        result = model.transcribe(audio_file)
        os.remove(input_video.name) 
        
        return result["text"]
    return image_features

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

            audio_results = []
            video_results = []
            image_results = []

            for uploaded_file in uploaded_files:
                if uploaded_file.type.startswith("audio/"):
                    try:
                        audio_result = transcribe_audio(uploaded_file)
                        audio_results.append(audio_result)
                    except Exception as e:
                        st.error(f"Error processing audio file {uploaded_file.name}: {e}")
                elif uploaded_file.type.startswith("video/"):
                    try:
                        video_result = transcribe_video(uploaded_file)
                        video_results.append(video_result)
                    except Exception as e:
                        st.error(f"Error processing video file {uploaded_file.name}: {e}")
                elif uploaded_file.type.startswith("image/"):
                    try:
                        image_result = extract_image_features(uploaded_file)
                        image_results.append(image_result)
                    except Exception as e:
                        st.error(f"Error processing image file {uploaded_file.name}: {e}")
            if audio_results:
                st.write("**Audio Transcriptions:**")
                for result in audio_results:
                    st.write(result)

            if video_results:
                st.write("**Video Transcriptions/Frame Processing:**")
                for result in video_results:
                    st.write(result)

            if image_results:
                st.write("**Image Features Extraction:**")
                for result in image_results:
                    st.image(uploaded_file, caption="Image", use_column_width=True)
                    st.write(result)
    else:
        st.warning("Please upload at least one file.")
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
