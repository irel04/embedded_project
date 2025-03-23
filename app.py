import cv2
import numpy as np
import time
from tensorflow.keras.models import load_model

# Load the pre-trained emotion detection model
emotion_model = load_model("emotion_model.h5")

# Emotion labels
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

# Ask for user's nickname
nickname = input("Enter your nickname: ")

# Allow user to select 3 emotions to demonstrate
print("Available emotions:", ", ".join(emotion_labels))
selected_emotions = set()

while len(selected_emotions) < 3:
    emotion = input(f"Choose emotion {len(selected_emotions) + 1}: ").strip().capitalize()
    if emotion in emotion_labels:
        selected_emotions.add(emotion)
    else:
        print("Invalid emotion, please choose from the list.")

print(f"\n{nickname}, you need to demonstrate these emotions: {', '.join(selected_emotions)}\n")

# Track detected emotions with timestamps
captured_emotions = []
last_detected_emotion = None
emotion_start_time = None

# Initialize face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

# Start timer
start_time = time.time()
max_duration = 60  # 1 minute time limit

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Check if time has exceeded 1 minute
    elapsed_time = time.time() - start_time
    if elapsed_time >= max_duration:
        print(f"\n{nickname}, you failed to complete the challenge in time! ⏳")
        break

    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_gray = cv2.resize(roi_gray, (48, 48))
        roi_gray = np.expand_dims(roi_gray, axis=0)
        roi_gray = np.expand_dims(roi_gray, axis=-1) / 255.0

        predictions = emotion_model.predict(roi_gray)[0]
        max_index = np.argmax(predictions)
        emotion = emotion_labels[max_index]
        confidence = round(predictions[max_index] * 100, 2)

        # Draw rectangle and label
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, f"{emotion}: {confidence}%", (x, y - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        # Check if emotion matches selected and is held for at least 2 seconds
        if emotion in selected_emotions and emotion not in captured_emotions:
            if last_detected_emotion == emotion:
                if time.time() - emotion_start_time >= 2:
                    captured_emotions.append(emotion)
                    print(f"{nickname}, emotion captured: {emotion}")
            else:
                last_detected_emotion = emotion
                emotion_start_time = time.time()

        # Check if all selected emotions have been demonstrated
        if set(captured_emotions) == selected_emotions:
            print(f"\n{nickname}, you completed the challenge! 🎉")
            print(f"Captured emotions: {captured_emotions}")
            cap.release()
            cv2.destroyAllWindows()
            exit()

    # Display progress on screen
    y_offset = 30
    for emotion in selected_emotions:
        color = (0, 255, 0) if emotion in captured_emotions else (0, 0, 255)
        cv2.putText(frame, f"{emotion}: {'✔' if emotion in captured_emotions else '❌'}",
                    (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        y_offset += 40

    cv2.imshow("Emotion Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
