from datetime import datetime
import pytz

RO_TZ = pytz.timezone('Europe/Bucharest')

def now_ro():
    return datetime.now(RO_TZ)