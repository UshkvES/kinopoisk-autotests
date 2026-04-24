"""UI тесты для Кинопоиска."""

import json
import os
from typing import Dict, Any
import allure
import pytest
from pages.main_page import MainPage

# Загрузка тестовых данных из JSON
current_dir: str = os.path.dirname(__file__)
json_path: str = os.path.join(current_dir, '..', 'config', 'test_data.json')
with open(json_path, 'r', encoding='utf-8') as f:
    test_data: Dict[str, Any] = json.load(f)


@allure.epic("UI Тесты")
@allure.feature("Поиск фильмов")
@allure.story("Проверка поиска на Кинопоиске")
@pytest.mark.ui
class TestUISearch:

    @allure.title("Поиск фильма по полному названию")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_search_by_full_title(self, driver) -> None:
        """Проверка поиска по полному названию фильма."""
        query: str = test_data["search_queries"]["full_title"]
        main_page = MainPage(driver)

        with allure.step(f"Поиск фильма '{query}'"):
            main_page.search(query)

        with allure.step("Проверить наличие результатов"):
            assert main_page.has_results(), \
                f"Результаты для '{query}' не найдены"

    @allure.title("Поиск с пустой строкой")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_empty_query(self, driver) -> None:
        """Проверка поиска с пустой строкой."""
        query: str = test_data["search_queries"]["empty"]
        main_page = MainPage(driver)

        with allure.step("Выполнить поиск с пустой строкой"):
            main_page.search(query)

        with allure.step("Проверить, что страница загрузилась"):
            current_url: str = main_page.get_current_url()
            assert "error" not in current_url.lower(), \
                f"Ошибка: {current_url}"

    @allure.title("Поиск с несуществующим названием")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_nonexistent_query(self, driver) -> None:
        """Проверка поиска с несуществующим названием."""
        query: str = test_data["search_queries"]["non_existent"]
        main_page = MainPage(driver)

        with allure.step(f"Поиск запроса '{query}'"):
            main_page.search(query)

        with allure.step("Проверить, что ничего не найдено"):
            assert main_page.has_no_results(), \
                f"Найдены результаты для несуществующего запроса '{query}'"

    @allure.title("Поиск по жанру")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_by_genre(self, driver) -> None:
        """Проверка поиска по жанру."""
        genre: str = test_data["filters"]["genre"]
        main_page = MainPage(driver)

        with allure.step(f"Поиск фильмов жанра '{genre}'"):
            url: str = f"https://www.kinopoisk.ru/search/?genres={genre}"
            main_page.open(url)

        with allure.step("Проверить наличие результатов"):
            assert main_page.has_results(), \
                f"Результаты для жанра '{genre}' не найдены"

    @allure.title("Поиск с фильтрами без результатов")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_no_results_filters(self, driver) -> None:
        """Проверка поиска с фильтрами без результатов."""
        genre: str = test_data["filters"]["genre"]
        country: str = test_data["filters"]["country"]
        y_from: int = test_data["filters"]["year_from"]
        y_to: int = test_data["filters"]["year_to"]
        main_page = MainPage(driver)

        params: str = (f"genres={genre}&countries={country}"
                       f"&yearFrom={y_from}&yearTo={y_to}")
        url: str = f"https://www.kinopoisk.ru/search/?{params}"

        with allure.step("Переход на страницу поиска с фильтрами"):
            main_page.open(url)

        with allure.step("Проверить, что ничего не найдено"):
            assert main_page.has_no_results(), \
                "Найдены результаты, хотя фильтры не должны давать результатов"
