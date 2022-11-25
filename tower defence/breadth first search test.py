import pygame
from collections import deque
from random import randint
#directions = [(-1,0),(0,-1),(1,0),(0,1),(1,1),(-1,-1),(-1,1),(1,-1)]#with diagonals
directions = [(-1,0),(0,-1),(1,0),(0,1)]#without diagonals
colours = {0:(100,100,79),1:(2.5,25,250),2:(20,20,20)}

class Board:
    def __init__(self,dimensions):
        self.grid = [[0 for x in range(dimensions[0])]for y in range(dimensions[1])]
        self.dimensions = dimensions
        self.width = 750/self.dimensions[1]
        self.height = 750/self.dimensions[0]
        self.searching = False
        self.all_paths = deque()
        self.found_path = []
        self.seen_points =[]
    def get_points(self,point):
        out = []
        for item in directions:
            trial = (point[0]+item[0],point[1]+item[1])
            if 0<=trial[1]<self.dimensions[0] and 0<=trial[0]<self.dimensions[1]:
                if self.grid[trial[0]][trial[1]] == 0:
                    out.append(trial)
        return out
    
    
    def search(self,goal):
        if len(self.all_paths)==0:
            self.searching = False
        else:
            path = self.all_paths.popleft()
        
            point = path[-1]
            
            
            
            if self.grid[point[0]][point[1]]!=0:
                self.searching = False
            if point == goal:
                self.found_path = path+[point]
                self.searching = False
                
            else:
                
                for newDestination in self.get_points(point):
                    
                    if newDestination not in self.seen_points:
                        self.seen_points.append(newDestination)
                        self.all_paths.append(path+[newDestination])
                        
    def start_search(self,start,goal):
        self.searching = True
        self.found_path = []
        self.seen_points =[]
        self.all_paths = deque()
        self.all_paths.append([start])
        for x in range(sum(self.grid,[]).count(0)+1):
            
            self.search(goal)
            if not self.searching:
                break
            
        
       
        return self.found_path
    def __str__(self):
        out = ""
        for item in self.grid:
            out+=" ".join(list(map(str,item)))+"\n"
        return out
    def fix_path(self):
        out_path = []
        for item in self.found_path:
            out_path.append((item[0]*self.width+self.width/2,item[1]*self.height+self.height/2))
        return out_path
    def draw(self,screen):
        for x,xitem in enumerate(self.grid):
            for y,yitem in enumerate(xitem):
                top = y*self.height
                left = x*self.width
                pygame.draw.rect(screen,colours[yitem],pygame.Rect(left,top,left+self.width,top+self.height))
        if len(self.found_path)>1:
            
            pygame.draw.lines(screen,(0,0,0),False,self.fix_path(),width = 4)
board = Board((30,30))
       
screen = pygame.display.set_mode((750,750))
START = (0,0)
END = (29,29)

for i in range(0):
    index = randint(0,board.dimensions[1]-1),randint(0,board.dimensions[0]-1)

    board.grid[index[0]][index[1]] = 2
    
    board.start_search(START,END)
    if board.found_path ==[]:
       
       board.grid[index[0]][index[1]] = 0
   

while 1:
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
                    
            mp = pygame.mouse.get_pos()
            idx = (int(mp[0]//board.width),int(mp[1]//board.height))
            value = board.grid[idx[0]][idx[1]]
            if value<2:
                board.grid[idx[0]][idx[1]] = int(not(value))
            board.start_search((0,0),END)
    k = pygame.key.get_pressed()
    if k[pygame.K_q]:
        mp = pygame.mouse.get_pos()
        idx = (int(mp[0]//board.width),int(mp[1]//board.height))
        value = board.grid[idx[0]][idx[1]]
        if value<2:
            board.grid[idx[0]][idx[1]] = 1
        board.start_search((0,0),END)
    board.draw(screen)
    pygame.display.flip()
        
