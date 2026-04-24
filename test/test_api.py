"""API тесты для Кинопоиска."""

import json
import os
from typing import Dict, Any
import allure
import pytest
from api.kinopoisk_api import KinopoiskAPI

# Загрузка тестовых данных из JSON
current_dir: str = os.path.dirname(__file__)
json_path: str = os.path.join(current_dir, '..', 'config', 'test_data.json')
with open(json_path, 'r', encoding='utf-8') as f:
    test_data: Dict[str, Any] = json.load(f)


@allure.epic("API Тесты")
@allure.feature("API Кинопоиска")
@allure.story("Проверка API методов")
@pytest.mark.api
class TestAPI:

    @allure.title("Поиск фильма по названию (позитивный)")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_search_movie_by_title(self, api_client: KinopoiskAPI) -> None:
        """Проверка поиска фильма по названию."""
        query: str = test_data["search_queries"]["full_title"]

        with allure.step(f"Отправить GET запрос на поиск '{query}'"):
            response = api_client.search_movie(query)

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200

        with allure.step("Проверить, что фильм найден"):
            data: Dict[str, Any] = response.json()
            assert len(data["docs"]) > 0

    @allure.title("Вывод списка фильмов по жанру")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_get_movies_by_genre(self, api_client: KinopoiskAPI) -> None:
        """Проверка вывода списка фильмов по жанру."""
        genre: str = test_data["filters"]["genre"]

        with allure.step(
            f"Отправить GET запрос на получение фильмов жанра '{genre}'"
        ):
            response = api_client.get_movies_by_genre(genre)

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200

        with allure.step("Проверить, что список фильмов не пуст"):
            data: Dict[str, Any] = response.json()
            assert len(data["docs"]) > 0

    @allure.title("Выбор конкретной серии в сериале")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_episode(self, api_client: KinopoiskAPI) -> None:
        """Проверка получения информации о серии."""
        movie_id: int = test_data["api"]["movie_id"]
        season_number: int = test_data["api"]["season_number"]
        episode_number: int = test_data["api"]["episode_number"]

        with allure.step("Отправить GET запрос на получение серии"):
            response = api_client.get_episode(
                movie_id, season_number, episode_number)

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200

        with allure.step("Проверить, что серия найдена"):
            data: Dict[str, Any] = response.json()
            assert len(data["docs"]) > 0

    @allure.title("Запрос без токена (негативный)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_request_without_token(self, api_client: KinopoiskAPI) -> None:
        """Проверка запроса без токена авторизации."""
        query: str = test_data["search_queries"]["full_title"]

        with allure.step("Отправить GET запрос без токена авторизации"):
            response = api_client.search_movie_no_token(query)

        with allure.step("Проверить статус код 401"):
            assert response.status_code == 401

    @allure.title("Поиск с несуществующим названием")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_nonexistent_movie(self, api_client: KinopoiskAPI) -> None:
        """Проверка поиска с несуществующим названием."""
        query: str = test_data["search_queries"]["non_existent"]

        with allure.step(f"Отправить GET запрос на поиск '{query}'"):
            response = api_client.search_nonexistent_movie(query)

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200

        with allure.step("Проверить, что список результатов пуст"):
            data: Dict[str, Any] = response.json()
            assert len(data["docs"]) == 0
