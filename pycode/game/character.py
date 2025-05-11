import pygame.transform
from pygame import Surface, Color, Rect

from pycode.settings import settings


class Character(pygame.sprite.Sprite):
    def __init__(self, registry, pos, size=(64, 64), data_textures=None):
        super().__init__()
        self.registry = registry
        self.width = round(size[0] * settings.k_width)
        self.height = round(size[1] * settings.k_height)
        self.size = self.width, self.height

        self.image = Surface(self.size)
        self.image.fill(Color(255, 0, 0))
        self.rect = Rect(*pos, *self.size)

        self.data_textures = data_textures
        if self.data_textures:
            self.image = pygame.transform.scale(self.data_textures['orig'], self.size)
            self.mask = pygame.mask.from_surface(self.image)

        self.speed_x = 100 * settings.k_width
        self.speed_y = 100 * settings.k_height
        self.bullet_damage = 1
        self.bullet_speed = 400 * settings.k_width / settings.fps
        self.speed_attack = settings.fps // 2
        self.speed_attack_i = 0
        self.x_vel = 0
        self.y_vel = 0

        self.command = {
            'up': False,
            'down': False,
            'left': False,
            'right': False,
            'space': False
        }
        self.direct = 'right'

        self.bullet = None
        self.health = 1

        self.bullet_damage = 1
        self.bullet_speed = 1

    def get_damage(self, damage):
        self.health -= damage

    def set_pose(self, x, y):
        self.rect.x, self.rect.y = x, y

    def update(self):
        if self.speed_attack_i > 0:
            self.speed_attack_i += 1
            if self.speed_attack_i >= self.speed_attack:
                self.speed_attack_i = 0

        if self.command['space'] and self.speed_attack_i == 0:
            self.speed_attack_i += 1
            self.bullet = {
                'direct': self.direct,
                'frames': self.data_textures['fire'],
                'pos': (self.rect.x, self.rect.y),
                'damage': self.bullet_damage,
                'speed': self.bullet_speed,
            }

        if self.command['up']:
            self.y_vel = -self.speed_y / settings.fps
        elif self.command['down']:
            self.y_vel = self.speed_y / settings.fps
        else:
            self.y_vel = 0

        if self.command['left']:
            self.x_vel = -self.speed_x / settings.fps
        elif self.command['right']:
            self.x_vel = self.speed_x / settings.fps
        else:
            self.x_vel = 0

        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
