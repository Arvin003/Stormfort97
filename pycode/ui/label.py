from pycode.settings import settings


class Label:
    def __init__(self, text, font, shadow=False):
        self.font = font
        self.text = text
        self.color = (255, 255, 255)
        self.color_shadow = (0, 0, 0)
        self.pos = (0, 0)
        self.pos_shadow = (0, 0)
        self.shadow = shadow

        self.text_render = None
        self.text_shadow_render = None

    def create(self):
        """Функция для создания"""
        self.text_render = None
        self.text_shadow_render = None

        self.text_render = self.font.render(self.text, True, self.color)

        if self.shadow:
            self.text_shadow_render = self.font.render(self.text, True, self.color_shadow)

    def set_pos(self, x, y):
        """Установка позиции текста"""
        self.pos = (x, y)
        step_shadow_x = round(settings.width / 400)
        step_shadow_y = round(settings.height / 300)
        self.pos_shadow = (x + step_shadow_x, y + step_shadow_y)

    def set_color(self, color=(255, 255, 255)):
        """Установка цвета текста"""
        self.color = color

    def set_text(self, text):
        """Установка текста"""
        self.text = text

    def set_color_shadow(self, color_shadow=(0, 0, 0)):
        """Установка цвета тени текста"""
        self.color_shadow = color_shadow

    def draw(self, screen):
        """Отрисовка текста"""
        if self.text_shadow_render:
            screen.blit(self.text_shadow_render, self.pos_shadow)

        if self.text_render:
            screen.blit(self.text_render, self.pos)

    def get_width_text(self):
        """Получение ширины текста"""
        if self.text_render:
            return self.text_render.get_width()

    def get_height_text(self):
        """Получение высоты текста"""
        if self.text_render:
            return self.text_render.get_height()
