from __future__ import print_function
import datetime as dt
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser
import pygame
import random
import smtplib
import pytz

#setup the speaking assistant
engine = pyttsx3.init("nsss")
voices = engine.getProperty("voices")
# print(voices)
engine.setProperty("voice", voices[7].id)


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
MONTHS = ["january", "february", "march", "april", "may", "june","july", "august", "september","october", "november", "december"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]
CALENDAR_STRS = ["what do i have", "do i have plans", "am i busy", "what's happening on", "do i have anything"]

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


def authenticate_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)


    return service

def get_events(day, service):
    # Call the Calendar API

    date = dt.datetime.combine(day, dt.datetime.min.time())
    end_date = dt.datetime.combine(day, dt.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)


    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(),
                                          timeMax = end_date.isoformat(), singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak('No upcoming events found.')
    else:
        speak(f"You have {len(events)} events on this day!")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split("T")[1].split("-")[0])
            if(int(start_time.split(":")[0]) < 12):
                start_time = start_time + "am"
            else:
                start_time = str(int(start_time.split(":")[0]) -12)
                start_time = start_time + "pm"

            speak(event["summary"] + "at" + start_time)

def get_date(text):
    text = text.lower()
    today = dt.date.today()
    if text.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year


    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass

    if month < today.month and month != -1:
        year = year +1

    if day < today.day and month == -1 and day != -1:
        month = month + 1

    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week


        if dif < 0:
            dif += 7
            if text.count("next") >=1:
                dif +=7
        return today + dt.timedelta(dif)
    if day == -1 or month == -1:
        return None

    return dt.date(month=month, day=day, year=year)




def main():
    wishMe()

    while True:
        service = authenticate_google()
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
        for phrase in CALENDAR_STRS:
            if phrase in voice_command:
                date = get_date(voice_command)
                if date:
                    get_events(date, service)
                else:
                    speak("I didn't catch that! Please try again!")





if __name__ == '__main__':
    main()


 #   text = takeCommand().lower()
  #  print(get_date(text))