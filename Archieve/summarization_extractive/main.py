from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from summarizer import Summarizer
import nltk
import re

# Function to read and process text from .srt file
def read_srt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    text = ''
    for line in lines:
        if re.match(r'^\d+$', line) or '-->' in line:
            continue
        text += line.strip() + ' '
    return text.strip()

# Reading text from the .srt file
file_path = 'C:/Файлы/Meznar-hakaton/resulted/1.srt'
text = read_srt(file_path)

# Manually load a summarization-specific model and tokenizer (T5)
model_name = 't5-small'
custom_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
custom_tokenizer = AutoTokenizer.from_pretrained(model_name)

# Initialize the Summarizer with custom model and tokenizer
summarizer = Summarizer(custom_model=custom_model, custom_tokenizer=custom_tokenizer)

# Summarization configuration
num_sentences = max(1, int(len(nltk.sent_tokenize(text)) * 0.3))  # Example: summarize to 30% of original size

# Perform summarization
result = summarizer(text, num_sentences=num_sentences)
full_summary = ''.join(result)

# Save result to output file
with open('C:/Файлы/Meznar-hakaton/resulted/summary.txt', 'w', encoding='utf-8') as output_file:
    output_file.write(full_summary)

print("Summarization complete. Result saved to summary.txt")