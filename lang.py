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
from gtts import gTTS
import os

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


def translate(obj):

    if obj in LANGUAGES.values():
        # for language in LANGUAGES:
        for key, val in LANGUAGES.items():
            if obj == val:
                destlang = key
                print("destination language:" + destlang)
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
    # speak(textranslated)
    file = gTTS(text=textranslated, lang="fr", slow=False)
    file.save('file.mp3')
    os.system('start file.mp3')
translate('zulu')