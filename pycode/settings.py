import json
import os.path


class Settings:
    """Класс настроек"""

    def __init__(self):
        """Конструктор"""
        self.reboot = True
        self.fps = 60
        self.size = self.width, self.height = 800, 600
        self.display = 0
        self.volume_music = 20
        self.volume_sound = 20
        self.show_fps = False
        self.fullscreen = False
        self.k_width = self.width / 1920
        self.k_height = self.height / 1080
        self.load()

    def load(self):
        """Загрузка настроек с файла"""
        if not os.path.exists('settings.json'):
            self.save()

        with open('settings.json', 'r', encoding='utf-8') as file:
            data = json.loads(file.read())
            self.fps = data['fps']
            self.show_fps = data['show_fps']
            self.size = self.width, self.height = data['display_width'], data['display_height']
            self.display = data['display']
            self.fullscreen = data['display_fullscreen']
            self.volume_music = data['volume_music']
            self.volume_sound = data['volume_sound']
            self.calculate_size_game_objects()

    def save(self):
        """Сохранение настроек в файл"""
        data = {
            'fps': self.fps,
            'show_fps': self.show_fps,
            'display': self.display,
            'display_width': self.width,
            'display_height': self.height,
            'display_fullscreen': self.fullscreen,
            'volume_music': self.volume_music,
            'volume_sound': self.volume_sound
        }

        with open('settings.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    def delete(self):
        if os.path.exists('settings.json'):
            os.remove('settings.json')

        self.fps = 60
        self.size = self.width, self.height = 800, 600
        self.display = 0
        self.volume_music = 20
        self.volume_sound = 20
        self.show_fps = False
        self.fullscreen = False

    def calculate_size_game_objects(self):
        """"""
        self.k_width = self.width / 1920
        self.k_height = self.height / 1080


settings = Settings()
