import subprocess
import sys
import pkg_resources

installed_packages = pkg_resources.working_set
installed_packages_list = sorted(["%s" % (i.key) for i in installed_packages])

dependencies = [
    'flask'
    ,'pydub'
    ,'speechrecognition'
    ,'gtts'
    ,'pyaudio'
    ,'playsound'
    ,'nltk'
    ,'recorder'
    ,'pytesseract'
    ,'ffmpeg'
    ,'diffusers'
    ,'transformers'
    ,'scipy'
    ,'ftfy'
    ,'torch'
    ,'seaborn'
    ,'replicate'
    ,'spacy'
    ,'langdetect'
]

for dependency in dependencies:
    if dependency in installed_packages_list:
        print(dependency,'installed :).')
    else:
        subprocess.check_call([sys.executable, "-m", "pip", "install", dependency])

print('All dependencies are satisfied...')

