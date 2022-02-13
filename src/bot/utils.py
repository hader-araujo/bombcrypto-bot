import src.env as env
from src.bot.action import getPositions

def isHome(hero, buttons):
    y = hero[1]

    for (_,button_y,_,button_h) in buttons:
        isBelow = y < (button_y + button_h)
        isAbove = y > (button_y - button_h)
        if isBelow and isAbove:
            return False
    return True

def isWorking(bar, buttons):
    y = bar[1]

    for (_,button_y,_,button_h) in buttons:
        isBelow = y < (button_y + button_h)
        isAbove = y > (button_y - button_h)
        if isBelow and isAbove:
            return False
    return True

def isRedBar(bar):
    green_bars = getPositions(env.images['green-bar'],
                              threshold=env.threshold['green_bar'] * env.scale_image['threshold'] if env.scale_image[
                                  'enable'] else env.threshold['green_bar'])

    for green in green_bars:

        diff = green[1] - bar[1]
        if -10 <= diff <= 20:
            return False

    return True
