from pycode.ui.background_ui import BackgroundUi


class BackgroundAnimatedUi(BackgroundUi):
    """Класс динамического заднего фона"""

    def __init__(self, images, speed):
        """Конструктор"""
        super().__init__(images[0])
        self.images = images
        self.len_images = len(self.images)
        self.speed = speed
        self.i = 0
        self.current = 0

    def update(self):
        """Функция обновления"""
        self.i += 1

        if self.i >= self.speed:
            self.current = (self.current + 1) % self.len_images
            self.i = 0
            self.image = self.images[self.current]
