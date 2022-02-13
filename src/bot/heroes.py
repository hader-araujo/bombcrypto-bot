import time
import pyautogui

import src.env as env
import src.bot.logger as Log
from src.bot.action import clickBtn, goToGame, goToHeroes, moveToWithRandomness, scroll, getPositions, scroll_backwards
from src.bot.utils import isHome, isWorking, isRedBar
from src.utils.opencv import show


def clickButtons():
    buttons = getPositions(env.images['go-work'],
                           threshold=env.threshold['go_to_work_btn'] * env.scale_image['threshold'] if env.scale_image[
                               'enable'] else env.threshold['go_to_work_btn'])
    if env.debug['clickButtons']:
        show(buttons, None, '[clickButtons] buttons')
    for (x, y, w, h) in buttons:
        moveToWithRandomness(x + (w / 2), y + (h / 2))
        pyautogui.click()
        env.hero_clicks = env.hero_clicks + 1
        if env.hero_clicks > 20:
            Log.logger('too many hero clicks, try to increase the go_to_work_btn threshold')
            return
    return len(buttons)


def clickWorkAllButton():
    if env.debug['clickWorkAllButton']:
        buttons = getPositions(env.images['go-work-all'],
                               threshold=env.threshold['go_to_work_all_btn'] * env.scale_image['threshold'] if
                               env.scale_image['enable'] else env.threshold['go_to_work_all_btn'])
        show(buttons, None, '[clickWorkAllButton] [temp] buttons')
    return clickBtn(env.images['go-work-all'], 'go-work-all', timeout=4,
                    threshold=env.threshold['go_to_work_all_btn'] * env.scale_image['threshold'] if env.scale_image[
                        'enable'] else env.threshold['go_to_work_all_btn'])


def clickGreenBarButtons():
    debug_mode_enabled = env.debug['clickGreenBarButtons']
    offset = 130

    green_bars = getPositions(env.images['green-bar'],
                              threshold=env.threshold['green_bar'] * env.scale_image['threshold'] if env.scale_image[
                                  'enable'] else env.threshold['green_bar'])
    Log.logger('🟩 %d green bars detected' % len(green_bars))
    buttons = getPositions(env.images['go-work'],
                           threshold=env.threshold['go_to_work_btn'] * env.scale_image['threshold'] if env.scale_image[
                               'enable'] else env.threshold['go_to_work_btn'])
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
        pos_click_x = x + offset + (w / 2)
        pos_click_y = y + (h / 2)
        moveToWithRandomness(pos_click_x, pos_click_y)
        pyautogui.click()
        env.hero_clicks = env.hero_clicks + 1
        if env.hero_clicks > 20:
            Log.logger('⚠️ Too many hero clicks, try to increase the go_to_work_btn threshold')
            return
    return len(not_working_green_bars)


def clickFullBarButtons():
    debug_mode_enabled = env.debug['clickFullBarButtons']
    offset = 100

    full_bars = getPositions(env.images['full-stamina'],
                             threshold=env.threshold['default'] * env.scale_image['threshold'] if env.scale_image[
                                 'enable'] else env.threshold['default'])
    buttons = getPositions(env.images['go-work'],
                           threshold=env.threshold['go_to_work_btn'] * env.scale_image['threshold'] if env.scale_image[
                               'enable'] else env.threshold['go_to_work_btn'])

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
        pos_click_x = x + offset + (w / 2)
        pos_click_y = y + (h / 2)
        moveToWithRandomness(pos_click_x, pos_click_y)
        pyautogui.click()
        env.hero_clicks = env.hero_clicks + 1

    return len(not_working_full_bars)


def sendHeroesHome(heroes_list):
    heroes_at_home = 0
    if not env.home['enable']:
        return heroes_at_home

    hero_index = 0
    while (True):

        go_home_buttons = getPositions(env.images['send-home'], threshold=env.home['home_button_threshold'])
        go_work_buttons = getPositions(env.images['go-work-old'], threshold=env.threshold['go_to_work_btn'])

        hero_position = None
        for hero in heroes_list:
            hero_positions = getPositions(hero, threshold=env.home['hero_threshold'])
            if len(hero_positions) == 0:
                hero_positions = getPositions(hero, threshold=env.home['hero_threshold'])
            if len(hero_positions) > hero_index:
                if not isHome(hero_positions[hero_index], go_home_buttons):
                    hero_position = hero_positions[hero_index]
                    break
                else:
                    continue
            else:
                continue

        if hero_position is None:
            print('No heroes that should be sent home found.')
            return heroes_at_home
        print(' hero should be sent home found')

        debug_mode_enabled = env.debug['sendHeroesHome']
        if debug_mode_enabled:
            show(hero_position, None, '[sendHeroesHome] HEROES')

        if debug_mode_enabled:
            show(go_home_buttons, None, '[sendHeroesHome] go_home_buttons')
            show(go_work_buttons, None, '[sendHeroesHome] go_work_buttons')

        if not isHome(hero_position, go_home_buttons):
            if (isRedBar(hero_position)):
                print('hero with red bar, sending him home')
                pos_click_x = go_home_buttons[0][0] + go_home_buttons[0][2] / 2
                pos_click_y = hero_position[1] + hero_position[3] / 2
                moveToWithRandomness(pos_click_x, pos_click_y)
                pyautogui.click()
                heroes_at_home += 1
                time.sleep(1)
            else:
                print('hero red, not sending him home')
                hero_index += 1
        else:
            print('hero already home, or home full(no dark home button)')
            hero_index += 1

    return heroes_at_home


def sendHeroesToWork():
    if env.cfg['select_heroes_mode'] == 'full':
        return clickFullBarButtons()
    elif env.cfg['select_heroes_mode'] == 'green':
        return clickGreenBarButtons()
    else:
        return clickButtons()


def refreshHeroes():
    Log.logger('🏢 Search for heroes to work')

    goToHeroes()

    if env.cfg['select_heroes_mode'] == "full":
        Log.logger('⚒️ Sending heroes with full stamina bar to work', 'green')
    elif env.cfg['select_heroes_mode'] == "green":
        Log.logger('⚒️ Sending heroes with green stamina bar to work', 'green')
    else:
        Log.logger('⚒️ Sending all heroes to work', 'green')

    empty_scrolls_attempts = env.cfg['scroll_attemps']
    work_all_clicked = False
    if env.cfg['select_heroes_mode'] == 'all':
        time.sleep(1)
        work_all_clicked = clickWorkAllButton()
        if work_all_clicked:
            Log.logger('💪 ALL heroes sent to work')
        time.sleep(2)

        env.hero_clicks = 0

        try:
            heroes_at_home = 0
            while (empty_scrolls_attempts > 0):
                if heroes_at_home >= env.home_qtd:
                    Log.logger('Casa já tem {} heroes'.format(env.home_qtd))
                    break
                heroes_at_home += sendHeroesHome(env.home_heroes)
                empty_scrolls_attempts = empty_scrolls_attempts - 1
                if heroes_at_home >= env.home_qtd:
                    Log.logger('Casa já tem {} heroes'.format(env.home_qtd))
                    break
                scroll()
                time.sleep(2)

            if heroes_at_home < env.home_qtd:
                empty_scrolls_attempts = env.cfg['scroll_attemps']
                while (empty_scrolls_attempts > 0):
                    if heroes_at_home >= env.home_qtd:
                        Log.logger('Casa já tem {} heroes'.format(env.home_qtd))
                        break
                    heroes_at_home += sendHeroesHome(env.home_heroes_backup)
                    empty_scrolls_attempts = empty_scrolls_attempts - 1
                    if heroes_at_home >= env.home_qtd:
                        Log.logger('Casa já tem {} heroes'.format(env.home_qtd))
                        break
                    scroll_backwards()
                    time.sleep(2)
        finally:
            Log.logger('💪 {} heroes sent to work'.format(env.hero_clicks))

    else:
        if not work_all_clicked:
            env.hero_clicks = 0
            while (empty_scrolls_attempts > 0):
                sendHeroesToWork()
                sendHeroesHome()
                empty_scrolls_attempts = empty_scrolls_attempts - 1
                scroll()
                time.sleep(2)
            Log.logger('💪 {} heroes sent to work'.format(env.hero_clicks))

    goToGame()

    return True
