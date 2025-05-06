import pygame

from pycode.game.bullet import Bullet
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

    def __init__(self, screen):
        """Конструктор (инициализация свойств)"""
        self.running = True
        self.registry = None
        self.screen = screen
        self.background = None
        self.clock = None

        self.statistic = {
            'is_won': False,
            'is_lose': False,
            'time': 0
        }
        self.labels = dict()
        self.buttons = dict()
        self.switches_buttons = dict()
        self.bullets_player = set()
        self.bullets_enemies = set()

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

        self.enemy = Player(self.registry, (settings.width // 2, settings.height // 2))
        self.enemy.set_pose(settings.width // 2, settings.height // 2 - (self.player.height // 2))

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
        await self.menu()

    async def menu(self):
        """Логика окна"""
        # Игровой цикл
        while self.running:
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

            destroy_bullet = set()
            for bullet in self.bullets_player:
                bullet.update()

                if pygame.sprite.collide_mask(self.enemy, bullet):
                    bullet.destroy_bullet()
                if bullet.is_kill:
                    destroy_bullet.add(bullet)

            for bullet in destroy_bullet:
                self.bullets_player.discard(bullet)
            destroy_bullet.clear()

            self.enemy.update()

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

            self.enemy.draw(self.screen)

            # Отображение
            pygame.display.flip()
            self.clock.tick(settings.fps)

        choose_level_window = ResultWindow(self.screen, self.statistic)
        await choose_level_window.run()

    async def back(self):
        self.running = False
