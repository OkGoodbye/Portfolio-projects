import socket
import pygame
from conversions import list_to_string,string_to_list
pygame.init()
font = pygame.font.SysFont("consolas",15)
PORT = 5050
HEADER = 16
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!D/C"
SERVER = "127.0.0.1"
ADDR = (SERVER,PORT)

class Player:
    def __init__(self,addr,name):
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.connect(ADDR)
        self.name = name
        self.send([name])
    def recv_input(self):
        
        msg_length = self.client.recv(HEADER).decode(FORMAT)
        
        if msg_length:
            msg_length = int(msg_length)
            msg = self.client.recv(msg_length).decode(FORMAT)
            return string_to_list(msg)
        else:
            print("broken message")
    def send(self,msg):
        
        message = list_to_string(msg).encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b" "*(HEADER-len(send_length))
        self.client.send(send_length)
        self.client.send(message)
    def draw_all(self,screen,rooms):
        screen.fill((255,255,255))
        
        
        
        rects = []
        for x,item in enumerate(rooms):
            #print(item)
            text = font.render(str(item),True,(0,0,0))
            rect = text.get_rect(center = (250,(x+1)*50))
            screen.blit(text,rect)
            rects.append(rect)
        return rects
player = Player(ADDR,"test")
screen = pygame.display.set_mode((500,500))
def joinloop():
    new_room_text = font.render("new room",True,(0,0,0))
    new_room_rect = new_room_text.get_rect(bottomright = (475,475))
    while True:
        
        rooms = player.recv_input()
        if "!JOIN" in rooms:
            break
        room_rects = player.draw_all(screen,rooms)
        
        screen.blit(new_room_text,new_room_rect)
        pygame.display.flip()
        mp = pygame.mouse.get_pos()
        to_send = [""]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player.send(DISCONNECT_MESSAGE)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for code,item in zip(rooms,room_rects):
                    if item.collidepoint(mp):
                        to_send = [code]
                if new_room_rect.collidepoint(mp):
                    to_send = ["!N/R"]
                    
        player.send(to_send)
def gameloop():
    while True:
        
        screen.fill((255,255,255))
        locations = player.recv_input()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player.send([DISCONNECT_MESSAGE])
        
        text = font.render(f"users in this room: {locations[0]}",True,(0,0,0))
        for item in locations[1:]:
            
            pygame.draw.circle(screen,(0,0,0),item,3)
        screen.blit(text,(35,35))
        player.send(pygame.mouse.get_pos())
        pygame.display.flip()
        
 
joinloop()
gameloop()
