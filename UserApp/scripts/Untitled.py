from gtts import gTTS
import pyaudio
from playsound import playsound
import  speech_recognition as sr
def speech_rec(lg):
    t=""
    r=sr.Recognizer()
    with sr.Microphone() as src:
        print('Say something....')
        audio = r.listen(src)
    try:
        t=r.recognize_google(audio,language=lg)
        print(t)
        #f=open('text.txt','a',encoding='utf-8')
        #f.writelines(t+'\n')
        #f.close()
        obj=gTTS(text=t,lang=lg,slow=False)
        #obj.save('text.mp3')
        #playsound('text.mp3')
    except sr.UnknownValueError as U:
        print(U)
    except sr.RequestError as R:
        print(R)
    return t