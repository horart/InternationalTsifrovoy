from sklearn.neural_network import MLPRegressor
from getting_data import *
import pickle

import time
class Vid2Traits:
    def __init__(self, weight_file, params=1):
        self.neural_network = MLPRegressor(max_iter=200, validation_fraction=0.3)
        self.weight_file = weight_file

        try:
            with open(self.weight_file, "rb")as file:
                self.neural_network.coefs_ = pickle.load(file)
        except: ...

    def calculate(self, video_file: str) -> dict:
        ...

    def train(self, first, second): # -> dict
        self.neural_network.fit(first, second)

        # print(self.neural_network.score(first, second))
        with open(self.weight_file, "wb") as file:
            pickle.dump(self.neural_network.coefs_, file)
            # print(self.neural_network.coefs_)


if __name__ == "__main__":

    modelechka = Vid2Traits(weight_file="weights.pkl")
    path_to_videos = r"C:\Users\ADM\Documents\learning\Projects\InternationalTsifrovoy\server\modelka\train_dataset_vprod_encr_train 2\train\train_data\training80_02"
    path_to_annotation = r"C:\Users\ADM\Documents\learning\Projects\InternationalTsifrovoy\server\modelka\train_dataset_vprod_encr_train 2\train\annotation\annotation_training.pkl"
    number_of_videos = 5
    start = time.time()
    fer_results, expected_results = get_data(get_files(path_to_annotation, path_to_videos, number_of_videos))
    modelechka.train(fer_results, expected_results)
    print(time.time() - start)


