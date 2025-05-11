import pygame

from pycode.game.character import Character
from pycode.settings import settings


class Player(Character):
    def __init__(self, registry, pos):
        super().__init__(registry, pos, size=(256, 80), data_textures=registry.player_texture)
        self.image_health = pygame.transform.scale(registry.player_texture['health'],
                                                   (64 * settings.k_width, 64 * settings.k_height))
        self.speed_y = 200 * settings.k_height
        self.direct = 'left'
        self.health = 3

    def update(self):
        super().update()

        # Не даем выйти за границы экрана (вправо/влево)
        if self.rect.x + self.width >= settings.width:
            self.rect.x = settings.width - self.width
        if self.rect.x < 1:
            self.rect.x = 1

        # Не даем выйти за границы экрана (вниз/вверх)
        if self.rect.y + self.height >= settings.height:
            self.rect.y = settings.height - self.height
        if self.rect.y < 1:
            self.rect.y = 1

    def controller(self, keys_pressed):
        if keys_pressed[pygame.K_w]:
            self.command['up'] = True
        else:
            self.command['up'] = False

        if keys_pressed[pygame.K_s]:
            self.command['down'] = True
        else:
            self.command['down'] = False

        if keys_pressed[pygame.K_a]:
            self.command['left'] = True
        else:
            self.command['left'] = False

        if keys_pressed[pygame.K_d]:
            self.command['right'] = True
        else:
            self.command['right'] = False

        if keys_pressed[pygame.K_SPACE]:
            self.command['space'] = True
        else:
            self.command['space'] = False
