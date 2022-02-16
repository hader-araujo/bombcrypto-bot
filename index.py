# -*- coding: utf-8 -*-    
from time import sleep
from src.main_multi_account import runMultiAccount
from src.utils.config import loadConfigsFromFile
from src.bot.logger import logger, exception

config = loadConfigsFromFile()

logger('Bombcrypto BOT starting', color='yellow')
while True:
    try:
        logger('Running bot for MULTI ACCOUNT ON SAME MONITOR', color='cyan')
        runMultiAccount()
    except KeyboardInterrupt:
        break
    except Exception as e:
        logger('Bombcrypto BOT crashed... restarting in 5 seconds.', color='red')
        logger("Exception: %s" % (str(e)), color='red')
        exception(e)
        sleep(5)
        continue
