import pygame

from pycode.registry import Registry
from pycode.settings import settings
from pycode.ui.background_animated_ui import BackgroundAnimatedUi
from pycode.ui.button import Button
from pycode.ui.label import Label
from pycode.ui.switch_button import SwitchButton
from pycode.windows.loading_window import LoadingWindow


class SettingsWindow:
    """Класс окна настроек"""

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
        pygame.display.set_caption("Настройка игры")
        pygame.display.set_icon(self.registry.icon)

        # Загрузка шрифтов
        self.registry.load_fonts()

        # Загрузка звуков и музыки
        self.registry.load_music()
        self.registry.load_sounds()

        # Загрузка изображений главного меню
        self.registry.load_main_menu_background()
        self.background = BackgroundAnimatedUi(self.registry.main_menu_background, settings.fps // 10)

        # Установка текста
        if settings.show_fps:
            label = Label(str(settings.fps), self.registry.fonts['main']['small'], True)
            label.create()
            label.set_pos(0,0)
            self.labels['fps'] = label

        label = Label("Настройки", self.registry.fonts['main']['title'], True)
        label.create()
        label.set_pos(settings.width // 2 - label.get_width_text() // 2,
                      settings.height * 0.0)
        self.labels['1'] = label

        label = Label("Монитор", self.registry.fonts['main']['small'], True)
        label.create()
        label.set_pos(settings.width * 0.075,
                      settings.height * 0.075)
        self.labels['2'] = label

        label = Label("Разрешение", self.registry.fonts['main']['small'], True)
        label.create()
        label.set_pos(settings.width * 0.525,
                      settings.height * 0.075)
        self.labels['3'] = label

        label = Label("Полноэкранный режим", self.registry.fonts['main']['small'], True)
        label.create()
        label.set_pos(settings.width * 0.075,
                      settings.height * 0.275)
        self.labels['4'] = label

        label = Label("Отображать частоту кадров", self.registry.fonts['main']['small'], True)
        label.create()
        label.set_pos(settings.width * 0.525,
                      settings.height * 0.275)
        self.labels['5'] = label

        label = Label("Громкость музыки", self.registry.fonts['main']['small'], True)
        label.create()
        label.set_pos(settings.width * 0.075,
                      settings.height * 0.475)
        self.labels['6'] = label

        label = Label("Громкость звуков", self.registry.fonts['main']['small'], True)
        label.create()
        label.set_pos(settings.width * 0.525,
                      settings.height * 0.475)
        self.labels['7'] = label

        # Установка кнопок
        button = Button("Сбросить", self.registry.fonts['main']['normal'], True)
        button.set_size(settings.width * 0.3, settings.height * 0.1)
        button.create()
        button.set_pos(settings.width - settings.width * 0.3 - settings.width * 0.033,
                       settings.height * 0.9)
        button.set_action(self.default)
        button.set_sound_click(self.registry.sounds['menu']['click'])
        self.buttons['default'] = button

        button = Button("Применить", self.registry.fonts['main']['normal'], True)
        button.set_size(settings.width * 0.3, settings.height * 0.1)
        button.create()
        button.set_pos(settings.width // 2 - (settings.width * 0.15),
                       settings.height * 0.9)
        button.set_action(self.apply)
        button.set_sound_click(self.registry.sounds['menu']['click'])
        self.buttons['apply'] = button

        button = Button("Назад", self.registry.fonts['main']['normal'], True)
        button.set_size(settings.width * 0.3, settings.height * 0.1)
        button.create()
        button.set_pos(settings.width * 0.033,
                       settings.height * 0.9)
        button.set_action(self.back)
        button.set_sound_click(self.registry.sounds['menu']['click'])
        self.buttons['back'] = button

        # Установка кнопчатых переключателей
        items = ["Экран: " + str(display + 1) for display in list(self.registry.displays.keys())]
        switch_button = SwitchButton(items, self.registry.fonts['main']['normal'], start_index=settings.display,
                                     shadow=True)
        switch_button.create()
        switch_button.set_pos(settings.width * 0.075,
                              settings.height * 0.125)
        switch_button.set_size(settings.width * 0.4, settings.height * 0.1)
        switch_button.set_on_change(self.on_switch_display)
        switch_button.set_sound_click(self.registry.sounds['menu']['click'])
        self.switches_buttons['display'] = switch_button

        items = [f"{width}x{height}" for width, height in list(self.registry.displays[settings.display])]
        switch_button = SwitchButton(items, self.registry.fonts['main']['normal'], shadow=True)
        switch_button.create()
        switch_button.set_pos(settings.width * 0.525,
                              settings.height * 0.125)
        switch_button.set_size(settings.width * 0.4, settings.height * 0.1)
        switch_button.set_by_text(f"{settings.width}x{settings.height}")
        switch_button.set_sound_click(self.registry.sounds['menu']['click'])
        self.switches_buttons['resolution'] = switch_button

        items = ["Да", "Нет"]
        if settings.fullscreen:
            start_index = 0
        else:
            start_index = 1
        switch_button = SwitchButton(items, self.registry.fonts['main']['normal'], start_index=start_index,
                                     shadow=True)
        switch_button.create()
        switch_button.set_pos(settings.width * 0.075,
                              settings.height * 0.325)
        switch_button.set_size(settings.width * 0.4, settings.height * 0.1)
        switch_button.set_sound_click(self.registry.sounds['menu']['click'])
        self.switches_buttons['fullscreen'] = switch_button

        if settings.show_fps:
            start_index = 0
        else:
            start_index = 1
        switch_button = SwitchButton(items, self.registry.fonts['main']['normal'], start_index=start_index,
                                     shadow=True)
        switch_button.create()
        switch_button.set_pos(settings.width * 0.525,
                              settings.height * 0.325)
        switch_button.set_size(settings.width * 0.4, settings.height * 0.1)
        switch_button.set_sound_click(self.registry.sounds['menu']['click'])
        self.switches_buttons['show_fps'] = switch_button

        items = [str(volume) for volume in range(0, 110, 10)]
        switch_button = SwitchButton(items, self.registry.fonts['main']['normal'], start_index=0,
                                     shadow=True)
        switch_button.create()
        switch_button.set_pos(settings.width * 0.075,
                              settings.height * 0.525)
        switch_button.set_size(settings.width * 0.4, settings.height * 0.1)
        switch_button.set_by_text(f"{settings.volume_music}")
        switch_button.set_sound_click(self.registry.sounds['menu']['click'])
        self.switches_buttons['volume_music'] = switch_button

        switch_button = SwitchButton(items, self.registry.fonts['main']['normal'], start_index=0,
                                     shadow=True)
        switch_button.create()
        switch_button.set_pos(settings.width * 0.525,
                              settings.height * 0.525)
        switch_button.set_size(settings.width * 0.4, settings.height * 0.1)
        switch_button.set_by_text(f"{settings.volume_sound}")
        switch_button.set_sound_click(self.registry.sounds['menu']['click'])
        self.switches_buttons['volume_sound'] = switch_button

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

    async def default(self):
        settings.reboot = True
        settings.delete()
        self.running = False

    async def apply(self):
        """Принятие новых настроек"""
        settings.reboot = True
        # Полноэкранный режим
        if self.switches_buttons['fullscreen'].get_current_index() == 1:
            settings.fullscreen = False
        else:
            settings.fullscreen = True

        # Отображение частоты кадров
        if self.switches_buttons['show_fps'].get_current_index() == 1:
            settings.show_fps = False
        else:
            settings.show_fps = True

        # Монитор
        settings.display = self.switches_buttons['display'].get_current_index()
        # Разрешение
        index = self.switches_buttons['display'].get_current_index()
        display = self.registry.displays[index]
        index = self.switches_buttons['resolution'].get_current_index()
        resolution = display[index]
        settings.width, settings.height = resolution

        # Громкость музыки и звуков
        settings.volume_music = int(self.switches_buttons['volume_music'].get_current_text())
        settings.volume_sound = int(self.switches_buttons['volume_sound'].get_current_text())

        settings.save()
        self.running = False

    async def back(self):
        self.running = False

    # Установка обработчика изменения выбранного монитора
    def on_switch_display(self, index, text):
        items = [f"{width}x{height}" for width, height in list(self.registry.displays[index])]
        self.switches_buttons['resolution'].items = items

        if settings.display == index:
            self.switches_buttons['resolution'].set_by_text(f"{settings.width}x{settings.height}")
        else:
            self.switches_buttons['resolution'].set_index(0)
