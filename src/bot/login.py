from time import sleep
import pyautogui
import pyperclip

import src.env as env
import src.bot.logger as Log
from src.bot.action import clickBtn, closeMetamaskWindow
from src.decorators.check_metamask_notification import checkMetamaskNotification


def login():
    try:
        Log.logger('😿 login')

        closeMetamaskWindow()

        sleep(1)

        metamask_password_login()

        if not clickBtn(env.images['connect-wallet'], name='connectWalletBtn', timeout=2):
            pyautogui.hotkey('ctrl','f5')

            sleep(13)

            Log.logger('Fim do sleep do ctrl F5')

            Log.logger("Vai clicar no wallet 1")
            if clickBtn(env.images['connect-wallet'], name='connectWalletBtn', timeout=15):
                Log.logger('🎉 Connect wallet button detected, logging in!')
            Log.logger("Clicou no wallet 1")

        Log.logger("Vai clicar no wallet 2")
        if clickBtn(env.images['connect-wallet-2'], name='connectWallet2Btn', timeout=5):
            Log.logger('🎉 Connect wallet 2 button detected, logging in!')
        Log.logger("Clicou no wallet 2")

        metamask_password_login()

        if clickOnSignIn():
            pass
            # clickBtn(env.images['treasure-hunt-icon'], name='teasureHunt', timeout = 5)

        Log.logger("Fim do login")
        return True
    except:
        Log.logger('Erro ao fazer login')
        return False


def metamask_password_login():
    Log.logger("Verifica se a metamask está deslogada")
    if clickBtn(env.images['metamask-notification'], name='metamaskNotificationBtn', timeout=2):
        sleep(1)
        Log.logger('🎉 Metamask notification button detected!')

        if clickBtn(env.images['input-password'], name='metamaskNotificationBtn', timeout=3, stop_window_activation=True):
            Log.logger('🎉 Input password detected!')

            pyperclip.copy(env.cfg['metamask_password'])
            pyautogui.hotkey("ctrl", "v")

            if clickBtn(env.images['metamask-unlock'], name='metamaskUnlockBtn', timeout=2,
                        stop_window_activation=True):
                Log.logger('🎉 Botao logar clicado!')

                if clickBtn(env.images['b-logo'], name='metamaskUnlockBtn', timeout=2,stop_window_activation=True):
                    if clickBtn(env.images['metamask-without-notification'], name='metamaskNotificationBtn', timeout=10, threshold=0.99, to_not_click=True):
                        sleep(1)
                        clickBtn(env.images['metamask-notification'], name='metamaskNotificationBtn', timeout=2)



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