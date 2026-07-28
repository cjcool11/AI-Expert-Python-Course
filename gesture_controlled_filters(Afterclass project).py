import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
filter_mode = None

def apply_filter(img, mode):
    if mode == "grayscale":
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if mode == "sepia":
        kernel = np.array([[0.272,0.534,0.131],[0.349,0.686,0.168],[0.393,0.769,0.189]])
        return cv2.transform(img, kernel)
    if mode == "negative":
        return cv2.bitwise_not(img)
    if mode == "blur":
        return cv2.GaussianBlur(img,(15,15),0)
    return img

while True:
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
            lm = hand.landmark
            h,w,c = frame.shape
            thumb = (int(lm[4].x*w), int(lm[4].y*h))
            index = (int(lm[8].x*w), int(lm[8].y*h))
            middle = (int(lm[12].x*w), int(lm[12].y*h))
            ring = (int(lm[16].x*w), int(lm[16].y*h))
            pinky = (int(lm[20].x*w), int(l))