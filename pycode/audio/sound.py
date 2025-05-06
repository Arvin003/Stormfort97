from pygame import mixer
from pycode.settings import settings


# Класс звуков
class Sound:
    # Инициализация свойств
    def __init__(self, sound_path):
        mixer.init()
        self.sound = mixer.Sound(sound_path)
        self.sound.set_volume(settings.volume_sound / 100)

    # Запуск звука
    def play(self):
        self.sound.play()
