import pysrt
from mfdp_simplifier import simplify_text  # Примерный импорт функции упрощения текста из репозитория MFDP_text_simplifier

# Функция для чтения текста из .srt файла
def read_srt_file(file_path):
    subtitles = pysrt.open(file_path)
    text = ''
    for subtitle in subtitles:
        text += subtitle.text + ' '  # Сочетание всех строк субтитров в один текст
    return text

# Функция для получения краткого содержания из .srt файла
def get_summary_from_srt(srt_file):
    # Чтение текста из SRT
    text = read_srt_file(srt_file)
    
    # Упрощение текста
    simplified_text = simplify_text(text)
    
    return simplified_text

# Основная функция, которая выполняет обработку
if __name__ == '__main__':
    # Путь к твоему файлу .srt
    srt_file = 'path_to_your_srt_file.srt'
    
    # Получаем упрощённое содержание
    summary = get_summary_from_srt(srt_file)
    
    # Записываем итоговое содержание в файл summary.txt
    with open('summary.txt', 'w', encoding='utf-8') as f:
        f.write(summary)
    
    # Выводим результат в консоль (по желанию)
    print("Краткое содержание сохранено в summary.txt")



