import os.path
import pygame.image

from pycode.audio.music import Music
from pycode.audio.sound import Sound
from pycode.settings import settings


class Registry:
    """Класс реестра ресурсов"""

    def __init__(self):
        """Конструктор"""
        self.icon = None
        self.main_menu_background = None
        self.game_background = None
        self.fonts = None
        self.displays = dict()
        self.buttons = dict()
        self.music = dict()
        self.sounds = dict()
        self.player_texture = dict()

    def load_player_texture(self):
        self.player_texture.clear()
        self.player_texture['orig'] = self.load_image(f"resources/images/ship_player/ship.png", True)
        temp = [self.load_image(f"resources/images/ship_player/fire/{i}.png", True) for i in range(3)]
        self.player_texture['fire'] = temp
        temp = [self.load_image(f"resources/images/ship_player/waves/{i}.png", True) for i in range(5)]
        self.player_texture['waves'] = temp
        self.player_texture['health'] = self.load_image(f"resources/images/ship_player/health.png", True)

    def load_music(self):
        """Загрузка музыки"""
        self.music.clear()
        self.music = {
            'menu': Music("resources/music/menu_music.mp3"),
            'game': Music("resources/music/game_music.mp3")
        }

    def load_sounds(self):
        """Загрузка звуков"""
        self.sounds.clear()
        self.sounds = {
            'menu': {
                'click': Sound("resources/sounds/menu/click.wav")
            }
        }

    def load_displays(self):
        """Загрузка доступных мониторов и разрешение экрана"""
        self.displays.clear()
        try:
            for i in range(pygame.display.get_num_displays()):
                self.displays[i] = pygame.display.list_modes(display=i)
        except Exception as e:
            print(e)

    def load_fonts(self):
        """Загрузка шрифтов игры"""
        self.fonts = dict()
        self.fonts['main'] = {
            'title': pygame.font.Font("resources/fonts/press_start2p_regular.ttf", round(settings.width / 30)),
            'normal': pygame.font.Font("resources/fonts/press_start2p_regular.ttf", round(settings.width / 35)),
            'small': pygame.font.Font("resources/fonts/press_start2p_regular.ttf", round(settings.width / 45)),
        }

    def load_icon(self):
        """Загрузка иконки"""
        self.icon = self.load_image(f"resources/images/icon.png", True)

    def load_main_menu_background(self):
        """Загрузка картинок для заднего фона главного меню"""
        self.main_menu_background = []
        for i in range(1, 39):
            temp = self.load_image(f"resources/images/main_menu_background/{i}.jpeg", size=settings.size)
            self.main_menu_background.append(temp)

    def load_game_background(self):
        """Загрузка картинок для заднего фона игры"""
        self.game_background = []
        for i in range(1, 5):
            temp = self.load_image(f"resources/images/game_background/{i}.jpeg", size=settings.size)
            self.game_background.append(temp)

    def load_buttons_images(self):
        """Загрузка картинок кнопок"""
        self.buttons = dict()
        self.buttons['standard'] = {
            'normal': self.load_image("resources/images/buttons/standard/normal.png", True),
            'hover': self.load_image("resources/images/buttons/standard/hover.png", True),
            'pressed': self.load_image("resources/images/buttons/standard/pressed.png", True),
        }

    def load_image(self, path, is_alpha=False, size=None, mirror_h=False, mirror_v=False):
        """Функция для загрузки изображений"""
        # Проверка существования файла
        if not os.path.exists(path):
            return

        # Загрузка изображения
        image = pygame.image.load(path)

        # Установка размера если он есть
        if size:
            image = pygame.transform.scale(image, size)

        # Отзеркалить изображение горизонтально, если нужно
        if mirror_h:
            image = pygame.transform.flip(image, True, False)
        # Отзеркалить изображение вертикально, если нужно
        if mirror_v:
            image = pygame.transform.flip(image, False, True)

        # Конвертирование картинки (прозразная или обычная
        if is_alpha:
            image.convert_alpha()
        else:
            image.convert()

        return image
