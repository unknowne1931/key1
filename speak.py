import pyttsx3
import time

# Wait for a few seconds before speaking (to ensure the server starts)
time.sleep(3)

engine = pyttsx3.init()
engine.say("Server started")
engine.runAndWait()
