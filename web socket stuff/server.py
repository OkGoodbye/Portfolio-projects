import socket
import threading
from conversions import list_to_string,string_to_list
from random import randint
HEADER = 16
PORT = 5050
SERVER = "127.0.0.1"
ADDR = (SERVER,PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!D/C"
print(string_to_list(list_to_string([DISCONNECT_MESSAGE])))
class ClientHandler:
    def __init__(self,conn,addr,parent):
        self.conn = conn
        self.name = self.recv_input()
        self.parent = parent
        
        self.room_index = 0
        self.joined = None
        self.join_loop()
        
    def recv_input(self):
        msg_length = self.conn.recv(HEADER).decode(FORMAT)
        
        if msg_length:
            msg_length = int(msg_length)
            msg = self.conn.recv(msg_length).decode(FORMAT)
            
            return msg
        
    def send(self,msg):
        message = list_to_string(msg).encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b" "*(HEADER-len(send_length))
        self.conn.send(send_length)
        self.conn.send(message)
    
    def get_output(self):
        #print("waiting for input")
        
        return string_to_list(self.recv_input())
    def join_loop(self):
        done = False
        chosen_room = ""
        while not done:
            
            self.send(self.parent.locations)
            
            user_message = self.get_output()
            
            if DISCONNECT_MESSAGE in user_message:
                done = True
            elif user_message[0]!="":
                if user_message[0] == "!N/R":
                    self.parent.generate_code()
                elif user_message[0] in self.parent.locations:
                    chosen_room = user_message[0]
                    done = True
                else:
                    print(user_message)
                
        self.send(["!JOIN",chosen_room])      
        self.room = self.parent.rooms[self.parent.locations.index(chosen_room)]
        self.room_index = self.room.add_client(self)
        self.game_loop()
    def game_loop(self):
        done = False
        
        while True:
            points = []
            for key,point in self.room.point:
                points.append(point)
            self.send([self.room.client_number]+self.room.points)
            
            mp = self.get_output()
            if DISCONNECT_MESSAGE in mp:
                break
                self.room.close(self.room_ind
            self.room.points[self.room_index] = mp
            
        
class Room:
    def __init__(self):
        self.client_number = 0
        self.clients = []
        self.points = {}
    def add_client(self,client):
        self.client_number += 1
        self.clients.append(client)
        self.points[self.client_number] = (0,0)
        return self.client_number
    def close(self,index):
        self.points.pop(index)
class Server:
    def __init__(self,addr):
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(addr)
        self.server.listen()
        self.connections = 0
        self.clients = []
        self.locations = []
        self.rooms = []
        while True:
            conn,addr = self.server.accept()
            thread = threading.Thread(target = self.handle_join,args = (conn,addr))
            thread.start()
    
    def handle_join(self,conn,addr):
        print("new player joined")
        self.connections += 1
        self.clients.append(ClientHandler(conn,addr,self))
    def generate_code(self):
        for k in range(100):
            code = ""
            for x in range(4):
                code+=chr(randint(65,90))
            if code not in self.locations:
                self.locations.append(code)
                self.rooms.append(Room())
                return True
                
        else:
            return False
        
s = Server(ADDR)
           
