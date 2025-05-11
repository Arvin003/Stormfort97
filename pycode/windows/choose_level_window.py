import pygame

from pycode.registry import Registry
from pycode.settings import settings
from pycode.ui.background_animated_ui import BackgroundAnimatedUi
from pycode.ui.button import Button
from pycode.ui.label import Label
from pycode.windows.game_window import GameWindow
from pycode.windows.loading_window import LoadingWindow


class ChooseLevelWindow:
    """Класс окна выбора уровня"""

    def __init__(self, screen):
        """Конструктор (инициализация свойств)"""
        self.running = True
        self.registry = None
        self.screen = screen
        self.background = None
        self.clock = None

        self.labels = dict()
        self.buttons = dict()
        self.switches_buttons = dict()

    async def load(self):
        """Загрузка ресурсов"""
        # Создание ресурсов
        self.registry = Registry()
        self.registry.load_displays()

        # Загрузка ресурсов панели окна
        self.registry.load_icon()
        pygame.display.set_caption("Выбор уровня")
        pygame.display.set_icon(self.registry.icon)

        # Загрузка шрифтов
        self.registry.load_fonts()

        # Загрузка звуков и музыки
        self.registry.load_music()
        self.registry.load_sounds()

        # Загрузка изображений главного меню
        self.registry.load_main_menu_background()
        self.background = BackgroundAnimatedUi(self.registry.main_menu_background, settings.fps // 10)

        # Загрузка изображений кнопок
        self.registry.load_buttons_images()

        # Установка текста
        if settings.show_fps:
            label = Label(str(settings.fps), self.registry.fonts['main']['small'], True)
            label.create()
            label.set_pos(0,0)
            self.labels['fps'] = label

        label = Label("Выбор уровня", self.registry.fonts['main']['title'], True)
        label.create()
        label.set_pos(settings.width // 2 - label.get_width_text() // 2,
                      settings.height * 0.05)
        self.labels['1'] = label

        # Установка кнопок
        button = Button("Уровень 1", self.registry.fonts['main']['normal'], True)
        button.set_images(normal=self.registry.buttons['standard']['normal'],
                          hover=self.registry.buttons['standard']['hover'],
                          pressed=self.registry.buttons['standard']['pressed'])
        button.set_size(settings.width * 0.4, settings.height * 0.1)
        button.create()
        button.set_pos(settings.width * 0.3,
                       settings.height * 0.15)
        button.set_action(lambda : self.start_level(1))
        button.set_sound_click(self.registry.sounds['menu']['click'])
        self.buttons['level1'] = button

        button = Button("Уровень 2", self.registry.fonts['main']['normal'], True)
        button.set_images(normal=self.registry.buttons['standard']['normal'],
                          hover=self.registry.buttons['standard']['hover'],
                          pressed=self.registry.buttons['standard']['pressed'])
        button.set_size(settings.width * 0.4, settings.height * 0.1)
        button.create()
        button.set_pos(settings.width * 0.3,
                       settings.height * 0.275)
        button.set_action(lambda: self.start_level(2))
        button.set_sound_click(self.registry.sounds['menu']['click'])
        self.buttons['level2'] = button

        button = Button("Бонусный уровень"
                        "", self.registry.fonts['main']['normal'], True)
        button.set_images(normal=self.registry.buttons['standard']['normal'],
                          hover=self.registry.buttons['standard']['hover'],
                          pressed=self.registry.buttons['standard']['pressed'])
        button.set_size(settings.width * 0.4, settings.height * 0.1)
        button.create()
        button.set_pos(settings.width * 0.3,
                       settings.height * 0.4)
        button.set_action(lambda: self.start_level(5))
        button.set_sound_click(self.registry.sounds['menu']['click'])
        self.buttons['level5'] = button

        button = Button("Назад", self.registry.fonts['main']['normal'], True)
        button.set_images(normal=self.registry.buttons['standard']['normal'],
                          hover=self.registry.buttons['standard']['hover'],
                          pressed=self.registry.buttons['standard']['pressed'])
        button.set_size(settings.width * 0.3, settings.height * 0.1)
        button.create()
        button.set_pos(settings.width // 2 - (settings.width * 0.15),
                       settings.height * 0.9)
        button.set_action(self.back)
        button.set_sound_click(self.registry.sounds['menu']['click'])
        self.buttons['back'] = button

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

            # Отрисовка
            self.background.draw(self.screen)
            for name, label in self.labels.items():
                label.draw(self.screen)

            for name, button in self.buttons.items():
                button.draw(self.screen)

            for name, switch in self.switches_buttons.items():
                switch.draw(self.screen)

            # Отображение
            pygame.display.flip()
            self.clock.tick(settings.fps)

    async def start_level(self, level=0):
        game_window = GameWindow(self.screen, level)
        await game_window.run()
        self.registry.music['menu'].play()

    async def back(self):
        self.running = False
