import pygame

from pycode.game.character import Character
from pycode.settings import settings


class Enemy(Character):
    def __init__(self, registry, pos):
        super().__init__(registry, pos, size=(256, 80), data_textures=registry.enemy_easy_texture)
        self.speed_y = 100 * settings.k_height
        self.speed_x = 40 * settings.k_width
        self.direct = 'right'
        self.bullet_damage = 1
        self.bullet_speed = 400 * settings.k_width / settings.fps
        self.speed_attack = settings.fps * 3
        self.health = 3

    def update(self):
        super().update()

        self.ai_controller()

        # Противник уничтожается сам если уходит
        if self.rect.x >= settings.width + 2:
            self.health = 0

    def ai_controller(self):
        """Искусственный интеллект"""
        self.command['right'] = True
        self.command['space'] = True
