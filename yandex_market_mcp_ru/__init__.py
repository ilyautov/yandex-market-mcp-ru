"""Тонкая обёртка: сервер Яндекс Маркет из пакета marketplaces-mcp-ru.

Своего кода тут нет намеренно. Пакет существует ради имени: его ищут словом
«яндекс маркет», а не словом «marketplaces». Логика, каталог и гейт
безопасности живут в зависимости и обновляются вместе с ней.
"""

from importlib.metadata import PackageNotFoundError, version as _dist_version

from yandex_mcp.server import main

__all__ = ["main"]

try:
    # Версия живёт в pyproject.toml и приезжает из метаданных дистрибутива.
    # Вторая копия числа в коде неизбежно отстаёт, и все шесть пакетов отстали.
    __version__ = _dist_version("yandex-market-mcp-ru")
except PackageNotFoundError:  # запуск из исходников без установки
    __version__ = "0+unknown"
