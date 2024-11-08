# main.py

import sys
sys.path.append(r"C:\Файлы\Meznar-hakaton\server\Flichendery\pisets")

from argparse import ArgumentParser
import codecs
import logging
import os
import sys
import tempfile

import numpy as np

from asr.asr import initialize_model_for_speech_recognition
from asr.asr import initialize_model_for_speech_classification
from asr.asr import initialize_model_for_speech_segmentation
from asr.asr import transcribe, check_language
from asr.asr import asr_logger
from utils.utils import time_to_str

import torch
from transformers import pipeline

# Функция для извлечения текста из видео
def extract_text_from_video(video_path):
    asr = ASR()  # Создаем объект ASR
    text = asr(video_path)  # Извлекаем текст из видео
    return text

# Функция для суммаризации текста
def summarize_text(text, language="ru"):
    # Определяем модель суммаризации
    if language == "ru":
        model_name = "facebook/mbart-large-50-many-to-many-mmt"
    else:
        model_name = "microsoft/mdeberta-v3-base"
    
    # Создаем pipeline для суммаризации
    summarizer = pipeline("summarization", model=model_name, tokenizer=model_name)

    # Делаем суммаризацию
    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    return summary[0]['summary_text']

# Основная функция
def main(video_path, language="ru"):
    print("Извлечение текста из видео...")
    text = extract_text_from_video(video_path)
    print("Текст успешно извлечен.")
    
    print("Выполнение суммаризации текста...")
    summary = summarize_text(text, language)
    print("Суммаризация завершена.")
    
    print("\nОригинальный текст:")
    print(text)
    
    print("\nСуммаризация:")
    print(summary)

# Запуск скрипта
if __name__ == "__main__":
    video_path = r"C:\Файлы\Meznar-hakaton\Archieve\video-test\_uNup91ZYw0.002.mp4"  # Укажите путь к вашему видеофайлу
    language = "ru"  # Выберите язык ('ru' или 'en')
    main(video_path, language)
