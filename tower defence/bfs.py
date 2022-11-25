import pygame
from collections import deque
from random import randint
#directions = [(-1,0),(0,-1),(1,0),(0,1),(1,1),(-1,-1),(-1,1),(1,-1)]#with diagonals
directions = [(-1,0),(0,-1),(1,0),(0,1)]#without diagonals
colours = {-1:(0,0,0),0:(150,150,150),1:(200,200,45),2:(150,150,150),3:(150,150,150)}

class Board:
    def __init__(self,dimensions,health):
        self.grid = [[0 for x in range(dimensions[0])]for y in range(dimensions[1])]
        self.dimensions = dimensions
        self.width = 750/self.dimensions[1]
        self.height = 750/self.dimensions[0]
        self.searching = False
        self.all_paths = deque()
        self.found_path = []
        self.seen_points =[]
        self.health = health
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
                self.found_path = path
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
            pass
            #pygame.draw.lines(screen,(0,0,0),False,self.fix_path(),width = 1)
