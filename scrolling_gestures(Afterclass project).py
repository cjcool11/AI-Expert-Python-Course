import cv2
import mediapipe as mp
import pyautogui

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

def is_open_palm(hand_landmarks):
    tips = [8, 12, 16, 20]
    pip = [6, 10, 14, 18]
    extended = 0
    for t, p in zip(tips, pip):
        if hand_landmarks.landmark[t].y < hand_landmarks.landmark[p].y:
            extended += 1
    thumb_tip = hand_landmarks.landmark[4]
    thumb_ip = hand_landmarks.landmark[3]
    if thumb_tip.x < thumb_ip.x:
        extended += 1
    return extended >= 4

def is_fist(hand_landmarks):
    tips = [8, 12, 16, 20]
    pip = [6, 10, 14, 18]
    folded = 0
    for t, p in zip(tips, pip):
        if hand_landmarks.landmark[t].y > hand_landmarks.landmark[p].y:
            folded += 1
    thumb_tip = hand_landmarks.landmark[4]
    thumb_ip = hand_landmarks.landmark[3]
    if thumb_tip.x > thumb_ip.x:
        folded += 1
    return folded >= 4

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            if is_open_palm(hand_landmarks):
                pyautogui.scroll(20)
            elif is_fist(hand_landmarks):
                pyautogui.scroll(-20)

    cv2.imshow("Gesture Scroll", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

hands.close()
cap.release()
cv2.destroyAllWindows()
