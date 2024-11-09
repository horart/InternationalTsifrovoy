import os
import numpy as np
from sklearn.neural_network import MLPRegressor
from source.getting_data import *
import pickle
import time
import config


class Vid2Traits:
    def __init__(self, weight_file):
        self.weight_file = weight_file
        try:
            with open(self.weight_file, "rb") as file:
                self.neural_network = pickle.load(file)
        except FileNotFoundError:
            self.neural_network = MLPRegressor(max_iter=200, validation_fraction=0.3)

    def predict(self, data: str) -> list:
        return self.neural_network.predict(data)
    

    def train(self, X, Y):  # -> dict
        self.neural_network.fit(X, Y)
        with open(self.weight_file, "wb") as file:
            pickle.dump(self.neural_network, file)


    def train_many(self, path_to_folder: str, path_to_annotation: str, count=None, start=0, limit=-1):
        folders = os.listdir(path_to_folder)
        count = len(folders) if count is None else count
        big_expected_results = []
        big_input = []
        for i in range(start, start + count):
            start = time.time()
            path_to_videos = path_to_folder + '/' + folders[i]
            fer_results, expected_results = get_data(get_files(path_to_annotation, path_to_videos, limit))
            big_expected_results += expected_results
            big_input += fer_results
            print(i + 1, time.time() - start)
        self.train(big_input, big_expected_results)


    def score_many(self, path_to_folder: str, path_to_annotation: str, count=None, start=0, limit=-1) -> float:
        folders = os.listdir(path_to_folder)
        count = len(folders) if count is None else count
        big_input = []
        big_output = []
        for i in range(start, start + count):
            start = time.time()
            path_to_videos = path_to_folder + '/' + folders[i]
            fer_results, expected_results = get_data(get_files(path_to_annotation, path_to_videos, limit))
            big_input += fer_results
            big_output += expected_results
            print(i + 1, time.time() - start)
        return self.neural_network.score(big_input, big_output)



if __name__ == "__main__":
    modelechka = Vid2Traits(weight_file=config.WEIGHT_PATH)
    path_to_folder = config.FOLDER_PATH
    path_to_annotation = config.ANNOTATION_PATH
    start = time.time()
    modelechka.train_many(path_to_folder, path_to_annotation, count=1, start=0, limit=5)
    print(modelechka.score_many(path_to_folder, path_to_annotation, count=1, start=1, limit=5))
    print(time.time() - start) # 61 -> 39
