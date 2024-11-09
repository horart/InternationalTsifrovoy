from typing import List
from moviepy.editor import VideoFileClip
import numpy as np
import os
import hashlib
from ferz import FERZ
import cv2

# Определяет, сколько кадров из видеовизитки мы возьмём
NUMBER_OF_FRAMES = 10
TRIVIAL_EMOTION_WEIGHTS = {'angry': 0, 'disgust': 0, 'fear': 0, 'happy': 0,
                   'sad': 0, 'surprise': 0, 'neutral': 0}
emotions_detector = FERZ(mtcnn=True)

# Создаём класс для обработки видео
class VideoProcessor:
    def __init__(self, number_of_frames=NUMBER_OF_FRAMES):
        self.number_of_frames = number_of_frames # Количество кадров, которое мы будем получать
    # Метод для получения эмоции с одного изображения

    def get_emotion_from_frame(self, path_to_jpg: str) -> dict:
        jpg = cv2.imread(path_to_jpg)
        captured_emotions = emotions_detector.detect_emotions(jpg)
        return captured_emotions[0]['emotions'] if captured_emotions else {k: 0.5 for k in TRIVIAL_EMOTION_WEIGHTS}

    def _cut_to_frames(self, path):
        video_clip = VideoFileClip(path) # Запись видео
        step = video_clip.duration / self.number_of_frames # Шаг, с которым мы будем проходиться по видеоклипу
        # Все полученные веса будем суммировать в weights
        frames: List[np.ndarray] = []
        for current_duration in np.arange(0, video_clip.duration, step):
            frames.append(video_clip.get_frame(current_duration))
        return frames

    def get_emotions(self, path: str) -> list:
        result = {k: v for k, v in TRIVIAL_EMOTION_WEIGHTS.items()}
        emotion_frames = emotions_detector.detect_emotions_frames(frames)
        for frame_idx, faces_on_frame in enumerate(emotion_frames):
            if faces_on_frame:
                for key in faces_on_frame[0]['emotions']:
                    result[key] += faces_on_frame[0]['emotions'][key]
            else:
                for key in TRIVIAL_EMOTION_WEIGHTS:
                    result[key] += result[key]/frame_idx
        #os.removedirs('tmp')
        return [result['angry'], result['disgust'], result['fear'],
                result['happy'], result['sad'], result['surprise'], result['neutral']]
    
    def process_files(self, paths: List[str]):
        big_frames = []
        for path in paths:
            frames = self._cut_to_frames(path)
            big_frames.extend(frames)

        emotion_frames = emotions_detector.detect_emotions_frames(big_frames)
        emotion_files = []
        for file_idx in range(len(paths)):
            emotion_files.append(TRIVIAL_EMOTION_WEIGHTS.copy())
            for frame_idx in range(10):
                if emotion_frames[file_idx*10+frame_idx]:
                    for key in emotion_frames[file_idx*10+frame_idx][0]['emotions']:
                        emotion_files[-1][key] += emotion_frames[file_idx*10+frame_idx][0]['emotions'][key]
                else:
                    emotion_files[-1][key] += emotion_files[-1][key]/frame_idx

        return emotion_files
        
vp = VideoProcessor()
vp.process_files(['data/train/train_data/training80_01/_uNup91ZYw0.002.mp4', 'data/train/train_data/training80_01/-AmMDnVl4s8.003.mp4'])
print()