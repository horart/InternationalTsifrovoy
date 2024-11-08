from sklearn.neural_network import MLPRegressor
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
import random
import pickle
x_train = [[random.randint(1,5) for x in range(7)] for y in range(10)]
y_train = [[random.randint(1,5) for x in range(5)] for y in range(10)]

class Vid2Traits:

    def __init__(self, weight_file, params=1):
        self.neural_network = MLPRegressor(max_iter=200)
        self.weight_file = weight_file
        try:
            with open(self.weight_file, "rb")as file:
                self.neural_network.coefs_ = pickle.load(file)
                print(self.neural_network.coefs_)
        except: ...

    def calculate(self, video_file: str) -> dict:
        ...

    def train(self, first, second): # -> dict
        self.neural_network.fit(first, second)
        print(self.neural_network.score(first, second))
        with open(self.weight_file, "wb") as file:
            pickle.dump(self.neural_network.coefs_, file)
            print(self.neural_network.coefs_)

modelechka = Vid2Traits(weight_file="weights.pkl")
modelechka.train(x_train, y_train)
