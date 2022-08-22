import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns

from glob import glob

import librosa
import librosa.display
import IPython.display as ipd

from itertools import cycle

sns.set_theme(style="white", palette=None)
color_pal = plt.rcParams["axes.prop_cycle"].by_key()["color"]
color_cycle = cycle(plt.rcParams["axes.prop_cycle"].by_key()["color"])

audio_files = list()
audio_files.append(glob(r'C:\Users\Admin1\Desktop\data\train\yes\*.wav'))
audio_files.append(glob(r'C:\Users\Admin1\Desktop\data\train\crowd\*.wav'))
    
def getMelSpectrogram(file, plot=4):
    y, sr = librosa.load(file)
    
    #Trim the audio data.
    y_trimmed, _ = librosa.effects.trim(y, top_db=20)
    if (len(y_trimmed) >= 50000):
        y_trimmed = y_trimmed[0:50000]
    else:
        padding = 50000 - len(y_trimmed)
        padding = np.zeros(padding)
        while (1):
            y_trimmed = np.append(y_trimmed, padding)
            if (len(y_trimmed) >= 50000):
                break
    
    y = y_trimmed    
    #print(len(y))
    #print(y)
    if (plot == 0):
        #Plot the trimmed audio.
        pd.Series(y_trimmed).plot(figsize=(10, 5), lw=1, title='Raw Audio Trimmed Example', color=color_pal[1])
        plt.show()
    
    #Create a spectrogram.
    D = librosa.stft(y)
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    
    if (plot == 1):
        #Plot the spectrogram.
        fig, ax = plt.subplots(figsize=(10, 5))
        img = librosa.display.specshow(S_db, x_axis='time', y_axis='log', ax=ax)
        ax.set_title('Spectogram Example', fontsize=20)
        fig.colorbar(img, ax=ax, format=f'%0.2f')
        plt.show()

    #Create a mel spectrogram.
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128 * 2)
    S_db_mel = librosa.amplitude_to_db(S, ref=np.max)
    
    if (plot == 2):    
        #Plot the mel spectrogram.
        fig, ax = plt.subplots(figsize=(10, 5))
        img = librosa.display.specshow(S_db_mel, x_axis='time', y_axis='log', ax=ax)
        ax.set_title('Mel Spectogram Example', fontsize=20)
        fig.colorbar(img, ax=ax, format=f'%0.2f')
        plt.show()
        
    return S_db_mel

if __name__ == "__main__":

    label_dir = 'yes'

    test_directory = f'./data/test/{label_dir}/'
    train_directory = f'./data/train/{label_dir}/'
        
    z = 0
    while (z < 2):
        x = 0
        while (x < len(audio_files[z])):
            print("Generating image from audio.")
            if (x % 3 == 0):
                print("Putting into testing set.")
                plt.imsave(fname=f'./data/test/{label_dir}/image'+str(x)+'.png',arr=getMelSpectrogram(audio_files[z][x],4),cmap="gray")
            else:
                plt.imsave(fname=f'./data/train/{label_dir}/image'+str(x)+'.png',arr=getMelSpectrogram(audio_files[z][x],4),cmap="gray")
            x += 1
            print("Done.")
        z += 1
        label_dir = 'crowd'
    
    
    
    