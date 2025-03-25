# Embedded Project - Facial Expression Recognition

## Challenge Flow
1. A user starts to randomly pick-out three different emotions then the person in-charge will input it on the screen along with its nickname
2. After the camera opens the user will try to imitate the selected emotions in 1-minute
3. Then, once the challenge is completed, camera will now detect and try to predict the hidden emotion on neutral face. After 1-minute it will send the result on the website and the prize box will now open
4. The challenger can now view the result and assessment
   
   ![image](https://github.com/user-attachments/assets/4dc9859f-b120-4826-80b5-ff7aa6078d75)

   
## FAQs & Disclaimer  

### 1. How does the future emotional tendency work?  
- **Emotion Detection** 🥉:  
  The script uses OpenCV to detect faces in real-time via a laptop/desktop webcam, alongside a pre-trained deep learning model. The model predicts probabilities for seven emotions: **Angry, Disgust, Fear, Happy, Neutral, Sad, and Surprise**.  

- **Tracking Trends in Neutral Detection** 🗿:  
  The script analyzes the second-highest probability emotion when a face is detected as Neutral. This helps determine if the user was slightly Happy, Sad, or Angry while appearing Neutral. A counter tracks how often these emotions occur during neutral moments.  

- **Making Assessment** 📈:  
  After one minute of detection, the script analyzes emotional trends. If no clear trend is detected, it assumes the user remains Neutral. Otherwise, it calculates probabilities for **Happy, Sad, or Angry** based on observed frequencies. A weighted random selection is then used to pick a pre-defined, randomized message.  

### 2. How reliable is this assessment? 🤨  
- This prediction method is **not scientifically validated** since we lack sufficient training data on emotional trends. It is meant to be a **fun, heuristic-based approximation** rather than an accurate psychological assessment.  

- **What is heuristic-based approximation?** 🤔  
  It refers to making predictions using patterns, past observations, and simplified rules instead of precise calculations or deep scientific models.  

### 3. How does heuristic-based approximation apply to our emotion assessment? ⛓️‍💥  
Our emotion detection script follows a **heuristic approach** because:  
- It assumes emotional trends continue—if you appeared slightly Happy most of the time while Neutral, it assess you may feel Happy later.  
- It applies a simple rule: **the most frequently observed secondary emotion = might be future emotion**.  
- It does not analyze deep psychological factors—only facial expressions observed within a short session.  
- It incorporates randomness to keep assessment varied, acknowledging that emotions are complex and influenced by multiple factors.  

---

This project is designed for **entertainment and experimental purposes only**. It is not intended for clinical or psychological evaluations. Enjoy and have fun with the results! 🎭  


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
