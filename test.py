from threading import Thread

def something():
    i = 1
    while(i<10000):
        i+=1
    print("neki")
def somethingElse():
    something()
    print("variable")


print("start")
new_thread = Thread(target=somethingElse)
new_thread.start()

print("finish")