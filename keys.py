import win32api
import time

def left(sleep):
    print("Left")
    win32api.keybd_event(0x01, 0, )
    time.sleep(sleep)
    win32api.keybd_event(0x01, 0, 2)

def right(sleep):
    print("Right")
    win32api.keybd_event(0x02, 0, )
    time.sleep(sleep)
    win32api.keybd_event(0x02, 0, 2)