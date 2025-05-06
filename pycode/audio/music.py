from pygame import mixer
from pycode.settings import settings


# Класс музыки
class Music:
    # Инициализация свойств
    def __init__(self, music_path, repeat=True):
        self.repeat = repeat
        self.music_path = music_path

        mixer.init()

    # Установка повтора
    def set_repeat(self, repeat):
        self.repeat = repeat

    # Запуск музыки
    def play(self):
        mixer.music.load(self.music_path)
        mixer.music.set_volume(settings.volume_music / 100)

        if self.repeat:
            mixer.music.play(-1)
        else:
            mixer.music.play()

    # Остановка музыки
    def stop(self):
        mixer.music.stop()
