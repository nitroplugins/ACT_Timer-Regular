import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import time
import threading

# Constants for the regular time timer
sections = [
    {"name": "English", "time": 45, "questions": 75, "seconds_per_question": 45 * 60 / 75},
    {"name": "Math", "time": 60, "questions": 60},
    {"name": "Break", "time": 10, "questions": None},
    {"name": "Reading", "time": 35, "questions": 40, "seconds_per_question": 35 * 60 / 40},
    {"name": "Science", "time": 35, "questions": 40, "seconds_per_question": 35 * 60 / 40},
]

class ACTTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ACT Regular Time Timer")
        self.current_section_index = 0
        self.time_left = 0
        self.running = False
        self.paused = False
        self.full_test_mode = False

        # UI Elements
        self.section_var = tk.StringVar(value="Full Test")
        self.section_label = tk.Label(root, text="Select Section:", font=("Helvetica", 14))
        self.section_menu = ttk.Combobox(root, textvariable=self.section_var, state="readonly", font=("Helvetica", 14))
        self.section_menu['values'] = ["Full Test"] + [section["name"] for section in sections]
        self.section_menu.bind("<<ComboboxSelected>>", self.set_section)

        self.current_section_display = tk.Label(root, text="", font=("Helvetica", 18), fg="blue")
        self.timer_label = tk.Label(root, text="", font=("Helvetica", 48))
        self.pacing_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.start_button = tk.Button(root, text="Start", command=self.start_timer, font=("Helvetica", 12))
        self.pause_button = tk.Button(root, text="Pause", command=self.pause_timer, font=("Helvetica", 12))
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer, font=("Helvetica", 12))

        # Layout
        self.section_label.pack(pady=10)
        self.section_menu.pack(pady=10)
        self.current_section_display.pack(pady=5)
        self.timer_label.pack(pady=10)
        self.progress.pack(pady=10)
        self.pacing_label.pack(pady=10)
        self.start_button.pack(side=tk.LEFT, padx=20, pady=20)
        self.pause_button.pack(side=tk.LEFT, padx=20, pady=20)
        self.reset_button.pack(side=tk.RIGHT, padx=20, pady=20)

        # Initialize UI
        self.update_ui()

    def set_section(self, event=None):
        selected_section = self.section_var.get()
        if selected_section == "Full Test":
            self.full_test_mode = True
            self.current_section_index = 0
        else:
            self.full_test_mode = False
            self.current_section_index = [section["name"] for section in sections].index(selected_section)
        self.time_left = sections[self.current_section_index]["time"] * 60
        self.update_ui()

    def start_timer(self):
        if not self.running:
            self.running = True
            self.paused = False
            threading.Thread(target=self.run_timer).start()

    def pause_timer(self):
        if self.running:
            self.paused = not self.paused
            self.pause_button.config(text="Resume" if self.paused else "Pause")

    def reset_timer(self):
        self.running = False
        self.paused = False
        self.time_left = 0
        self.current_section_index = 0
        self.full_test_mode = False
        self.section_var.set("Full Test")
        self.pause_button.config(text="Pause")
        self.update_ui()

    def run_timer(self):
        while self.running and self.time_left > 0:
            if not self.paused:
                time.sleep(1)
                self.time_left -= 1
                self.update_ui()

        if self.running and not self.paused:
            self.running = False
            if self.full_test_mode and self.current_section_index < len(sections) - 1:
                self.current_section_index += 1
                self.time_left = sections[self.current_section_index]["time"] * 60
                self.start_timer()
            elif self.full_test_mode and self.current_section_index == len(sections) - 1:
                messagebox.showinfo("ACT Timer", "Test Complete!")
            else:
                messagebox.showinfo("ACT Timer", "Time's up!")

    def update_ui(self):
        section = sections[self.current_section_index]
        minutes, seconds = divmod(self.time_left, 60)
        self.timer_label.config(text=f"{minutes:02}:{seconds:02}")
        self.current_section_display.config(text=f"Current Section: {section['name']}")

        if "questions" in section and section["questions"]:
            elapsed = (section["time"] * 60 - self.time_left)
            questions_done = int(elapsed / section["seconds_per_question"])
            self.pacing_label.config(text=f"You should have completed ~{questions_done} questions.")
        else:
            self.pacing_label.config(text="")

        self.progress["value"] = ((section["time"] * 60 - self.time_left) / (section["time"] * 60)) * 100 if self.time_left > 0 else 0

# Create the main application window
if __name__ == "__main__":
    root = tk.Tk()
    app = ACTTimerApp(root)
    root.mainloop()
