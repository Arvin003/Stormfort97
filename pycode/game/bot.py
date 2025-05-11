import pygame
import random

from pycode.game.character import Character
from pycode.settings import settings

class Bot(pygame.sprite.Sprite):
    def init(self):
        super().init()
        self.image = bot_img
        self.rect = self.image.get_rect()
        self.rect.x = -self.rect.width
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.speed = 50

    def update(self):
        self.rect.x += self.speed # перемещение ботинка вправо
        if self.rect.left > WIDTH: # вышел за правую границу экрана
            self.kill() # удаляем бота из всех групп спрайтов

    @staticmethod
    def spawn_bot(group, max_bots=5):
        if len(group) < max_bots and random.random() < 0.02:
            group.add(Bot())
