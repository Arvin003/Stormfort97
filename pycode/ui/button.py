import pygame
from pycode.ui.label import Label


class Button:
    """Класс кнопки с поддержкой эффектов наведения, изображений и центрирования текста"""

    def __init__(self, text, font, shadow=False):
        self.label = Label(text, font, shadow)
        self.rect = None
        self.color = (0, 0, 0)  # Цвет фона по умолчанию
        self.color_motion = (255, 0, 0)  # Цвет фона при наведении
        self.color_motion_text = (255, 0, 0)  # Цвет фона при наведении
        self.color_pressed = (200, 0, 0)  # Цвет фона при нажатии
        self.size = None  # Размер кнопки (None - авто по тексту)
        self.pos = (0, 0)  # Позиция кнопки
        self.is_motion = False  # Курсор над кнопкой
        self.is_pressed = False  # Кнопка мыши нажата на этой кнопке
        self.was_pressed = False  # Кнопка была нажата (для обработки отпускания)
        self.action = None  # Действие при клике

        # Изображения для разных состояний
        self.image_normal = None
        self.image_hover = None
        self.image_pressed = None
        self.current_image = None

        # Выравнивание текста
        self.text_align = 'center'  # center, left, right

        # Звук нажатия
        self.sound_click = None

    def create(self):
        """Создает кнопку (вызывается один раз после настройки)"""
        self.label.create()

        # Если размер не указан, определяем по тексту
        if self.size is None:
            self.size = (self.label.get_width_text(), self.label.get_height_text())

        self.rect = pygame.Rect(*self.pos, *self.size)

        # Центрируем текст, если нужно
        self._align_text()

        # Устанавливаем текущее изображение
        if self.image_normal:
            self.current_image = self.image_normal
        elif self.image_hover:
            self.current_image = self.image_hover
        elif self.image_pressed:
            self.current_image = self.image_pressed

    def _align_text(self):
        """Выравнивает текст внутри кнопки"""
        if self.text_align == 'center':
            text_width = self.label.get_width_text()
            text_height = self.label.get_height_text()
            x = self.pos[0] + (self.size[0] - text_width) // 2
            y = self.pos[1] + (self.size[1] - text_height) // 2
            self.label.set_pos(x, y)
        # Для left и right позиция уже установлена при set_pos

    def set_size(self, width, height):
        """Устанавливает размер кнопки (0, 0 - авторазмер)"""
        if width == 0 or height == 0:
            self.size = None
        else:
            self.size = (width, height)
        if self.rect:
            self.create()  # Пересоздаем для обновления размеров

    def set_pos(self, x, y):
        """Устанавливает позицию кнопки"""
        self.pos = (x, y)
        if self.rect:
            self.rect.topleft = self.pos
            self._align_text()

    def set_sound_click(self, sound):
        """Установка звука клика"""
        self.sound_click = sound

    def set_action(self, action):
        """Устанавливает действие при клике"""
        self.action = action

    def set_images(self, normal=None, hover=None, pressed=None):
        """Устанавливает изображения для разных состояний кнопки"""
        self.image_normal = normal
        self.image_hover = hover
        self.image_pressed = pressed
        self.current_image = normal

    def set_text_align(self, align):
        """Устанавливает выравнивание текста ('center', 'left', 'right')"""
        self.text_align = align
        if self.rect:
            self._align_text()

    async def update(self, mouse_pos, mouse_buttons):
        """Обновляет состояние кнопки"""
        self.is_motion = self.rect.collidepoint(mouse_pos)

        # Обработка нажатия кнопки мыши
        if self.is_motion and mouse_buttons and mouse_buttons[0]:  # Левая кнопка мыши нажата
            if not self.is_pressed:
                if self.sound_click:
                    self.sound_click.play()
            self.is_pressed = True
        elif self.is_motion:
            # Обработка отпускания кнопки мыши
            if self.is_pressed:
                await self.action()
            self.is_pressed = False
        else:
            self.is_pressed = False

        # Обновление текущего изображения
        if self.is_pressed:
            if self.image_pressed:
                self.current_image = self.image_pressed
            elif self.image_hover:
                self.current_image = self.image_hover
            elif self.image_normal:
                self.current_image = self.image_normal
        elif self.is_motion:
            self.label.color = self.color_motion_text
            self.label.create()
            if self.image_hover:
                self.current_image = self.image_hover
            elif self.image_normal:
                self.current_image = self.image_normal
        else:
            self.label.color = (255, 255, 255)
            self.label.create()
            if self.image_normal:
                self.current_image = self.image_normal

    def draw(self, screen):
        """Отрисовывает кнопку"""
        # Рисуем изображение или фон
        if self.current_image:
            # Масштабируем изображение под размер кнопки
            scaled_image = pygame.transform.scale(self.current_image, self.size)
            screen.blit(scaled_image, self.pos)
        else:
            # Рисуем прямоугольник фона
            if self.is_pressed:
                pygame.draw.rect(screen, self.color_pressed, self.rect)
            elif self.is_motion:
                pygame.draw.rect(screen, self.color_motion, self.rect)
            else:
                pygame.draw.rect(screen, self.color, self.rect)

        # Рисуем текст
        self.label.draw(screen)
