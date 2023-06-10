from django.shortcuts import render, redirect
from .models import *
from .serializer import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
import pymongo
import random
from .Untitled import speech_rec,translate_text
from .answer_script import answer2,answer

from langdetect import detect
import requests
from PIL import Image
from io import BytesIO
import torch
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler, EulerAncestralDiscreteScheduler
import matplotlib.pyplot as plt
from django.http import JsonResponse
import os
import datetime as dt
from datetime import datetime
import stripe
from .scripts.Untitled import speech_rec
import torch
from diffusers import StableDiffusionPipeline
import matplotlib.pyplot as plt
import os
import shutil
import argparse
import math
from pathlib import Path
import sys
from PIL import Image
from tqdm.notebook import tqdm
import numpy as np
from base64 import b64encode
from IPython import display
import spacy
import requests
import nltk
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, EulerAncestralDiscreteScheduler, DDPMScheduler, PNDMScheduler, EulerDiscreteScheduler
import re
import matplotlib.pyplot as plt
import tempfile
import io
import base64
import seaborn as sns
import pandas as pd
import json
from django.core.serializers.json import DjangoJSONEncoder
import os
import shutil
import argparse
import math
from pathlib import Path
import sys
from PIL import Image
from tqdm.notebook import tqdm
import numpy as np
from base64 import b64encode
from IPython import display
import os
from moviepy.editor import *
from gtts import gTTS
import nltk
nltk.download('punkt')
font_size = 30
from PIL import Image, ImageDraw, ImageFont
import textwrap
import spacy
import replicate

API_KEY = settings.STRIPE_SECRET_KEY

#-------------------------------------------------------------------------------------------------------------------------------------
# Views function starts here.
#-------------------------------------------------------------------------------------------------------------------------------------
client = replicate.Client(api_token="r8_Se7xU17hTLkvB2tLmpe8pZ7nc2lmLRN2XI4Gl")

male_description = ["curly brown hair, green eyes, red shirt, blue jeans",
                    "short blonde hair, blue eyes, black shirt, cargo shorts",
                    "messy black hair, brown eyes, green hoodie, gray sweatpants",
                    "dark brown hair, hazel eyes, yellow polo, khaki shorts",
                    "short black hair, blue-green eyes, white button-up, black pants",
                    "spiky blonde hair, green eyes, blue cap, orange shirt, denim shorts",
                    "short brown hair, brown eyes, red and white soccer jersey, black shorts",
                    "wavy black hair, hazel eyes, leather jacket, gray t-shirt, ripped jeans",
                    "messy brown hair, bright blue eyes, green shirt",
                    "short blond hair, brown eyes, striped polo",
                    "curly black hair, hazel eyes, red hoodie",
                    "spiky brown hair, gray eyes, denim jacket",
                    "slicked-back blond hair, green eyes, yellow shirt",
                    "shaggy black hair, brown eyes, plaid button-up",
                    "buzz cut, blue eyes, black leather jacket",
                    "wavy red hair, green eyes, white tank top",
                    "short black hair, brown eyes, graphic tee",
                    "curly blond hair, blue eyes, baseball cap"]
female_description = ["curly blonde hair and pink headband",
                      "black hair, brown eyes, yellow shirt",
                      "short brown hair, green eyes, freckles",
                      "long wavy hair, purple hair clip, white skirt",
                      "pigtails, red bow, striped shirt",
                      "curly brown hair, blue eyes, pink dress",
                      "curly black hair, green eyes, yellow shirt",
                      "blonde hair, blue eyes, pink skirt",
                      "short brown hair, hazel eyes, red hoodie",
                      "black hair, brown eyes, purple dress",
                      "curly brown hair, blue eyes, bow, white blouse, jeans",
                      "blonde hair, blue eyes, pink hair bow, white dress",
                      "braided brown hair, hazel eyes, purple turtleneck, jeans",
                      "brown curly hair, brown eyes, pink headband, blue shirt, green shorts",
                      "long pink hair, round glasses, yellow top, red shorts"]
from PIL import Image, ImageDraw, ImageFont
import textwrap
#! python -m spacy download en_core_web_md
import spacy
import requests
import random

nlp = spacy.load("en_core_web_md")

prompt_parameters = ""

def get_gender(name):
    url = 'https://api.genderize.io'
    params = {'name': name}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        result = response.json()
        if result['gender'] is not None:
            return result['gender']
    return None

def get_entities(text):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            entities.append(ent.text)
    return entities

def get_genders(text):
    doc = nlp(text)
    genders = {}
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            gender = get_gender(name)
            if gender is not None:
                genders[name] = gender.lower()
    for pronoun in doc:
        if pronoun.text.lower() in ['he', 'him', 'He', 'Him']:
            genders[pronoun.text] = 'male'
        elif pronoun.text.lower() in ['she', 'her', 'She', 'Her']:
            genders[pronoun.text] = 'female'
    gender_list = []
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            gender = genders.get(name)
            if gender is not None:
                gender_list.append(gender)
    return gender_list

boy_description = random.choice(male_description)
girl_description = random.choice(female_description)

def add_adjectives(sentence):
    global prompt_parameters
    doc = nlp(sentence)
    entities = {}
    described_genders = set()  # keep track of genders that have already been described
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            gender = get_genders(ent.text)
            if 'female' in gender or ent.text.lower() in ["she", "her", "hers", "She", "Her", "Hers"]:
                #if 'female' not in described_genders:
                prompt_parameters = prompt_parameters + ", with " + girl_description + ", expressive, pretty hands, pretty face, pretty eyes, " 
                    #described_genders.add('female')
            elif 'male' in gender or ent.text.lower() in ["he", "him", "his", "He", "Him", "His"]:
                #if 'male' not in described_genders:
                prompt_parameters = prompt_parameters + ", with "  + boy_description + ", expressive, pretty hands, pretty face, pretty eyes, "
                    #described_genders.add('male')

    
    return prompt_parameters
def replace_names_with_gabriella_gabriel(sentence):
    nlp = spacy.load("en_core_web_md")

    def get_genders_transform(text):
        doc = nlp(text)
        genders = {}
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                name = ent.text
                gender = get_gender(name)
                if gender is not None:
                    genders[name] = gender.lower()
        return genders

    # Detect names and pronouns using get_genders function
    genders = get_genders_transform(sentence)

    # Replace names with "Gabriella" for females and "Gabriel" for males
    replaced_sentence = sentence
    for name, gender in genders.items():
        if gender == "female":
            replaced_sentence = replaced_sentence.replace(name, "Gabriella")
        elif gender == "male":
            replaced_sentence = replaced_sentence.replace(name, "Gabriel")

    pronouns = {" he ": " Gabriel ", " He ": " Gabriel ",
                " she ": " Gabriella ", " She ": " Gabriella "}

    for pronoun, replacement in pronouns.items():
        replaced_sentence = replaced_sentence.replace(pronoun, replacement)

    return replaced_sentence
import re
import nltk
nltk.download('averaged_perceptron_tagger')


def transform_text(text):
    tokens = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokens)
    transformed_words = []
    for word, pos in tagged:
        if pos.startswith('NN'): # check if the word is a noun
            word = word.capitalize() # capitalize the first letter of the noun
            transformed_words.append(word)
        elif re.match(r'\d+', word): # check if the word is a string of digits
            word = '[' + word + ']' # add brackets around the digits
            transformed_words.append(word)
        else:
            transformed_words.append(word)
    transformed_text = ' '.join(transformed_words)
    return transformed_text


def delete_extra_spaces(string):
    # Split the string by spaces
    words = string.split()
    
    # Join the words back with a single space
    result = ' '.join(words)
    
    return result
def set_image_text(img, img_path, text):
  
  # Open the image file
  image = img

  # Initialize the drawing context with the image object as background
  draw = ImageDraw.Draw(image)

  # Define the font to be used for the text
  font = ImageFont.truetype("C:/Users/dmzou/OneDrive/Bureau/Intellectia_F/UserApp/fonts/Arial-1.ttf", 20)

  # Wrap the text to fit within the image width
  max_width = int(0.8 * image.width)
  lines = textwrap.wrap(text, width=30)
  if len(lines)>1:
        
        image = Image.open(img_path+"Copie.png")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("C:/Users/dmzou/OneDrive/Bureau/Intellectia_F/UserApp/fonts/Arial-1.ttf", 32)
  
    

  # Initialize the drawing context with the image object as background
  #draw = ImageDraw.Draw(image)
  # Calculate the position of the text
  x = image.width / 4
  y = (image.height - font.getsize(lines[0])[1] * len(lines)) -80

  # Draw the text on the image
  for line in lines:
    text_width, text_height = font.getsize(line)
   
    #draw.text((x, y), line, font=font, fill=(255, 255, 255))
    y += text_height
    rect_width = text_width + 10
    rect_height = text_height + 10
    rect_x = x - 5
    rect_y = y - 5 + 10
    draw.rectangle((rect_x, rect_y, rect_x+rect_width, rect_y+rect_height), fill=(0, 0, 0))
    draw.text((x, y+5), line, font=font, fill=(255, 255, 255))
    

  # Define the size of the rectangle to draw
  #rect_width = max_width + 10
  #rect_height = font.getsize(lines[0])[1] * len(lines) + 10

  # Determine the position to draw the rectangle
  #rect_x = x - 5
  #rect_y = (image.height - rect_height) / 2

  # Draw the rectangle
  #draw.rectangle((rect_x, rect_y, rect_x+rect_width, rect_y+rect_height), fill=(0, 0, 0))

  # Save the modified image
    image.save(img_path+".png")










def generate_seed(text):
#    """Generates a seed integer based on the input text."""
    return abs(hash(text)) % ((10 ** 12)+7)


#paragraphe = "a"
#paragraphe = "A baseball ball and baseball bat. A baseball bat . The baseball ball. How much does the baseball ball cost" 
#paragraphe = "Mark having a garden with flowers. He planting plants of three different colors in it. Ten of flowers are yellow, and there are 80% more flowers in purple. There are only 25% as many green flowers as there are yellow and purple flowers. How many flowers does Mark have in his garden?, confused expression"
#paragraphe = "The Library having [215] Books about Sports. A Library having [157] Books about Science. Difference in the number of books about sports and science in the library?"
#paragraphe = "Molly and James building houses for dogs. Molly building a dog house 12 meters by 8 meters. James building a dog house 15 meters by 6 meters. Who will need more fencing to build the dog house?"
#paragraphe = "Karima picking flowers in the garden. Karima arranging six bouquets of flowers in the room. Karima giving the bouquets of flowers to three guy friends in the garden. How many flowers are in each bouquet?"
#paragraphe = "Angela owning eight Computer-Games. Angela getting three more Computer-Games. How many computer games Angela having?"
def detect_language(text):
    lang_code = detect(text)
    return lang_code

def generate_images(paragraphe):
    original_Text="Karima collected 42 flowers from her garden. She made 6 bouquets of flowers. She gave the bouquets to her three friends. How many flowers are in each bouquet?"
    text ="Gabriella picking flowers from her garden. Gabriella arranging bouquets of flowers, in her room. Gabriella handing flowers to her 3 friends. image of a Bouquet of flowers."
    #trans_text=translate_text(paragraphe,'en')
    phrases = nltk.sent_tokenize(text)
    original_phrases = nltk.sent_tokenize(original_Text)
    #phrases=["The library containing 321 scientific books and 192 stories for children."," 105 books and stories were purchased."," How many books are left in the library?"]
    lang_code = "en"#detect_language(paragraphe)
    #original_Text=translate_text(trans_text,lang_code)
   
    #original_phrases=['في المكتبة 321 كتابًا علميًا و192 قصة للأطفال.', 'تم شراء 105 كتابًا وقصة ',' ؟كم كتابًا بقي في المكتبة']
    
    
    clips2=[]
    new_size = (512, 512)
    for index, i in enumerate(phrases):
        text= i #"Gabriel reading books in his room home" #
        prompt_parameters = ""
        #text = replace_names_with_gabriella_gabriel(text)
       # text = transform_text(text)
        seed: int = generate_seed(text)
        character_param = add_adjectives(text)
        print(character_param)

        prompt_param = ")," + " 4k, detailed, fine details, full body"+ character_param  #, cut off"# octane render
        print(prompt_param) 
        prompt = "modern disney style (" + text + prompt_param
        print("prompt"+prompt)
        negative_prompt = "poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, ugly eyes, deformed, disfigured, blurry, cut off, bad quality, worst quality"
        prompt_parameters = ""
        print(prompt)
    
        
        output = client.run(
        "tstramer/mo-di-diffusion:4cee26e8ef4979d7faa7118eb938b258cea03b2b99f23796248e4d93ba5c4e25",
        input={"prompt": prompt,#"modern disney style (Anna making [6] bouquets of flowers), pretty hands, pretty face, pretty eyes, 4k, detailed, fine details, unreal engine, sharp focus, high quality", #, digital art, smooth, sharp focus, gravity falls style, doraemon style, shinchan style, anime style, unreal engine, cozy indoor lighting, artstation, detailed, digital painting,cinematic,character design by mark ryden and pixar and hayao miyazaki, unreal 5, daz, hyperrealistic, octane render",
        #", unreal engine, cozy indoor lighting, artstation, detailed, digital painting,cinematic,character design by mark ryden and pixar and hayao miyazaki, unreal 5, daz, hyperrealistic, octane render",# , unreal engine, cozy indoor lighting, artstation, detailed, digital painting,cinematic,character design by mark ryden and pixar and hayao miyazaki, unreal 5, daz, hyperrealistic, octane render",# sharp focus, matte, elegant, the most beautiful image ever seen, digital paint, octane render, 8k, 4k, sharp, beautiful, post processing",
        #"negative_prompt": "watermank,ugly, ugly arms, ugly hands,Deformed, blurry, bad anatomy, disfigured, poorly drawn face, mutation, mutated, extra limb, ugly, poorly drawn hands, missing limb, blurry, floating limbs, disconnected limbs, malformed hands, blur, out of focus, long neck, long body"}, #"exra heads, poorly drawn limbs, poorly drawn face , out of frame, extra limbs"},
        "negative_prompt":negative_prompt#"poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, ugly eyes, deformed, disfigured, blurry, cut off"
        },
        seed=generate_seed(text),
        image_dimensions="512x512",
        num_inference_steps=100,
        scheduler="K_EULER_ANCESTRAL"
        )

        print(output)
        response = requests.get(output[0])
        image = Image.open(BytesIO(response.content))
        img_path="C:/Users/dmzou/OneDrive/Bureau/Intellectia_F/UserApp/images/image"+str(index)
        image.save(img_path+".png")
        image.save(img_path+"Copie.png")
        clips = []
    # Get the image and description for this iteration
        desc = i
        img = Image.open(img_path+".png")
        img = img.resize(new_size)
        speech = gTTS(text=original_phrases[index], lang="en", slow=False)
        speech.save('C:/Users/dmzou/OneDrive/Bureau/Intellectia_F/UserApp/audio_vid/temp.mp3')
    # Load the speech using AudioFileClip
        speech = AudioFileClip('C:/Users/dmzou/OneDrive/Bureau/Intellectia_F/UserApp/audio_vid/temp.mp3')
        leng=speech.duration
        result_list = original_phrases[index].split()
        s=0
        txt=""
        for j in range(len(result_list)):
            txt+=result_list[j]+" "
            print(txt)
            set_image_text(img,img_path,txt)
            img2 = ImageClip(img_path+".png").resize(new_size)
            #speech1 = gTTS(text=result_list[j], lang='en', slow=False)
            #speech1.save('temp1.mp3')
            #speech1 = AudioFileClip('temp1.mp3')
            video = img2.set_duration(leng/len(result_list))
            #s+=speech1.duration
            img2 = Image.open(img_path+".png")
            #img2.show()
            clips.append(video)
        final_clip = concatenate_videoclips(clips).set_audio(speech)
    
        clips2.append(final_clip)
    #os.remove('C:/Users/dmzou/OneDrive/Bureau/intellect/Intellectia/Intellectia/UserApp/templates/audio_vid/temp.mp3')
    # Concatenate the clips into a single video
    final_clip2 = concatenate_videoclips(clips2)

    # Export the video with the filename "output.mp4"
    final_clip2.write_videofile("C:/Users/dmzou/OneDrive/Bureau/Intellectia_F/UserApp/static/videos/output11123.mp4",fps=60)



    #from IPython.display import Image
    #img=Image(url=output[0])
    #from PIL import Image

    # Assuming 'output[0]' contains the image data
    #img = Image.open(url=output[0])
    #img.save(f"C:/Users/dmzou/OneDrive/Bureau/intellect/Intellectia/Intellectia/UserApp/templates/images/aaaa.png")
    #plt.imshow(plt.imread(f"C:/Users/dmzou/OneDrive/Bureau/intellect/Intellectia/Intellectia/UserApp/templates/images/aaaa.png"))
    #plt.axis('off')
    #plt.show()

#-------------------------------------------------------------------------------------------------------------------------------------
def logout_user(request):
    logout(request)
    return redirect('/')

def index(request):
    if request.user.is_authenticated:
        print(request.user.type == 'STUDENT')
    else:
        request.session['attemps'] = 3
    if request.method == 'POST' and request.user.is_authenticated:
        logout_user(request)
    return render(request,'index.html')

def about(request):
    if request.method == 'POST' and request.user.is_authenticated:
        logout_user(request)
    return render(request,'about.html')

def contact(request):
    if request.method == 'POST' and request.user.is_authenticated:
        if 'messageButton' in request.POST:
            send_mail(
                request.POST['subject'],
                request.POST['message'],
                request.POST['email'],
                ['louay.guetat1@gmail.com'],
                fail_silently=False,
            )
            return redirect('/')
        else:
            logout_user(request)
    return render(request,'contact.html')

@login_required
def profile(request):
    if request.method == 'POST':
        if 'updateProfile' in request.POST :
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            phoneNumber = request.POST['phoneNumber']
            address = request.POST['address']
            password = request.POST['password']
            verify_password = request.POST['password2']
            hashed_password = ''
            user = request.user
            if len(firstname) != 0:
                user.firstname = firstname
            if len(lastname) != 0:
                user.lastname = lastname
            if len(phoneNumber) != 0:
                user.phoneNumber = phoneNumber
            if len(address) != 0:
                user.adress = address
            if len(password) != 0:
                if(password == verify_password):
                    hashed_password = make_password(password)      
                    user.password = hashed_password                      
            user.save()
            return redirect('/')
        else:
            logout_user(request)
    return render(request,'profile.html')

def login_user(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        print('auth:',user)
        if user is not None:
            login(request,user)
            print("success")
            context = {'user':user}
            return redirect('/',context)
        else: 
            messages.success(request, ("Username/Password invalid, Please check out your credentials!"))
            return redirect('/login')

    return render(request,'authentification/login.html',{})

def signup(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        phoneNumber = request.POST.get('phoneNumber')
        if(len(phoneNumber)>8 or len(phoneNumber)<8 or phoneNumber[0] == '-'):
            messages.success(request, ("Phone number not valid"))
            return redirect('/signup')
        adress = request.POST.get('adress')

        username = request.POST.get('username')
        if(username):
            pass
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPass')
        if(password != confirm_password):
            messages.success(request, ("Password and confirm password not valid"))
            return redirect('/signup')
        hashed_password = make_password(password)

        birthdate = request.POST.get('birthdate')
        birthdate = dt.datetime.strptime(birthdate, '%Y-%m-%d')
        year = dt.date.today().year
        if(birthdate.year >= year-6):
            messages.success(request, ("Birthdate invalid, you must at least have 6 years old"))
            return redirect('/signup')
        gender = request.POST.get('gender')
    
        User.objects.create(firstname=firstname,lastname=lastname,phoneNumber=phoneNumber,adress=adress
                            ,username=username,password=hashed_password,birthdate=birthdate,gender=gender,type='SIMPLE_USER')
        return redirect('/login')
    return render(request,'authentification/signup.html')

@login_required
def upgrade(request):
    if request.method == 'POST':
        method = 'Monthly'
        context = {}
        if method == 'Freemuim':
            user = request.user
            user.attemps = 3
            user.payement_method = method
            user.save()
            return redirect('/')
        if method == 'Monthly':
            request.session['offer'] = 'Monthly'
            return render(request,'payment/payment.html',context)
        if method == 'Yearly':
            request.session['offer'] = 'Yearly'
            return render(request,'payment/payment.html',context)
    if request.user.payed == True:
        return redirect('/')
    else:
        return render(request,'payment/upgrade.html')

@login_required
def payment(request):
    paymentDetails = request.session['offer']
    user = request.user
    if request.method == 'POST':
        context = {}
        stripe.api_key = API_KEY
        if paymentDetails == 'Monthly':
            client = stripe.Customer.create()
            client['address'] = user.adress
            client['email'] = request.POST.get('email')
            client['name'] = user.username
            client['phone'] = user.phoneNumber
            print('Customer is:',client)
            payment_intent = stripe.PaymentIntent.create(
                amount = 1500,
                currency='usd',
                payment_method_types = ['card'],
                description = 'Intellectia user: ' + request.user.username + ' has payed for a month',
                customer = client
            )
            context['secret_key'] = payment_intent.client_secret
            context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY
            user.attemps = -1
            user.payement_method = 1
            user.payed = True
            user.payment_date = datetime.now()
            user.save()
        else:
            client = stripe.Customer.create()
            client['address'] = user.adress
            client['email'] = request.POST.get('email')
            client['name'] = user.username
            client['phone'] = user.phoneNumber
            print('Customer is:',client)
            payment_intent = stripe.PaymentIntent.create(
                amount = 2900,
                currency='usd',
                payment_method_types = ['card'],
                description = 'Intellectia user: ' + request.user.username + ' has payed for a year',
                customer = client
            )
            context['secret_key'] = payment_intent.client_secret
            context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY
            user.attemps = -1
            user.payement_method = 2
            user.payed = True
            user.payment_date = datetime.now()
            user.save()
    return render(request,'payment/thankyou.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import speech_recognition as sr
import datetime
@csrf_exempt
def intellectia(request):
    print(request)
    if request.method == 'POST' and request.FILES.get('audio'):
            now = datetime.datetime.now()
            current_time = now.strftime("%H%M%S")
            audio_file = request.FILES.get('audio')
            audio_file1 = "C:/Users/dmzou/OneDrive/Bureau/Intellectia_F/UserApp/audio/audio.mp3"
            audio_file2 = "C:/Users/dmzou/OneDrive/Bureau/Intellectia_F/UserApp/audio/audio.wav"
            if audio_file:
                print("dd")
                # Save the audio file to disk
                with open(audio_file1, 'wb') as f:

                    for chunk in audio_file.chunks():
                        f.write(chunk)
            language = request.POST.get('language')           
            # convert audio file to WAV format using ffmpeg
            
            import subprocess
            # convert mp3 to wav using ffmpeg
            subprocess.call(['ffmpeg', '-i', audio_file1, audio_file2])
            #os.system('ffmpeg -i '+audio_file+' '+audio_file1)

            # load the WAV file
            r = sr.Recognizer()
            with sr.AudioFile(audio_file2) as source:
                audio = r.record(source)

            # transcribe the audio
            text = r.recognize_google(audio,language=language)#,language="ar"
            recognized_text=text
            os.remove(audio_file2)
            os.remove(audio_file1)
            sample_dict = {'recognized_text': recognized_text}

            return JsonResponse(sample_dict)
        
    elif request.method == 'POST' and request.POST.get('action')=='Upload' and request.FILES['image']:
        print('imggg')
        language = request.POST.get('language')
        print(str(language))
        if  language=="en":  
            
            import pytesseract
            from PIL import Image
            uploaded_file = request.FILES['image']
            image = Image.open(uploaded_file)
            recognized_text = pytesseract.image_to_string(image)
            recognized_text=delete_extra_spaces(recognized_text)
            
            print(recognized_text)
        elif  language=="fr":
            
            import pytesseract
            from PIL import Image
            uploaded_file = request.FILES['image']
            image = Image.open(uploaded_file)
            recognized_text = pytesseract.image_to_string(image,lang='fra')
            recognized_text=delete_extra_spaces(recognized_text)
            print(recognized_text)  
        else:
            
            import pytesseract
            from PIL import Image
            uploaded_file = request.FILES['image']
            image = Image.open(uploaded_file)
            recognized_text = pytesseract.image_to_string(image,lang='ara')
            recognized_text=delete_extra_spaces(recognized_text)
            print(recognized_text)  
        return render(request, 'main/intellectia.html', {'recognized_text': recognized_text})
    elif(request.POST.get('action')=='genarateAnswer'):
        print("genarateAnswer")
        problem = request.POST.get('problem')
        problem=delete_extra_spaces(problem)
        lang_code = detect_language(problem)
        print(lang_code)
        problem1=translate_text(problem,'en')
        print("translation: "+problem1)
        rep2=answer2(problem1)
        problem2=translate_text(rep2,lang_code)
        return render(request, 'main/intellectia.html', {'problem2': problem2,'recognized_text': problem})
    elif request.method == 'POST' and request.POST.get('problem') != None:
        txt = request.POST.get('problem')
        print(txt)
        generate_images(txt)
        video_path="C:/Users/dmzou/OneDrive/Bureau/Intellectia_F/UserApp/static/videos/output11123.mp4"
         # Replace with the actual path of your generated videoi
        
        return render(request, 'main/intellectia.html',{'video_path': video_path})
    else:
        logout_user(request)
        
    return render(request, 'main/intellectia.html')

@login_required
def quiz(request):
    if request.user.is_authenticated:
        user = Student.objects.get(id=request.user.id)
        if request.method == 'POST':
            key_to_remove = 'csrfmiddlewaretoken'
            QA = {k: v for k, v in request.POST.items() if k != key_to_remove}
            questions = list(QA.keys())
            answers = [int(value) for value in list(QA.values())]
            correctAnswers = []
            types = []
            for question in questions :
                client = pymongo.MongoClient("mongodb://localhost:27017")
                db = client["Intellectia"]
                collection = db["Quiz"]
                QA = list(collection.find({'Question':question}))
                correctAnswers.append(QA[0]['Answer'])
                types.append(QA[0]['Types'])
            note = 0
            for i in range(0,5):
                if correctAnswers[i] == int(answers[i]):
                    note = note + 2
            Quiz.objects.create(questions=questions,types=types,answer=answers,correctAnswers=correctAnswers,note=note,student=user)
            return redirect('/quizResults')
        
        client = pymongo.MongoClient("mongodb://localhost:27017")
        db = client["Intellectia"]
        collection = db["Quiz"]
        data = None
        grade = user.grade.all()[0].level
        
        if grade == '1':
            data = collection.find({"$or": [{"Types": {"$in": ["Addition"]}}]})

        if grade == '2':
            data = collection.find({"$or": [{"Types": {"$in": ["Addition", "Subtraction"]}}]})

        if grade == '3':
            data = collection.find({"$or": [{"Types": {"$in": ["Addition", "Subtraction","AdditionSubstraction","Multiplication"]}}]})

        if grade == '4':
            data = collection.find({"$or": [{"Types": {"$in": ["AdditionSubstraction","Multiplication","AdditionMultiplication","SubtractionMultiplication","AdditionSubtractionMultiplication","Division"]}}]})

        if grade == '5':
            data = collection.find({"$or": [{"Types": {"$in": ["AdditionSubstraction","Multiplication","AdditionMultiplication","SubtractionMultiplication","AdditionSubtractionMultiplication","Division","AdditionDivision","SubtractionDivision","AdditionSubtractionDivision","AdditionMultiplicationDivision","SubtractionMultiplicationDivision","MultiplicationDivision","AdditionSubtractionMultiplicationDivision"]}}]})

        if grade == '6':
            data = collection.find({"$or": [{"Types": {"$in": ["AdditionSubstraction","Multiplication","AdditionMultiplication","SubtractionMultiplication","AdditionSubtractionMultiplication","Division","AdditionDivision","SubtractionDivision","AdditionSubtractionDivision","AdditionMultiplicationDivision","SubtractionMultiplicationDivision","MultiplicationDivision","AdditionSubtractionMultiplicationDivision","Ratio","Percent","Geometry"]}}]})

        data = list(data)
        random.shuffle(data)
        data = data[:5]
        questions = {}
        for question in data:
            
            false_answer_1 = random.randint(question['Answer']-10, question['Answer']+10)
            false_answer_2 = random.randint(question['Answer']-10, question['Answer']+10)
            false_answer_3 = random.randint(question['Answer']-10, question['Answer']+10)

            while false_answer_1 == question['Answer']:
                false_answer_1 = random.randint(question['Answer']-10, question['Answer']+10)

            while false_answer_2 == question['Answer'] or false_answer_2 == false_answer_1:
                false_answer_2 = random.randint(question['Answer']-10, question['Answer']+10)

            while false_answer_3 == question['Answer'] or false_answer_3 == false_answer_1 or false_answer_3 == false_answer_2:
                false_answer_3 = random.randint(question['Answer']-10, question['Answer']+10)
            questions[question['Question']] = {question['Answer'],false_answer_1,false_answer_2,false_answer_3}
            
        return render(request, 'quiz/quiz.html',{'questions': questions})
    else:
        return redirect('/login')

@login_required   
def quizResults(request):
    quiz = Quiz.objects.latest('id')
    return render(request, 'quiz/quizResult.html',{'questions':quiz.questions,'answers':quiz.answer,'correct':quiz.correctAnswers,'note':quiz.note,})

class StudentEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Student):
            # Convert Student object to a dictionary
            return {
                'firstname': obj.firstname,
                'lastname':obj.lastname,
                'gender':obj.gender,
                'phoneNumber':obj.phoneNumber,
                'matricule':obj.matricule
                # Include other attributes as needed
            }
        return super().default(obj)
    
class QuizEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Quiz):
            # Convert Student object to a dictionary
            return {
                'questions': obj.questions,
                'answers':obj.answer,
                'correctAnswers':obj.correctAnswers,
                'types':obj.types,
                'note':obj.note,
                'date':obj.quizDate
                # Include other attributes as needed
            }
        return super().default(obj)


@login_required
def dashboard(request):
    #os.remove('C:/Users/louay/Desktop/Educational-Interactive-Intelligent-Platform/Intellectia/UserApp/static/img/chart.png')
    user = request.user
    if user.type == 'STUDENT':
        student = Student.objects.get(id=user.id)
        quizs = Quiz.objects.filter(student=student.id)
        classe = Classes.objects.get(student=user.id)
        teachers = classe.teachers.all()
        classmates = Student.objects.filter(grade=classe.level).exclude(id=user.id)
        for q in quizs : 
            typ = q.types
            types = []
            for t in typ: 
                split_phrase = re.findall('[A-Z][^A-Z]*', t)
                result = ' '.join(split_phrase)
                types.append(result)
            q.types = types
        moyenne = 0
        for quiz in quizs: 
            moyenne=moyenne+quiz.note
        if(len(quizs)!= 0):
            moyenne = round(moyenne/len(quizs),2)
            #Pie chart
            correct = 0
            false = 0
            for quiz in quizs:
                for i in range(0,5):
                    if quiz.correctAnswers[i] == quiz.answer[i]:
                        correct = correct +1
                    else:
                        false = false+1

            quizLabels = ['Correct Answers','Wrong Answers']
            sizes = [correct, false]
            colors = ['#3f8f29', '#bf1029']

            # Create the pie chart
            plt.pie(sizes, labels=quizLabels, colors=colors, autopct='%1.1f%%', startangle=90)
            plt.title('OverAll')
            plt.axis('equal')

            # Save the chart to a temporary file
            chart_path = 'C:/Users/dmzou/OneDrive/Bureau/Intellectia_F/UserApp/static/img/chart.png'
            plt.savefig(chart_path)
            
            if classe.level == '2':
                types = ["Addition", "Subtraction"]
                
            if classe.level == '3':
                types = ["Addition", "Subtraction","AdditionSubstraction","Multiplication"]

            if classe.level == '4':
                types = ["AdditionSubstraction","Multiplication","AdditionMultiplication","SubtractionMultiplication","AdditionSubtractionMultiplication","Division"]

            if classe.level == '5':
                types = ["AdditionSubstraction","Multiplication","AdditionMultiplication","SubtractionMultiplication","AdditionSubtractionMultiplication","Division","AdditionDivision","SubtractionDivision","AdditionSubtractionDivision","AdditionMultiplicationDivision","SubtractionMultiplicationDivision","MultiplicationDivision","AdditionSubtractionMultiplicationDivision"]
            
            if classe.level == '6':
                types = ["AdditionSubstraction","Multiplication","AdditionMultiplication","SubtractionMultiplication","AdditionSubtractionMultiplication","Division","AdditionDivision","SubtractionDivision","AdditionSubtractionDivision","AdditionMultiplicationDivision","SubtractionMultiplicationDivision","MultiplicationDivision","AdditionSubtractionMultiplicationDivision","Ratio","Percent","Geometry"]

            return render(request,'dashboard/studentDashboard.html',{'student':student,'teachers':teachers,'quizs':quizs
                                                                    ,'classe':classe,'classmates':classmates,'moyenne':moyenne
                                                                    ,'piechart':chart_path})
        else:
            return render(request,'dashboard/studentDashboard.html',{'student':student,'teachers':teachers,'quizs':quizs
                                                                    ,'classe':classe,'classmates':classmates,'moyenne':moyenne})
            
    
    elif user.type == 'TEACHER':
        teacher = Teacher.objects.get(id=user.id)
        classes = Classes.objects.filter(teachers=teacher.id)
        students = []
        studentsByClasse = {}
        studentsNumber = {}
        for classe in classes:
            s = Student.objects.filter(grade=classe.id)
            studentsNumber[classe] = len(s)
            students.append(s)
            student_list = list(s)
            json_data = json.dumps(student_list, cls=StudentEncoder)
            studentsByClasse[classe.designiation] = json_data
        quizByStudent = {}
        for i in range(0,len(students)):
            for student in students[i]:
                quizs = Quiz.objects.filter(student=student.id)
                quizs = list(quizs)
                json_data = json.dumps(quizs, cls=QuizEncoder)
                quizByStudent[student.firstname+''+student.lastname] = json_data
        print(studentsNumber)
        return render(request,'dashboard/teacherDashboard.html',{'teacher':teacher,'classes':studentsNumber,'students':json.dumps(studentsByClasse)
                                                                 ,'quizs':json.dumps(quizByStudent),'studentsNumber':studentsNumber})
    
    elif user.type == 'PARENT':
        parent = Parent.objects.get(id=user.id)
        return render(request,'dashboard/parentDashboard.html')
    
    else:
        return render(request,'dashboard/userDashboard.html')
# Create your views here.
