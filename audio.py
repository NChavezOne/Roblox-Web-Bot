import soundcard as sc
import struct

import sys
import numpy
numpy.set_printoptions(threshold=sys.maxsize)

import time

#============
#For creating audio files

from scipy.io.wavfile import write
import os
from pydub import AudioSegment

#============
#For playing audio files

from glob import glob

#Replaced from pyDub for portability
from playsound import playsound

import threading
import io

#============
#misc imports

import cprint
import machinelearning

#============

# get a list of all speakers:
speakers = sc.all_speakers()
# get the current default speaker on your system:
default_speaker = sc.default_speaker()

# get a list of all microphones:v
mics = sc.all_microphones(include_loopback=True)
print("The microphones on this system")
print(mics)
# Set the microphone for recording.
global default_mic
default_mic = mics[0] #Default for my desktop computer is 3, but set it to 0 for compatibility -Nicholas

def print_to_string(*args, **kwargs):
    output = io.StringIO()
    print(*args, file=output, **kwargs)
    contents = output.getvalue()
    output.close()
    return contents

def Average(lst):
    return sum(lst) / len(lst)

def getCorrectMic():
    #The purpose of this function is to get the correct audio recording device for the client
    print("Attempting to get the correct mic!")
    audio_files = glob('Test Audio/*.wav')
    song = r"Test Audio/sample-crowd.wav"
    files = list()
    z = 0
    global default_mic
    guess = list()
    for x in mics:
        default_mic = mics[z]
        time.sleep(0.5)
        t1 = threading.Thread(target=playsound,args=(song,))
        t1.start()
        information = recordAudio(3)
        createFileFromData(r"Test Audio/",information,str(z),"wav")
        file = r"Test Audio/"+str(z)+".wav"
        if (os.path.isfile(file)):
            guess.append(machinelearning.predictIfCrowd(file)[0][1])
        z += 1
    print("The correct mic is ")
    print(mics[guess.index(min(guess))])
    print("Setting correct mic.")
    default_mic = mics[guess.index(min(guess))]
    
    
def playAudio(data):
    with default_mic.recorder(samplerate=44100) as mic, \
                default_speaker.player(samplerate=44100) as sp:
        sp.play(data)

def recordAudio(duration=1): #records audio, duration in seconds
    with default_mic.recorder(samplerate=44100) as mic, \
                default_speaker.player(samplerate=44100) as sp:
        print("Recording...")
        framenum = duration * 44100
        millisec1 = int(round(time.time() * 1000))
        data = mic.record(numframes=framenum) #take the audio information and put it into a variable called data
        millisec2 = int(round(time.time() * 1000))
        #If the recording is less than 50 percent of the duration, it means the device
        #Was not a proper recording device. We need to wait.
        if (millisec2 - millisec1 < ((duration/2) * 1000)):
            time.sleep(duration)
        print("Done.")
        print("")
        return data

def createFileFromData(exportDirectory, data, filename, file_format):
    filename += r"." + file_format
    filename = exportDirectory + filename
    data = (data * 10000).astype(numpy.int16)
    #Convert WAV file to INT encoding
    write(exportDirectory + 'output.wav', 44100, data)
    sound = AudioSegment.from_wav(exportDirectory + 'output.wav')
    sound.export(filename, format=file_format)

def testAudioAndFiles():
    global default_mic
    default_mic = mics[0]
    print("Testing audio device recording.")
    data = recordAudio(2)
    playAudio(data)
    
    print("Testing File exporting.")
    createFileFromData(r"Audio & Spectrograms/",data,"AudioScriptTesting","wav")

if __name__ == "__main__":
    
    print("Hello world!")
    print("Audio script is running as main!")
    getCorrectMic()
    while(1):
        while (int(input("Waiting for a value greater than 1...")) > 1):
            time.sleep(0.1)
        testAudioAndFiles()
    