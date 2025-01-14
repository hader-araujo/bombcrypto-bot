import time
import sys
import pygetwindow

from src.utils.number import addRandomness
import src.bot.logger as Log
import src.env as env
import src.bot.heroes as Heroes
import src.bot.action as Action
import src.bot.login as Auth

def runMultiAccount():
    time.sleep(5)
    intervals = env.cfg['time_intervals']

    windows = []
    title = env.multi_account_same_monitor['window_contains_title']

    Log.logger('🆗 Start')
    Log.logger('Searching for windows with contains title: {}'.format(title), color='yellow')

    for w in pygetwindow.getWindowsWithTitle(title):
        if w.title.lower() == title.lower():
            windows.append({
                "window": w,
                "heroes" : 0,
                "new_map" : 0,
                "refresh_heroes" : 0
            })

    Log.logger('Found {} window(s):'.format(len(windows)), color='cyan')
    for index, last in enumerate(windows):
        Log.logger('{} -> {}'.format(index+1, last['window'].title), color='cyan')

    if len(windows) == 0:
        Log.logger('Exiting because dont have windows contains "{}" title'.format(title), color='red')
        exit()

    while True:
        
        for index, last in enumerate(windows):
            env.window_object = last["window"]
            Log.logger('CLIENT ACTIVE WINDOW -> {} : {}'.format(index+1, last['window'].title), color='green')
            time.sleep(2)

            now = time.time()
            if now - last["heroes"] > addRandomness(intervals['send_heroes_for_work'] * 60):
                Action.activeWindow()

                if Heroes.refreshHeroes():
                    last["heroes"] = now
                    last["refresh_heroes"] = now
                else:
                    Action.activeWindow()
                    sys.stdout.flush()

                    if Auth.login():
                        last["refresh_heroes"] = now

            now = time.time()
            if now - last["refresh_heroes"] > addRandomness( intervals['refresh_heroes_positions'] * 60):
                Action.activeWindow()
                if Action.refreshHeroesPositions():
                    last["refresh_heroes"] = now
                else:
                    Action.activeWindow()
                    sys.stdout.flush()

                    if Auth.login():
                        if Heroes.refreshHeroes():
                            last["heroes"] = now
                            last["refresh_heroes"] = now

            Log.logger(None, progress_indicator=True)
            sys.stdout.flush()

            time.sleep(1)
