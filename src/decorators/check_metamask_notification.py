import time
from src.bot.action import maximizeMetamaskNotification

def checkMetamaskNotification(fn):
    def exec(*args, **kwargs):
        maximizeMetamaskNotification()
        time.sleep(1)
        return fn(*args, **kwargs)
    return exec