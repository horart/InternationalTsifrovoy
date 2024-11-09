from sklearn.neural_network import MLPRegressor
from getting_data import *
import pickle
import os
import time
from process_video_better import VideoProcessor 

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

    def getVideo(self, vid):
        # Ensure vid.get_emotions() outputs the correct feature vector shape
        features = vid.get_emotions()
        if features is None or len(features) == 0:
            raise ValueError("No features returned from get_emotions()")

        # Predict using the trained model
        prediction = self.neural_network.predict([features])
        return prediction

class ConvertFromOceanToMbti:
    def __init__(self, traits_array):
        # Инициализация типов личности из OCEAN на основе массива
        self.extraversion = traits_array[0]
        self.neuroticism = traits_array[1]
        self.agreeableness = traits_array[2]
        self.conscientiousness = traits_array[3]
        self.openness = traits_array[4]
        # Мы оставляем последний элемент на будущее использование (если необходимо)
        self.additional_value = traits_array[5]

    def big_five_to_mbti(self):
        # Функция для расчета MBTI на основе шкалы OCEAN с учетом описанных групп
        EI_score = self.extraversion - 0.5 * self.agreeableness
        SN_score = self.openness - 0.6 * self.conscientiousness
        TF_score = self.agreeableness - 0.4 * self.neuroticism
        JP_score = self.conscientiousness - 0.4 * self.openness

        # Рассчитываем шкалы для MBTI на основе характеристик OCEAN
        E_I = 'E' if EI_score >= 0.2 else 'I'
        S_N = 'S' if SN_score <= 0.65 else 'N'
        T_F = 'F' if TF_score > 0.35 else 'T'
        J_P = 'P' if JP_score <= 0.5 else 'J'

        # Определение типа MBTI на основе значений
        mbti_type = E_I + S_N + T_F + J_P
        return mbti_type

if __name__ == "__main__":

    modelechka = Vid2Traits(weight_file="weights.pkl")
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))  # One level up
    path_to_videos = os.path.join(root_dir, r"video-test")  # Path to the directory, not the specific file
    path_to_annotation = r"server\Fatum\model\annotation_training.pkl"
    number_of_videos = 5
    start = time.time()
    fer_results, expected_results = get_data(get_files(path_to_annotation, path_to_videos, number_of_videos))
    modelechka.train(fer_results, expected_results)
    vid = VideoProcessor(r"C:\Файлы\Meznar-hakaton\video-test\_uNup91ZYw0.002.mp4")
    print(modelechka.neural_network.predict([vid.get_emotions()])[0])
    print(time.time() - start)
    
    # Initialize the ConvertFromOceanToMbti class with the traits array
    mbti_converter = ConvertFromOceanToMbti(modelechka.neural_network.predict([vid.get_emotions()])[0])
    
    # Get the MBTI type using the OCEAN traits
    mbti_type = mbti_converter.big_five_to_mbti()
    
    # Print the calculated MBTI type
    print(f"Calculated MBTI type: {mbti_type}")