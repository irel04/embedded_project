import cv2
import numpy as np
import time
import mediapipe as mp
from tensorflow.keras.models import load_model

# Load the pre-trained emotion detection model
emotion_model = load_model("emotion_model.h5")

# Emotion labels
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

# Initialize Mediapipe Face Mesh for facial landmarks
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

def emotion_detection(nickname, selected_emotions):
    captured_emotions = []
    last_detected_emotion = None
    emotion_start_time = None

    cap = cv2.VideoCapture(0)

    start_time = time.time()
    max_duration = 60  # 1 minute time limit

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        elapsed_time = time.time() - start_time
        if elapsed_time >= max_duration:
            print(f"\n{nickname}, you failed to complete the challenge in time! ⏳")
            return [False, round(elapsed_time, 2)]

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Extract face bounding box coordinates
                h, w, _ = frame.shape
                x_min = int(min([lm.x * w for lm in face_landmarks.landmark]))
                y_min = int(min([lm.y * h for lm in face_landmarks.landmark]))
                x_max = int(max([lm.x * w for lm in face_landmarks.landmark]))
                y_max = int(max([lm.y * h for lm in face_landmarks.landmark]))

                # Extract face ROI
                roi_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)[y_min:y_max, x_min:x_max]
                roi_gray = cv2.resize(roi_gray, (48, 48))
                roi_gray = np.expand_dims(roi_gray, axis=0)
                roi_gray = np.expand_dims(roi_gray, axis=-1) / 255.0

                predictions = emotion_model.predict(roi_gray)[0]
                max_index = np.argmax(predictions)
                emotion = emotion_labels[max_index]
                confidence = round(predictions[max_index] * 100, 2)

                # Draw facial landmarks
                for landmark in face_landmarks.landmark:
                    x, y = int(landmark.x * w), int(landmark.y * h)
                    cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

                cv2.putText(frame, f"{emotion}: {confidence}%", (x_min, y_min - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                # Emotion capture logic
                if emotion in selected_emotions and emotion not in captured_emotions:
                    if last_detected_emotion == emotion:
                        if time.time() - emotion_start_time >= 5:
                            captured_emotions.append(emotion)
                            print(f"{nickname}, emotion captured: {emotion}")
                    else:
                        last_detected_emotion = emotion
                        emotion_start_time = time.time()

                if set(captured_emotions) == set(selected_emotions):
                    print(f"\n{nickname}, you completed the challenge! 🎉")
                    print(f"Captured emotions: {captured_emotions}")

                    cap.release()
                    cv2.destroyAllWindows()
                    return [True, round(elapsed_time, 2)]

        # Display progress
        y_offset = 30
        for emotion in selected_emotions:
            color = (0, 255, 0) if emotion in captured_emotions else (0, 0, 255)
            cv2.putText(frame, f"{'[/]' if emotion in captured_emotions else '[ ]'} {emotion}",
                        (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            y_offset += 40

        cv2.imshow("Emotion Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    emotion_detection(nickname="irel", selected_emotions=["Angry", "Sad", "Happy"])
