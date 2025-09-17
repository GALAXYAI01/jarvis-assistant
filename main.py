import speech_recognition as sr
import webbrowser
import pyttsx3
import subprocess
import musiclib
import requests
from openai import OpenAI
from gtts import gTTS
from pygame import mixer
import pygame
import os

engine = pyttsx3.init()
newsapi = "56466cd3aa3d45239445d131afec1d84"   

def speak_old(text):
    engine.say(text)
    engine.runAndWait()
    
def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')   
    
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3")   

    

def aiProcess(command):
    client = OpenAI(api_key="{API_KEY}")
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
    ]
    )
    return completion.choices[0].message.content
def processcommand(command):
    command = command.lower()
    if "open google" in command:
        subprocess.Popen(["start", "https://google.com"], shell=True)
    elif "open facebook" in command:
        subprocess.Popen(["start", "https://facebook.com"], shell=True)
    elif "open youtube" in command:
        subprocess.Popen(["start", "https://youtube.com"], shell=True)
    elif "open gmail" in command:
        subprocess.Popen(["start", "https://gmail.com"], shell=True)
    elif command.startswith("play"):
        song = command.replace("play", "").strip()
        if song in musiclib.music:
            link = musiclib.music[song]
            webbrowser.open(link)
        else:
            speak("Sorry, I don't know that song.")
    elif "news" in command:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles[:5]:  # limit to 5 headlines
                title = article.get('title')
                if title:
                    speak(title)
        else:
            output=aiProcess(command)
            speak(output)
        

if __name__ == "__main__":
    speak("Jarvis is now online")
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Calibrating microphone...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Do this ONCE

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)

            print("Recognizing...")
            command = recognizer.recognize_google(audio)  # still online, but faster now
            print(f"You said: {command}")

            if "jarvis" in command.lower():
                speak("Yes, how can I assist you?")
            else:
                processcommand(command)

        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except Exception as e:
            print(f"Error: {e}")
