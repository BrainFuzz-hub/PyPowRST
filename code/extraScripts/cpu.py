import multiprocessing
from time import sleep
import threading


def worker():
    while True:
        l = (2 * 33) >> 3


def stop():
    sleep(5)
    try:
        exit()
    except Exception as e:
        print(e)


stopper = threading.Thread(target=stop)

if __name__ == '__main__':
    cpu = multiprocessing.cpu_count()
    stopper.start()
    for i in range(cpu):
        p = multiprocessing.Process(target=worker)
        p.start()
