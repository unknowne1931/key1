import speech_recognition as sr
import keyboard
import threading

recognizer = sr.Recognizer()
mic = sr.Microphone()
recording = False
audio_data = None

def listen_in_background():
    global audio_data, recording
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("🎤 Ready. Hold [Space] to speak... Press [Esc] to quit.")
        while True:
            keyboard.wait('space')
            if recording:
                continue

            recording = True
            print("🛑 Listening...")

            # Start recording
            try:
                audio_data = recognizer.listen(source, phrase_time_limit=5)
            except sr.WaitTimeoutError:
                audio_data = None

            while keyboard.is_pressed('space'):
                pass  # Wait until space is released

            if audio_data:
                try:
                    text = recognizer.recognize_google(audio_data)
                    print("📝 You said:", text)
                except sr.UnknownValueError:
                    print("🤷 Couldn't understand.")
                except sr.RequestError as e:
                    print(f"❌ API Error: {e}")
            else:
                print("⚠️ No audio captured.")

            recording = False

# Run listener in the main thread
try:
    listen_thread = threading.Thread(target=listen_in_background)
    listen_thread.start()

    while True:
        if keyboard.is_pressed('esc'):
            print("\n👋 Exiting. Bye!")
            break

except KeyboardInterrupt:
    print("\n👋 Interrupted.")
