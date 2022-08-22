import audio
import audioprocessing
import learning

import matplotlib.pylab as plt

import time
import numpy as np
import tensorflow as tf

import cprint

def predictIfCrowd(file):
    file_format = r".png"
    file_generated = file[0:len(file)-4] + file_format
    plt.imsave(fname=file_generated,arr=audioprocessing.getMelSpectrogram(file),cmap="gray")
    savedModel=learning.load_model('gfgModel.h5')
    img = tf.keras.preprocessing.image.load_img(file_generated, grayscale=False, color_mode='rgb', target_size=[256,256],interpolation='nearest')
    img_tensor = np.array(img)
    pred = savedModel.predict(img_tensor[None,:,:])
    return pred
    
if __name__ == "__main__":
    
    while (1 == 2):
        myRecording = audio.recordAudio(2)
        audio.playAudio(myRecording)
        audio.createFileFromData(myRecording, "recording", "wav")
        time.sleep(1)
        plt.imsave(fname=r'C:\Users\Admin1\Desktop\recording.png',arr=audioprocessing.getMelSpectrogram(r"C:\Users\Admin1\Desktop\recording.wav"),cmap="gray")

        savedModel=learning.load_model('gfgModel.h5')

        path=r'C:\Users\Admin1\Desktop\recording.png'

        img = tf.keras.preprocessing.image.load_img(path, grayscale=False, color_mode='rgb', target_size=[256,256],interpolation='nearest')
        img_tensor = np.array(img)
        pred = savedModel.predict(img_tensor[None,:,:])
        cprint.clearConsole()
        print (pred)
        if (np.argmax(pred) == 1):
            print("You said yes.")
        if (np.argmax(pred) == 0):
            print("You said no.")
        time.sleep(5)
        
    option1 = predictIfCrowd(r"option1.wav")
    option2 = predictIfCrowd(r"option2.wav")
    option3 = predictIfCrowd(r"option3.wav")
    
    print (option1[0][1])
