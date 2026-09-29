import speech_recognition as sr
import pyttsx3
from datetime import datetime

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now")
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Could not understand.")
        except sr.RequestError as e:
            print(f"Api Error: {e}")

    return ""

def respond_to_command(command):
    if "hello" in command or "hi" in command:
        speak("Hi there! how can i help you?")
    elif "your name" in command:
        speak("I am your Python voice assistant.")
    elif "time" in command:
        now = datetime.now().strftime("%H:%M")
        speak(f"The time is {now}")
    elif "How are you today" in command:
        speak("I am feeling great! How About you?")
    elif "good" in command or "fine" in command or "great" in command:
        speak("Im very happy to hear that!")
    elif "bad" in command or "sad" in command or "not feeling well" in command:
        speak("Oh okay, let's hope we can change that!")
    elif "Thanks" in command or "Thank you" in command:
        speak("No problem")
    elif "what is your favorite fruit" in command:
        speak("I may be a program, but that doesn't stop me from having a favorite fruit. I love mangoes.")
    elif "What do you think of Apple" in command:
        speak("I think they are also very delicious, i love their sweet taste.")
    elif "exit" in command or "stop" in command:
        speak("Goodbye")
        return False
    else:
        speak("I'm not sure how to help with that.")
    return True

def main():
    speak("Voice assistant activated. Say something")
    while True:
        command = get_audio()
        if command and not respond_to_command(command):
            break

if __name__ == "__main__":
    main()


