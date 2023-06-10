#!/usr/bin/env python
# coding: utf-8

# In[1]:


#pip install speechrecognition


# In[2]:


#pip install gtts


# In[4]:


#pip install pyaudio


# In[15]:


#pip install playsound


# In[1]:


from gtts import gTTS
import pyaudio
from playsound import playsound
import  speech_recognition as sr
def speech_rec(lg):
    t=""
    r=sr.Recognizer()
    with sr.Microphone() as src:
        print('Say something....')
        audio=r.listen(src)
    try:
        print("...")
        t=r.recognize_google(audio,language=lg)
        print(t)
        #f=open('text.txt','a',encoding='utf-8')
        #f.writelines(t+'\n')
        #f.close()
        #obj=gTTS(text=t,lang=lg,slow=False)
        #obj.save('text.mp3')
        #playsound('text.mp3')
    except sr.UnknownValueError as U:
        print(U)
    except sr.RequestError as R:
        print(R)
    return t


# In[3]:


#txt=speech_rec('ar')


# In[ ]:


#في المكتبه 321 كتابا علميا 192 قصه للاطفال تم شراء 105 كتابا وقصه كم كتابا بقي في المكتبه


# In[5]:


#pip install nltk


# In[5]:


import nltk
import requests

nltk.download('punkt')

def translate_text(text, target_lang):
    tokenized_text = nltk.tokenize.sent_tokenize(text)
    translated_sentences = []
    for sentence in tokenized_text:
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={}&dt=t&q={}".format(target_lang, sentence)
        response = requests.get(url)
        result = response.json()
        translated_sentences.append(result[0][0][0])
    return ' '.join(translated_sentences)

##input_text = "حصل محمد على نسبة 82% من الإجابة الصحيحة في اختبار الرياضيات، إذا علمتَ أنّ المجموع الكلي للعلامات يساوي 140، ما هي نتيجة محمد في الاختبار؟"
#input_text=txt
#translated_text = translate_text(input_text)

#print(translated_text)

