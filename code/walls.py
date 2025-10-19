import pygame

walls = [
    pygame.Rect(0,0,800,10),     # top
    pygame.Rect(0,590,800,10),   # bottom
    pygame.Rect(0,0,10,600),     # left
    pygame.Rect(790,0,10,600),   # right
    pygame.Rect(200,200,400,10),
    pygame.Rect(200,400,400,10)
]

def draw_walls(win):
    for w in walls:
        pygame.draw.rect(win, (100,100,100), w)
