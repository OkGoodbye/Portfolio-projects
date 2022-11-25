from definitions import WIDTH,HEIGHT,DEPTH
from math import dist
import numpy as np
import pygame
from random import randint
pygame.init()
transform_matrix = np.array([[0.5*WIDTH,-0.5*WIDTH,0],[0.25*HEIGHT,0.25*HEIGHT,0],[0,0,DEPTH]])
inverse_matrix = np.linalg.inv(transform_matrix)
from_isometric = lambda p:transform_matrix@np.array(p)
to_isometric = lambda p:inverse_matrix@np.array(p)
screen = pygame.display.set_mode((500,500))
cube = pygame.transform.scale(pygame.image.load("blue cube.png").convert_alpha(),(WIDTH,HEIGHT))
font = pygame.font.SysFont("consolas",10)
class Box:
    def __init__(self,iso_coord,camera,image):
        self.coord = np.array(iso_coord)
        self.camera = camera
        camera.to_draw.append(self)
        self.image = image
    def draw(self,screen,offset):
        
        divided_center = from_isometric(self.coord)
        draw_center = np.array([divided_center[0],divided_center[1]+divided_center[2]])
        
        screen.blit(self.image,self.image.get_rect(center = draw_center))
    
        
    def dist2(self,point):
        return dist(self.coord,point)
    def collide(self,box):
        k = self.coord-box.coord
        
        collides = (abs(k[0])<=1 and abs(k[1])<=1 and abs(k[2])<=0.5)
        
        return collides
class Player(Box):
    def __init__(self,iso_coord,camera,image):
        Box.__init__(self,iso_coord,camera,image)
        
    def move(self,height_map,offset):
               
        final_position = self.coord.copy()
        #print(final_position)
        final_position+=offset.copy()
        
        collides = False
        cubes = self.camera.to_draw[:]
        cubes.remove(self)
        for item in cubes:
            if item.collide(self):
                collides = True
                break
        if not collides:
            
            self.coord = final_position
class Camera:
    def __init__(self,screen,pos):
        self.screen = screen
        self.pos = pos
        self.to_draw = []
    def draw(self):
        self.to_draw.sort(key = lambda box:-box.dist2(self.pos))
        for item in self.to_draw:
            item.draw(self.screen,self.pos)
camera = Camera(screen,(0,0,0))
height_map = [[0,0,0,0,0,0,0,0,0,0,0,0],
              [0,1,1,1,1,1,1,1,1,1,1,0],
              [0,1,1,1,1,2,1,1,1,1,1,0],
              [0,1,1,1,1,3,1,1,1,1,1,0],
              [0,1,1,1,1,4,1,1,1,1,1,0],
              [0,1,1,1,1,5,1,1,1,1,1,0],
              [0,1,1,1,1,4,1,1,1,1,1,0],
              [0,1,1,1,1,3,1,1,1,1,1,0],
              [0,1,1,1,1,1,1,1,1,1,1,0],
              [0,1,1,1,1,1,1,1,1,1,1,0],
              [0,1,1,1,1,1,1,1,1,1,1,0],
              [0,0,0,0,0,0,0,0,0,0,0,0],]
for x,xitem in enumerate(height_map):
    for y,yitem in enumerate(xitem):
        for z in range(yitem):
            Box((x+10,y,1-z),camera,cube)
b = Player((18,7,0),camera,cube)
clock = pygame.time.Clock()
camera.pos = (100,100,-1000)
while 1:
    #camera.pos = (camera.pos[0]+0.1,camera.pos[1],camera.pos[2])
    screen.fill((0,0,0))
    pygame.event.pump()
    clock.tick(60)
    camera.draw()
    keys = pygame.key.get_pressed()
    to_move = [int(keys[pygame.K_RIGHT]-keys[pygame.K_LEFT]),int(-keys[pygame.K_UP]+keys[pygame.K_DOWN]),0]
    
    b.move(height_map,np.array(to_move,dtype = int32)*0.125)

    
    pygame.display.flip()
                     

