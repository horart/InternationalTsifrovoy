from moviepy.editor import VideoFileClip
import numpy as np
import os
import hashlib
from fer import FER
import cv2

# Определяет, сколько кадров из видеовизитки мы возьмём
NUMBER_OF_FRAMES = 10

# Создаём класс для обработки видео
class VideoProcessor:
    def __init__(self, path: str, number_of_frames=NUMBER_OF_FRAMES):
        self.path = path # Путь к видеоролику
        self.number_of_frames = number_of_frames # Количество кадров, которое мы будем получать
        self.video_clip = VideoFileClip(path) # Запись видео
        self.video_name = os.path.splitext(self.path)[0] # Имя видео
        self.step = self.video_clip.duration / self.number_of_frames # Шаг, с которым мы будем проходиться по видеоклипу

    # Метод для получения эмоции с одного изображения
    @staticmethod
    def get_emotion_from_frame(self, path_to_jpg: str) -> dict:
        jpg = cv2.imread(path_to_jpg)
        emotions_detector = FER(mtcnn=True)
        captured_emotions = emotions_detector.detect_emotions(jpg)
        return captured_emotions[0]['emotions']

    def __get_raw_emotions(self): ...
    def get_emotions(self):
        # Все полученные веса будем суммировать в weights
        weights = {'angry': 0, 'disgust': 0, 'fear': 0, 'happy': 0,
                   'sad': 0, 'surprise': 0, 'neutral': 0}
        # Хэшируем имя видеоролика, чтобы не возникало ошибок кодировки при создании папки и изображений
        hashed_name = hashlib.md5(self.video_name.encode()).hexdigest()
        os.mkdir(hashed_name)

        for current_duration in np.arange(0, self.video_clip.duration, self.step):
            frame_filename = hashlib.md5(bytes(current_duration)).hexdigest()
            frame_filename = os.path.join(hashed_name, frame_filename + ".jpg")
            self.video_clip.save_frame(frame_filename, current_duration)
            try:
                emotions_from_frame = self.get_emotion_from_frame(frame_filename)
                for emotion in emotions_from_frame:
                    weights[emotion] += emotions_from_frame[emotion]
            except:
                pass
            os.remove(frame_filename)
        os.removedirs(hashed_name)
        return [weights['angry'], weights['disgust'], weights['fear'],
                weights['happy'], weights['sad'], weights['surprise'], weights['neutral']]
