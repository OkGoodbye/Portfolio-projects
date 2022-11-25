import pygame
import time
test = pygame.image.load("hbd.png")
screen = pygame.display.set_mode((500,500))
def draw_slice(dfs,dx):
    texture_slice = int(dfs%test.get_width())
    draw_image = pygame.Surface((5,test.get_height()))
    draw_image.blit(test,(-texture_slice,0))
    draw_image = pygame.transform.scale(draw_image,(5,500))
    
    screen.blit(draw_image,(dx,0))
    pygame.display.flip()
    time.sleep(0.2)
for i in range(100):
    pygame.event.pump()
    draw_slice(i*5,i*5)
