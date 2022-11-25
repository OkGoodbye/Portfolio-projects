import socket 
import threading
import pygame
import math
HEADER = 16
PORT = 5050
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SPEED = .3
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
p_list = [(500,250),(0,250),(250,250),(0,0)]
magnitude = 0.15
angle = math.pi/4.1
def list_to_string(l):
    k = ""
    for item in l:
        k += f"{int(item[0])},{int(item[1])} "
  
    return k
def clamp(mini,maxi,value):
    return min(max(value,mini),maxi)
players = 0
def handle_client(conn, addr,idx):
    global players
    global angle
    global magnitude
    players += 1
    
    connected = True
    while connected:
        if players>1:
            p_list[2] = (p_list[2][0]+math.cos(angle)*magnitude,p_list[2][1]+math.sin(angle)*magnitude)
            
            if -1>p_list[2][1] or 501<p_list[2][1]:
                angle = math.pi*2-angle
                
                p_list[2] = (p_list[2][0],clamp(0,500,p_list[2][1]))
            if p_list[2][0]<0:
                if (p_list[1][1]-75)<p_list[2][1]<(p_list[1][1]+75):
                    angle = math.pi-angle
                    p_list[2] = (clamp(0,500,p_list[2][0]),p_list[2][1])
                    angle -= (p_list[1][1]-p_list[2][1])/300
                else:
                    p_list[2] =(250,250)
                    p_list[3] = (p_list[3][0],p_list[3][1]+1)
                    magnitude+=0.0004
                    
            if p_list[2][0]>500:
                if (p_list[0][1]-75)<p_list[2][1]<(p_list[0][1]+75):
                    angle = math.pi-angle
                    p_list[2] = (clamp(0,500,p_list[2][0]),p_list[2][1])
                    angle += (p_list[0][1]-p_list[2][1])/300
                else:
                    p_list[2] =(250,250)
                    p_list[3]= (p_list[3][0]+1,p_list[3][1])
                    magnitude+=0.0004

        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            elif msg and msg!=" ":
                direction = tuple(map(int,msg.split()))
                p_list[idx] = (p_list[idx][0],p_list[idx][1]+direction[0]*SPEED*direction[1])
            #print(f"[{addr}] {msg}")
            
            conn.send(list_to_string(p_list).encode(FORMAT))

    conn.close()
    print("disconnected") 

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr,threading.active_count() - 2))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] server is starting...")
start()
