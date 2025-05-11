import random

import pygame

from pycode.game.bullet import Bullet
from pycode.game.enemy import Enemy
from pycode.game.player import Player
from pycode.registry import Registry
from pycode.settings import settings
from pycode.ui.background_animated_ui import BackgroundAnimatedUi
from pycode.ui.button import Button
from pycode.ui.label import Label
from pycode.windows.loading_window import LoadingWindow
from pycode.windows.result_window import ResultWindow


class GameWindow:
    """Класс окна игры"""

    def __init__(self, screen, level):
        """Конструктор (инициализация свойств)"""
        self.running = True
        self.registry = None
        self.screen = screen
        self.background = None
        self.clock = None
        self.level = level

        self.statistic = {
            'is_won': False,
            'is_lose': False,
            'time': 0,
            'enemy_kills': 0
        }
        self.labels = dict()
        self.buttons = dict()
        self.switches_buttons = dict()
        self.bullets_player = set()
        self.bullets_enemy = set()
        self.enemies = set()

        self.player = None

    async def load(self):
        """Загрузка ресурсов"""
        # Создание ресурсов
        self.registry = Registry()
        self.registry.load_displays()

        # Загрузка ресурсов панели окна
        self.registry.load_icon()
        pygame.display.set_caption("Игра")
        pygame.display.set_icon(self.registry.icon)

        # Загрузка шрифтов
        self.registry.load_fonts()

        # Загрузка звуков и музыки
        self.registry.load_music()
        self.registry.load_sounds()
        self.registry.music['game'].play()

        # Загрузка изображений кнопок
        self.registry.load_buttons_images()

        # Загрузка изображений главного меню
        self.registry.load_game_background()
        self.background = BackgroundAnimatedUi(self.registry.game_background, settings.fps // 7.5)

        # Загрузка изображений корабля
        self.registry.load_player_texture()

        # Установка текста
        if settings.show_fps:
            label = Label(str(settings.fps), self.registry.fonts['main']['small'], True)
            label.create()
            label.set_pos(0, 0)
            self.labels['fps'] = label

        # Установка кнопок
        button = Button("Меню", self.registry.fonts['main']['normal'], True)
        button.set_size(settings.width * 0.2, settings.height * 0.1)
        button.set_images(normal=self.registry.buttons['standard']['normal'],
                          hover=self.registry.buttons['standard']['hover'],
                          pressed=self.registry.buttons['standard']['pressed'])
        button.create()
        button.set_pos(settings.width - (settings.width * 0.2), 0)
        button.set_action(self.back)
        button.set_sound_click(self.registry.sounds['menu']['click'])
        self.buttons['back'] = button

        # Игровые объекты
        self.player = Player(self.registry, (settings.width // 2, settings.height // 2))
        self.player.set_pose(settings.width - self.player.width, settings.height // 2 - (self.player.height // 2))

        self.bullets_player = set()
        self.bullets_enemy = set()
        self.enemies = set()

        # Предварительная настройка
        self.clock = pygame.time.Clock()
        self.running = True

    async def run(self):
        """Запуск окна"""
        pygame.init()
        settings.load()
        await LoadingWindow(self.screen, delay_after=0.5).show(
            self.load(),
            "Загрузка"
        )
        self.running = True
        await self.game()

    async def game(self):
        """Логика окна"""

        time_i = 0
        # Игровой цикл
        while self.running:
            time_i += 1
            await self.narrator_controller(time_i)

            # Получаем позицию мыши
            mouse_pos = pygame.mouse.get_pos()
            # Получаем состояние всех кнопок мыши
            mouse_buttons = pygame.mouse.get_pressed()
            # Получаем все нажатые клавиши
            keys_pressed = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            # Обработка логики
            destroy_bullet_player = set()
            destroy_bullet_enemy = set()
            destroy_enemies = set()

            self.background.update()

            for name, button in self.buttons.items():
                await button.update(mouse_pos, mouse_buttons)

            for name, switch in self.switches_buttons.items():
                await switch.update(mouse_pos, mouse_buttons)

            if settings.show_fps and 'fps' in self.labels:
                self.labels['fps'].set_text(str(int(self.clock.get_fps())))
                self.labels['fps'].create()

            self.player.controller(keys_pressed)
            self.player.update()
            if self.player.bullet:
                frames = self.player.bullet['frames']
                direct = self.player.bullet['direct']
                pos = self.player.bullet['pos']
                self.player.bullet = None
                self.bullets_player.add(Bullet(frames, direct, pos))

            for enemy in self.enemies:
                enemy.update()
                if enemy.health <= 0:
                    destroy_enemies.add(enemy)

                if enemy.bullet:
                    frames = enemy.bullet['frames']
                    direct = enemy.bullet['direct']
                    pos = enemy.bullet['pos']
                    enemy.bullet = None
                    self.bullets_enemy.add(Bullet(frames, direct, pos))

            # Обработка пуль
            for bullet in self.bullets_player:
                bullet.update()
                for enemy in self.enemies:
                    if pygame.sprite.collide_mask(enemy, bullet) and not bullet.is_destroy:
                        enemy.get_damage(bullet.damage)
                        if enemy.health <= 0:
                            self.statistic['enemy_kills'] += 1
                            destroy_enemies.add(enemy)
                        bullet.destroy_bullet()
                if bullet.is_kill:
                    destroy_bullet_player.add(bullet)

            for bullet in self.bullets_enemy:
                bullet.update()
                if pygame.sprite.collide_mask(self.player, bullet) and not bullet.is_destroy:
                    self.player.get_damage(bullet.damage)
                    bullet.destroy_bullet()
                if bullet.is_kill:
                    destroy_bullet_player.add(bullet)

            # Удаление пуль игрока
            for bullet in destroy_bullet_player:
                self.bullets_player.discard(bullet)

            # Удаление пуль врага
            for bullet in destroy_bullet_enemy:
                self.bullets_enemy.discard(bullet)

            # Удаление врагов
            for enemy in destroy_enemies:
                self.enemies.discard(enemy)

            # Отрисовка
            self.background.draw(self.screen)

            self.player.draw(self.screen)

            for name, label in self.labels.items():
                label.draw(self.screen)

            for name, button in self.buttons.items():
                button.draw(self.screen)

            for name, switch in self.switches_buttons.items():
                switch.draw(self.screen)

            for bullet in self.bullets_player:
                bullet.draw(self.screen)

            for bullet in self.bullets_enemy:
                bullet.draw(self.screen)

            for enemy in self.enemies:
                enemy.draw(self.screen)

            # Жизнь персонажа
            if self.player.health > 0:
                for i in range(self.player.health):
                    self.screen.blit(self.player.image_health,
                                     (self.player.width + self.player.image_health.get_width() * i, 0))
            else:
                self.statistic['is_lose'] = True
                self.running = False

            # Отображение
            pygame.display.flip()
            self.clock.tick(settings.fps)

        self.statistic['time'] = time_i // settings.fps
        choose_level_window = ResultWindow(self.screen, self.statistic)
        await choose_level_window.run()

    async def back(self):
        self.running = False

    async def create_enemy(self, pos):
        """Создание врага"""
        enemy = Enemy(self.registry, (settings.width // 2, settings.height // 2))
        enemy.set_pose(*pos)
        self.enemies.add(enemy)

    async def narrator_controller(self, time):
        """Рассказчик игры"""
        if self.level == 1:
            if time == 1:
                await self.create_enemy((0, settings.height // 2 - (self.player.height // 2)))
        elif self.level == 2:
            if time == 1:
                await self.create_enemy((0, settings.height // 2 - (self.player.height // 2)))
        elif self.level == 5:
            if time % (settings.fps * 10) == 0:
                x = -settings.width * 0.2
                y = random.randint(0, settings.height - 80)
                await self.create_enemy((x, y))
