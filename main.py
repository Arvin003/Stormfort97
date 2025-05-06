import asyncio
from pycode.windows.main_window import MainWindow
from pycode.settings import settings

# Запуск игры
while settings.reboot:
    settings.reboot = False  # Отключаем бесконечную перезагрузку
    main_window = MainWindow()
    asyncio.run(main_window.run())
