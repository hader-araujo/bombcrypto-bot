# -*- coding: utf-8 -*-    
from time import sleep
from src.main import run
from src.main_multi_account import runMultiAccount
from src.utils.config import loadConfigsFromFile
from src.bot.logger import logger

config = loadConfigsFromFile()
run_multi_account = config['multiples_accounts_same_monitor']['enable']

logger('Bombcrypto BOT starting', color='yellow')
while True:
    try:
        if run_multi_account:
            logger('Running bot for MULTI ACCOUNT ON SAME MONITOR', color='cyan')
            runMultiAccount()
        else:
            logger('Running bot', color='cyan')
            run()
    except KeyboardInterrupt:
        break
    except:
        logger('Bombcrypto BOT crashed... restarting in 5 seconds.', color='red')
        sleep(5)
        continue
