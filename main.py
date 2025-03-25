import tkinter as tk
from tkinter import messagebox
import time
import threading
from emotion_assumption import emotional_tendency
from emotion_challenge import emotion_detection
from supabase_client import supabase_client

# Emotion labels
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

class EmotionChallengeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Emotion Challenge")
        self.root.geometry("500x400")

        # Nickname input
        self.nickname_label = tk.Label(root, text="Enter your nickname:")
        self.nickname_label.pack()
        self.nickname_entry = tk.Entry(root)
        self.nickname_entry.pack()

        # Emotion selection
        self.selected_emotions = set()
        self.emotion_checkbuttons = []
        self.emotion_vars = {}

        self.emotion_label = tk.Label(root, text="Select 3 emotions to demonstrate:", pady=10)
        self.emotion_label.pack()

        for emotion in emotion_labels:
            if emotion != "Neutral":  # Exclude "Neutral" from the checkboxes
                var = tk.IntVar()
                chk = tk.Checkbutton(root, text=emotion, variable=var, command=self.update_selected_emotions)
                chk.pack(anchor="w", padx=30, pady=2)  # Added padding for better spacing
                self.emotion_checkbuttons.append(chk)
                self.emotion_vars[emotion] = var

        # Start button
        self.start_button = tk.Button(root, text="Start Challenge", command=self.start_challenge)
        self.start_button.pack()

        # Countdown label
        self.status_label = tk.Label(root, text="")
        self.status_label.pack()

        # Reset button
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_app, state=tk.DISABLED)
        self.reset_button.pack()

    def update_selected_emotions(self):
        """Ensures only 3 emotions are selected."""
        self.selected_emotions = {emotion for emotion, var in self.emotion_vars.items() if var.get() == 1}

        if len(self.selected_emotions) > 3:
            # Uncheck the last selected one
            for emotion, var in self.emotion_vars.items():
                if emotion not in self.selected_emotions:
                    var.set(0)
                    break
            self.selected_emotions = {emotion for emotion, var in self.emotion_vars.items() if var.get() == 1}

    def start_challenge(self):
        """Runs the emotion challenge."""
        nickname = self.nickname_entry.get().strip()
        if not nickname:
            messagebox.showerror("Error", "Please enter your nickname.")
            return

        if len(self.selected_emotions) != 3:
            messagebox.showerror("Error", "Please select exactly 3 emotions.")
            return

        self.start_button.config(state=tk.DISABLED)
        self.status_label.config(text="Get ready! Starting in 3...")
        self.root.update()

        # Countdown
        def countdown():
            for i in range(3, 0, -1):
                self.status_label.config(text=f"Starting in {i}...")
                self.root.update()
                time.sleep(1)

            self.status_label.config(text="Challenge started! 🎥")
            self.root.update()

            # Run emotion detection
            is_successful, elapsed_time = emotion_detection(nickname=nickname, selected_emotions=self.selected_emotions)

            # Run emotional tendency prediction
            tendency = emotional_tendency()


            # Insert result into Supabase
            supabase_client.table("embedded_system").insert({
                "nickname": nickname,
                "is_success": is_successful,
                "time_completed": elapsed_time,
                "prediction": tendency
            }).execute()

            self.reset_button.config(state=tk.NORMAL)
        
       

        threading.Thread(target=countdown, daemon=True).start()

    def reset_app(self):
        """Resets the application."""
        self.nickname_entry.delete(0, tk.END)
        for var in self.emotion_vars.values():
            var.set(0)
        self.selected_emotions.clear()
        self.status_label.config(text="")
        self.start_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)

# Run the GUI
root = tk.Tk()
app = EmotionChallengeApp(root)
root.mainloop()
