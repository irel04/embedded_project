# Face Expression Recognition

## Prerequisite 
1. python 11 below to enable tensorflow

## Installation
1. Clone repository
   ```bash
   git clone https://github.com/irel04/facial_emotion_recognition.git
   cd ./facial_emotion_recognition
   ```
2. Create a virtual environment (venv)

   ```bash
   py -3.[version < 11] -m venv venv
   source venv/Scripts/activate
   ```

   if iisa lang version ng python niyo and 3.11 lang pede na ata ung ganito

   ```bash
   python -m venv venv
   source venv/Scripts/activate
   ```

   Use git bash for this one until lumabas ung parang ganito sa taas ibig sabihin activated na environment pede ka na mag pip install
   
   ![image](https://github.com/user-attachments/assets/ef3385b6-38e0-4ff1-9d68-31f0a92639ab)
4. Install requirements

   ```bash
   pip install -r requirements.txt
   ```
5. Run the program and test

   ```bash
   python main.py
   ```

   dito kahit hindi ka na gumamit ng alias like ung py -3.[version < 11] kasi nasa loob ka na ng environment and matic kung ano ung ginamit mo pang-generate ayon ung python version non

## Challenge Flow
1. A user starts to randomly pick-out three different emotions then the person in-charge will input it on the screen along with its nickname
2. After the camera opens the user will try to imitate the selected emotions in 1-minute
3. Then, once the challenge is completed, camera will now detect and try to predict the hidden emotion on neutral face. After 1-minute it will send the result on the website and the prize box will now open
4. The challenger can now view the result and prediction
   ![image](https://github.com/user-attachments/assets/4dc9859f-b120-4826-80b5-ff7aa6078d75)

   
## FAQs
1. How does the future emotional tendency works?
   - **Emotion detection** 🥉. Script uses opencv to detect faces in realt-time using laptop/desktop webcam along with a pre-trained deep learning model. The model outputs probabilities for 7 emotions: Angry, Disgust, Fear, Happy, Neutral, Sad, and Surprise.
   - **Tracking Trends in Neutral Detection** 🗿. The script looks at the second-highest probability emotion (since a truly neutral face might lean towards another hidden emotion). It then tracks whether the user was slightly Happy, Sad, or Angry while appearing Neutral.  A counter keeps track of how often each of these emotions appeared during neutral moments.
   - **Making Predictions** 📈. After one minute of detection the script analyzes the emotional trends, if no detection, it assumes the user remains neutral, if emotional trend somehow recorded, it calculates the probabilities for Happy, Sad, Angry based on how frequently they appeared. It uses weighted random selection and pick from the pre-defined randomized message

2. How reliable is this prediction? 🤨
   - The prediction approach that was used is not scientifically reliable as we do not have enough train data models for the trends. It is rather a fun, heuristic-based approximations.
   - **A heuristic-based approximation** is a method of making decisions or predictions using rules of thumb, patterns, or past experiences rather than precise calculations or scientific models

 4. How does Heuristic-based approximation applies to our emotion prediction ⛓️‍💥

    _Our emotion detection script follows a heuristic approach because:_
    - It assumes emotional trends continue: If you were slightly happy most of the time while neutral, the script assumes you might feel happy later.
    - It uses a simple rule (most frequent secondary emotion = future emotion).
    - It doesn't analyze deep psychological factors—just observed facial expressions within a short session.
    - It adds randomness to make predictions feel varied, even though emotions are complex and influenced by many factors.


   

