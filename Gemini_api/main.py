import speech_recognition as sr
import threading
import tkinter as tk
import keyboard
import time

recognizer = sr.Recognizer()
mic = sr.Microphone()
listening = False
last_speech_time = 0
stop_flag = False

def listen_in_background():
    global listening, stop_flag, last_speech_time

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

    def background_task():
        global stop_flag, last_speech_time
        while listening and not stop_flag:
            with mic as source:
                try:
                    audio = recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    text = recognizer.recognize_google(audio)
                    output_box.config(state='normal')
                    output_box.insert(tk.END, text + '\n')
                    output_box.config(state='disabled')
                    output_box.see(tk.END)
                    last_speech_time = time.time()
                except sr.WaitTimeoutError:
                    pass
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    output_box.insert(tk.END, f"Error: {e}\n")

            # If no speech for 1 second, stop
            if time.time() - last_speech_time > 1:
                stop_listening()

    threading.Thread(target=background_task).start()

def start_listening():
    global listening, stop_flag, last_speech_time
    if not listening:
        output_box.config(state='normal')
        output_box.insert(tk.END, "[Listening started...]\n")
        output_box.config(state='disabled')
        output_box.see(tk.END)
        status_label.config(text="Status: Listening...")
        last_speech_time = time.time()
        stop_flag = False
        listening = True
        listen_in_background()

def stop_listening():
    global listening, stop_flag
    if listening:
        listening = False
        stop_flag = True
        output_box.config(state='normal')
        output_box.insert(tk.END, "[Listening stopped due to silence or keypress]\n")
        output_box.config(state='disabled')
        output_box.see(tk.END)
        status_label.config(text="Status: Not Listening")

def toggle_listening():
    if listening:
        stop_listening()
    else:
        start_listening()

def handle_space_key():
    while True:
        keyboard.wait("space")
        toggle_listening()
        time.sleep(0.2)  # Debounce

# GUI Setup
root = tk.Tk()
root.title("Speech to Text")
root.geometry("600x400")
root.configure(bg="#f0f0f0")

title_label = tk.Label(root, text="Speech to Text", font=("Arial", 20), bg="#f0f0f0")
title_label.pack(pady=10)

status_label = tk.Label(root, text="Status: Not Listening", font=("Arial", 14), bg="#f0f0f0")
status_label.pack()

output_box = tk.Text(root, height=15, wrap='word', state='disabled', font=("Arial", 12)) 
output_box.pack(padx=20, pady=10, fill='both', expand=True)

start_button = tk.Button(root, text="Start Listening (or press Space)", command=toggle_listening,
                         font=("Arial", 14), bg="#007bff", fg="white")
start_button.pack(pady=10)

# Start spacebar listener thread
threading.Thread(target=handle_space_key, daemon=True).start()

# Run the GUI
root.mainloop()
