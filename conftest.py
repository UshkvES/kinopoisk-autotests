"""Фикстуры для тестов."""

from typing import Generator
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config.settings import Config
from api.kinopoisk_api import KinopoiskAPI


@pytest.fixture(scope="session")
def api_client() -> KinopoiskAPI:
    """Фикстура для API тестов."""
    return KinopoiskAPI()


@pytest.fixture(scope="function")
def driver() -> Generator[webdriver.Chrome, None, None]:
    """Фикстура для UI тестов."""
    with allure.step("Запуск Chrome браузера"):
        options: Options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver: webdriver.Chrome = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        driver.implicitly_wait(Config.IMPLICIT_WAIT)

    yield driver

    with allure.step("Закрытие браузера"):
        driver.quit()


def pytest_addoption(parser: pytest.Parser) -> None:
    """Добавление кастомных опций для pytest."""
    parser.addoption(
        "--run-api",
        action="store_true",
        default=False,
        help="Запустить только API тесты"
    )
    parser.addoption(
        "--run-ui",
        action="store_true",
        default=False,
        help="Запустить только UI тесты"
    )


def pytest_collection_modifyitems(config: pytest.Config, items: list) -> None:
    """Модификация сбора тестов для фильтрации по опциям."""
    run_api: bool = config.getoption("--run-api")
    run_ui: bool = config.getoption("--run-ui")

    if run_api and not run_ui:
        items[:] = [item for item in items if "api" in item.keywords]
    elif run_ui and not run_api:
        items[:] = [item for item in items if "ui" in item.keywords]
