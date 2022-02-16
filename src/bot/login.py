from time import sleep
import pyautogui

import src.env as env
import src.bot.logger as Log
from src.bot.action import clickBtn, closeMetamaskWindow
from src.decorators.check_metamask_notification import checkMetamaskNotification


def login():
    try:
        Log.logger('😿 login')

        closeMetamaskWindow()

        sleep(1)

        pyautogui.hotkey('ctrl','f5')

        sleep(15)

        Log.logger('Fim do sleep do ctrl F5')

        Log.logger("Vai clicar no wallet 1")
        if clickBtn(env.images['connect-wallet'], name='connectWalletBtn', timeout = 15):
            Log.logger('🎉 Connect wallet button detected, logging in!')

        Log.logger("Clicou no wallet 1")

        if clickOnSignIn():
            pass
            # clickBtn(env.images['treasure-hunt-icon'], name='teasureHunt', timeout = 5)

        Log.logger("Fim do login")
        return True
    except:
        Log.logger('Erro ao fazer login')
        return False

@checkMetamaskNotification
def clickOnSignIn():
    env.in_login_process = True
    env.force_full_screen = True
    Log.logger("Vai clicar no wallet 2")
    result = clickBtn(env.images['select-wallet-2'], name='sign button', timeout=8)
    Log.logger("Clicou no wallet 2")
    env.in_login_process = False
    env.force_full_screen = False

    Log.logger("Fim do signIn")

    return result