import win32api, win32con
import subprocess
import time

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

def press(key):
    keyboard.press(key)
    keyboard.release(key)

subprocess.check_output(["chrome.exe", "https://www.skyscanner.es/transporte/vuelos/mad/fran/200801/?adults=1&children=0&adultsv2=1&childrenv2=&infants=0&cabinclass=economy&rtn=0&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home"])
time.sleep(20)
click(10,10)
time.sleep(1)
press(Key.f12)

click(10,10)