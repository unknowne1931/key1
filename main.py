import requests
import os
import sys
import time

def fetch_languages():
    url = "http://localhost/all/lang/data"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and "data" in data and isinstance(data["data"], list):
                languages = data["data"]
                if languages:
                    print("Available languages:")
                    for index, lang in enumerate(languages, start=1):
                        print(f"{index}. {lang}")
                    return languages
            print("No languages found.")
            return []
        else:
            print("Failed to fetch languages. Status code:", response.status_code)
            print(response)
            return []
    except requests.exceptions.RequestException as e:
        print("Error fetching languages:", e)
        os.system("start_ai.bat")
        return []

def loading_spinner():
    spinner = ["|", "/", "-", "\\"]
    for _ in range(20):  # Runs for 20 iterations
        for symbol in spinner:
            sys.stdout.write(f"\rLoading {symbol}")  # Overwrites the line
            sys.stdout.flush()
            time.sleep(0.1)

    sys.stdout.write("\rLoading complete!   \n")
    sys.stdout.flush()

def fetch_data():
    while True:
        user_input = input("Type 'help' (or type 'exit' to quit) $: ")
        if user_input.lower() == "exit":
            print("Exiting...")
            break
        elif user_input.lower() == "lang":
            fetch_languages()
        elif user_input.lower() == "help":
            os.system("cls")
            print("Help -------------------------")
            print("'lang'     : check list of language")
            print("'cls'      : clear screen")
            print("'c etoto'  : Change Question tough from Easy Medium Tough from Users Answerd")
            print("'show qno' : Check the Question Number list only a Question Number and Tough [Easy, Medium, Tough]")
            # print("lang = "
        elif user_input.lower() == "cls":
            os.system("cls") 
    
        elif user_input.lower() == "start tough":
            os.system("start_tough.bat")

        
        elif user_input.lower() == "show qno":
            languages = fetch_languages()
            print(f"I Found these Languages : {languages}" )
            i = input("Select any One Language : ")
            print("")
            url = f"http://localhost/all/{i}"

            if i in languages:
                try:
                    response = requests.get(url)
                    loading_spinner()
                    if response.status_code == 200:
                        print("Response:", response.json())
                    else:
                        print("Failed to fetch data. Status code:", response.status_code)
                except requests.exceptions.RequestException as e:
                    print("Error fetching data:", e)
            else:
                print(f"{i} not found in Languages Data")


        elif user_input.lower() == "c etoto":

            languages = fetch_languages()
            print(f"I Found these Languages : {languages}" )
            i = input("Select any One Language : ")
            print("")
            url = f"http://localhost/get/questions/from/qno/{i}"

            if i in languages:
                try:
                    response = requests.get(url)
                    loading_spinner()
                    if response.status_code == 200:
                        print("Response:", response.json())
                    else:
                        print("Failed to fetch data. Status code:", response.status_code)
                except requests.exceptions.RequestException as e:
                    print("Error fetching data:", e)
            else:
                print(f"{i} not found in Languages Data")

            
        
        else:
            print("Invalid input. Please enter a valid language from the list or type 'exit' to quit.")

if __name__ == "__main__":
    fetch_data()














# import requests
# import os
# import sys
# import time
# import cmd

# try:
#     import pyreadline3  # Import pyreadline3 for Windows
# except ImportError:
#     pyreadline3 = None  # Fallback if not installed

# class LanguageShell(cmd.Cmd):
#     prompt = "Type 'help' (or type 'exit' to quit) $: "
    
#     def __init__(self):
#         super().__init__()
#         self.languages = []

#     def fetch_languages(self):
#         """Fetch and display available languages from API"""
#         url = "http://localhost/all/lang/data"
#         try:
#             response = requests.get(url)
#             if response.status_code == 200:
#                 data = response.json()
#                 if isinstance(data, dict) and "data" in data and isinstance(data["data"], list):
#                     self.languages = data["data"]
#                     print("\nAvailable languages:")
#                     for index, lang in enumerate(self.languages, start=1):
#                         print(f"{index}. {lang}")
#                     return
#             print("No languages found.")
#         except requests.exceptions.RequestException as e:
#             print("Error fetching languages:", e)
#             os.system("start_ai.bat")

#     def loading_spinner(self):
#         """Show a loading spinner"""
#         spinner = ["|", "/", "-", "\\"]
#         for _ in range(10):  # Reduce iterations for better speed
#             for symbol in spinner:
#                 sys.stdout.write(f"\rLoading {symbol}")
#                 sys.stdout.flush()
#                 time.sleep(0.1)
#         sys.stdout.write("\rLoading complete!\n")
#         sys.stdout.flush()

#     def do_lang(self, arg):
#         """Check the list of languages"""
#         self.fetch_languages()

#     def do_cls(self, arg):
#         """Clear the console screen"""
#         os.system("cls" if os.name == "nt" else "clear")

#     def do_show_qno(self, arg):
#         """Check the question number list"""
#         if not self.languages:
#             self.fetch_languages()

#         print(f"I Found these Languages: {self.languages}")
#         i = input("Select any One Language: ").strip()

#         if i in self.languages:
#             url = f"http://localhost/all/{i}"
#             try:
#                 response = requests.get(url)
#                 self.loading_spinner()
#                 if response.status_code == 200:
#                     print("Response:", response.json())
#                 else:
#                     print("Failed to fetch data. Status code:", response.status_code)
#             except requests.exceptions.RequestException as e:
#                 print("Error fetching data:", e)
#         else:
#             print(f"'{i}' not found in Languages Data.")

#     def do_c_etoto(self, arg):
#         """Change Question Toughness based on user's answers"""
#         if not self.languages:
#             self.fetch_languages()

#         print(f"I Found these Languages: {self.languages}")
#         i = input("Select any One Language: ").strip()

#         if i in self.languages:
#             url = f"http://localhost/get/questions/from/qno/{i}"
#             try:
#                 response = requests.get(url)
#                 self.loading_spinner()
#                 if response.status_code == 200:
#                     print("Response:", response.json())
#                 else:
#                     print("Failed to fetch data. Status code:", response.status_code)
#             except requests.exceptions.RequestException as e:
#                 print("Error fetching data:", e)
#         else:
#             print(f"'{i}' not found in Languages Data.")

#     def do_exit(self, arg):
#         """Exit the shell"""
#         print("Goodbye!")
#         return True  # Exits the command loop

#     def completedefault(self, text, line, begidx, endidx):
#         """Enable tab auto-completion for commands"""
#         commands = ["lang", "cls", "show_qno", "c_etoto", "exit"]
#         return [cmd for cmd in commands if cmd.startswith(text)]

# if __name__ == "__main__":
#     if pyreadline3:
#         print("Tab completion enabled for Windows!")
#     else:
#         print("Tab completion not available. Install 'pyreadline3' using 'pip install pyreadline3'.")

#     LanguageShell().cmdloop()
