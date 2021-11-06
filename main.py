from ip2geotools.databases.noncommercial import DbIpCity
import requests
from selenium import webdriver
r = requests.get("https://get.geojs.io/")
ip_request=requests.get("https://get.geojs.io/v1/ip.json")
ipAdd=ip_request.json()['ip']

url="https://get.geojs.io/v1/ip/geo/"+ipAdd+'.json'
geo_request=requests.get(url)
geo_data=geo_request.json()
timezone=geo_request.json()['timezone']
country=geo_request.json()['country']

#print(country)
city=DbIpCity.get(ipAdd,api_key="free")

#print(country)
location=city.region+","+country
#********************************************************************************
import nltk
from nltk.stem.lancaster import LancasterStemmer
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen


from selenium import webdriver
from time import sleep
from kivy.logger import Logger

from gtts import gTTS
import os

stemmer = LancasterStemmer()


import numpy
import tflearn
import tensorflow
import random
import json
#**************************************
import kivy

kivy.require('1.0.6')  # replace with your current kivy version !

from kivy.app import App

from kivy.core.window import Window


#Window.clearcolor = (0, 102/255, 102/255, 1)
Window.clearcolor = (0, 0, 0, 0)

#CONVERT SPEECH TO TEXT
from ibm_watson import SpeechToTextV1
from  ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from googletrans import LANGUAGES
L=dict()
K=dict()
#setting up our speech detect server
sttapikey= 'Fj6JqkOjQR-vV9NBQJCD5d9SF2DVvJmbVrx688IHwQZR'
stturl= 'https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/789036b7-491e-477d-937d-88d1aff01511'
import speech_recognition as sr
import pyttsx3 as p
#Setup Service
sttauthenticator = IAMAuthenticator(sttapikey)
stt = SpeechToTextV1(authenticator= sttauthenticator)
stt.set_service_url(stturl)

#in order to authentificate we need to set up our server so basically we need to set up a watson language translation service
apikey ='pVQFuMwemLn5ciYiG36AqIIZliFverYjrAKeEG3XyslK'
url = 'https://api.eu-gb.language-translator.watson.cloud.ibm.com/instances/8d978fbc-a90e-4204-82bf-3372dd132107'

#import our dependencies
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

#setup service
authenticator = IAMAuthenticator(apikey)
lt = LanguageTranslatorV3(version= "2018-05-01", authenticator = authenticator)
lt.set_service_url(url)

ttsapikey='4SCVd-VwLIawSBRCqXfuNFISBtDOY2HkfMbkyzOF-4_s'
ttsurl= 'https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/14c2620a-fff1-4e55-a66c-ae6975a4c416'

#import our  dependencies
from ibm_watson import TextToSpeechV1

#Authneticate
ttsauthenticator = IAMAuthenticator(ttsapikey)
tts = TextToSpeechV1(authenticator = ttsauthenticator)
tts.set_service_url(ttsurl)
engine = p.init()
rate=engine.getProperty('rate')
engine.setProperty('rate',130)
voices=engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
 engine.say(text)
 engine.runAndWait()



with open("intents.json") as file:
        data = json.load(file)

print(data["intents"])


words = []
labels = []
docs_x = []
docs_y = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["tag"])

    if intent["tag"] not in labels:
        labels.append(intent["tag"])

words = [stemmer.stem(w.lower()) for w in words if w != "?"]
words = sorted(list(set(words)))

labels = sorted(labels)

training = []
output = []

out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []
    wrds = [stemmer.stem(w.lower()) for w in doc]

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)

training = numpy.array(training)
output = numpy.array(output)



    # this is the complete ai model

tensorflow.compat.v1.reset_default_graph()  # getting ready of all the previous settings

net = tflearn.input_data(shape=[None, len(training[
                                                  0])])  # defines the input shape expected to our model #in this case all the inputs have the same lengths that's why we entered  len(training[0])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]),
                                  activation="softmax")  # the output layer will have 6 neurons because we have 6 tags in our json file
net = tflearn.regression(net)
'''
we will pick a random response from the highest predicted model 

'''

model = tflearn.DNN(net)

model.fit(training, output, n_epoch=1000, batch_size=8,
              show_metric=True)  # n_epoch is the number of times it's gonna see the same data  #the more it sees the data, the better it gets at classifying #batch_size represents the number of training samples to work through
model.save("model.tflearn")  # the model is going to be saved as model.tflearn


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)

def translate():
        speak("to which language do you want to translate")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.energy_threshold = 10000
            r.adjust_for_ambient_noise(source, 1.2)
            print("listening..")
            audio = r.listen(source)

        obj = r.recognize_google(audio)
        if obj in LANGUAGES.values():
            # for language in LANGUAGES:
            for key, val in LANGUAGES.items():
                if obj == val:
                    destlang = key
                    print("destination language:"+destlang)
        speak('What do you want to translate?')

        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.energy_threshold = 10000
            r.adjust_for_ambient_noise(source, 1.2)
            print("listening..")
            audio = r.listen(source)

        text = r.recognize_google(audio)  # , language = detect(text))

        sourcelanguage = lt.identify(text).get_result()

        dictddict = sourcelanguage['languages'][0]

        srclan = dictddict['language']
        print(text)
        print(srclan)
        # print(lang_dest)

        translation = lt.translate(text=text, model_id=srclan + '-' + destlang).get_result()  # model_id= 'en-de'

        textranslated = translation['translations'][0]['translation']
        print(textranslated)
        print(obj)
        #speak(textranslated)
        file = gTTS(text=textranslated, lang="fr", slow=False)
        file.save('file.mp3')
        os.system('start file.mp3')

def showingmap(self, url):  # ,destination):
        speak('Excuse me ,Where do you want to go?')
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.energy_threshold = 10000
            r.adjust_for_ambient_noise(source, 1.2)
            print("listening..")
            audio = r.listen(source)

        destination = r.recognize_google(audio)
        driver = webdriver.Chrome("C://Users/imenm/Desktop/chromedriver")
        driver.get(url)
        #driver.set_window_position()
        driver.set_window_size(10, 700)
        driver.set_window_position(180,18)

        direction=driver.find_element_by_xpath("/html/body/jsl/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/button")
        direction.click()
        sleep(2)

        depart=driver.find_element_by_xpath("/html/body/jsl/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[2]/div/div/input")
        depart.send_keys(location)
        arrivee=driver.find_element_by_xpath("/html/body/jsl/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[2]/div[2]/div/div/input")
        arrivee.send_keys(destination)
        submit = driver.find_element_by_xpath( "/html/body/jsl/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[2]/div[2]/button[1]")
        submit.click()
        reduire=driver.find_element_by_xpath("/html/body/jsl/div[3]/div[9]/div[8]/div/div[3]/button")
        reduire.click()


def showinglocation(url):
 current_location="You are currently in "+timezone+"  ,exactly in,  "+location
 speak(current_location)
 driver = webdriver.Chrome("C://Users/imenm/Desktop/chromedriver")
 driver.get(url)
 # driver.set_window_position()
 driver.set_window_size(10, 700)
 driver.set_window_position(180, 18)




 loc=driver.find_element_by_xpath("/html/body/jsl/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[2]/form/div/div[3]/div/input[1]")
 loc.send_keys(location)

 submit = driver.find_element_by_xpath( "/html/body/jsl/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]/button")
 submit.click()



Window.size = (400, 600)
kv=Builder.load_file("main.kv")

#*****************************************************************************************************************
class MainScreen(Screen):



    def quit(self,obj):
        print(obj)

        App.get_application_icon(self).stop()
        Window.close()


    def chat(self,msg):

        speak(msg)
        while True:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                r.energy_threshold = 10000
                r.adjust_for_ambient_noise(source, 1.2)
                print("listening..")
                audio = r.listen(source)

            inp = r.recognize_google(audio)
            #inp = input("You: ")



            results = model.predict([bag_of_words(inp, words)])
            print(results)
            results_index = numpy.argmax(results)  # this gives us the index of our greatest value in our list "results"
            tag = labels[results_index]
            # print(tag)

            if results[0][results_index] > 0.7:
                for tg in data["intents"]:

                    if tg['tag'] == tag:
                        responses = tg['responses']

                ch = random.choice(responses)
                print(ch)
                if ch=="bye":

                    speak("Talk to you later")
                    break
                elif ch == "itineraire":
                    showingmap("https://www.google.com/maps/")
                    speak("if you need anything else i am here")
                    break
                elif ch=="current location":
                    showinglocation("https://www.google.com/maps/")
                    speak("if you need anything else i am here")
                    break

                elif ch == "translation":

                    speak("Sure, there is a translation button you can use it,if you need anything else i am here")
                    break

                else:
                    speak(ch)

            else:
                speak("sorry, i didn't get what you mean")




class TranslationScreen(Screen):
    def spinner_clicked(self,obj):
        if obj in LANGUAGES.values():
            # for language in LANGUAGES:
            for key, val in LANGUAGES.items():
                if obj == val:
                    destlang = key
                    print(destlang)
        speak('Excuse me ,What do you want to translate?')

        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.energy_threshold = 10000
            r.adjust_for_ambient_noise(source, 1.2)
            print("listening..")
            audio = r.listen(source)

        text = r.recognize_google(audio)  # , language = detect(text))

        sourcelanguage = lt.identify(text).get_result()

        dictddict = sourcelanguage['languages'][0]

        srclan = dictddict['language']
        print(text)
        print(srclan)
        # print(lang_dest)

        translation = lt.translate(text=text, model_id=srclan + '-' + destlang).get_result()  # model_id= 'en-de'

        textranslated = translation['translations'][0]['translation']
        print(textranslated)
        print(obj)
        #speak(textranslated)
        file = gTTS(text=textranslated, lang=str(destlang), slow=False)
        file.save('file.mp3')
        os.system('start file.mp3')



class TestApp(App):
    def on_stop(self):
        Logger.critical("Good bye")


    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(TranslationScreen(name='translation'))


        return sm


if __name__ == '__main__':
    TestApp().run()