import socket
import threading
import pygame
pygame.init()
font = pygame.font.SysFont("consolas",12)
PORT = 5050
HEADER = 16
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
REFRESH_MESSAGE = "!REFRESH"
SEPERATOR = "@!"
SERVER = "10.24.80.117"
ADDR = (SERVER,PORT)
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" "*(HEADER-len(send_length))
    client.send(send_length)
    client.send(message)
    
last_message = "w"
def refresh_message():
    
   
    send(REFRESH_MESSAGE)


    length = client.recv(HEADER).decode(FORMAT)
    if length:
        
        length = int(length)
        return client.recv(length).decode(FORMAT)
                
        
screen = pygame.display.set_mode((500,500))

        
def do_send():
    messages = []
    current_msg = ""
        
        
    while True:
        
        screen.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha() or event.unicode == " ":
                    current_msg += event.unicode
                elif event.key == pygame.K_BACKSPACE and len(current_msg)>0:
                    current_msg = current_msg[:-1]
                elif event.key == pygame.K_RETURN:
                    send(current_msg)
                    current_msg = ""
        
                
        messages = refresh_message().split(SEPERATOR)
        for x,item in enumerate(messages):
            surface = font.render(item,True,(0,0,0))
            screen.blit(surface,surface.get_rect(topleft = (50,10*x+30)))
        typing = font.render(current_msg,True,(0,0,0))
        screen.blit(typing,typing.get_rect(bottomleft = (13,487)))
        pygame.display.flip()

do_send()
    



