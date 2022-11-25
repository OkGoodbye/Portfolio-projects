import pygame
from random import randint,uniform
pygame.init()
import time
screen = pygame.display.set_mode((500,750))
hsfont = pygame.font.SysFont("timesnewroman", 36)
sfont = pygame.font.SysFont("timesnewroman", 20)

def getside(rect,offset):
  
  if offset[0] == 1:
    if offset[2]>0:
      return (rect.bottom>500,1,-500)
    else:
      return (rect.top<0,1,500)
  else:
    if offset[2]>0:
      return (rect.right>500,0,-500)
    else:
      return (rect.left<0,0,500)
class Board:
  def __init__(self,dim,shuffle = True):
    self.dim = dim
    self.won = False
    self.state = [[x*dim+y+1 for x in range(dim)]for y in range(dim)]
    self.winstate = [[x*dim+y+1 for x in range(dim)]for y in range(dim)]
    self.colmods = (uniform(1,3.5),uniform(1,3.5),uniform(1,3.5))
    if shuffle:
      for i in range(2*dim**2):
        self.move((randint(0,self.dim-1),randint(0,self.dim-1)),randint(0,1),randint(-(dim-1),(dim-1)))
    
  def __str__(self):
    out = ""
    for item in self.state:
      for k in item:
        out += str(k)+" "*(3-len(str(k)))
      out+= "\n"
    return out
  def move(self,pos,axis,dir):
    if axis == 0:
      for i in range(abs(dir)):
        k = self.state[pos[0]]
        if dir<0:
          self.state[pos[0]] = [k[-1]]+k[:-1]
        else:
          self.state[pos[0]] = k[1:] +[k[0]]
    else:
      for i in range(abs(dir)):
        k = []
        for item in self.state:
          k.append(item[pos[1]])
        if dir<0:
          k = [k[-1]]+k[:-1]
        else:
          k = k[1:] +[k[0]]
        for x,item in enumerate(self.state):
          item[pos[1]] = k[x]
    if self.state == self.winstate:
      self.won = True
    else:
      self.won = False
  def draw(self,screen,offset = False):#offset = (axis,pos,move)
    board = pygame.Surface((500,500))
    for x,xitem in enumerate(self.state):
      for y,yitem in enumerate(xitem):
        boxsize = (500/self.dim,500/self.dim)
        im = pygame.Surface(boxsize)
        darkness = 255*yitem/self.dim**2
        tcol = 255
        if darkness>127.5:
          tcol = 0
        im.fill((darkness/self.colmods[0],darkness/self.colmods[1],darkness/self.colmods[2]))
        if self.dim<10:
          text = hsfont.render(str(yitem),True,(tcol,tcol,tcol))
        else:
          text = sfont.render(str(yitem),True,(tcol,tcol,tcol))
          
        im.blit(text,text.get_rect(center = (boxsize[0]/2,boxsize[1]/2)))
        blitPos = [x*boxsize[0],y*boxsize[1]]
        if offset != False:
          if offset[0] == 0 and offset[1][0] == y:
            blitPos[0]+= offset[2]
          elif offset[0] == 1 and offset[1][1] == x:
            blitPos[1]+=offset[2]
            
          wrapTest = getside(im.get_rect(topleft = blitPos),offset)
          if wrapTest[0]:
            wBlit = blitPos[::-1][::-1]
            
            wBlit[wrapTest[1]]+=wrapTest[2]
              
            board.blit(im,wBlit)
        board.blit(im,blitPos)
        
    screen.blit(board,(0,0))
def game(difficulty):
  b = Board(difficulty)
  done = False
  held = False
  hold_pos = (0,0)
  axis = None
  offset = (0,(0,0),0)
  c = pygame.time.Clock()
  taken = 0
  quit = hsfont.render("give up?",True,(0,0,0))
  quit = (quit,quit.get_rect(topright = (200,502)))
  while not done:
    c.tick(60)
    taken+=c.get_time()
    screen.fill((255,255,255))
    b.draw(screen,offset)
    time_surf = hsfont.render(str(round(taken/1000,2)),True,(0,0,0))
    screen.blit(time_surf,time_surf.get_rect(topleft = (350,502)))
    screen.blit(quit[0],quit[1])
    pygame.draw.circle(screen,(0,0,0),pygame.mouse.get_pos(),7,3)
    
    pygame.display.flip()
    if b.won:
      time.sleep(1.5)
      done = True
    k = pygame.mouse.get_pos()
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN:
        if k[1]<500:
          held = True
          hold_pos = pygame.mouse.get_pos()
          axis = None
        if quit[1].collidepoint(k):
          done = True
      elif event.type == pygame.MOUSEBUTTONUP:
        
          held = False
          offset = (0,(0,0),0)
          if axis!= None:
            m = (k[axis]-hold_pos[axis])
            if abs(m)>(500/b.dim)/2 :
            
              b.move((int(hold_pos[0]//(500/b.dim)),int(hold_pos[1]//(500/b.dim))),abs(1-axis),int(round(-m/(500/b.dim),0)))
            hold_pos = pygame.mouse.get_pos()
   
    if held:
      
      if abs(k[0]-hold_pos[0])>abs(k[1]-hold_pos[1]):
        axis = 0
      else:
        axis = 1
    if held and axis!=None:
      m = (k[axis]-hold_pos[axis])
      offset = (axis,(hold_pos[1]//(500/b.dim),hold_pos[0]//(500/b.dim)),m)
def load(imname):
  return pygame.transform.scale(pygame.image.load(imname),(300,150))
def ui():
  
  easy = load("easy.png")
  easy = (easy,easy.get_rect(center = (250,100)))
  hard = load("hard.png")
  hard = (hard,hard.get_rect(center = (250,250)))
  huge = load("huge.png")
  huge = (huge,huge.get_rect(center = (250,400)))
  while True:
    pygame.event.pump()
    
    
    
    screen.fill((255,255,255))
    
    screen.blit(easy[0],easy[1])
    screen.blit(hard[0],hard[1])
    screen.blit(huge[0],huge[1])
   
    pygame.draw.circle(screen,(0,0,0),pygame.mouse.get_pos(),7,3)
    
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN:
        
        mp = pygame.mouse.get_pos()
        pygame.draw.circle(screen,(0,0,0),mp,5,3)
        
        
          
        if easy[1].collidepoint(mp):
          game(3)
        elif hard[1].collidepoint(mp):
          game(5)
        elif huge[1].collidepoint(mp):
          game(10)
      
    
   
    pygame.display.flip()
ui()
