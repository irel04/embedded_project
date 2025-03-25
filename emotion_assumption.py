import cv2
import numpy as np
import time
from tensorflow.keras.models import load_model
import random
import webbrowser
import mediapipe as mp

# Load the pre-trained emotion detection model
emotion_model = load_model("emotion_model.h5")

# Emotion labels
emotion_labels = ['Angry', 'Disgust', 'Fear',
                'Happy', 'Neutral', 'Sad', 'Surprise']

# Initialize Mediapipe Face Mesh for facial landmarks
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

def emotional_tendency():
	

    # Initialize face detection
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    # Track occurrences of emotions when neutral is detected
    emotion_trends = {"Happy": 0, "Sad": 0, "Angry": 0}
    neutral_detections = 0

    print("Starting emotion detection. Press 'q' to exit.")

    start_time = time.time()
    max_duration = 60  # Run for 1 minute (can be adjusted)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        elapsed_time = time.time() - start_time
        if elapsed_time >= max_duration:
            print("\nStopping detection... Analyzing future prediction.")
            break

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

            # Neutral Face Prediction Logic
            if emotion == "Neutral":
                neutral_detections += 1

                # Get second strongest emotion
                sorted_indices = np.argsort(predictions)[::-1]
                second_emotion = emotion_labels[sorted_indices[1]]
                second_confidence = round(predictions[sorted_indices[1]] * 100, 2)

                # Track emotional tendency
                if second_emotion in emotion_trends:
                    emotion_trends[second_emotion] += 1

                # Display real-time interpretation
                if second_emotion == "Happy":
                    message = "You look neutral, but slightly happy!"
                elif second_emotion == "Sad":
                    message = "You seem calm, but maybe a bit down."
                elif second_emotion == "Angry":
                    message = "You look neutral, but a little tense."
                else:
                    message = "You appear calm and neutral."

                cv2.putText(frame, message, (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        cv2.imshow("Emotion Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # **Predict Future Emotion Based on Trends**
    # Ensure there were neutral detections
    if neutral_detections > 0:
        total_emotions = sum(emotion_trends.values())

        if total_emotions == 0:
            future_prediction = "You will likely remain neutral. 😐"
        else:
            # Normalize emotion frequencies into probabilities
            probabilities = {
                emotion: count / total_emotions for emotion, count in emotion_trends.items()}

            # Generate a weighted random choice for variability
            predicted_emotion = random.choices(
                list(probabilities.keys()), weights=probabilities.values(), k=1)[0]

            # Provide multiple potential outcomes
            prediction_options = {
                "Happy": [
                    "You may feel more positive and cheerful in the next few hours! Keep spreading your joy and uplifting those around you. 😃",
                    "A sudden burst of happiness might make you smile for no reason. Enjoy the good vibes and share them with others! 😊",
                    "Your day is about to get brighter! Expect uplifting moments, whether from good news, a fun conversation, or a simple act of kindness. 🎉"
                ],
                "Sad": [
                    "You might experience a wave of sadness or nostalgia soon. Try engaging in a favorite hobby or reaching out to a friend for support. 😔",
                    "A sense of low energy could affect your mood. Stay active, listen to uplifting music, or take a short walk to refresh yourself. 🌱",
                    "Memories from the past may resurface, making you feel emotional. Keep a comforting playlist or a happy distraction ready to lift your spirits. 🎶"
                ],
                "Angry": [
                    "Frustration may arise due to unexpected challenges. Remember to take deep breaths, stay patient, and approach situations with a calm mind. 😠",
                    "You could feel irritated by small inconveniences. Try mindfulness techniques or a short break to avoid unnecessary stress. 🧘",
                    "A difficult conversation or situation might test your patience. Stay composed, think before you react, and handle things wisely to maintain peace. 🚦"
                ]
            }


            # Select a random prediction from the chosen emotion category
            future_prediction = random.choice(prediction_options.get(
                predicted_emotion, ["Your emotions seem unpredictable. Stay mindful! 🧘"]))

        print("\n📢 **Future Emotion Prediction (4 hours later):**")
        print(future_prediction)

        webbrowser.open_new("https://jci-n-web.vercel.app/embedded-system")

        return future_prediction

    else:
        print("\nNot enough neutral face detections to make a future prediction.")

        return None

if __name__ == "__main__":
    emotional_tendency()