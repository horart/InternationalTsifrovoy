import re
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk
from nltk import sent_tokenize

nltk.download('punkt')
nltk.download('punkt_tab')

def extract_text_from_srt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    text = ""
    for line in lines:
        if not re.match(r'^\d+$', line) and not re.match(r'^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', line):
            text += line.strip() + " "
    return text.strip()

def summarize_text(text):
    parser = PlaintextParser.from_string(text, Tokenizer("russian"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 5)  # Увеличьте количество предложений
    
    # Форматируем сводку в строку
    summary_text = ' '.join(str(sentence) for sentence in summary)

    return summary_text

def save_summary_to_file(summary, output_path):
    # Форматируем выходной файл с разделением на абзацы
    formatted_summary = summary.replace('. ', '.\n\n')  # Разделяем на абзацы
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(formatted_summary)

def main():
    srt_file_path = r"C:\Файлы\Meznar-hakaton\resulted\1.srt"
    output_path = r"C:\Файлы\Meznar-hakaton\resulted\summary.txt"
    
    transcript_text = extract_text_from_srt(srt_file_path)
    print("Извлеченный текст:", transcript_text)
    
    summary = summarize_text(transcript_text)
    print("Краткое содержание:", summary)
    
    save_summary_to_file(summary, output_path)
    print(f"Краткое содержание сохранено в файл: {output_path}")

if __name__ == "__main__":
    main()

