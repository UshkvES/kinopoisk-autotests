"""Главная страница Кинопоиска."""

import time
from typing import List
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
from config.settings import Config, Selectors


class MainPage(BasePage):
    """Класс для работы с главной страницей."""

    def __init__(self, driver: WebElement) -> None:
        """Инициализация главной страницы."""
        super().__init__(driver)

    @allure.step("Поиск по тексту '{query}'")
    def search(self, query: str) -> None:
        """Выполнить поиск по тексту."""
        self._driver.get(Config.UI_URL)
        time.sleep(2)

        search_input: WebElement = self.find_element(Selectors.SEARCH_INPUT)
        search_input.clear()
        search_input.send_keys(query)
        time.sleep(1)

        search_input.send_keys(Keys.RETURN)
        time.sleep(3)

    @allure.step("Открыть URL {url}")
    def open(self, url: str) -> None:
        """Открыть указанный URL."""
        self._driver.get(url)
        time.sleep(2)

    @allure.step("Проверить наличие результатов")
    def has_results(self) -> bool:
        """Проверить, есть ли результаты поиска."""
        time.sleep(2)

        selectors: List[str] = [
            Selectors.RESULT_ITEM,
            "a[href*='/film/']",
            ".search_results__item",
            "[data-tid='movie-card']"
        ]

        for selector in selectors:
            elements: List[WebElement] = self._driver.find_elements(
                By.CSS_SELECTOR, selector
            )
            if len(elements) > 0:
                allure.attach(
                    f"Найдено {len(elements)} результатов",
                    "Результаты поиска",
                    allure.attachment_type.TEXT
                )
                return True
        return False

    @allure.step("Проверить отсутствие результатов")
    def has_no_results(self) -> bool:
        """Проверить, что ничего не найдено."""
        time.sleep(2)

        page_text: str = self._driver.page_source.lower()

        expected: str = "к сожалению, по вашему запросу ничего не найдено..."

        if expected in page_text:
            return True

        alt_expected: str = "к сожалению, по вашему запросу ничего не найдено"
        if alt_expected in page_text:
            return True

        if not self.has_results():
            return True

        return False
