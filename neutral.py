import cv2
import numpy as np
import time
from tensorflow.keras.models import load_model
import random


def emotional_tendency():
	# Load the pre-trained emotion detection model
    emotion_model = load_model("emotion_model.h5")

    # Emotion labels
    emotion_labels = ['Angry', 'Disgust', 'Fear',
                    'Happy', 'Neutral', 'Sad', 'Surprise']

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
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5)

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
                    message = "You look neutral, but slightly happy! 😊"
                elif second_emotion == "Sad":
                    message = "You seem calm, but maybe a bit down. 😔"
                elif second_emotion == "Angry":
                    message = "You look neutral, but a little tense. 😠"
                else:
                    message = "You appear calm and neutral. 😐"

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
                    "You may feel more positive and cheerful in the next 4 hours! 😃",
                    "You might find yourself smiling for no reason later. 😊",
                    "A good mood boost is on the way! 🎉"
                ],
                "Sad": [
                    "You might feel a bit down later. Try to do something uplifting! 😔",
                    "You could experience moments of low energy. Stay engaged! 🌱",
                    "A wave of nostalgia might hit you. Keep some good music ready! 🎶"
                ],
                "Angry": [
                    "You may experience some stress or frustration. Take deep breaths! 😠",
                    "Watch out for minor irritations that might pile up. Stay mindful! 🧘",
                    "A challenging situation might test your patience. Stay calm! 🚦"
                ]
            }

            # Select a random prediction from the chosen emotion category
            future_prediction = random.choice(prediction_options.get(
                predicted_emotion, ["Your emotions seem unpredictable. Stay mindful! 🧘"]))

        print("\n📢 **Future Emotion Prediction (4 hours later):**")
        print(future_prediction)

        return future_prediction

    else:
        print("\nNot enough neutral face detections to make a future prediction.")

        return None
