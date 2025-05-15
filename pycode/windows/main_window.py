import pygame

from pycode.registry import Registry
from pycode.settings import settings
from pycode.ui.background_animated_ui import BackgroundAnimatedUi
from pycode.ui.button import Button
from pycode.ui.label import Label
from pycode.windows.choose_level_window import ChooseLevelWindow
from pycode.windows.loading_window import LoadingWindow
from pycode.windows.settings_window import SettingsWindow


class MainWindow:
    """Класс главного окна"""

    def __init__(self):
        """Конструктор (инициализация свойств)"""
        self.running = True
        self.registry = None
        self.screen = None
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
        pygame.display.set_caption("Главное меню")
        pygame.display.set_icon(self.registry.icon)

        # Загрузка шрифтов
        self.registry.load_fonts()

        # Загрузка изображений главного меню
        self.registry.load_main_menu_background()
        self.background = BackgroundAnimatedUi(self.registry.main_menu_background, settings.fps // 10)

        # Загрузка изображений кнопок
        self.registry.load_buttons_images()

        # Загрузка звуков и музыки
        self.registry.load_music()
        self.registry.load_sounds()
        self.registry.music['menu'].play()

        # Установка текста
        if settings.show_fps:
            label = Label(str(settings.fps), self.registry.fonts['main']['small'], True)
            label.create()
            label.set_pos(0,0)
            self.labels['fps'] = label

        label = Label("Главное меню", self.registry.fonts['main']['title'], True)
        label.create()
        label.set_pos(settings.width // 2 - label.get_width_text() // 2,
                      settings.height * 0.02)
        self.labels['1'] = label

        # Установка кнопок
        button = Button("Начать игру", self.registry.fonts['main']['normal'], True)
        button.set_images(normal=self.registry.buttons['standard']['normal'],
                          hover=self.registry.buttons['standard']['hover'],
                          pressed=self.registry.buttons['standard']['pressed'])
        button.set_size(settings.width * 0.4, settings.height * 0.1)
        button.create()
        button.set_pos(settings.width // 2 - settings.width * 0.4 // 2,
                       settings.height * 0.3)
        button.set_action(self.start_button)
        button.set_sound_click(self.registry.sounds['menu']['click'])
        self.buttons['start'] = button

        button = Button("Магазин Кораблей", self.registry.fonts['main']['normal'], True)
        button.set_images(normal=self.registry.buttons['standard']['normal'],
                          hover=self.registry.buttons['standard']['hover'],
                          pressed=self.registry.buttons['standard']['pressed'])
        button.set_size(settings.width * 0.4, settings.height * 0.1)
        button.create()
        button.set_pos(settings.width // 2 - settings.width * 0.4 // 2,
                       settings.height * 0.4)
        button.set_action(self._button)
        button.set_sound_click(self.registry.sounds['menu']['click'])
        self.buttons['shop'] = button

        button = Button("Настройки", self.registry.fonts['main']['normal'], True)
        button.set_images(normal=self.registry.buttons['standard']['normal'],
                          hover=self.registry.buttons['standard']['hover'],
                          pressed=self.registry.buttons['standard']['pressed'])
        button.set_size(settings.width * 0.4, settings.height * 0.1)
        button.create()
        button.set_pos(settings.width // 2 - settings.width * 0.4 // 2,
                       settings.height * 0.5)
        button.set_action(self.settings_button)
        button.set_sound_click(self.registry.sounds['menu']['click'])
        self.buttons['settings'] = button

        button = Button("Выход", self.registry.fonts['main']['normal'], True)
        button.set_images(normal=self.registry.buttons['standard']['normal'],
                          hover=self.registry.buttons['standard']['hover'],
                          pressed=self.registry.buttons['standard']['pressed'])
        button.set_size(settings.width * 0.4, settings.height * 0.1)
        button.create()
        button.set_pos(settings.width // 2 - settings.width * 0.4 // 2,
                       settings.height * 0.6)
        button.set_action(self.exit_game)
        button.set_sound_click(self.registry.sounds['menu']['click'])
        self.buttons['exit'] = button

        # Предварительная настройка
        self.clock = pygame.time.Clock()
        self.running = True

    async def run(self):
        """Запуск окна"""
        pygame.init()
        settings.load()
        if settings.fullscreen:
            self.screen = pygame.display.set_mode(settings.size, pygame.FULLSCREEN, display=settings.display)
        else:
            self.screen = pygame.display.set_mode(settings.size, display=settings.display)
        await LoadingWindow(self.screen, delay_after=0.5).show(
            self.load(),
            "Загрузка"
        )
        self.running = True
        await self.menu()
        pygame.quit()

    async def menu(self):
        """Логика окна"""
        # Игровой цикл
        while self.running and not settings.reboot:
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

        for i in range(settings.fps):
            # Обработка логики
            self.background.update()

            # Отрисовка
            self.background.draw(self.screen)

            # Отображение
            pygame.display.flip()
            self.clock.tick(settings.fps)

    async def start_button(self):
        choose_level_window = ChooseLevelWindow(self.screen)
        await choose_level_window.run()

    async def settings_button(self):
        settings_window = SettingsWindow(self.screen)
        await settings_window.run()

    async def exit_game(self):
        self.running = False
