import os
import speech_recognition as sr
from moviepy.editor import VideoFileClip
from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch
from langdetect import detect

class createSummarization:
    def __init__(self, model_name='utrobinmv/t5_summary_en_ru_zh_base_2048', cache_dir=r"server\Flichendery\model", device=None):
        # Устанавливаем работу модели на Cuda, иначе с помощью CPU
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')

        # Загружаем модель и токен для работы Т5
        self.model = T5ForConditionalGeneration.from_pretrained(model_name, cache_dir=cache_dir)
        self.model.eval()
        self.model.to(self.device)
        self.tokenizer = T5Tokenizer.from_pretrained(model_name, cache_dir=cache_dir)

    # Получаем текст из видео
    def extract_text_from_video(self, video_path, output_dir=r"video-test-audio"):
        # Проверка наличия директории
        os.makedirs(output_dir, exist_ok=True)
        
        # Обрабатываем файлы с различными разрешениями, которые можем использовать как видео
        video_base_name = os.path.splitext(os.path.basename(video_path))[0]
        
        # Определяем аудиофайл
        audio_file = os.path.join(output_dir, f"{video_base_name}.wav")
        
        # Выгружаем из видео аудио
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(audio_file)
        
        # Запускаем распознавание
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            # Определяем язык
            try:
                text = recognizer.recognize_google(audio_data, language='ru-RU')
            except sr.UnknownValueError:
                text = recognizer.recognize_google(audio_data, language='en-US')
        
        return text, audio_file

    # Определение языка
    def detect_language_and_summarize(self, text):
        language = detect(text)
        
        if language == 'en':
            summary_type = 'summary'
        elif language == 'ru':
            summary_type = 'summary'
        else:
            summary_type = 'summary'
        
        return self.generate_summary(text, summary_type)

    # Генерация сводки используя модель
    def generate_summary(self, text, summary_type='summary'):
        prefix = f'{summary_type}: '
        src_text = prefix + text
        input_ids = self.tokenizer(src_text, return_tensors="pt")

        # Создаём сводку
        generated_tokens = self.model.generate(**input_ids.to(self.device))
        result = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        
        return result[0]

    # Основная функция для запуска суммаризации и её возвращения
    def summarize_video(self, video_path):
        # Берём текст из аудиофайла
        extracted_text, audio_file = self.extract_text_from_video(video_path)
        print(f"Extracted Text from {audio_file}: {extracted_text}")

        # Определяем язык
        summary = self.detect_language_and_summarize(extracted_text)

        # Генерируем краткую суммаризацию
        brief_summary = self.generate_summary(extracted_text, summary_type="summary brief")

        # Генерируем расширенную суммаризацию
        big_summary = self.generate_summary(extracted_text, summary_type="summary big")

        # Возвращаем всё в качестве словаря
        return {
            "extracted_text": extracted_text,
            "summary": summary,
            "brief_summary": brief_summary,
            "big_summary": big_summary
        }


# Использование
def process_video_and_generate_summary(video_path):
    # Создаём зависимость для класса
    summarization = createSummarization()

    # Вызываем суммаризацию
    summaries = summarization.summarize_video(video_path)

    # Печатаем в терминал по необходимости
    print("Extracted Text:", summaries["extracted_text"])
    print("Summary:", summaries["summary"])
    print("Brief Summary:", summaries["brief_summary"])
    print("Big Summary:", summaries["big_summary"])

# Пример вызова
video_file_path = r"video-test\_uNup91ZYw0.002.mp4"
process_video_and_generate_summary(video_file_path)