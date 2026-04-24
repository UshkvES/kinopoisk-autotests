"""Класс для работы с API Кинопоиска."""

import allure
import requests
from config.settings import Config


class KinopoiskAPI:
    """Класс для взаимодействия с API Кинопоиска."""

    def __init__(self) -> None:
        """Инициализация API клиента."""
        self.base_url: str = Config.API_BASE_URL
        self.token: str = Config.API_TOKEN
        self.headers: dict = {"x-api-key": self.token}

    @allure.step("API: Поиск фильма по названию '{query}'")
    def search_movie(self, query: str, page: int = 1,
                     limit: int = 1) -> requests.Response:
        """
        Поиск фильма по названию.

        Args:
            query: Поисковый запрос
            page: Номер страницы
            limit: Количество результатов

        Returns:
            Response object
        """
        url = f"{self.base_url}/v1.4/movie/search"
        params = {"page": page, "limit": limit, "query": query}
        return requests.get(url, headers=self.headers, params=params)

    @allure.step("API: Получить список фильмов по жанру '{genre}'")
    def get_movies_by_genre(self, genre: str, page: int = 1,
                            limit: int = 10) -> requests.Response:
        """
        Получить список фильмов по жанру.

        Args:
            genre: Название жанра
            page: Номер страницы
            limit: Количество результатов

        Returns:
            Response object
        """
        url = f"{self.base_url}/v1.4/movie"
        params = {"page": page, "limit": limit, "genres.name": genre}
        return requests.get(url, headers=self.headers, params=params)

    @allure.step("API: Получить информацию о серии")
    def get_episode(self, movie_id: int, season_number: int,
                    episode_number: int) -> requests.Response:
        """
        Получить информацию о конкретной серии.

        Args:
            movie_id: ID сериала
            season_number: Номер сезона
            episode_number: Номер серии

        Returns:
            Response object
        """
        url = f"{self.base_url}/v1.4/season"
        params = {
            "page": 1,
            "limit": 1,
            "movieId": movie_id,
            "number": season_number,
            "episodes.number": episode_number
        }
        return requests.get(url, headers=self.headers, params=params)

    @allure.step("API: Поиск фильма без токена")
    def search_movie_no_token(self, query: str) -> requests.Response:
        """
        Поиск фильма без передачи токена авторизации.

        Args:
            query: Поисковый запрос

        Returns:
            Response object
        """
        url = f"{self.base_url}/v1.4/movie/search"
        params = {"page": 1, "limit": 1, "query": query}
        return requests.get(url, params=params)

    @allure.step("API: Поиск с несуществующим названием '{query}'")
    def search_nonexistent_movie(self, query: str) -> requests.Response:
        """
        Поиск фильма с несуществующим названием.

        Args:
            query: Несуществующий поисковый запрос

        Returns:
            Response object
        """
        return self.search_movie(query)
