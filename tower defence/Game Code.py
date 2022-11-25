import pygame
from bfs import Board
from random import randint
import math
pygame.init()
font = pygame.font.SysFont("gadugi",30)
def lerp(p1,p2,t):
    return ((1-t)*p1[0]+t*p2[0],(1-t)*p1[1]+t*p2[1])
print(int(not(int(not 3)))*3)
descriptions = {0:"delete",1:"Wall: blocks enemies",2:"Turret: shoots enemies",3:"Dragon: burns many enemies"}

images = {2:pygame.transform.scale(pygame.image.load("Turret.png"),(75,75))}
class Enemy:
   
    def __init__(self,delay,speed,damage,bh):
        self.pos = (-100,-100)
        self.health = 50
        self.speed = speed
        self.age = -delay*self.speed
        self.damage = damage
        bh.children.append(self)
        self.bh = bh
    def draw(self,screen):
        pygame.draw.circle(screen,(0,0,0),self.pos,13)
    def update(self):
        if self.health <=0:
            self.bh.children.remove(self)
class Bullet:
    def __init__(self,speed,start,enemy,tower):
        self.speed = speed
        self.start = start
        self.enemy = enemy
        self.tower = tower
        self.tower.bullets.append(self)
        self.age = 0
        self.pos = start
        
        self.image = pygame.image.load("Bullet.png")
    def draw(self,screen):
        
        rotim = pygame.transform.rotate(self.image,math.degrees(math.atan2(self.pos[0]-self.enemy.pos[0],self.pos[1]-self.enemy.pos[1])))
        screen.blit(rotim,rotim.get_rect(center = self.pos))
    def move(self):
        self.age += self.speed
        if self.age<=1:
            self.pos = lerp(self.start,self.enemy.pos,self.age)
        else:
            self.tower.bullets.remove(self)
            self.enemy.health -= 1
        
class Tower:
    def __init__(self,pos,range_rad,image,bh):
        self.pos = pos
        
        self.bh = bh
        self.pos = (self.pos[0]*bh.board.width+bh.board.width/2,self.pos[1]*bh.board.height+bh.board.height/2)
        self.bh.towers.append(self)
        self.range_rad = range_rad
        self.image = image
        self.angle = 0
    def update(self):
        self.target()
    def target(self):
        if len(self.bh.children)>0:
            closest = min(self.bh.children,key = lambda child:(self.pos[0]-child.pos[0])**2+(self.pos[1]-child.pos[1])**2)
            if ((self.pos[0]-closest.pos[0])**2+(self.pos[1]-closest.pos[1])**2)**0.5 <= self.range_rad:
                self.shoot(closest)
        
    def shoot(self,enemy):
        pass
    def draw(self,screen):
        screen.blit(self.image,self.image.get_recT(center = self.pos))
class Turret(Tower):
    def __init__(self,pos,range_rad,image,bh):
        Tower.__init__(self,pos,range_rad,image,bh)
        self.lookat = (self.pos[0],self.pos[1]+2)
        self.cooldown = 0
        self.maxcool = 10
        self.bullets = []
        self.barrel_length = self.image.get_width()/2
    def shoot(self,enemy):
        self.lookat = enemy.pos
        if self.cooldown<=0:
            shootpos= (self.pos[0]+math.sin(self.angle)*self.barrel_length,self.pos[1]+math.cos(self.angle)*self.barrel_length)
            Bullet(0.2,self.pos,enemy,self)
            self.cooldown = self.maxcool
        else:
            self.cooldown -= 1
             
    def update(self):
        self.target()
        for item in self.bullets:
            item.move()
    def draw(self,screen):
        self.angle = math.atan2(self.pos[0]-self.lookat[0],self.pos[1]-self.lookat[1])+math.pi/2
        rotim = pygame.transform.rotate(self.image,math.degrees(self.angle))
        screen.blit(rotim,rotim.get_rect(center = self.pos))
        for item in self.bullets:
            item.draw(screen)
def calculate_pos(age,path,board):
    idx = int(age//1)
    if idx<(len(path)-1) and age>=0:
        points = path[idx],path[idx+1]
        pos = lerp(points[0],points[1],age%1)
        pos = (pos[0]*board.width+board.width/2,pos[1]*board.height+board.height/2)
        return pos
    else:
        return False
class boardHandler:
    def __init__(self,board):
        self.board= board
        self.children = []
        self.towers = []
    def move_children(self):
        for enemy in self.children:
            enemy.age+=enemy.speed
            
            wfp = self.board.found_path+[(END[0]+1,END[1])]
            p = calculate_pos(enemy.age,wfp,self.board)
            if p:
                enemy.pos = p
            enemy.update()
        for tower in self.towers:
            tower.update()
    def draw(self,screen):
        self.board.draw(screen)
        for item in self.children+self.towers:
            item.draw(screen)
        
b = Board((18,18),10)
for x, xitem in enumerate(b.grid):
    for y,yitem in enumerate(xitem):
        if x == 0 or y == 0 or x==17 or y == 17:
            b.grid[x][y] = -1
START = (0,randint(1,16))
END = (17,randint(1,16))
b.grid[START[0]][START[1]] = 0
b.grid[END[0]][END[1]] = 0
board_handler = boardHandler(b)

clock = pygame.time.Clock()
screen = pygame.display.set_mode((750,750))
b.start_search(START,END)
def show_ui(board,screen):
    health = font.render(str(board.health),True,(45,255,25))
    screen.blit(health,health.get_rect(topright = (740,0)))
towers = {2:Turret}
def placement(board):
    done = False
    selection = 1
    showcool = 0
    showdesc = None
    t_list = []
    while not done:
        if showcool > 0:
            showcool -= 1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            mp = pygame.mouse.get_pos()
            pos = (int(mp[0]//board.width),int(mp[1]//board.height))
            if board.grid[pos[0]][pos[1]] ==0 or (selection == 0 and board.grid[pos[0]][pos[1]]>0):
                board.grid[pos[0]][pos[1]] = selection
                if selection == 0:
                    for item in t_list:
                        if item[1] == pos:
                            t_list.remove(item)
                board.start_search(START,END)
                if len(board.found_path) == 0:
                    board.grid[pos[0]][pos[1]] = 0
                    board.start_search(START,END)
                elif selection > 1:
                    t_list.append((selection,pos,700))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mp = pygame.mouse.get_pos()
                pos = (int(mp[0]//board.width),int(mp[1]//board.height))
                if board.grid[pos[0]][pos[1]] ==0 or (selection == 0 and board.grid[pos[0]][pos[1]]>0):
                    board.grid[pos[0]][pos[1]] = selection
                    board.start_search(START,END)
                    if len(board.found_path) == 0:
                        board.grid[pos[0]][pos[1]] = selection
                        board.start_search(START,END)
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE:
                    done = True
                elif event.key == pygame.K_0:
                    showcool = 90
                    showdesc = "Delete"
                    selection = 0
                elif event.key == pygame.K_1:
                    showcool = 90
                    showdesc = "Wall: blocks enemies"
                    selection = 1
                elif event.key == pygame.K_2:
                    showcool = 90
                    showdesc = "Turret: shoots enemies"
                    selection = 2
                elif event.key == pygame.K_3:
                    showcool = 90
                    showdesc = "Dragon: burns many enemies"
                    selection = 3
        board.draw(screen)
        show_ui(board,screen)
        if showcool>0:
            text = font.render(showdesc,True,(255,0,0))
            
            screen.blit(text,text.get_rect(center = (375,375)))
        for item in t_list:
            screen.blit(images[item[0]],images[item[0]].get_rect(center = (item[1][0]*board.width+board.width/2,item[1][1]*board.height+board.height/2)))
        pygame.display.flip()
    return t_list
def wave(board,e_list,t_list):
    
    bh = boardHandler(board)
    for item in t_list:
        towers[item[0]](item[1],item[2],images[item[0]],bh)#pos,range_rad,image,bh
    
    for item in e_list:
        Enemy(item[0],item[1],item[2],bh)
    c = pygame.time.Clock()
    done = False
    while not done:
        c.tick(30)
        bh.move_children()
        bh.draw(screen)
       
        show_ui(board,screen)
        pygame.display.flip()
        if len(bh.children)==0:
            done = True

wave(b,[[20*x,0.15,0.2] for x in range(3)],placement(b))
