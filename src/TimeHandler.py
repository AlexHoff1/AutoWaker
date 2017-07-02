import datetime
import time

def today():
    return time.strftime("%Y-%m-%d")

def clocktime():
    return time.strftime("%H:%M:%S")

def endCheckTime():
    return datetime.time(3,0,0,0)

def startCheckTime():
    return datetime.time(2,0,0,0)
    
def now():
    return datetime.datetime.now().time()
    
def stallAction(second_duration):
    time.sleep(second_duration)

def addHours(datetime_object, hours):
    time_to_add = datetime.timedelta(seconds = hours*3600)
    try:
        return datetime_object + time_to_add
    except:
        return datetime_object