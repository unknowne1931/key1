# ki1931ck Done

import requests
import time
import psutil
import subprocess
import pyttsx3

# Configuration
SERVER_SCRIPT = "server.js"
SERVER_URL = "http://localhost/get/questions/from/qno/English"
MAX_RETRIES = 5
RETRY_DELAY = 2  # seconds

# Text-to-Speech Setup
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('voice', engine.getProperty('voices')[1].id)

def speak(text):
    print(f"> {text}")
    engine.say(text)
    engine.runAndWait()

def is_node_server_running(script_name=SERVER_SCRIPT):
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if 'node' in proc.info['name'].lower():
                cmdline = proc.info.get('cmdline', [])
                if cmdline and script_name.lower() in " ".join(cmdline).lower():
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def kill_node_server(script_name="server.js"):
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] == 'node.exe' or 'node' in proc.info['name'].lower():
                cmdline = proc.info.get('cmdline', [])
                if cmdline and script_name.lower() in " ".join(cmdline).lower():
                    print(f"Killing PID {proc.pid} -> {' '.join(cmdline)}")
                    proc.terminate()  # Or proc.kill() for force kill
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


def start_node_server(script_name=SERVER_SCRIPT):
    speak("Starting the server in a minimized window.")
    subprocess.Popen(['start', '/MIN', 'cmd', '/k', f'node {script_name}'], shell=True)
    time.sleep(2)  # Initial wait before polling

def wait_for_server(url, retries=MAX_RETRIES, delay=RETRY_DELAY):
    for i in range(retries):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response
        except requests.exceptions.RequestException:
            speak(f"Waiting for server... ({i + 1}/{retries})")
            time.sleep(delay)
    return None

def main():
    try:
        response = requests.get(SERVER_URL)
        if response.status_code == 200:
            print("Server already running.")
            print("Response:", response.json())
            # kill_node_server("server.js")  # Optional: remove if you don't want to stop it
            # return
        else:
            print(f"Server responded with status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Initial request failed: {e}")
        speak("I will now attempt to start the server.")
        
        if not is_node_server_running():
            start_node_server()
        else:
            speak("Server appears to be running. Waiting for it to respond.")

        response = wait_for_server(SERVER_URL)
        if response:
            speak("Server is now online.")
            print("Final Response:", response.json())
        else:
            speak("Unable to connect to server after multiple attempts.")
            print("Failed to get response after retries.")

if __name__ == "__main__":
    main()
