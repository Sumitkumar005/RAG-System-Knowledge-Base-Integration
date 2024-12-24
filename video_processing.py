import ffmpeg
import whisper
import ffmpeg

def extract_frames(video_path, output_folder, frame_rate=1):
    input_video = ffmpeg.input(video_path)
    (
        ffmpeg
        .output(input_video, f"{output_folder}/frame_%04d.png", vframes=frame_rate)
        .run(overwrite_output=True)
    )
    
    frame_files = [f"{output_folder}/frame_{i:04d}.png" for i in range(ffmpeg.probe(video_path)["streams"][0]["nb_frames"])]
    return frame_files


def transcribe_video(video_path):
    model = whisper.load_model("base")
    result = model.transcribe(video_path)
    return result
