import os

from sklearn.neural_network import MLPRegressor
from source.getting_data import *
import pickle
import time


class Vid2Traits:
    def __init__(self, weight_file):
        self.weight_file = weight_file
        try:
            with open(self.weight_file, "rb") as file:
                self.neural_network = pickle.load(file)
        except:
            self.neural_network = MLPRegressor(max_iter=200, validation_fraction=0.3)

    def predict(self, data: str) -> list:
        return self.neural_network.predict(data)

    def score_many(self, path_to_folder: str, path_to_annotation: str) -> float:
        folders = os.listdir(path_to_folder)
        count, score = len(folders), 0
        for i in range(1):
            path_to_videos = path_to_folder + '/' + folders[i]
            fer_results, expected_results = get_data(get_files(path_to_annotation, path_to_videos, 3))
            score += self.neural_network.score(fer_results, expected_results)
        return score / count

    def train(self, first, second):  # -> dict
        self.neural_network.fit(first, second)
        with open(self.weight_file, "wb") as file:
            pickle.dump(self.neural_network, file)


    def train_many(self, path_to_folder: str, path_to_annotation: str):
        folders = os.listdir(path_to_folder)
        for i in range(1, 3):
            path_to_videos = path_to_folder + '/' + folders[i]
            fer_results, expected_results = get_data(get_files(path_to_annotation, path_to_videos, 3))
            #print(fer_results)
            self.train(fer_results, expected_results)


if __name__ == "__main__":
    modelechka = Vid2Traits(weight_file=r"source/weights.pkl")
    path_to_folder = r"data/train"
    path_to_annotation = r"data/annotation_training.pkl"
    modelechka.train_many(path_to_folder, path_to_annotation)
    print(modelechka.score_many(path_to_folder, path_to_annotation))
