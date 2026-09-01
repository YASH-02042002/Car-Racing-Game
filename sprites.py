import pygame
import random
from setting import *
class PlayerCar(pygame.sprite.Sprite):
    def __init__(self, images_path):
        super().__init__()
        try:
            self.image = pygame.image.load(images_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 80))
            # self.image.set_colorkey((255, 255, 255))
            self.mask = pygame.mask.from_surface(self.image)
        except:
            self.image = pygame.Surface((50, 80))
            self.image.fill(GREEN)

        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20

    def update(self):
        """Handle movement logic and boundaries"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x  += PLAYER_SPEED

        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += PLAYER_SPEED

class EnemyCar(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.speed = speed
        enemy_images = [
            "assets/images/enemy2.png",
            "assets/images/enemy4.png",
            "assets/images/enemy3.png"
        ]
        chosen_image = random.choice(enemy_images)

        try:
            self.image = pygame.image.load(chosen_image).convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 80))
            # self.image.set_colorkey((255, 255, 255))
            self.mask = pygame.mask.from_surface(self.image)
        except:
            self.image = pygame.Surface((50, 80))
            self.image.fill(RED)
            self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(150, SCREEN_WIDTH - 150 - self.rect.width)
        self.rect.y = random.randint(-100, -40)

    def update(self):
        """Move the enemy down the screen."""
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.speed = speed

        try:
            self.image = pygame.image.load("assets/image.coin.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 40))
            self.mask = pygame.mask.from_surface(self.image)
        except:
            self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 215, 0), (20, 20), 20)
            self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(150, SCREEN_WIDTH - 150 - self.rect.width)
        self.rect.y = random.randint(-100, -40)
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class FloatingText(pygame.sprite.Sprite):
    def __init__(self, text, x, y):
        super().__init__()
        font = pygame.font.SysFont("Arial", 20, bold=True)
        self.image = font.render(text, True, (255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.timer = 30

    def update(self):
        self.rect.y -= 3
        self.timer -= 1
        if self.timer <= 0:
            self.kill()