from bfs import Board
import pygame
def toiso(coord,width,height):
  a = (0.5*width*(coord[0]+9),0.25*height*(coord[0]+9))
  b = (-0.5*width*coord[1],0.25*height*coord[1])
  return(a[0]+b[0],a[1]+b[1])
def fiso(coord,width,height):
  a = 0.5*width
  b = -0.5*height
  c = 0.25*height
  d = c
  determ = 1/(a*d-b*c)
  l = (d*determ*(coord[0]-9),-c*determ*(coord[0]-9))
  r = (-b*determ*coord[1],a*determ*coord[1])
  return (l[0]+r[0]-0.5,l[1]+r[1])
def fix(point,board):
  iso_point = toiso((point[0]+1,point[1]),board.width,board.height)
  dim = fiso((board.width,board.height),board.width,board.height)
  return (iso_point[0]+dim[0],iso_point[1]+dim[1])
def lerp(p1,p2,t):
    return ((1-t)*p1[0]+t*p2[0],(1-t)*p1[1]+t*p2[1])
def calculate_pos(age,path,board):
    idx = int(age//1)
    if idx<(len(path)-1) and age>=0:
        points = path[idx],path[idx+1]
        pos = lerp(points[0],points[1],age%1)
        
        return pos
    else:
        return False
class Enemy:
  def __init__(self,speed,board,pos):
    self.age = 0
    self.pos = pos
    self.speed = speed
    self.board = board
    self.image = pygame.image.load("White Cylinder.png")
  def update(self):
    self.age += self.speed
    p = calculate_pos(self.age,self.board.found_path,self.board)
    if p:
      self.pos =  toiso((p[0]-0.5,p[1]-1),self.board.width,self.board.height)
  def draw(self,screen):
    screen.blit(self.image,self.pos)
def draw(board,screen,elist):
    black_sq = pygame.transform.scale(pygame.image.load("Black Square.png"),(board.width,board.height))
    white_sq = pygame.transform.scale(pygame.image.load("White Square.png"),(board.width,board.height))
    foreground = pygame.Surface((750,750),pygame.SRCALPHA)
    
    for x,xitem in enumerate(board.grid):
        for y,yitem in enumerate(xitem):
            pos = toiso((x,y),board.width,board.height)
            
            if (x+y)%2 == 0:
                im = black_sq
            else:
                im = white_sq
            screen.blit(im,pos)
            if (9-elist[0].pos[0]/board.width)**2+(9-elist[0].pos[1]/board.height)**2 < ((9-x)**2+(9-y)**2):
              elist[0].draw(foreground)
            if yitem == 1:
                foreground.blit(pygame.transform.scale(im,(board.width,board.height)),(pos[0],pos[1]-board.height/2))
            
    if len(board.found_path)>1:
      pygame.draw.lines(screen,(180,180,255),False,list(map(lambda point: fix(point,board),board.found_path)),width = 4)
      
    screen.blit(foreground,(0,0))
screen = pygame.display.set_mode((750,750))
board = Board((10,10),10)
board.grid[1][0] = 1
done = False
k = Enemy(.015,board,(0,0))
board.start_search((0,0),(9,9))
while not done:
  screen.fill((245,255,235))
  pygame.event.pump()
  
  draw(board,screen,[k])
 
  pygame.display.flip()
  
  k.update()
  for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONDOWN:
      mp = fiso(pygame.mouse.get_pos(),board.width,board.height)
      if 0<=(mp[0]-9)<board.dimensions[0] and 0<=mp[1]<board.dimensions[1]:
        board.grid[int(mp[0])-9][int(mp[1])] = pygame.mouse.get_pressed(3)[0]
        
        board.start_search((0,0),(9,9))
        
