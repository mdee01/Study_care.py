import tkinter as tk
from tkinter import messagebox
import random
import json
import os

# ---------------- DATA PERSISTENCE ----------------
class DataHandler:
    @staticmethod
    def save_data(data):
        with open("study_data.json", "w") as f:
            json.dump(data, f)

    @staticmethod
    def load_data():
        if os.path.exists("study_data.json"):
            with open("study_data.json", "r") as f:
                return json.load(f)
        return {"moods": []}

# ---------------- STUDY TIMER ----------------
class StudyTimer:
    def __init__(self, canvas, label, username):
        self.canvas = canvas
        self.label = label
        self.username = username
        self.remaining = 0
        self.total = 0

    def start_timer(self, minutes):
        try:
            self.total = int(minutes) * 60
            self.remaining = self.total
            self.countdown()
        except ValueError:
            messagebox.showerror("Error", "Enter valid minutes.")

    def countdown(self):
        if self.remaining >= 0:
            mins, secs = divmod(self.remaining, 60)
            self.label.config(text=f"{mins:02d}:{secs:02d}")
            self.update_ring()
            self.remaining -= 1
            self.label.after(1000, self.countdown)
        else:
            messagebox.showinfo("Time's Up", f"Great work, {self.username}! Time for a break!")

    def update_ring(self):
        self.canvas.delete("all")
        self.canvas.create_oval(10, 10, 190, 190, outline="#ddd", width=10, fill="white")
        extent = 360 * (self.total - self.remaining) / self.total if self.total > 0 else 0
        self.canvas.create_arc(10, 10, 190, 190, start=90, extent=-extent, outline="#4CAF50", width=10, style="arc")

# ---------------- BREAK TRACKER ----------------
class BreakTracker:
    def __init__(self, label):
        self.label = label
        self.remaining = 0

    def start_break(self, minutes):
        try:
            self.remaining = int(minutes) * 60
            self.countdown()
        except ValueError:
            messagebox.showerror("Error", "Enter valid minutes.")

    def countdown(self):
        if self.remaining >= 0:
            mins, secs = divmod(self.remaining, 60)
            self.label.config(text=f"Break: {mins:02d}:{secs:02d}")
            self.remaining -= 1
            self.label.after(1000, self.countdown)
        else:
            self.label.config(text="Break Over!")
            messagebox.showinfo("Break Finished", "Ready to study again? Let's go!")

# ---------------- MOOD TRACKER ----------------
class MoodTracker:
    def __init__(self, data_list):
        self.mood_list = data_list
        self.quotes = [
            "Keep shining!",
            "Stay positive!",
            "Your mood matters!",
            "Every emotion is valid!",
            "You're awesome!"
        ]

    def log_mood(self, mood):
        self.mood_list.append(mood)
        quote = random.choice(self.quotes)
        return f"Mood recorded: {mood}\n\n{quote}"

# ---------------- MAIN APP ----------------
class StudyCareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("StudyCare Tracker")
        self.root.geometry("420x720")
        self.root.configure(bg="#e3f2fd")
        
        self.data = DataHandler.load_data()
        self.build_ui()

    def build_ui(self):
        title = tk.Label(self.root, text="StudyCare Tracker", font=("Arial", 26, "bold"), bg="#e3f2fd", fg="#2c3e50")
        title.pack(pady=10)

        # ---------- NAME ----------
        tk.Label(self.root, text="Enter Your Name:", bg="#e3f2fd").pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack(pady=5)
        self.name_entry.bind("<Return>", lambda event: self.set_name())
        
        tk.Button(self.root, text="Confirm Name", bg="#8bc34a", fg="white", command=self.set_name).pack(pady=5)
        self.name_label = tk.Label(self.root, text="Name: --", bg="#e3f2fd", font=("Arial", 10, "bold"))
        self.name_label.pack(pady=5)

        # ---------- 1. STUDY TIMER ----------
        tk.Label(self.root, text="Study Timer", font=("Arial", 14, "bold"), bg="#e3f2fd").pack()
        self.timer_entry = tk.Entry(self.root)
        self.timer_entry.pack(pady=5)
        self.timer_entry.bind("<Return>", lambda event: self.start_timer())
        
        self.timer_canvas = tk.Canvas(self.root, width=200, height=200, bg="#e3f2fd", highlightthickness=0)
        self.timer_canvas.pack(pady=5)
        self.timer_label = tk.Label(self.root, text="00:00", font=("Arial", 24), bg="#e3f2fd")
        self.timer_label.pack(pady=5)
        self.timer_button = tk.Button(self.root, text="Start Study", bg="#4CAF50", fg="white", command=self.start_timer)
        self.timer_button.pack(pady=5)
        self.timer_button.config(state="disabled")

        # ---------- 2. BREAK TRACKER ----------
        tk.Label(self.root, text="Study Break Tracker", font=("Arial", 14, "bold"), bg="#e3f2fd").pack()
        self.break_entry = tk.Entry(self.root)
        self.break_entry.pack(pady=5)
        self.break_entry.bind("<Return>", lambda event: self.start_break())
        
        self.break_label = tk.Label(self.root, text="Break: --:--", font=("Arial", 18), bg="#e3f2fd", fg="#2980b9")
        self.break_label.pack(pady=5)
        self.break_button = tk.Button(self.root, text="Start Break", bg="#2196F3", fg="white", command=self.start_break)
        self.break_button.pack(pady=5)
        self.break_button.config(state="disabled")

        # ---------- 3. MOOD TRACKER ----------
        tk.Label(self.root, text="Mood Tracker", font=("Arial", 14, "bold"), bg="#e3f2fd").pack()
        self.mood_entry = tk.Entry(self.root)
        self.mood_entry.pack(pady=5)
        self.mood_entry.bind("<Return>", lambda event: self.log_mood())
        
        self.mood_button = tk.Button(self.root, text="Log Mood", bg="#FF9800", fg="white", command=self.log_mood)
        self.mood_button.pack(pady=5)
        self.mood_label = tk.Label(self.root, text="Last Mood: --", bg="#e3f2fd", font=("Arial", 12))
        self.mood_label.pack()
        self.mood_button.config(state="disabled")

        # ---------- REPORT ----------
        tk.Button(self.root, text="Show Report", bg="#F44336", fg="white", command=self.show_report).pack(pady=20)

    def set_name(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter your name!")
            return
        self.username = name
        self.name_label.config(text=f"Name: {self.username}")
        
        self.timer = StudyTimer(self.timer_canvas, self.timer_label, name)
        self.break_tracker = BreakTracker(self.break_label)
        self.mood_tracker = MoodTracker(self.data['moods'])

        # Enable buttons
        self.timer_button.config(state="normal")
        self.break_button.config(state="normal")
        self.mood_button.config(state="normal")
        messagebox.showinfo("Welcome", f"Hello {name}! Let's start!")

    def start_timer(self):
        self.timer.start_timer(self.timer_entry.get())

    def start_break(self):
        self.break_tracker.start_break(self.break_entry.get())

    def log_mood(self):
        mood = self.mood_entry.get()
        if mood:
            result = self.mood_tracker.log_mood(mood)
            self.mood_label.config(text=f"Last Mood: {mood}")
            messagebox.showinfo("Mood Tracker", result)
            DataHandler.save_data(self.data)
        else:
            messagebox.showwarning("Warning", "Please enter your mood!")

    def show_report(self):
        moods = ", ".join(self.data['moods']) if self.data['moods'] else "None"
        report = f"""
Report for {self.username}

Moods Logged: {moods}
"""
        messagebox.showinfo("Your Report", report)

# ---------------- RUN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = StudyCareApp(root)
    root.mainloop()
