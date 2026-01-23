# gestorsei/webdriver_factory.py
import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

def create_firefox_driver(
    firefox_binary: str,
    gecko_log_path: str,
    geckodriver_path: str | None = None,
    headless: bool = False,
):
    options = Options()
    if firefox_binary:
        options.binary_location = firefox_binary
    if headless:
        options.add_argument("--headless")

    if not geckodriver_path:
        geckodriver_path = os.environ.get("GECKODRIVER_PATH")

    if not geckodriver_path:
        # fallback webdriver-manager
        from webdriver_manager.firefox import GeckoDriverManager
        geckodriver_path = GeckoDriverManager().install()

    service = Service(executable_path=geckodriver_path, log_output=gecko_log_path)
    return webdriver.Firefox(service=service, options=options)
