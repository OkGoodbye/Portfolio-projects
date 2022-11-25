import pygame
import math

surf = pygame.Surface((1280,720))
surf.fill((255,255,255))
pixel = pygame.Surface((1,1))
CENTER = (-0.3888,0.677777778)
RANGE = (1,1)
ITERATIONS = 200
def shrink(point):
    xr = RANGE[0]
    yr = RANGE[1]
    x = point[0]*(xr/720)+CENTER[0]/2
    y = point[1]*(yr/720)+CENTER[1]/2
    return (x,y)



for x in range(1280):
    for y in range(720):
        z = (0,0)
        point = shrink((x,y))
        escape_time = 0
        for i in range(ITERATIONS):
            z = (z[0]+point[0],z[1]+point[1])
            z = (z[0]**2-z[1]**2,2*z[0]*z[1])
            escape_time +=1
            if math.hypot(z[0],z[1])>2:
                break
        if escape_time == ITERATIONS:
            pixel.fill((0,0,0))
            surf.blit(pixel,(x,y))
        else:
            pixel.fill((math.log(escape_time+1,10)*68.4,255-math.log(escape_time,10)*68.4,0))
            surf.blit(pixel,(x,y))
    print(x/1280)
pygame.image.save(surf,"mandlebrot.png")
screen = pygame.display.set_mode((1980,720))
while 1:
    pygame.event.pump()
    #print(shrink(pygame.mouse.get_pos()))
    screen.blit(surf,(0,0))
    pygame.display.flip()
    
