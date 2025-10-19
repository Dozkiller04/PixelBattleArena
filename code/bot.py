import pygame, random
from bullets import Bullet

class Bot:
    def __init__(self, x, y, sprite_path=None):
        self.x = x
        self.y = y
        self.size = 40
        self.health = 5
        self.bullets = []
        if sprite_path:
            self.sprite = pygame.image.load(sprite_path)
            self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))
        else:
            self.sprite = pygame.Surface((self.size, self.size))
            self.sprite.fill((255,0,0))

    def draw(self, win):
        win.blit(self.sprite, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def move(self, walls, players):
        # Move randomly but towards players if close
        if random.randint(0,1):
            dx = random.choice([-2,0,2])
            dy = random.choice([-2,0,2])
        else:
            # Track nearest player
            target = min(players, key=lambda p: (self.x-p.x)**2 + (self.y-p.y)**2)
            dx = 2 if target.x>self.x else -2 if target.x<self.x else 0
            dy = 2 if target.y>self.y else -2 if target.y<self.y else 0

        new_rect = pygame.Rect(self.x+dx, self.y+dy, self.size, self.size)
        if not any(new_rect.colliderect(w) for w in walls):
            self.x += dx
            self.y += dy

        # Shoot at nearest player occasionally
        if random.randint(0,100)<3:
            target = min(players, key=lambda p: (self.x-p.x)**2 + (self.y-p.y)**2)
            dx = target.x - self.x
            dy = target.y - self.y
            if abs(dx) > abs(dy):
                direction = "right" if dx>0 else "left"
            else:
                direction = "down" if dy>0 else "up"
            self.bullets.append(Bullet(self.x+self.size//2, self.y+self.size//2, direction))
