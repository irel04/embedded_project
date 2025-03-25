import time
from neutral import emotional_tendency
from emotion_challenge import emotion_detection
from supabase_client import supabase_client

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

# Countdown before starting the challenge
print("Get ready! Starting in...")
for i in range(3, 0, -1):
    print(i)
    time.sleep(1)

print("\nChallenge started! 🎥")

# Run emotion detection
[is_successful, elapsed_time] = emotion_detection(nickname=nickname, selected_emotions=selected_emotions)

# Run emotional tendency prediction
tendency = emotional_tendency()

print(f'Hi {nickname}, here is your challenge result: completed: {is_successful}, elapsed_time: {elapsed_time}, prediction: {tendency}')

# Insert result into Supabase
supabase_client.table("embedded_system").insert({
    "nickname": nickname,
    "is_success": is_successful,
    "time_completed": elapsed_time,
    "prediction": tendency
}).execute()
