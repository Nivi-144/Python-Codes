
import threading
import time

buffer = []
capacity = 3
total_items = 5

empty = threading.Semaphore(capacity)
full = threading.Semaphore(0)
mutex = threading.Semaphore(1)

def producer():
    for item in range(1, total_items + 1):
        empty.acquire()
        mutex.acquire()

        buffer.append(item)
        print("Produced:", item, "| Buffer:", buffer)

        mutex.release()
        full.release()
        time.sleep(0.1)

def consumer():
    for i in range(total_items):
        full.acquire()
        mutex.acquire()

        item = buffer.pop(0)
        print("Consumed:", item, "| Buffer:", buffer)

        mutex.release()
        empty.release()
        time.sleep(0.1)

p = threading.Thread(target=producer)
c = threading.Thread(target=consumer)

p.start()
c.start()

p.join()
c.join()

print("Final Buffer:", buffer)
