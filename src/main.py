import time
from src.utils.number import addRandomness
import src.bot.logger as Log
import src.env as env
import src.bot.heroes as Heroes
import src.bot.login as Auth
import src.bot.action as Action
from src.bot.action import clickBtn
import sys

def run():
    time.sleep(5)
    intervals = env.cfg['time_intervals']

    last = {
        "login" : 0,
        "heroes" : 0,
        "new_map" : 0,
        "refresh_heroes" : 0
    }

    while True:

        now = time.time()
        if now - last["login"] > addRandomness(intervals['check_for_login'] * 60):
            sys.stdout.flush()

            if Auth.login():
                last["login"] = now
                last["refresh_heroes"] = now

        now = time.time()
        if now - last["heroes"] > addRandomness( intervals['send_heroes_for_work'] * 60):
            if Heroes.refreshHeroes():
                last["heroes"] = now
                last["refresh_heroes"] = now

        # if now - last["new_map"] > intervals['check_for_new_map_button']:
        #     last["new_map"] = now
        #
        #     if clickBtn(env.images['new-map']):
        #         Log.logNewMapClicked()

        now = time.time()
        if now - last["refresh_heroes"] > addRandomness( intervals['refresh_heroes_positions'] * 60):
            if Action.refreshHeroesPositions():
                last["refresh_heroes"] = now

        Log.logger(None, progress_indicator=True)

        sys.stdout.flush()

        time.sleep(1)