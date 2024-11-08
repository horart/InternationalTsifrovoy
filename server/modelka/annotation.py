

def get_goal_emotions(filename: str, emotions) -> dict:
    ocean_results = dict()
    for emot in emotions:
        ocean_results[emot] = emotions[emot][filename]
    return ocean_results

