import pygame
import math
WIDTH = 1000
HEIGHT = 500
TEST = 1000
def lerp(p1,p2,t):
    return (p1[0]*(1-t)+p2[0]*t,p1[1]*(1-t)+p2[1]*t)
def to_pygame(point):
    return (int(point[0]),int(point[1]))
class Boundary:
    def __init__(self,a,b,colour):
        self.a = a
        self.b = b
        self.colour = colour
    def apply_darkness(self,distance):
        output = []
        
        for channel in self.colour:
            new_channel = max(0,min(channel,channel/(distance**2)*10))
            output.append(new_channel)
        return output
class Ray:
    def __init__(self,point,angle):
        self.point = point
        self.angle = angle
    def collide(self,boundary):
        (x1,y1),(x2,y2),(x3,y3),(x4,y4)=self.point,(self.point[0]+math.cos(self.angle),self.point[1]+math.sin(self.angle)),boundary.a,boundary.b
        d = ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
        if d!=0:
            t = ((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4))/d
            u = ((x1-x3)*(y1-y2)-(y1-y3)*(x1-x2))/d
            return 0<u<1 and t>0,(x1+t*(x2-x1),y1+t*(y2-y1))
        else:
            return False,None
    def collide_all(self,b_list):
        record = (float("inf"),None)
        for item in b_list:
            collision = self.collide(item)
            if collision[0]:
                dist = math.hypot(collision[1][0]-self.point[0],collision[1][1]-self.point[1])
                if dist<record[0]:
                    record = (dist,item)
        
        return record
    
class Player:
    def __init__(self,pos,angle,boundaries):
        self.pos = pos
        self.angle = angle
        self.fov = math.pi/2
        self.resolution = 500
        self.boundaries = boundaries
        
    def draw(self,screen):
        
        ray_list = []
        x_range = 500
        step = 1
        line_width = int(WIDTH/self.resolution)
        for i in range(self.resolution):
            x_coord = (i-self.resolution/2)*step
            ray = Ray(self.pos,math.atan2(x_coord,TEST)+self.angle)
            collision_check = ray.collide_all(self.boundaries)
            collides = collision_check[0]
            
            draw_point = i/self.resolution*WIDTH
            if collides!=float("inf"):
                
                
                
                d =  collides
                h = 1/(d)*HEIGHT
                a = (draw_point,250-h/2)
                b = (draw_point,250+h/2)
                
                
                pygame.draw.line(screen,collision_check[1].apply_darkness(d),to_pygame(a),to_pygame(b),line_width)
            
    def move(self,keys,rotate):
        self.angle += rotate/500
        fb = keys[pygame.K_s]-keys[pygame.K_w]
        lr = -keys[pygame.K_a]+keys[pygame.K_d]
        self.pos = (self.pos[0]-math.cos(self.angle)*fb/30,self.pos[1]-math.sin(self.angle)*fb/30)
        self.pos = (self.pos[0]+math.cos(self.angle+math.pi/2)*lr/60,self.pos[1]+math.sin(self.angle+math.pi/2)*lr/60)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
b_list = []
levelfile = open("level.txt", "r")
level = levelfile.read().split("\n")
for i in range(len(level)):
    cline = level[i].split(" ")
    a = cline[0].split(",")
    b = cline[1].split(",")
    b_list.append(Boundary((float(a[0])/30, float(a[1])/30),( float(b[0])/30, float(b[1])/30),(75,255,150)))
player = Player((0,0),math.pi/2,b_list)
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)
while 1:
    pygame.event.pump()
    screen.fill((0,0,0))
    player.draw(screen)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        TEST += 5
    if keys[pygame.K_DOWN]:
        TEST -= 5
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
    player.move(keys,pygame.mouse.get_rel()[0])
    
    pygame.display.flip()

        
