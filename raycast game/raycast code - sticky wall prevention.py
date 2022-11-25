import pygame
import math
import random
WIDTH = 1000
HEIGHT = 800
TEST = 1000
def dist2(p1,p2):
    return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
class Boundary:
    def __init__(self,a,b,texture):
        self.a = a
        self.b = b
        self.texture = texture
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
                    record = (dist,item,collision[1])
        
        return record

class Player:
    def __init__(self,pos,angle,boundaries):
        self.pos = pos
        self.angle = angle
        self.fov = math.pi/2
        self.resolution = 800
        self.boundaries = boundaries
        self.radius = 0.02
    def draw(self,screen):
        
        ray_list = []
        x_range = 1
        step = 1
        line_width = int(WIDTH/self.resolution)+1
        linear_test = []
        
        for i in range(self.resolution):
            x_coord = (i-self.resolution/2)*step
            ray = Ray(self.pos,math.atan2(x_coord,TEST)+self.angle)
            collision_check = ray.collide_all(self.boundaries)
            collides = collision_check[0]
            
            draw_point = i/self.resolution*WIDTH
            if collides!=float("inf"):
                
                
                
                d =  collides
                h = 1/(d)*HEIGHT
                
                b = (draw_point,250+h/2)
                texture_distance = math.hypot(collision_check[2][0]-collision_check[1].a[0],collision_check[2][1]-collision_check[1].a[1])
                texture_slice = int((math.hypot(collision_check[2][0]-collision_check[1].a[0],collision_check[2][1]-collision_check[1].a[1])*collision_check[1].texture.get_width()*4)%collision_check[1].texture.get_width())
                draw_image = pygame.Surface((line_width,collision_check[1].texture.get_height()),pygame.SRCALPHA)
                
                draw_image.blit(collision_check[1].texture,(-texture_slice,0))
                darkener = pygame.Surface((line_width,collision_check[1].texture.get_height()))
                darkener.set_alpha(max(0,min(255,255-h)))
                draw_image.blit(darkener,(0,0))
                #draw_image.set_alpha(20)
                draw_image = pygame.transform.smoothscale(draw_image,(line_width,h))
                screen.blit(draw_image,draw_image.get_rect(center = (draw_point,HEIGHT/2)))
                
    def collide(self,boundary,point):
        v,w = boundary.a,boundary.b
        l2 = dist2(v,w)
        if l2 == 0:
          return dist2(point,v)**0.5<self.radius
        else:
          t = ((point[0] - v[0]) * (w[0] - v[0]) + (point[1] - v[1]) * (w[1] - v[1])) / l2
          t = max((0,min(1,t)))
          return dist2(point,(v[0] + t * (w[0] - v[0]), v[1] + t * (w[1] - v[1])) )**0.5<self.radius
    def collide_all(self,trial_location):
        collides =  False
        for boundary in self.boundaries:
            if self.collide(boundary,trial_location):
                #print(f"colided with boundraw from {boundary.a} to {boundary.b}")
                collides = True
        
        return collides
    def move(self,keys,rotate):
        self.angle += rotate/500
        fb = keys[pygame.K_s]-keys[pygame.K_w]
        lr = -keys[pygame.K_a]+keys[pygame.K_d]
        normal_trial = (self.pos[0]-math.cos(self.angle)*fb/30+math.cos(self.angle+math.pi/2)*lr/60,self.pos[1])
        
        if not self.collide_all(normal_trial):
           
            self.pos = normal_trial
        tangent_trial = (self.pos[0],self.pos[1]+math.sin(self.angle+math.pi/2)*lr/60-math.sin(self.angle)*fb/30)
        if not self.collide_all(tangent_trial):
            
            self.pos = tangent_trial
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.transform.set_smoothscale_backend("GENERIC")
b_list = []
levelfile = open("level.txt", "r")
level = levelfile.read().split("\n")
texture = pygame.image.load("brick_texture.png")
texture.set_colorkey((0, 0, 0))
for i in range(len(level)):
    cline = level[i].split(" ")
    a = cline[0].split(",")
    b = cline[1].split(",")
    b_list.append(Boundary((float(a[0]), float(a[1])),( float(b[0]), float(b[1])),texture))
player = Player((1,1.2),math.pi/2,b_list)
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

        
