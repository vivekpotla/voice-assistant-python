import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import python_weather
import asyncio

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#setting listening and speaking
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


def setVolume(vol):
    # Get default audio device using PyCAW
    if vol == 'half':
        volume.SetMasterVolumeLevelScalar(0.5, None)
        vl = str((int)(volume.GetMasterVolumeLevelScalar() * 100)) + "%"
        talk("volume set to "+ vl)
        print("volume set to " + vl)

    elif vol == 'zero':
        volume.SetMasterVolumeLevelScalar(0, None)
        vl = str((int)(volume.GetMasterVolumeLevelScalar() * 100)) + "%"
        print("volume set to "+ vl)
    elif vol == 'full' or vol == 'high':
        volume.SetMasterVolumeLevelScalar(1, None)
        vl = str((int)(volume.GetMasterVolumeLevelScalar() * 100)) + "%"
        talk("volume set to "+ vl)
        print("volume set to " + vl)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def getdate():
    x = datetime.date.today()
    talk("the date is " + x.strftime("%b %d %Y"))
    print("the date is " + x.strftime("%b %d %Y"))


async def getweather(city):
    async with python_weather.Client(format=python_weather.IMPERIAL) as client:
        weather = await client.get(city)
        cel = round((weather.current.temperature - 32) * (5 / 9), 2)
        talk("Temperature in " + city + "is " + str(cel) + "degree celcius")
        print("Temperature in " + city + "is " + str(cel) + "degree celcius")


def take_command():
    with sr.Microphone() as source:
        print('listening...')
        voice = listener.listen(source)
        command = listener.recognize_google(voice)
        command = command.lower()
        if 'hey buddy' in command:
            command = command.replace('hey buddy', '')
            print(command)

    return command


def run_siri():
    command = take_command()

    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    elif 'weather' in command:
        city = command.replace('what is the weather in', '')
        asyncio.run(getweather(city))
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
        print('Current time is ' + time)
    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 2)
        print(info)
        talk(info)
    elif 'set volume to' in command:
        vol = command.replace('set volume to', '')
        setVolume(vol)
        talk(vol + " set")
        print("Volume set to 100%")
    elif 'good morning' in command:
        talk("Very Good morning Buddy , Have a nice day ahead ")
        print("Very Good morning Buddy , Have a nice day ahead ")
    elif 'good night' in command:
        talk("Good night Buddy , Sweet Dreams ")
        print("Good night Buddy , Sweet Dreams ")
    elif 'good afternoon' in command:
        talk("Good afternoon Buddy ")
        print("Good afternoon Buddy ")
    elif 'good evening' in command:
        talk("Good evening")
        print("Good evening")
    elif 'date' in command:
        getdate()
    elif 'are you single' in command:
        talk('No I am in relationship with laptop')
        
    elif 'joke' in command:
        joke =pyjokes.get_joke(language="en", category="all")
        talk(joke)
        print(joke)
    elif 'stop' or 'bye' in command:
        talk("Bye Buddy, talk to you later")
        quit()
    else:
        talk('Please say the command again.')


#main
while True:
    run_siri()
#setVolume('half')
