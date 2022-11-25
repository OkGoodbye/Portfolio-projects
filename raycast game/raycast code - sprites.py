import pygame
import math
import random
WIDTH = 1000
HEIGHT = 800
TEST = 1000
def dist2(p1,p2):
    return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
def fix(point):
    return (point[0]*90+10,point[1]*90+10)
class Boundary:
    def __init__(self,a,b,texture):
        self.a = a
        self.b = b
        self.length = math.hypot(a[0]-b[0],a[1]-b[1])
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
class Image_section:
    def __init__(self,surface,pos,dist):
        self.image = surface
        self.pos = pos
        self.dist = dist
    def draw(self,screen):
        screen.blit(self.image,self.image.get_rect(center = self.pos))
class Sprite:
    def __init__(self,image,pos,player):
        self.image = image
        player.sprites.append(self)
        self.player = player
        self.pos = pos
        self.distance = 0
    def draw(self,angle,screen):
        rel_angle = math.atan2(-self.pos[1]+self.player.pos[1],-self.pos[0]+self.player.pos[0])+math.pi
        #rel_angle = math.atan2(-self.player.focal_plane.a[0]+self.player.pos[0],-self.player.focal_plane.a[1]+self.player.pos[1])
        trial_ray = Ray(self.player.pos,rel_angle)
        collision_test = trial_ray.collide(self.player.focal_plane)
        
        if collision_test[0]:
            dist = math.hypot(collision_test[1][0]-self.player.focal_plane.a[0],collision_test[1][1]-self.player.focal_plane.a[1])
            
            distance_scale = math.hypot(self.pos[0]-self.player.pos[0],self.pos[1]-self.player.pos[1])
            if distance_scale>0:
                #print("drawing")
                distance_scale = int(1/distance_scale)
                im = pygame.transform.scale(self.image,(self.image.get_width()*distance_scale,self.image.get_height()*distance_scale))
                screen.blit(im,im.get_rect(center = (dist,HEIGHT/2)))
        
    
class Player:
    def __init__(self,pos,angle,boundaries):
        self.pos = pos
        self.angle = angle
        self.fov = math.pi
        self.resolution = 800
        self.boundaries = boundaries
        self.sprites = []
        self.radius = 0.2
        self.create_focal_plane()
    def create_focal_plane(self):
        self.forward = (self.pos[0]+math.cos(self.angle)*TEST,self.pos[1]+math.sin(self.angle)*TEST)
        normal_angle = self.angle - math.pi/2
        a = (self.forward[0]+math.cos(normal_angle)*self.resolution/2,self.forward[1]+math.sin(normal_angle)*self.resolution/2)
        b = (self.forward[0]-math.cos(normal_angle)*self.resolution/2,self.forward[1]-math.sin(normal_angle)*self.resolution/2)
        self.focal_plane = Boundary(a,b,None)
    def debug_draw(self,screen):
        screen.fill((0,0,0))
        for item in self.boundaries:
            pygame.draw.line(screen,(255,255,255),fix(item.a),fix(item.b))
        pygame.draw.circle(screen,(0,0,255),fix(self.pos),4)
        for item in [self.focal_plane.a,self.focal_plane.b,self.forward]:
            pygame.draw.line(screen,(255,0,0),fix(self.pos),fix(item),4)
            #print(item)
        for item in self.sprites:
            pygame.draw.circle(screen,(255,0,0),fix(item.pos),4)
            item.draw(self.angle,screen)
    def draw(self,screen):
        
        ray_list = []
        
        step = 1
        line_width = int(WIDTH/self.resolution)+1
        to_draw = []
        undrawn_sprites = self.sprites[::-1]
        for sprite in undrawn_sprites:
            sprite.distance = math.hypot(self.pos[0]-sprite.pos[0],self.pos[1]-sprite.pos[1])
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
                to_draw.append(Image_section(draw_image,(draw_point,HEIGHT/2),d))
        to_draw.sort(key = lambda x:-x.dist)
        
        for item in to_draw:
            for sprite in undrawn_sprites:
                    if math.hypot(self.pos[0]-sprite.pos[0],self.pos[1]-sprite.pos[1])<item.dist:
                        sprite.draw(self.angle,screen)
            item.draw(screen)
            
                    
                               
                
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
        for item in self.sprites:
            if math.hypot(self.pos[0]-item.pos[0],self.pos[1]-item.pos[1])<self.radius:
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
        self.create_focal_plane()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.transform.set_smoothscale_backend("GENERIC")
b_list = []
levelfile = open("level.txt", "r")
level = levelfile.read().split("\n")
texture = pygame.image.load("purple_bricks.png").convert_alpha()
texture.set_colorkey((0, 0, 0))
for i in range(len(level)):
    cline = level[i].split(" ")
    a = cline[0].split(",")
    b = cline[1].split(",")
    b_list.append(Boundary((float(a[0]), float(a[1])),( float(b[0]), float(b[1])),texture))
player = Player((2,1),0,b_list)
Sprite(pygame.image.load("test_texture.png"),(1,1),player)
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)
clock= pygame.time.Clock()
while 1:
    clock.tick(6)
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

        
