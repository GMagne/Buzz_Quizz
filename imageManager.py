import os
from os import listdir
import pygame


class Image:

    def __init__(self, image_path):
        try:
            self.image = pygame.image.load(image_path) #imatge original
            self.size = self.image.get_size() #size de la imatge
        except FileNotFoundError:
            self.image = None
            self.size = (0,0)

    def get_size(self):
        return self.size

    def get_image(self):
        return self.image

    def get_surface(self, scaled, x, y):
        if scaled and x>0 and y>0 and self.size[0]>0 and self.size[1]>0:
            if self.size[0]/x > self.size[1]/y :
                size = (x, int(x*self.size[1]/self.size[0]))
                return pygame.transform.scale(self.image, size), size
            else:
                size = ( int(y*self.size[0]/self.size[1]), y)
                return pygame.transform.scale(self.image, size), size
        else:
            return self.image, self.size




imageDict = {'blank': Image('')}
folder_dir = 'imatges/'
for images in os.listdir(folder_dir):
    if images.endswith(".png") or images.endswith(".jpg") or images.endswith(".jpeg"):
        imageDict[folder_dir+images] = Image(folder_dir+images)

