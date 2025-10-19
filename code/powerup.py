import pygame, random

class HealthPack:
    def __init__(self, sprite_path=None):
        self.size = 20
        self.x = random.randint(0, 800 - self.size)
        self.y = random.randint(0, 600 - self.size)
        if sprite_path:
            self.sprite = pygame.image.load(sprite_path)
            self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))
        else:
            self.sprite = pygame.Surface((self.size, self.size))
            self.sprite.fill((0,255,0))

    def draw(self, win):
        win.blit(self.sprite, (self.x, self.y))

    def pickup(self, player):
        return pygame.Rect(self.x, self.y, self.size, self.size).colliderect(player.get_rect())
