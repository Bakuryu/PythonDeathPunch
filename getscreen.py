import win32gui
import win32ui
import win32con
import win32api
import numpy as np
import pywintypes

winlist = []
def enum_cb(hwnd,results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

def get_screen(windowName):
    toplist = []
    win32gui.EnumWindows(enum_cb, toplist)

    game = [(hwnd, title) for hwnd, title in winlist if windowName in title.lower()]
    game = game[0]
    if game[1] == 'One Finger Death Punch':
        hwnd = game[0]
    else:
        return

    try:
        if win32gui.GetForegroundWindow() is not hwnd:
            win32gui.SetForegroundWindow(hwnd)
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        w = right - left
        h = bot - top
        if w is not 800 and h is not 470:
            win32gui.MoveWindow(hwnd, 0, 0, 800, 470, True)
        wDC = win32gui.GetWindowDC(hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, w - 18, h - 48)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (w - 18, h - 48), dcObj, (left + 9, top + 37), win32con.SRCCOPY)

        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')

        img.shape = (h - 48, w - 18, 4)

        return img, win32gui.GetWindowRect(hwnd)
    except pywintypes.error:
        return