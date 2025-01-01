import sys
import pytest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException,WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Logging Configuration
log_file = 'selenium_test.log'
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# Constants
SELENIUM_URL = "https://www.lambdatest.com/selenium-playground/table-sort-search-demo"
SEARCH_INPUT_SELECTOR = "#example_filter input[type='search']"
RESULT_INFO_ID = "example_info"

BROWSER_CHOICES = {
    'chrome': ChromeService(ChromeDriverManager().install()),
    'firefox': FirefoxService(GeckoDriverManager().install(),log_output=sys.stdout),
    'edge': EdgeService(EdgeChromiumDriverManager().install())
}

class TestTableSearch:

    @pytest.fixture(scope="class")
    def setup(self, request):
        """Setup WebDriver for Chrome and Firefox browsers based on user input."""

        browser = request.config.getoption("--browser", default="chrome")
        if browser not in BROWSER_CHOICES:
            pytest.fail(f"Unsupported browser: {browser}. Only 'chrome' and 'firefox' are supported.")

        logger.info(f"Initializing WebDriver for {browser}.")
        try:
            if browser == 'chrome':
                self.driver = webdriver.Chrome(service=BROWSER_CHOICES['chrome'])
            elif browser == 'firefox':
                self.driver = webdriver.Firefox(service=BROWSER_CHOICES['firefox'])
            elif browser == 'edge':
                self.driver = webdriver.Edge(service=BROWSER_CHOICES['edge'])
        except WebDriverException as we:
            logger.error("Falling back to chrome as firefox browser  or driver not available")
            logger.exception(e)
            self.driver = webdriver.Chrome(service=BROWSER_CHOICES['chrome'])
        except Exception as e:
            logger.exception(e)

        self.driver.maximize_window()
        yield self.driver
        logger.info("Quitting the browser.")
        self.driver.quit()

    """Navigate to the Selenium URL."""
    def navigate_to_page(self):
        logger.info(f"Navigating to the page: {SELENIUM_URL}")
        self.driver.get(SELENIUM_URL)

    """Perform a search operation for a specific term."""
    def perform_search(self, search_term):
        logger.info(f"Performing search for: {search_term}")
        try:
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, SEARCH_INPUT_SELECTOR))
            )
            search_box.clear()
            search_box.send_keys(search_term)
        except TimeoutException:
            logger.error(f"Search box not found after waiting.")
            pytest.fail(f"Search box was not located on the page.")
        except NoSuchElementException:
            logger.error("Search box element is missing from the DOM.")
            pytest.fail(f"Search box not found.")

    def get_search_results_text(self):
        """Extract the text from the result info box."""
        logger.info("Fetching search result text.")
        try:
            result_info = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, RESULT_INFO_ID))
            )
            return result_info.text
        except TimeoutException:
            logger.error("Result info not found or took too long to load.")
            pytest.fail("Result info element not found.")
        except NoSuchElementException:
            logger.error("Result info element is missing from the DOM.")
            pytest.fail("Result info element not found.")
        return ""

    def validate_results(self, search_term, expected_count):
        """Validate that the search results match the expected count."""
        result_text = self.get_search_results_text()
        logger.info(f"Result Info Text: {result_text}")
        # Extract the actual count of entries from the result text
        assert f"filtered from 24 total entries" in result_text, \
            f"Expected 'filtered from 24 total entries' but got: {result_text}"
        assert f"Showing 1 to {expected_count} of {expected_count}" in result_text, \
            f"Expected '{expected_count}' entries but got: {result_text}"

    @pytest.mark.parametrize("search_term, expected_count", [
        ("New York", 5),
        ("San Francisco", 3),
        ("Chicago", 1)
    ])
    def test_search_and_validate(self, setup, search_term, expected_count):
        self.driver = setup
        self.navigate_to_page()
        self.perform_search(search_term)
        self.validate_results(search_term, expected_count)
        logger.info(f"Search and validation test passed for '{search_term}'.")


if __name__ == "__main__":
    pytest.main(["-v", "--tb=short", "--disable-warnings"])
