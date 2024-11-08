# summarize_script.py

import re

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def extract_text_from_srt(file_path):
    """
    Извлекает текст из .srt файла, удаляя временные метки и номера строк.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    text = ""
    for line in lines:
        if not re.match(r'^\d+$', line) and not re.match(r'^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', line):
            text += line.strip() + " "
    return text.strip()

def summarize_text(text):
    """
    Создает краткое содержание текста с помощью модели Summarus.
    """
    tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")  # Используйте другую модель
    model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")
    
    inputs = tokenizer.encode(text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(
        inputs, 
        max_length=20000,
        min_length=50,
        length_penalty=1.5,
        num_beams=60,
        early_stopping=True
    )
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    return summary


def save_summary_to_file(summary, output_path):
    """
    Сохраняет краткое содержание в файл.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(summary)

def main():
    srt_file_path = r"C:\Файлы\Meznar-hakaton\resulted\1.srt"  # замените на путь к вашему .srt файлу
    output_path = r"C:\Файлы\Meznar-hakaton\resulted\summary.txt"  # путь для сохранения краткого содержания
    
    transcript_text = extract_text_from_srt(srt_file_path)
    print("Извлеченный текст:", transcript_text)
    
    summary = summarize_text(transcript_text)
    print("Краткое содержание:", summary)
    
    # Сохранение краткого содержания в файл
    save_summary_to_file(summary, output_path)
    print(f"Краткое содержание сохранено в файл: {output_path}")

if __name__ == "__main__":
    main()
