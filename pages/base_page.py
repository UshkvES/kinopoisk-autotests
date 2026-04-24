"""Базовый класс для всех PageObject."""

from typing import Optional, List
import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config.settings import Config, Selectors


class BasePage:
    """Базовый класс с общими методами для страниц."""

    def __init__(self, driver: WebDriver) -> None:
        """Инициализация базовой страницы."""
        self._driver: WebDriver = driver
        self._wait: WebDriverWait = WebDriverWait(driver, Config.EXPLICIT_WAIT)

    @allure.step("Открыть страницу {url}")
    def open(self, url: str) -> None:
        """Открыть указанную страницу."""
        self._driver.get(url)

    @allure.step("Найти элемент по селектору {selector}")
    def find_element(self, selector: str,
                     timeout: Optional[int] = None) -> WebElement:
        """Найти элемент с ожиданием."""
        wait_time = timeout or Config.EXPLICIT_WAIT
        wait = WebDriverWait(self._driver, wait_time)
        return wait.until(EC.presence_of_element_located(
            ("css selector", selector)
        ))

    @allure.step("Найти все элементы по селектору {selector}")
    def find_elements(self, selector: str,
                      timeout: Optional[int] = None) -> List[WebElement]:
        """Найти все элементы с ожиданием."""
        wait_time = timeout or Config.EXPLICIT_WAIT
        wait = WebDriverWait(self._driver, wait_time)
        return wait.until(EC.presence_of_all_elements_located(
            ("css selector", selector)
        ))

    @allure.step("Кликнуть на элемент {selector}")
    def click(self, selector: str) -> None:
        """Кликнуть на элемент."""
        element: WebElement = WebDriverWait(
            self._driver, Config.EXPLICIT_WAIT
        ).until(EC.element_to_be_clickable(("css selector", selector)))
        element.click()

    @allure.step("Ввести текст '{text}' в поле {selector}")
    def input_text(self, selector: str, text: str) -> None:
        """Ввести текст в поле ввода."""
        element: WebElement = self.find_element(selector)
        element.clear()
        element.send_keys(text)

    @allure.step("Получить текущий URL")
    def get_current_url(self) -> str:
        """Получить текущий URL страницы."""
        return self._driver.current_url

    @allure.step("Получить текст элемента {selector}")
    def get_text(self, selector: str) -> str:
        """Получить текст элемента."""
        element: WebElement = self.find_element(selector)
        return element.text

    @allure.step("Проверить видимость элемента {selector}")
    def is_element_visible(self, selector: str,
                           timeout: Optional[int] = None) -> bool:
        """Проверить, виден ли элемент."""
        try:
            wait_time = timeout or 5
            wait = WebDriverWait(self._driver, wait_time)
            wait.until(EC.visibility_of_element_located(
                ("css selector", selector)
            ))
            return True
        except TimeoutException:
            return False

    @allure.step("Закрыть модальные окна")
    def close_modals(self) -> None:
        """Закрыть все модальные окна."""
        self._driver.execute_script(
            "var event = new KeyboardEvent('keydown', {key: 'Escape'});"
            "document.dispatchEvent(event);"
        )

    @allure.step("Принять куки")
    def accept_cookies(self) -> None:
        """Принять куки, если кнопка видна."""
        if self.is_element_visible(Selectors.COOKIE_ACCEPT, 3):
            try:
                self.click(Selectors.COOKIE_ACCEPT)
            except Exception:
                pass
