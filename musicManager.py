from pygame import mixer
import os
from os import listdir

mixer.init()


musicDict = {}
folder_dir = 'musica/'
for track in os.listdir(folder_dir):
    if track.endswith(".mp3") or track.endswith(".ogg") or track.endswith(".m4a") or images.endswith(".mp4") or images.endswith(".wav") or images.endswith(".wma") or images.endswith(".aac"):
        sound = mixer.Sound(folder_dir + track)
        sound.set_volume(0.5)
        musicDict[folder_dir+track] = sound
