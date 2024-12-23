import os
from PyPDF2 import PdfReader
from docx import Document
import pandas as pd
import pytesseract
from PIL import Image
import whisper
import json
from whisper import load_model  # Only import load_model from whisper
from moviepy.editor import VideoFileClip

def clean_text(text):
    return text.replace("\n", " ").strip()

def process_pdf(file):
    reader = PdfReader(file)
    return clean_text(" ".join(page.extract_text() for page in reader.pages))

def process_docx(file):
    doc = Document(file)
    return clean_text(" ".join(paragraph.text for paragraph in doc.paragraphs))

def process_txt(file):
    return clean_text(file.read().decode("utf-8"))

def process_csv(file):
    df = pd.read_csv(file)
    return clean_text(df.to_string())

def process_json(file):
    data = json.load(file)
    return clean_text(json.dumps(data, indent=2))

def process_image(file):
    image = Image.open(file)
    return clean_text(pytesseract.image_to_string(image))

def process_audio(audio_file):
    # Load Whisper model
    model = load_model("base")
    transcript = model.transcribe(audio_file)["text"]
    return {"type": "audio", "content": transcript}

def process_video(video_file):
    # Extract audio from video
    clip = VideoFileClip(video_file.name)
    audio = clip.audio
    audio.write_audiofile("temp_audio.wav")
    
    # Process the audio for transcription
    transcript = process_audio("temp_audio.wav")
    return {"type": "video", "content": transcript["content"]}




def process_uploaded_files(files):
    text_data = []
    for file in files:
        _, ext = os.path.splitext(file.name)
        if ext == ".pdf":
            text_data.append(process_pdf(file))
        elif ext == ".docx":
            text_data.append(process_docx(file))
        elif ext == ".txt":
            text_data.append(process_txt(file))
        elif ext == ".csv":
            text_data.append(process_csv(file))
        elif ext == ".json":
            text_data.append(process_json(file))
        elif ext in [".png", ".jpg", ".jpeg"]:
            text_data.append(process_image(file))
        elif ext in [".mp3", ".wav"]:
            text_data.append(process_audio(file))
        elif ext in [".mp4", ".avi", ".mkv"]:
            text_data.append(process_video(file))  # Ensure this matches correctly
        else:
            raise ValueError("Unsupported file type")
    return text_data


"""def process_video(file):
    # First, extract the audio and transcribe it
    with VideoFileClip(file.name) as video:
        text_data = []
        # Process the audio part
        audio = video.audio
        audio.write_audiofile("temp_audio.wav")
        transcript = process_audio("temp_audio.wav")  # Transcribe the audio
        text_data.append(transcript["content"])  # Add audio transcript
        
        # Process frames at 1-second intervals (or adjust interval as needed)
        for t in range(0, int(video.duration), 1):  # You can adjust the frame rate (1 second here)
            frame = video.get_frame(t)
            # Convert the frame to an image (using PIL)
            image = Image.fromarray(frame)
            # Use pytesseract to extract text from the image
            text = pytesseract.image_to_string(image)
            if text.strip():  # Only add text if there's anything recognized
                text_data.append(text)
        
        return clean_text(" ".join(text_data))"""
