"""Конфигурационные настройки проекта."""


class Config:
    """Базовые настройки."""

    # URL
    UI_URL: str = "https://www.kinopoisk.ru/"
    API_BASE_URL: str = "https://api.poiskkino.dev"

    # Токен для API
    API_TOKEN: str = "CCGYGDP-HB84E4G-QP51HA0-ZYC8ZJK"

    # Настройки браузера
    IMPLICIT_WAIT: int = 10
    EXPLICIT_WAIT: int = 20

    # Таймауты
    TIMEOUT: int = 30


class Selectors:
    """CSS-селекторы для UI тестов."""

    # Поиск
    SEARCH_INPUT: str = "input[name='kp_query']"
    SEARCH_BUTTON: str = "button[type='submit']"

    # Результаты поиска
    RESULTS_LIST: str = "[data-tid='search_results']"
    RESULT_ITEM: str = "[data-tid='movie-card']"
    NO_RESULTS: str = "[data-tid='no_results']"

    # Куки
    COOKIE_ACCEPT: str = "[data-tid='cookie_accept']"
