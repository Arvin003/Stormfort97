import pygame

from pycode.registry import Registry
from pycode.settings import settings
from pycode.ui.background_animated_ui import BackgroundAnimatedUi
from pycode.ui.button import Button
from pycode.ui.label import Label
from pycode.windows.game_window import GameWindow
from pycode.windows.loading_window import LoadingWindow


class ShoplWindow:
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
        pygame.display.set_caption("Выбор Корабля")
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

        label = Label("Выбор  Корабля", self.registry.fonts['main']['title'], True)
        label.create()
        label.set_pos(settings.width // 2 - label.get_width_text() // 2,
                      settings.height * 0.05)
        self.labels['shop'] = label