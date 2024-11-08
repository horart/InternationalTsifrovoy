from moviepy.editor import VideoFileClip
import numpy as np
import os
import hashlib

from fer import FER
import cv2
def getFaceEmotionsFromFrame(file_name):
    test_img = cv2.imread(file_name)
    emo_detector = FER(mtcnn=True)
    captured_emotions = emo_detector.detect_emotions(test_img)
    return captured_emotions[0]['emotions']


# Определяет, сколько кадров из видеовизитки мы возьмём
NUMBER_OF_FRAMES = 5

def get_emotions(video_file):
    # загрузить видеоклип
    video_clip = VideoFileClip(video_file)

    # Все полученные веса будем суммировать в weights
    weights = {'angry': 0,
               'disgust': 0,
               'fear': 0,
               'happy': 0,
               'sad': 0,
               'surprise': 0,
               'neutral': 0}

    # создаем папку по названию видео файла
    filename, _ = os.path.splitext(video_file)
    if not os.path.isdir(filename):
        os.mkdir(filename)

    # перебираем каждый возможный кадр
    step = video_clip.duration / NUMBER_OF_FRAMES
    count = 1
    for current_duration in np.arange(0, video_clip.duration, step):
        #frame_filename = os.path.join(filename, f"frame{count}.jpg")
        #frame_filename = hashlib.md5(filename + format_timedelta(current_duration)).hexdigest()
        frame_filename = hashlib.md5(bytes(current_duration)).hexdigest()
        # print(type(frame_filename))
        frame_filename = os.path.join(filename, frame_filename + ".jpg")
        video_clip.save_frame(frame_filename, current_duration)
        try:
            emotions_from_frame = getFaceEmotionsFromFrame(frame_filename)
            for emotion in emotions_from_frame:
                weights[emotion] += emotions_from_frame[emotion]
        except:
            pass

        os.remove(frame_filename)

        count += 1


    os.removedirs(filename)
    return weights



if __name__ == "__main__":
    video_file = 'woman.mp4'
    import time
    begtime = time.perf_counter()
    ans = get_emotions(video_file)
    endtime = time.perf_counter()
    print(ans)
    print(f"\nЗатрачено, с: {endtime - begtime} ")