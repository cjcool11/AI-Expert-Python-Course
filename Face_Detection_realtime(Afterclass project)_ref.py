import cv2
from deepface import DeepFace

# 1. Initialize OpenCV's built-in Haar Cascade for face bounding boxes
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 2. Start video capture from your local webcam
cap = cv2.VideoCapture(0)

while True:
    # Read individual frames from the stream
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale for faster face detection optimization
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Isolate the region of interest (the cropped face)
        face_roi = frame[y:y+h, x:x+w]

        try:
            # 3. Analyze the isolated face using DeepFace's pre-trained model
            # enforce_detection=False prevents crashes if a face disappears briefly
            analysis = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
            
            # Extract the dominant emotion label
            dominant_emotion = analysis[0]['dominant_emotion']

            # 4. Draw bounding box and label text over the live frame
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, dominant_emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        except Exception as e:
            # Handle potential background noise or calculation glitches silently
            pass

    # Display the processed frame in a window
    cv2.imshow('Real-time Emotion Detection', frame)

    # Break the loop immediately if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera hardware and destroy open windows
cap.release()
cv2.destroyAllWindows()