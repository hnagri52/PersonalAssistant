import os
import speech_recognition as sr
import datetime as dt
import pyttsx3
import wikipedia
import webbrowser
import pygame
import random
import smtplib

#setup the speaking assistant
engine = pyttsx3.init("nsss")
voices = engine.getProperty("voices")
# print(voices)
engine.setProperty("voice", voices[7].id)



def speak(audio):
    """Will relay a message back to the user"""
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    """Greet the user with basic hello"""
    hour = int(dt.datetime.now().hour)
    if hour>= 0 and hour<12:
        speak("Good Morning")
    elif hour>=12 and hour<18:
        speak("Good afternoon!")
    else:
        speak("Good Evening")

    speak("I am your personal assistant! How may I help you?")

def takeCommand():
    """Will take a voice command from user, and return a string output"""

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing... ")
        voice_input = r.recognize_google(audio, language="en-US")
        print(f"The user said: {voice_input}\n")
    except Exception as e:
        # print(e)
        print("Please say that again")
        return "None"
    return voice_input


def musiconloop(song, keyword):
    """Will play music files"""
    pygame.mixer.init()
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    while True:
        inp = input(f"Please enter {keyword} to continue: ")
        if inp == keyword:
            pygame.mixer.music.stop()
            break;

def sendEmail(recipient, content):
    """Will send a personal email"""
    server = smtplib.SMTP("smtp@gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login("youremail@gmail.com", "password")
    server.sendmail("youremail@gmail.com", recipient, content)
    server.close()

def main():
    wishMe()

    while True:
        voice_command = takeCommand().lower()
        print(f"lower case: {voice_command}")
        if "wikipedia" == voice_command:
            continue
        if "wikipedia" in voice_command:
            speak("Searching Wikipedia...")
            voice_command = voice_command.replace("wikipedia", "")
            results = wikipedia.summary(voice_command, sentences=2)
            print(results)
            speak("According to wikipedia," + results)
        elif "open youtube" in voice_command or "open youtube.com" in voice_command:
            webbrowser.open("https://www.youtube.com")
        elif "open google" in voice_command or "open google.com" in voice_command:
            webbrowser.open("https://www.google.ca")
        elif "open facebook" in voice_command or "open facebook.com" in voice_command:
            webbrowser.open("https://www.facebook.com")
        elif "play music" in voice_command or "put on a song" in voice_command:
            mus_dir = os.chdir(r"/Users/husseinnagri/Music/iTunes/iTunes Media/Music/Unknown Artist/Unknown Album")
            songs = os.listdir(mus_dir)
            print(songs)
            for song in songs:
                if ".mp3" in song:
                    continue
                elif ".mp3" not in song:
                    songs.remove(song)
            musiconloop(random.choice(songs), "done")

        elif "the time" in voice_command or "time" in voice_command:
            strTime = dt.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime} right now!")

        elif "open code" in voice_command:
            os.system("open -a /Applications/Xcode.app ")

        elif "what is your name" in voice_command:
            speak("My name is Jarvis! I will be your personal assistant.")
        elif "send email" in voice_command:
            try:
                speak("What should I say? ")
                email_content = takeCommand()
                to = "husseinnagri@hotmail.com"
                sendEmail(to, email_content)
                speak("The email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry, the email could not be sent!")


if __name__ == '__main__':
    main()
