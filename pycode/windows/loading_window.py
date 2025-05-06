import pygame
import asyncio
from typing import Coroutine


class LoadingWindow:
    def __init__(self, screen: pygame.Surface, delay_after: float = 1.0):
        self.screen = screen
        self.delay_after = delay_after  # Доп. задержка после загрузки
        self.font = pygame.font.SysFont('Arial', 32)
        self.is_active = False
        self.dots = 0

    async def show(self, task: Coroutine, title: str = "Загрузка"):
        """Запуск загрузки с анимацией"""
        self.is_active = True
        self.dots = 0

        # Запускаем основную задачу
        main_task = asyncio.create_task(task)

        # Запускаем анимацию
        animation_task = asyncio.create_task(self._animate(title))

        # Ждем завершения основной задачи
        try:
            result = await main_task
        except Exception as e:
            main_task.cancel()
            animation_task.cancel()
            raise e

        # Добавляем задержку после загрузки
        await asyncio.sleep(self.delay_after)
        animation_task.cancel()
        self.is_active = False

        return result

    async def _animate(self, title: str):
        """Анимация загрузки"""
        clock = pygame.time.Clock()

        while self.is_active:
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # Обновление анимации
            self.dots = (self.dots + 1) % 4

            # Отрисовка
            self.screen.fill((0, 0, 0))

            # Текст с точками
            loading_text = f"{title}{'.' * self.dots}"
            text_surface = self.font.render(loading_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2,
                                                      self.screen.get_height() // 2))
            self.screen.blit(text_surface, text_rect)

            pygame.display.flip()
            await asyncio.sleep(0.2)  # Скорость анимации
            clock.tick(60)