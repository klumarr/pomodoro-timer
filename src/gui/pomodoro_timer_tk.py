import tkinter as tk
from tkinter import messagebox
import os
import platform

# Function to play a notification sound
def play_notification_sound():
    if platform.system() == "Windows":
        try:
            import winsound
            winsound.MessageBeep()
        except ImportError:
            print("Notification sound not supported on this platform.")
    elif platform.system() == "Darwin":  # macOS is identified by 'Darwin'
        os.system("afplay /System/Library/Sounds/Ping.aiff")
    else:
        print("Notification sound not supported on this platform.")

# Global variables to manage timer state
running = False
paused = False
paused_duration = 0

# Function to start the timer
def start_timer(duration, label, is_work=True):
    global running, paused, paused_duration, current_duration, current_is_work
    running = True
    paused = False
    paused_duration = duration
    current_duration = duration
    current_is_work = is_work
    update_timer(label)

# Function to update the timer
def update_timer(label):
    global paused_duration, running, paused
    if running and not paused:
        mins, secs = divmod(paused_duration, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        label.config(text=timeformat)
        if paused_duration > 0:
            paused_duration -= 1
            label.after(1000, update_timer, label)
        else:
            play_notification_sound()
            if current_is_work:
                messagebox.showinfo("Time's up!", "Work session complete. Take a break!")
                global pomodoro_count
                pomodoro_count += 1
                pomodoro_count_label.config(text=f"Pomodoros completed: {pomodoro_count}")
                start_rest_button.pack()
            else:
                messagebox.showinfo("Time's up!", "Break time is over. Back to work!")
                start_work_button.pack()

# Function to pause the timer
def pause_timer():
    global paused
    paused = True

# Function to resume the timer
def resume_timer(label):
    global paused
    paused = False
    update_timer(label)

# Function to stop the timer
def stop_timer():
    global running, paused_duration
    running = False
    paused_duration = current_duration
    label.config(text="25:00" if current_is_work else "05:00")
    start_work_button.pack()
    start_rest_button.pack_forget()

# Function to bring the window to the top
def bring_to_top():
    root.attributes("-topmost", True)
    root.after(1000, lambda: root.attributes("-topmost", False))

# Initialize the main window
root = tk.Tk()
root.title("Pomodoro Timer")

# Variables to track the number of completed Pomodoros
pomodoro_count = 0

# Create the timer label
label = tk.Label(root, font=('Helvetica', 48), text="25:00")
label.pack()

# Create the Pomodoro count label
pomodoro_count_label = tk.Label(root, font=('Helvetica', 12), text=f"Pomodoros completed: {pomodoro_count}")
pomodoro_count_label.pack()

# Create the start work button
start_work_button = tk.Button(root, text="Start Work (25 min)", command=lambda: [start_timer(1500, label), bring_to_top(), start_work_button.pack_forget()])
start_work_button.pack()

# Create the start rest button
start_rest_button = tk.Button(root, text="Start Rest (5 min)", command=lambda: [start_timer(300, label, is_work=False), bring_to_top(), start_rest_button.pack_forget()])
start_rest_button.pack_forget()

# Create the pause button
pause_button = tk.Button(root, text="Pause", command=pause_timer)
pause_button.pack()

# Create the resume button
resume_button = tk.Button(root, text="Resume", command=lambda: resume_timer(label))
resume_button.pack()

# Create the stop button
stop_button = tk.Button(root, text="Stop", command=stop_timer)
stop_button.pack()

# Start the main event loop
root.mainloop()
