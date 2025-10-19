# main.py
import pygame
import random
import os
from player import Player
from bot import Bot
from bullets import Bullet
from powerup import HealthPack
from walls import draw_walls, walls
from save_utils import load_profile, save_profile

# ---------------- Pygame init ----------------
pygame.init()
WIN_W, WIN_H = 800, 600
win = pygame.display.set_mode((WIN_W, WIN_H))
pygame.display.set_caption("Pixel Battle Arena")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# ---------------- Paths ----------------
BASE = os.path.dirname(__file__)
ASSETS_IMAGES = os.path.join(BASE, "..", "assets", "images")
ASSETS_SOUNDS = os.path.join(BASE, "..", "assets", "sounds")

# ---------------- Audio (safe load) ----------------
def safe_music_load(path):
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except Exception:
        # music missing or mixer issue - ignore
        pass

def play_sound_file(filename):
    path = os.path.join(ASSETS_SOUNDS, filename)
    if os.path.exists(path):
        try:
            s = pygame.mixer.Sound(path)
            s.play()
        except Exception:
            pass

safe_music_load(os.path.join(ASSETS_SOUNDS, "bg_music.mp3"))

# ---------------- Profile ----------------
profile = load_profile()
high_score = profile.get("high_score", 0)

# ---------------- Controls ----------------
controls_p1 = {
    "up": pygame.K_w, "down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d,
    "shoot_up": pygame.K_t, "shoot_down": pygame.K_g, "shoot_left": pygame.K_f, "shoot_right": pygame.K_h
}
controls_p2 = {
    "up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT,
    "shoot_up": pygame.K_i, "shoot_down": pygame.K_k, "shoot_left": pygame.K_j, "shoot_right": pygame.K_l
}

# ---------------- Create players & bots ----------------
p1_img = os.path.join(ASSETS_IMAGES, "player1.png")
p2_img = os.path.join(ASSETS_IMAGES, "player2.png")
bot_img = os.path.join(ASSETS_IMAGES, "bot.png")
hp_img = os.path.join(ASSETS_IMAGES, "healthpack.png")

p1 = Player(80, 80, controls_p1, p1_img)
p2 = Player(720, 80, controls_p2, p2_img)
players = [p1, p2]

bots = [
    Bot(600, 350, bot_img),
    Bot(200, 400, bot_img)
]

# ---------------- Game state ----------------
player_bullets = []   # bullets fired by players
healthpack = None
healthpack_timer = 0
score = 0
level = 1

# ---------------- Helper ----------------
def safe_play(name):
    # wrapper to play sound from ASSETS_SOUNDS
    play_sound_file(name)

def remove_if_exists(container, item):
    try:
        container.remove(item)
    except ValueError:
        pass

# ---------------- Main loop ----------------
run = True
while run:
    clock.tick(60)
    win.fill((30, 30, 40))  # simple background

    # draw walls (solid)
    draw_walls(win)

    # spawn healthpack occasionally
    if healthpack is None:
        healthpack_timer += 1
        if healthpack_timer > random.randint(300, 600):
            # HealthPack expects optional sprite path; if missing it creates fallback surface
            if os.path.exists(hp_img):
                healthpack = HealthPack(hp_img)
            else:
                healthpack = HealthPack(None)
            healthpack_timer = 0
    else:
        healthpack.draw(win)

    # event handling (shooting and quit)
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            # player shooting (iterate players in same order)
            for p, controls in zip(players, [controls_p1, controls_p2]):
                if event.key == controls["shoot_up"]:
                    player_bullets.append(Bullet(p.x + p.size // 2, p.y, "up"))
                    safe_play("shoot.wav")
                if event.key == controls["shoot_down"]:
                    player_bullets.append(Bullet(p.x + p.size // 2, p.y + p.size, "down"))
                    safe_play("shoot.wav")
                if event.key == controls["shoot_left"]:
                    player_bullets.append(Bullet(p.x, p.y + p.size // 2, "left"))
                    safe_play("shoot.wav")
                if event.key == controls["shoot_right"]:
                    player_bullets.append(Bullet(p.x + p.size, p.y + p.size // 2, "right"))
                    safe_play("shoot.wav")

    # update + draw players
    for p in players:
        p.move(keys, walls)
        p.draw(win)

    # update bots: movement, bot bullets, collisions vs players
    for b in bots[:]:
        b.move(walls, players)
        # update bot bullets
        for bl in b.bullets[:]:
            bl.move()
            bl.draw(win)
            # collision with players
            for p in players:
                if bl.rect().colliderect(p.get_rect()):
                    p.health -= 1
                    safe_play("hit.wav")
                    remove_if_exists(b.bullets, bl)
            # remove bullet if offscreen
            if bl.x < -50 or bl.x > WIN_W + 50 or bl.y < -50 or bl.y > WIN_H + 50:
                remove_if_exists(b.bullets, bl)
        b.draw(win)

    # update player bullets: movement, collision with bots
    for bl in player_bullets[:]:
        bl.move()
        bl.draw(win)
        hit_any_bot = False
        for b in bots[:]:
            if bl.rect().colliderect(b.get_rect()):
                b.health -= 1
                safe_play("hit.wav")
                hit_any_bot = True
                remove_if_exists(player_bullets, bl)
                if b.health <= 0:
                    remove_if_exists(bots, b)
                    score += 1
                    safe_play("levelup.wav")
                    # spawn replacement bot
                    bots.append(Bot(random.randint(50, WIN_W-90), random.randint(50, WIN_H-90), bot_img if os.path.exists(bot_img) else None))
                break
        # remove offscreen bullets if not already removed
        if bl in player_bullets and (bl.x < -50 or bl.x > WIN_W + 50 or bl.y < -50 or bl.y > WIN_H + 50):
            remove_if_exists(player_bullets, bl)

    # healthpack pickup
    if healthpack is not None:
        for p in players:
            if healthpack.pickup(p):
                p.heal(2)
                safe_play("pickup.wav")
                healthpack = None
                break

    # draw UI
    win.blit(font.render(f"Score: {score}", True, (255, 255, 0)), (10, 10))
    win.blit(font.render(f"Level: {level}", True, (0, 255, 0)), (10, 30))
    win.blit(font.render(f"P1 HP: {p1.health}", True, (200, 200, 200)), (10, 50))
    win.blit(font.render(f"P2 HP: {p2.health}", True, (200, 200, 200)), (10, 70))
    win.blit(font.render(f"High Score: {high_score}", True, (255, 160, 0)), (10, 90))

    pygame.display.update()

    # end conditions
    if all(p.health <= 0 for p in players) or keys[pygame.K_ESCAPE]:
        run = False

# Save high score if beaten
if score > high_score:
    profile["high_score"] = score
    save_profile(profile)
    print("New high score saved:", score)

pygame.quit()
