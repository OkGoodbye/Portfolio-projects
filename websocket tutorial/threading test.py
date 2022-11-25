import time # import time module  
import threading  
def test(msg):
    print(input(msg))
while True:
    t1 = threading.Thread(target = test,args = ("1: "))
    t1.start()
    t2 = threading.Thread(target = test, args = ("2: "))
    t2.start()
    print("thank you for your input")
    
