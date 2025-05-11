import pygame.sprite
from pygame import Rect

from pycode.settings import settings


class Bullet(pygame.sprite.Sprite):
    def __init__(self, frames, direct="left", pos=(0, 0), size=(48, 16)):
        super().__init__()
        self.size = self.width, self.height = size
        self.frames = frames
        self.image = frames[0]
        self.rect = Rect(*pos, *self.size)
        self.image = pygame.transform.scale(self.image, self.size)
        self.mask = pygame.mask.from_surface(self.image)

        self.time_start = settings.fps // 7.5
        self.time_end = settings.fps // 10

        self.time = 0
        self.speed_x = 400 * settings.k_width / settings.fps
        self.direct = direct
        if self.direct == 'left':
            self.speed_x = -self.speed_x

        self.damage = 1  # Урон пули

        self.is_destroy = False
        self.is_kill = False

    def update(self):
        if self.is_kill:
            return

        if not self.is_destroy:
            self.rect.x += self.speed_x

        self.time += 1

        if 0 <= self.time_start <= self.time:
            self.time = 0
            self.time_start = -1
            self.image = self.frames[1]

        if self.is_destroy:
            if self.time >= self.time_end:
                self.is_kill = True
                self.kill()

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def destroy_bullet(self):
        self.image = self.frames[2]
        self.is_destroy = True
        self.time = 0

    class Player:
        def __init__(self):
            # ...
            self.shoot_delay = 200  # миллисекунд между выстрелами (напр. 0.2 сек)
            self.last_shot_time = pygame.time.get_ticks()  # время последнего выстрела

        def shoot(self):
            now = pygame.time.get_ticks()
            if now - self.last_shot_time >= self.shoot_delay:
                self.last_shot_time = now
                bullet = Bullet(...)  # создать пулю
                self.bullets_group.add(bullet)
