import os
import pickle
from source.process_video import VideoProcessor
import multiprocessing
from joblib import Parallel, delayed, parallel_config
def get_goal_emotions(filename: str, emotions) -> dict:
    ocean_results = dict()
    for emot in emotions:
        ocean_results[emot] = emotions[emot][filename]
    return ocean_results

def get_files(annotation_path: str, video_directory: str, limit=-1) -> dict:
    videos = os.listdir(video_directory)[:limit]
    files = dict()
    with open(annotation_path, "rb") as anno_file:
        emotions = pickle.load(anno_file, encoding='latin')
        for video in videos:
            expected_results = get_goal_emotions(video, emotions)
            files[video_directory + '/' + video] = [expected_results['extraversion'],
                                                    expected_results['neuroticism'],
                                                    expected_results['agreeableness'],
                                                    expected_results['conscientiousness'],
                                                    expected_results['openness'],
                                                    expected_results['interview']]
        return files

def worker(path):
    video = VideoProcessor(path)
    return video.get_emotions()

def get_data(files: dict):
    inp = []
    output = []

    inp = Parallel(n_jobs=-1, prefer='threads')(delayed(worker)(x) for x in list(files.keys()))
    output = list(files.values())
    return inp, output

    for path, exp in files.items():
        video = VideoProcessor(path)
        emotions = video.get_emotions()
        inp.append(emotions)
        output.append(exp) 
    return inp, output
