import pygame

class Bullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.size = 8
        self.speed = 6
        self.color = (255,255,0)
        self.direction = direction

    def move(self):
        if self.direction=="up":
            self.y -= self.speed
        elif self.direction=="down":
            self.y += self.speed
        elif self.direction=="left":
            self.x -= self.speed
        elif self.direction=="right":
            self.x += self.speed

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))

    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)
