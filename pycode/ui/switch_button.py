import pygame
import time
from pycode.ui.button import Button


class SwitchButton(Button):
    """Класс переключающейся кнопки с возможностью циклического выбора значений"""

    def __init__(self, items, font, shadow=False, start_index=0):
        """Конструктор"""
        super().__init__(items[start_index] if items else "", font, shadow)
        self._items = items if items else []
        self.current_index = start_index if 0 <= start_index < len(self._items) else 0
        self.min_index = 0
        self.max_index = len(self._items) - 1 if self._items else 0

        # Цвета для разных состояний
        self.color_left = (0, 255, 0)  # Цвет для левого переключения
        self.color_right = (0, 0, 255)  # Цвет для правого переключения

        # Обработчики событий
        self.on_change = None

        # Время последнего переключения
        self.last_switch_time = 0
        self.switch_delay = 0.1  # Задержка между переключениями в секундах

        # Флаги для обработки нажатия
        self.left_pressed = False
        self.right_pressed = False

        # Звук нажатия
        self.sound_click = None

    @property
    def items(self):
        """Возвращает текущий список элементов"""
        return self._items

    @items.setter
    def items(self, new_items):
        """Устанавливает новый список элементов и сбрасывает индекс"""
        self._items = new_items if new_items else []
        self.max_index = len(self._items) - 1 if self._items else 0
        self.current_index = 0 if self._items else -1
        self._update_text()

    def set_sound_click(self, sound):
        """Установка звука клика"""
        self.sound_click = sound

    def get_current_text(self):
        """Возвращает текущий отображаемый текст"""
        return self._items[self.current_index] if self._items and 0 <= self.current_index < len(self._items) else ""

    def get_current_index(self):
        """Возвращает текущий индекс выбранного элемента"""
        return self.current_index if self._items else -1

    def set_on_change(self, callback):
        """Устанавливает обработчик изменения значения"""
        self.on_change = callback

    def set_index(self, index):
        """Устанавливает новый индекс и обновляет отображение"""
        if not self._items:
            return

        if 0 <= index < len(self._items):
            self.current_index = index
            self._update_text()

            if self.on_change:
                self.on_change(self.current_index, self.get_current_text())

    def set_by_text(self, text):
        """Активирует элемент с указанным текстом"""
        if not self._items:
            return False

        try:
            index = self._items.index(text)
            self.set_index(index)
            return True
        except ValueError:
            return False

    def _update_text(self):
        """Обновляет текст кнопки в соответствии с текущим элементом"""
        if self._items and 0 <= self.current_index < len(self._items):
            self.label.text = self._items[self.current_index]
            self.label.create()  # Пересоздаем текст
            self._align_text()  # Перевыравниваем текст
        else:
            self.label.text = ""
            self.label.create()

    def _switch_left(self):
        """Переключает на предыдущий элемент"""
        if self.sound_click:
            self.sound_click.play()

        if not self._items:
            return

        self.current_index -= 1
        if self.current_index < self.min_index:
            self.current_index = self.max_index

        self._update_text()

        if self.on_change:
            self.on_change(self.current_index, self.get_current_text())

    def _switch_right(self):
        """Переключает на следующий элемент"""
        if self.sound_click:
            self.sound_click.play()

        if not self._items:
            return

        self.current_index += 1
        if self.current_index > self.max_index:
            self.current_index = self.min_index

        self._update_text()

        if self.on_change:
            self.on_change(self.current_index, self.get_current_text())

    async def update(self, mouse_pos, mouse_buttons):
        """Обновляет состояние кнопки с задержкой между переключениями"""
        self.is_motion = self.rect.collidepoint(mouse_pos)
        current_time = time.time()

        # Обработка нажатия левой кнопки мыши
        if self.is_motion and mouse_buttons[0]:  # Левая кнопка нажата
            if not self.left_pressed and current_time - self.last_switch_time > self.switch_delay:
                self._switch_left()
                self.last_switch_time = current_time
                self.is_pressed = True
                self.color = self.color_left
            self.left_pressed = True
        else:
            self.left_pressed = False

        # Обработка нажатия правой кнопки мыши
        if self.is_motion and mouse_buttons[2]:  # Правая кнопка нажата
            if not self.right_pressed and current_time - self.last_switch_time > self.switch_delay:
                self._switch_right()
                self.last_switch_time = current_time
                self.is_pressed = True
                self.color = self.color_right
            self.right_pressed = True
        else:
            self.right_pressed = False

        # Сброс состояния нажатия, если кнопка мыши отпущена
        if not (mouse_buttons[0] or mouse_buttons[2]):
            self.is_pressed = False
            self.color = (0, 0, 0)  # Возвращаем стандартный цвет

        # Обновление текущего изображения
        if self.is_pressed:
            if self.image_pressed:
                self.current_image = self.image_pressed
            elif self.image_hover:
                self.current_image = self.image_hover
            elif self.image_normal:
                self.current_image = self.image_normal
        elif self.is_motion:
            if self.image_hover:
                self.current_image = self.image_hover
            elif self.image_normal:
                self.current_image = self.image_normal
        else:
            if self.image_normal:
                self.current_image = self.image_normal

    def draw(self, screen):
        """Отрисовывает кнопку с индикацией направления переключения"""
        # Рисуем изображение или фон
        if self.current_image:
            scaled_image = pygame.transform.scale(self.current_image, self.size)
            screen.blit(scaled_image, self.pos)
        else:
            # Рисуем прямоугольник фона с цветом в зависимости от последнего действия
            if self.is_pressed:
                pygame.draw.rect(screen, self.color, self.rect)
            elif self.is_motion:
                pygame.draw.rect(screen, self.color_motion, self.rect)
            else:
                pygame.draw.rect(screen, (0, 0, 0), self.rect)

        # Рисуем индикаторы переключения
        arrow_size = min(self.size) // 4
        left_arrow = [(self.pos[0] + arrow_size, self.pos[1] + self.size[1] // 2),
                      (self.pos[0], self.pos[1] + self.size[1] // 2 - arrow_size),
                      (self.pos[0], self.pos[1] + self.size[1] // 2 + arrow_size)]

        right_arrow = [(self.pos[0] + self.size[0] - arrow_size, self.pos[1] + self.size[1] // 2),
                       (self.pos[0] + self.size[0], self.pos[1] + self.size[1] // 2 - arrow_size),
                       (self.pos[0] + self.size[0], self.pos[1] + self.size[1] // 2 + arrow_size)]

        pygame.draw.polygon(screen, (255, 255, 255), left_arrow)
        pygame.draw.polygon(screen, (255, 255, 255), right_arrow)

        # Рисуем текст
        self.label.draw(screen)
