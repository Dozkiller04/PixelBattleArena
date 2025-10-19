import pygame

class Player:
    def __init__(self, x, y, controls, sprite_path=None):
        self.x = x
        self.y = y
        self.size = 40
        self.health = 10
        self.controls = controls
        # Load player image
        if sprite_path:
            self.sprite = pygame.image.load(sprite_path)
            self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))
        else:
            self.sprite = pygame.Surface((self.size, self.size))
            self.sprite.fill((0,0,255))

    def draw(self, win):
        win.blit(self.sprite, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def move(self, keys, walls):
        dx = dy = 0
        if keys[self.controls['up']]:
            dy = -3
        if keys[self.controls['down']]:
            dy = 3
        if keys[self.controls['left']]:
            dx = -3
        if keys[self.controls['right']]:
            dx = 3

        # Check wall collisions
        new_rect = pygame.Rect(self.x+dx, self.y+dy, self.size, self.size)
        if not any(new_rect.colliderect(w) for w in walls):
            self.x += dx
            self.y += dy

    def heal(self, amount):
        self.health += amount
        if self.health > 10:
            self.health = 10
