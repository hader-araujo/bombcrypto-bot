from cv2 import cv2
from os import listdir
import src.env as env
from src.utils import string
from src.utils.image import resizeImageForScale

def loadHeroesImagesToHome():
    file_names = listdir('./src/assets/{}/heroes-to-send-home'.format(env.system))
    heroes = []
    for file in file_names:
        if file != '.gitkeep':
            path = './src/assets/{}/heroes-to-send-home/{}'.format(env.system, file)
            hero_image = cv2.imread(path)
            heroes.append(hero_image)

    print('>>---> %d heroes that should be sent home loaded' % len(heroes))
    return heroes

def loadImages():
    file_names = listdir('./src/assets/{}'.format(env.system))
    targets = {}
    for file in file_names:
        path = 'src/assets/{}/{}'.format(env.system,file)
        target_name = string.removeSuffix(file, '.png')
        temp_image = cv2.imread(path)
        if env.scale_image['enable']:
            targets[target_name] = resizeImageForScale(temp_image, env.scale_image['percent'])
        else:
            targets[target_name] = temp_image

    return targets