import os
import speech_recognition as sr
from moviepy.editor import VideoFileClip
from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch
from langdetect import detect

# Set device to use GPU if available, otherwise CPU
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Load the T5 summarization model and tokenizer from Hugging Face
model_name = 'utrobinmv/t5_summary_en_ru_zh_base_2048'
model = T5ForConditionalGeneration.from_pretrained(model_name, cache_dir=r"server\Flichendery\model")
model.eval()
model.to(device)
tokenizer = T5Tokenizer.from_pretrained(model_name, cache_dir=r"server\Flichendery\model")

# Function to extract audio from video and convert it to text
def extract_text_from_video(video_path, output_dir=r"video-test-audio"):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract base name of the video file without extension
    video_base_name = os.path.splitext(os.path.basename(video_path))[0]
    
    # Define the output audio file path with the same base name as the video file
    audio_file = os.path.join(output_dir, f"{video_base_name}.wav")
    
    # Load video file and extract audio
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_file)
    
    # Initialize recognizer
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        # Recognize speech in Russian and English
        try:
            text = recognizer.recognize_google(audio_data, language='ru-RU')  # Recognize Russian first
        except sr.UnknownValueError:
            # If speech cannot be understood in Russian, try English
            text = recognizer.recognize_google(audio_data, language='en-US')  # Then recognize in English
    
    return text, audio_file

# Function to detect language and return the appropriate summary type
def detect_language_and_summarize(text):
    # Detect language of the text
    language = detect(text)
    
    if language == 'en':
        summary_type = 'summary'
    elif language == 'ru':
        summary_type = 'summary'
    else:
        summary_type = 'summary'  # Default summary type if language is unsupported
    
    return generate_summary(text, summary_type)

# Function to generate summaries using the T5 model
def generate_summary(text, summary_type='summary'):
    # Prepare text with prefix based on summary type
    prefix = f'{summary_type}: '
    src_text = prefix + text
    input_ids = tokenizer(src_text, return_tensors="pt")

    # Generate summary
    generated_tokens = model.generate(**input_ids.to(device))
    result = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    
    return result[0]

# Main function to handle text extraction and summarization
def summarize_video(video_path):
    # Step 1: Extract text from video and save audio file with the same name
    extracted_text, audio_file = extract_text_from_video(video_path)
    print(f"Extracted Text from {audio_file}: {extracted_text}")

    # Step 2: Detect language and generate summary
    summary = detect_language_and_summarize(extracted_text)
    print("\nSummary:", summary)

    # Generate brief summary
    brief_summary = generate_summary(extracted_text, summary_type="summary brief")
    print("\nBrief Summary:", brief_summary)

    # Generate big summary
    big_summary = generate_summary(extracted_text, summary_type="summary big")
    print("\nBig Summary:", big_summary)

# Run summarization on a video file (provide your video path here)
video_path = r"video-test\_uNup91ZYw0.002.mp4"  # Update with the correct path to your video
summarize_video(video_path)