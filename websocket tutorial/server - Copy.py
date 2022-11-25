import socket 
import threading
import pygame
import math
HEADER = 16
PORT = 5050
SERVER = "10.24.80.117"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
REFRESH_MESSAGE = "!REFRESH"
SEPERATOR = "@!"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

current_messages = []
def send(msg,conn):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" "*(HEADER-len(send_length))
    conn.send(send_length)
    conn.send(message)

def handle_client(conn, addr,idx):
    global current_messages
    
    connected = True
    while connected:

        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length[0].isdigit():
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            elif msg==REFRESH_MESSAGE:
                
                send(SEPERATOR.join(current_messages),conn)
                
                
                
            elif msg:
                
                current_messages.append(str(idx)+": "+msg)

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
