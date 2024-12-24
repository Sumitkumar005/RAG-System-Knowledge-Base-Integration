import os
import logging
from PyPDF2 import PdfReader
from docx import Document
import pandas as pd
import pytesseract
from PIL import Image
import whisper
import json
from concurrent.futures import ThreadPoolExecutor
from langdetect import detect
from whisper import load_model
from moviepy.editor import VideoFileClip

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def clean_text(text):
    return text.replace("\n", " ").strip()

def validate_file(file):
    if file.size == 0:
        raise ValueError(f"The file {file.name} is empty and cannot be processed.")
    logging.info(f"File {file.name} passed validation.")



def process_pdf(file):
    try:
        reader = PdfReader(file)
        return clean_text(" ".join(page.extract_text() for page in reader.pages))
    except Exception as e:
        logging.error(f"Error processing PDF file {file.name}: {e}")
        return ""
    
def process_docx(file):
    try:
        doc = Document(file)
        return clean_text(" ".join(paragraph.text for paragraph in doc.paragraphs))
    except Exception as e:
        logging.error(f"Error processing DOCX file {file.name}: {e}")
        return ""

def process_txt(file):
    try:
        return clean_text(file.read().decode("utf-8"))
    except Exception as e:
        logging.error(f"Error processing TXT file {file.name}: {e}")
        return ""

def process_csv(file):
    try:
        df = pd.read_csv(file)
        return clean_text(df.to_string())
    except Exception as e:
        logging.error(f"Error processing CSV file {file.name}: {e}")
        return ""
def process_json(file):
    try:
        data = json.load(file)
        return clean_text(json.dumps(data, indent=2))
    except Exception as e:
        logging.error(f"Error processing JSON file {file.name}: {e}")
        return ""

def process_image(file):
    try:
        image = Image.open(file)
        return clean_text(pytesseract.image_to_string(image))
    except Exception as e:
        logging.error(f"Error processing image file {file.name}: {e}")
        return ""

def process_audio(audio_file):
    try:
        model = load_model("base")
        transcript = model.transcribe(audio_file)["text"]
        return {"type": "audio", "content": transcript}
    except Exception as e:
        logging.error(f"Error processing audio file {audio_file.name}: {e}")
        return {"type": "audio", "content": ""}
        

def process_video(video_file):
    try:
        clip = VideoFileClip(video_file.name)
        audio = clip.audio
        audio.write_audiofile("temp_audio.wav")
        
        transcript = process_audio("temp_audio.wav") 
        os.remove("temp_audio.wav") 
        
        text_data = []
        frame_interval = 1 
        
        for t in range(0, int(clip.duration), frame_interval):
            frame = clip.get_frame(t)
            image = Image.fromarray(frame)
            text = pytesseract.image_to_string(image)
            if text.strip():
                text_data.append(text)
        
        return {"type": "video", "content": clean_text(" ".join(text_data))}
    except Exception as e:
        logging.error(f"Error processing video file {video_file.name}: {e}")
        return {"type": "video", "content": ""}

def detect_language(text):
    try:
        return detect(text)
    except Exception as e:
        logging.error(f"Error detecting language: {e}")
        return "unknown"

def process_uploaded_files(files):
    text_data = []
    for file in files:
        _, ext = os.path.splitext(file.name)
        if ext == ".pdf":
            result = process_pdf(file)
        elif ext == ".docx":
            result = process_docx(file)
        elif ext == ".txt":
            result = process_txt(file)
        elif ext == ".csv":
            result = process_csv(file)
        elif ext == ".json":
            result = process_json(file)
        elif ext in [".png", ".jpg", ".jpeg"]:
            result = process_image(file)
        elif ext in [".mp3", ".wav"]:
            result = process_audio(file)
        elif ext in [".mp4", ".avi", ".mkv"]:
            result = process_video(file)
        else:
            raise ValueError("Unsupported file type")
        
        language = detect_language(result) 
        text_data.append({"file_name": file.name, "text": result, "language": language})
    with ThreadPoolExecutor() as executor:
       text_data = list(executor.map(process_uploaded_files, files))
   
  
    return text_data