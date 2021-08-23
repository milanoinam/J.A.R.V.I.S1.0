import pyttsx3 
import speech_recognition as sr
import datetime
import os
import cv2
import random
import requests
import wikipedia
import webbrowser
import pywhatkit
import smtplib # SMTP/ESMTP client class (module)
import sys
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import instaloader
from pywikihow import search_wikihow


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices',voices[0].id)
# engine.setProperty('rate',210)
# text to speech
def speak(string):
    engine.say(string)
    print(string)
    engine.runAndWait()

# voice (from mic) to text
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source,phrase_time_limit=5)        # i removed the timeout parameter
        # timeout : number of seconds the system waits for a response from the user before raising WaitTimeoutError

        try:
            print("Recognizing...")
            query = r.recognize_google(audio,language="en-in")
            print(f"user said:{query}")
        except Exception as e:
            speak("Sorry Sir, I am not able to understand your command")
            print("returning 'none'")
            return "none"

    return query

def wish():
    hour = int(datetime.datetime.now().hour)

    if hour>=0 and hour<=12:
        speak("Good Morning, Sir")
    elif hour>=12 and hour <= 18:
        speak("Good Afternoon, Sir")
    else:
        speak("Good Evening, Sir")
    

    t = time.strftime('%I:%M %p')
    speak(f"It is {t}")
    speak("I am Jarvis. Please tell me how can I help you?")

def news():
    main_url = "https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=061d740d7ad24f0a9f195a37ee368446"
    main_page = requests.get(main_url).json()
    articles = main_page["articles"]
    print(articles)
    head = []
    day = ["first","second","third","fourth","fifth","sixth","seventh","eighth","ninth","tenth"]
    for ar in articles:
        head.append(ar["title"])

    for i in range (len(day)):
        speak(f"today's {day[i]} news is: {head[i]}")
    speak("Sir, do you need help with anything else?")

def account_info():
    with open('account_info.txt','r') as f:
        info = f.read().split()
        email = info[0]
        password = info[1]
    return email, password

def tweet():
   
    email, password = account_info()

    tweet = "this is a testing tweet2"
    options = Options()
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(options=options)

    driver.get("https://twitter.com/login")

    email_xpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[1]/label/div/div[2]/div/input'
    password_xpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[2]/label/div/div[2]/div/input'
    login_xpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[3]/div/div'

    time.sleep(2)

    driver.find_element_by_xpath(email_xpath).send_keys(email)
    time.sleep(0.5)
    driver.find_element_by_xpath(password_xpath).send_keys(password)
    time.sleep(0.5)
    driver.find_element_by_xpath(login_xpath).click()

    tweet_xpath = '//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a/div/span/div/div/span/span'
    message_xpath = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[3]/div/div/div/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div/div/div/div'
    post_xpath = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[3]/div/div/div/div[1]/div/div/div/div/div[2]/div[3]/div/div/div[2]/div[4]/div/span/span'

    time.sleep(2)

    driver.find_element_by_xpath(tweet_xpath).click()
    time.sleep(0.5)
    driver.find_element_by_xpath(message_xpath).send_keys(tweet)
    time.sleep(0.5)
    driver.find_element_by_xpath(post_xpath).click()
    speak("it's done, sir")

def openProg(progpath):
    try:
        os.startfile(progpath)
    except Exception as e:
        print(e)
        speak("sorry, the program you requested cannot be opened")



def closeProg(exename):
    try:
        speak(f'ok closing {exename}')
        os.system(f"taskkill /f /im {exename}.exe")
    except Exception as e:
        print(e)
        speak("sorry, there is an issue closing this file")
    

def TaskExecution():
    wish()
    while True:
        
        query = take_command().lower()

        if "no thanks" in query:
            speak("Thank you Sir, have a nice day")
            sys.exit()
        # elif 'wake up google' in query or 'reach google' in query or 'reach out to google' in query or 'wake up your brother' in query or 'reach out to your brother' in query:
        #     speak("Waking up Google")

        elif "who are you" in query:
            speak("Sir, I am Jarvis 1.0 . I am Just A Rather Very Intelligent System. This is my basic version.")
            speak("sir, do you have any task for me to perform")

        elif("tell me about you" in query or "tell me about yourself" in query):
            speak("Sir, I am Jarvis 1.0 . I am Just A Rather Very Intelligent System. This is my basic version. I am your personal assistant and a friend. I will improve over time and will have more capabilities in the future.")
        elif "open notepad" in query:
            speak("ok, opening notepad")
            openProg("C:\\Windows\\system32\\notepad.exe")
            speak("Anything else?")
        elif "close notepad" in query:
            closeProg('notepad')
            speak("done sir, what is your next command")
        
        elif "open command prompt" in query:
            speak("okay here you go")
            os.system("start cmd")
            speak("Anything else?")

        elif "close command prompt" in query:
            closeProg('cmd')
            speak("done sir, what is your next command")
        
        
        elif "open calendar" in query:
            webbrowser.open("https://calendar.google.com/calendar/u/0/r")
            time.sleep(1)
            speak("sir, anything else?")
        
        elif "open camera" in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('webcam',img)
                k = cv2.waitKey(50)
                if k == 27:
                   break;
            cap.release()
            cv2.destroyAllWindows()
            speak("Anything else?")
        

        elif "play music" in query or "play some music" in query or "music please" in query:
            speak("sure")
            music_dir = "C:\\Users\\Milan\\Music\\playlist1"
            songs = os.listdir(music_dir)
            rd = random.choice(songs)
            os.startfile(os.path.join(music_dir, rd))
            speak("Anything else?")
            # for song in songs:
            #     if song.endswith('.mp3'):
            #         os.startfile(os.path.join(music_dir, song))

        elif "ip address" in query:
            speak("wait a second")
            ip = requests.get('https://api.ipify.org').text
            speak(f"your IP address is {ip}")
            speak("Anything else?")

        elif "wikipedia" in query or "according to wikipedia"in query:
            speak("searching wikipedia...")
            query = query.replace("wikipedia","")
            results= wikipedia.summary(query, sentences=2)
            speak("according to wikipedia")
            speak(results)
            speak("Anything else?")

        elif "open youtube" in query:
            webbrowser.open("www.youtube.com")
            speak("Anything else?")

        elif "open facebook" in query:
            webbrowser.open("www.facebook.com")
            speak("Anything else?")
        
        elif "open google" in query:
            speak("sir, what should i search on google")
            cm = take_command().lower()
            webbrowser.open(f"{cm}")
            speak("Anything else?")
        
        # elif "send message" in query:
        #     pywhatkit.sendwhatmsg("+916009914610","this is a test message sent using Jarvis",16,58)
        #     speak("Anything else?")

        elif "play songs on youtube" in query or "play song on youtube" in query or "play a song on youtube" in query:
            speak("OK, which song?")
            songname = take_command().lower()
            pywhatkit.playonyt(songname)
            time.sleep(3)
            speak("Anything else?")

        elif "send email" in query:
            try:
                speak("OK, Please tell me the message you want to send")
                msg = take_command().lower()
                sender_email = "mcoinam01@gmail.com"
                password= "tech100business"
                receiver_email = "dhrubitaoinam888@gmail.com"
                
                server = smtplib.SMTP("smtp.gmail.com",587)
                server.starttls() # Puts the connection to the SMTP server into TLS mode
                server.login(sender_email, password)
                server.sendmail(sender_email,receiver_email,msg)
                speak("Email has been sent")
                speak("Do you have any other work for me?")
            except Exception as e:
                print(e)
                speak("Sorry Sir, I am not able to send this email")
                speak("Anything else you want me to do?")
            

        elif "switch the window" in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(1)
            pyautogui.keyUp("alt")
            speak("Do you need me to do anything else?")

        elif "tell me the news" in query:
            speak("please wait sir, fetching the latest news")
            news()

        elif "take screenshot" in query or "take a screenshot" in query:
            speak("sir, tell me a file name for the screenshot")
            name = take_command().lower()
            speak("Ok, let me just take the screenshot")
            # time.sleep(1)
            img = pyautogui.screenshot()
            img.save(f"{name}.png")
            speak("Done, the screenshot has been saved in our main folder. now i am ready for next command")
        elif "send a tweet" in query or "tweet something" in query or "tweet for me" in query:
            tweet()
            speak("Sir, do you have any other command?")

        elif "where am i" in query or "my location" in query or "current location" in query:
            speak("wait sir, let me check")
            try:
                # ip based location may not be accurate
                currentip = requests.get("https://api.ipify.org").text
                print(currentip)
                url = 'https://get.geojs.io/v1/ip/geo/' + currentip + '.json'
                geo_requests = requests.get(url)
                geo_data = geo_requests.json()

                city = geo_data['city']
                country = geo_data['country']
                speak(f'sir i am not sure, but i think we are in {city}, {country}')
                speak("next command please")

            except Exception as e:
                speak("Sorry sir, i am not able to find where we are")
        
     
        elif "check instagram profile" in query:
            profile_name = input("Enter the profile name of the account you want to search for\n")
            speak(f"searching for {profile_name}")
            webbrowser.open(f"www.instagram.com/{profile_name}")
            speak("sir here is the profile, do you want me to download the profile picture")
            resp = take_command().lower()
            if resp in ["yes","yap","yeah","yes please","yes sure"]:
                mod = instaloader.Instaloader()
                mod.download_profile(profile_name, profile_pic_only=True)
                speak("Done sir, prfile picture has been saved in the main folder, now i am ready for next command")
       

        elif "activate how to do mode" in query or "enter how to do mode" in query:
            speak('how to do mode is activated please tell me what you want to know')
            while True:
                q = take_command().lower()
                try:
                    if 'no' in q:
                        speak('ok, please tell me your next how to query')
                    
                    elif 'yes' in q or 'exit' in q or 'close' in q:
                        speak("okay sir, how to do mode is closed")
                        break
                    else:
                        max_results = 1
                        how_to = search_wikihow(q, max_results)
                        assert len(how_to) == 1
                        how_to[0].print()
                        speak(how_to[0].summary) 
                except Exception as e:
                    speak("sorry sir, i am not able to find this")
                speak("sir, do you want to exit from how to do mode")
            speak("ok, i am ready for next command")  

        elif 'battery level' in query or 'battery' in query or 'power left' in query:
            import psutil
            battery = psutil.sensors_battery()
            try:
                pc = battery.percent
                speak(f'Sir, system is at {pc} percent battery level')
            except Exception as e:
                speak('sir, i am not able to check the battery level... i think your system does not have a battery') 
            speak("Any other command")
        
        elif 'set alarm' in query:
            hh = int(datetime.datetime.now().hour)
            speak("When should I set the alarm")
            atime = take_command().lower()
            if hh == atime:
                sound_dir = 'C:\\Users\\Milan\\Music\\soundcollection\\Alarm-ringtone.mp3'
                os.startfile(sound_dir)
        elif 'send message' in query:
            speak("sir what should i say")
            msg = take_command()
            from twilio.rest import Client
            account_sid = 'ACb280b367bb8a71222da402b6faf9bef3'
            auth_token = '12b84b782f61fdfdbdce519725ca37e2'
            client = Client(account_sid, auth_token)

            message = client.messages \
                .create(
                    body=msg,
                    from_ = '+17604401151',
                    to = '+919366514316'
                )
            print(message.sid)
            speak("any other command")
        
        else: # query is "none" or "some_unknown_string"
            speak("Say that again please")
        
def take_command1():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source,timeout=4,phrase_time_limit=5)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio,language="en-in")
            print(f"user said:{query}")
        except Exception as e:
            # speak("Sorry Sir, I am not able to understand your command")
            # print("returning 'none'")
            return "none"
    return query


if __name__ == '__main__':
    while True:
        wake_q = take_command1().lower()
        if 'wake up' in wake_q:
            print("Activating J.A.R.V.I.S")
            TaskExecution()
        elif 'sleep' in wake_q:
            speak('I am going to sleep now, you can wake me up anytime')
            sys.exit()
        

    