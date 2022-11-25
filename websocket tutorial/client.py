import socket
import pygame
pygame.init()
PORT = 5050
HEADER = 16
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "127.0.0.1"
ADDR = (SERVER,PORT)
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)
font = pygame.font.SysFont("consolas",30)
image = pygame.Surface((35,150))
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" "*(HEADER-len(send_length))
    client.send(send_length)
    client.send(message)
    return client.recv(2048).decode(FORMAT)
screen = pygame.display.set_mode((500,500))
done = False
clock = pygame.time.Clock()
while not done:
    clock.tick()
    pygame.event.pump()
    screen.fill((255,255,255))
    keys = pygame.key.get_pressed()
    direction = keys[pygame.K_DOWN]-keys[pygame.K_UP]
    send_info = f"{direction} {clock.get_time()}"
    
    data = send(send_info).split()
    data = list(map(lambda item:tuple(map(int,item.split(","))),data))
    
    for item in data[:2]:
        pos =item
        screen.blit(image,image.get_rect(center = pos))
    pygame.draw.circle(screen,(0,0,0), data[2],6)
    p1_score = font.render(str(data[3][0]),True,(0,0,0))
    p2_score = font.render(str(data[3][1]),True,(0,0,0))
    screen.blit(p1_score,p1_score.get_rect(center = (30,30)))
    screen.blit(p2_score,p2_score.get_rect(center = (470,30)))
    pygame.display.flip()
