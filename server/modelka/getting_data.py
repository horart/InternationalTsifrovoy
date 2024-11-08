import os
from annotation import get_goal_emotions
import pickle
from process_video import get_emotions
#OCEAN -> NEO BIg Five


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


def get_data(files: dict):
    input = []
    output = []
    for path, exp in files.items():
        input.append(get_emotions(path))
        output.append(exp)
    return input, output
