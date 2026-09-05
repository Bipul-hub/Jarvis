import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import ollama 
from gtts import gTTS   
import pygame
import os

recognizer = sr.Recognizer()
newsapi = "6348032d4ad145fea073122c6db24672"

def speak_old(text):
    engine = pyttsx3.init("sapi5")
    engine.setProperty("rate", 150)
    engine.setProperty("volume", 1.0)
    engine.say(text)
    engine.runAndWait()
    engine.stop()  

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def ask_ollama(command):
    completion = ollama.chat(
        model="llama3.2:3b",
        messages=[
            { "role": "system",
               "content": "You are a virtual assistant named Jarvis, skilled in general tasks like Alexa and Google cloud. Give short responses." 
            },
            { "role": "user",
               "content": command
            }
        ],
        keep_alive = "5m",
        options ={"num_predict":300}
    ) 
    return completion["message"]["content"]

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        print("NEWS COMMAND DETECTED!")

        try:
            r = requests.get(
                f"https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={newsapi}",
                timeout=10
            )

            print("News API status:", r.status_code)
            print("Response:", r.text)

            if r.status_code == 200:
                data = r.json()
                articles = data.get("articles", [])

                print("Number of articles:", len(articles))

                for article in articles[:5]:
                    title = article.get("title")

                    if title:
                        print(title)
                        speak(title)

            else:
                speak("Sorry, I could not get the news.")

        except Exception as e:
            print("News error:", e)
            speak("There was an error getting the news.")

    else:
        output = ask_ollama(c) 
        print("Jarvis:", output) 
        speak(output)
        


if __name__ == "__main__":
    speak("Initializing jarvis.....")

    while True:
        #Listen for the wake word "Jarvis"
        r = sr.Recognizer()
        
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            
            word = r.recognize_google(audio)
            if (word.lower() == "jarvis"):
                speak("Ya")
                #Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    print("command:", command)

                    processCommand(command)
        
        except Exception as e:
            print("Error; {0}".format(e))

