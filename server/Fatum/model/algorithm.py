import sys
from model import Vid2Traits
from process_video_better import VideoProcessor

class ConvertFromOceanToMbti:
    def __init__(self, openness, conscientiousness, extraversion, agreeableness, neuroticism):
        # Инициализация типов личности из OCEAN
        self.openness = openness
        self.conscientiousness = conscientiousness
        self.extraversion = extraversion
        self.agreeableness = agreeableness
        self.neuroticism = neuroticism

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

def main():
    # Path to the video file you want to process
    video_file_path = r"C:\Файлы\Meznar-hakaton\video-test\_uNup91ZYw0.002.mp4"
    
    # Initialize Vid2Traits object to extract personality traits from the video
    model = Vid2Traits(weight_file=r"weights.pkl")
    video_processor = VideoProcessor(video_file_path)
    
    # Use getVideo method to get the prediction
    try:
        prediction = model.getVideo(video_processor)
        print("Predicted Traits from Video:", prediction)
    except ValueError as e:
        print(f"Error while processing video: {e}")
        sys.exit(1)
    
    # If you want to extract OCEAN values, you can use the same logic from earlier
    emotions = video_processor.get_emotions()
    if emotions is None or len(emotions) == 0:
        print("Error: No emotions data found.")
        sys.exit(1)
    
    # Assuming emotions order is [extraversion, neuroticism, agreeableness, conscientiousness, openness]
    extraversion, neuroticism, agreeableness, conscientiousness, openness = emotions[:5]
    print(extraversion, neuroticism, agreeableness, conscientiousness, openness)
    
    # Convert OCEAN values to MBTI
    converter = ConvertFromOceanToMbti(
        openness=openness,
        conscientiousness=conscientiousness,
        extraversion=extraversion,
        agreeableness=agreeableness,
        neuroticism=neuroticism
    )

    # Get MBTI type from OCEAN traits
    mbti_type = converter.big_five_to_mbti()
    print(f"Predicted MBTI Type: {mbti_type}")

if __name__ == "__main__":
    main()
