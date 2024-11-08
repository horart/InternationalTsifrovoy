from fer import FER
import cv2
def getFaceEmotionsFromFrame(file_name):
    test_img = cv2.imread(file_name)
    emo_detector = FER(mtcnn=True)
    captured_emotions = emo_detector.detect_emotions(test_img)
    return captured_emotions[0]['emotions']

#print(getFaceEmotionsFromFrame('i.webp'))