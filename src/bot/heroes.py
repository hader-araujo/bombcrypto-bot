import sys
import time
import pyautogui

import src.env as env
import src.bot.logger as Log
from src.bot.action import clickBtn, goToGame, goToHeroes, moveToWithRandomness, scroll, getPositions
from src.bot.utils import isHome, isWorking
from src.utils.opencv import show

def clickButtons():
    buttons = getPositions(env.images['go-work'], threshold=env.threshold['go_to_work_btn']*env.scale_image['threshold'] if env.scale_image['enable'] else env.threshold['go_to_work_btn'])
    if env.debug['clickButtons']:        
        show(buttons, None, '[clickButtons] buttons')
    for (x, y, w, h) in buttons:
        moveToWithRandomness(x+(w/2),y+(h/2))
        pyautogui.click()
        env.hero_clicks = env.hero_clicks + 1
        if env.hero_clicks > 20:
            Log.logger('too many hero clicks, try to increase the go_to_work_btn threshold')
            return
    return len(buttons)

def clickWorkAllButton():
    if env.debug['clickWorkAllButton']:
        buttons = getPositions(env.images['go-work-all'], threshold=env.threshold['go_to_work_all_btn']*env.scale_image['threshold'] if env.scale_image['enable'] else env.threshold['go_to_work_all_btn'])
        show(buttons, None, '[clickWorkAllButton] [temp] buttons')
    return clickBtn(env.images['go-work-all'],'go-work-all', timeout=2, threshold=env.threshold['go_to_work_all_btn']*env.scale_image['threshold'] if env.scale_image['enable'] else env.threshold['go_to_work_all_btn'])

def clickGreenBarButtons():
    debug_mode_enabled = env.debug['clickGreenBarButtons']
    offset = 130    

    green_bars = getPositions(env.images['green-bar'], threshold=env.threshold['green_bar']*env.scale_image['threshold'] if env.scale_image['enable'] else env.threshold['green_bar'])
    Log.logger('🟩 %d green bars detected' % len(green_bars))
    buttons = getPositions(env.images['go-work'], threshold=env.threshold['go_to_work_btn']*env.scale_image['threshold'] if env.scale_image['enable'] else env.threshold['go_to_work_btn'])
    Log.logger('🆗 %d buttons detected' % len(buttons))

    if debug_mode_enabled:
        show(green_bars, None, '[clickGreenBarButtons] green_bars')
        show(buttons, None, '[clickGreenBarButtons] buttons')

    not_working_green_bars = []
    for bar in green_bars:
        if not isWorking(bar, buttons):
            not_working_green_bars.append(bar)
    if len(not_working_green_bars) > 0:
        Log.logger('🆗 %d buttons with green bar detected' % len(not_working_green_bars))
        Log.logger('👆 Clicking in %d heroes' % len(not_working_green_bars))

    for (x, y, w, h) in not_working_green_bars:
        pos_click_x = x+offset+(w/2)
        pos_click_y = y+(h/2)
        moveToWithRandomness(pos_click_x,pos_click_y)
        pyautogui.click()
        env.hero_clicks = env.hero_clicks + 1
        if env.hero_clicks > 20:
            Log.logger('⚠️ Too many hero clicks, try to increase the go_to_work_btn threshold')
            return
    return len(not_working_green_bars)

def clickFullBarButtons():
    debug_mode_enabled = env.debug['clickFullBarButtons']
    offset = 100

    full_bars = getPositions(env.images['full-stamina'], threshold=env.threshold['default']*env.scale_image['threshold'] if env.scale_image['enable'] else env.threshold['default'])
    buttons = getPositions(env.images['go-work'], threshold=env.threshold['go_to_work_btn']*env.scale_image['threshold'] if env.scale_image['enable'] else env.threshold['go_to_work_btn'])
    
    if debug_mode_enabled:
        show(full_bars, None, '[clickFullBarButtons] full_bars')
        show(buttons, None, '[clickFullBarButtons] buttons')

    not_working_full_bars = []
    for bar in full_bars:
        if not isWorking(bar, buttons):
            not_working_full_bars.append(bar)

    if len(not_working_full_bars) > 0:
        Log.logger('👆 Clicking in %d heroes' % len(not_working_full_bars))

    for (x, y, w, h) in not_working_full_bars:
        
        pos_click_x = x+offset+(w/2)
        pos_click_y = y+(h/2)
        moveToWithRandomness(pos_click_x,pos_click_y)
        pyautogui.click()
        env.hero_clicks = env.hero_clicks + 1

    return len(not_working_full_bars)

def sendHeroesHome():
    if not env.home['enable']:
        return
    heroes_positions = []
    for hero in env.home_heroes:
        hero_positions = getPositions(hero, threshold=env.home['hero_threshold'])
        if not len (hero_positions) == 0:
            hero_position = hero_positions[0]
            heroes_positions.append(hero_position)

    n = len(heroes_positions)
    if n == 0:
        print('No heroes that should be sent home found.')
        return
    print(' %d heroes that should be sent home found' % n)

    debug_mode_enabled = env.debug['sendHeroesHome']
    if debug_mode_enabled:
        show(heroes_positions, None, '[sendHeroesHome] HEROES')

    go_home_buttons = getPositions(env.images['send-home'], threshold=env.home['home_button_threshold'])
    go_work_buttons = getPositions(env.images['go-work-old'], threshold=env.threshold['go_to_work_btn'])
    if debug_mode_enabled:
        show(go_home_buttons, None, '[sendHeroesHome] go_home_buttons')
        show(go_work_buttons, None, '[sendHeroesHome] go_work_buttons')

    for position in heroes_positions:
        if not isHome(position,go_home_buttons):
            if(not isWorking(position, go_work_buttons)):
                print ('hero not working, sending him home')
                pos_click_x = go_home_buttons[0][0]+go_home_buttons[0][2]/2
                pos_click_y = position[1]+position[3]/2
                moveToWithRandomness(pos_click_x,pos_click_y)
                pyautogui.click()
            else:
                print ('hero working, not sending him home(no dark work button)')
        else:
            print('hero already home, or home full(no dark home button)')

def sendHeroesToWork():
    if env.cfg['select_heroes_mode'] == 'full':
        return clickFullBarButtons()
    elif env.cfg['select_heroes_mode'] == 'green':
        return clickGreenBarButtons()
    else:
        return clickButtons()

def refreshHeroes():
    try:
        Log.logger('🏢 Search for heroes to work')

        if not goToHeroes():
            Log.logger('Erro ao selecionar o botao voltar')
            return False

        if not env.home['enable'] and env.cfg['select_heroes_mode'] == 'all':
            time.sleep(1)
            work_all_clicked = clickWorkAllButton()
            if work_all_clicked:
                Log.logger('💪 ALL heroes sent to work')
            else:
                Log.logger('Tentando clicar no botao all novamente')
                clickWorkAllButton()
            time.sleep(2)

        goToGame()
        return True
    except:
        Log.logger('Erro tentar dar refresh nos heroes')
        return False
