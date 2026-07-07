import cv2
import mediapipe as mp
import numpy as np

mp_hands=mp.solutions.hands
mp_draw=mp.solutions.drawing_utils
hands=mp_hands.Hands(max_num_hands=1,min_detection_confidence=0.5,min_tracking_confidence=0.5)

cap=cv2.VideoCapture(0)
draw=False
pts=[]
cx,cy=300,300

while True:
    ret,frame=cap.read()
    if not ret:
        break
    frame=cv2.flip(frame,1)
    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    res=hands.process(rgb)

    if res.multi_hand_landmarks:
        lm=res.multi_hand_landmarks[0]
        h,w,_=frame.shape
        x=int(lm.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x*w)
        y=int(lm.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y*h)
        d=lm.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y - lm.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y

        if d<0.02:
            draw=True
        else:
            draw=False

        if draw:
            pts.append((x,y))
        else:
            cx,cy=x,y
            pts=[]

        cv2.circle(frame,(cx,cy),20,(0,255,0),-1)

    for i in range(1,len(pts)):
        cv2.line(frame,pts[i-1],pts[i],(255,0,0),4)

    cv2.imshow("frame",frame)
    if cv2.waitKey(1)&0xFF==27:
        break

cap.release()
cv2.destroyAllWindows()
