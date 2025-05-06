class BackgroundUi:
    """Класс статического заднего фона"""

    def __init__(self, image=None, color=(0, 0, 0)):
        """Конструктор"""
        self.image = image
        self.color = color

    def update(self):
        """Функция обновления логики"""
        pass

    def draw(self, screen):
        """Функция для отрисовки заднего фона"""
        if self.image:
            screen.blit(self.image, (0, 0))
        else:
            screen.fill(self.color)
