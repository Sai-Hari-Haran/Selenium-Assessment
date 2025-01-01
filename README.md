
# Selenium Assessment

This assessment contains automated tests using `Selenium` and `pytest` for verifying table search functionality on [selenium-playgorund](https://www.lambdatest.com/selenium-playground/table-sort-search-demo)

## Prerequisites

Before running the tests, ensure you have the following installed:

- Python 3.7+
- Google Chrome, Mozilla Firefox or Edge browser (depending on which browser you'd like to run the tests on)
- Pip (Python package manager)

## Setting Up the Environment

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Sai-Hari-Haran/Selenium-Assessment.git
   cd Selenium-Assessment
   ```

2. **Create a virtual environment (optional but recommended)**:
   ```bash
   python -m venv .env # inplace of .env you can give your own environment name
   source .env/bin/activate  # On Windows use: .env\Scripts\activate
   ```

3. **Install the required Python packages**:
   All the dependencies are listed in the `requirements.txt` file. Install them by running:
   ```bash
   pip install -r requirements.txt
   ```

   If you don't have the `requirements.txt` file, use the following commands to manually install the necessary packages:
   ```bash
   pip install pytest selenium webdriver_manager
   ```

## Test Configuration

This project uses `webdriver_manager` to automatically download and manage the browser drivers for Chrome, Firefox and Edge. You don't need to manually download the drivers. If you want you can but paths has to be provided

### Supported Browsers

- **Google Chrome** (Default)
- **Mozilla Firefox**
- **Microsoft Edge**

### Command-Line Options

You can specify the browser when running the tests. If no browser is specified, Chrome will be used by default.

## Running the Tests

### Option 1: Run with Default Browser (Chrome)

To run the tests using the default browser (Chrome), use the following command:
```bash
pytest qa_selenium_test.py
```

### Option 2: Run with Firefox

To run the tests with Firefox, specify the `--browser` option as follows:
```bash
pytest qa_selenium_test.py --browser firefox
```

### Option 3: Run with Edge

To run the tests with Edge, specify the `--browser` option as follows:
```bash
pytest qa_selenium_test.py --browser edge
```

If Firefox is not installed on your system, the test will automatically fallback to Chrome.

### Example Usage

1. **Run with Chrome (default)**:
   ```bash
   pytest qa_selenium_test.py
   ```

2. **Run with Firefox**:
   ```bash
   pytest qa_selenium_test.py --browser firefox
   ```
   
3. **Run with Edge**:
   ```bash
   pytest qa_selenium_test.py --browser edge
   ```

### Viewing the Logs

Logs for each test run are saved in the `selenium_test.log` file. You can view the logs for debugging or test progress:
```bash
cat selenium_test.log
```

## Test Description

The tests verify the functionality of the table search feature on a given webpage. Specifically, the tests:

1. Navigate to the URL provided.
2. Perform search operations for specific terms.
3. Validate the search results by comparing them against expected values.

### Parameters:

- **Search terms**: `New York`, `San Francisco`, `Chicago` (as examples).
- **Expected result count**: The number of entries that should be displayed for each search term.

## Dependencies

- `pytest`: Used as the test runner.
- `selenium`: Web browser automation.
- `webdriver_manager`: Automatically handles browser driver downloads.
  
## Troubleshooting

- **Browser not launching**: Ensure the browser (Chrome or Firefox or Edge) is installed on your machine.
- **Driver download issues**: The browser drivers are cached for 7 days by default to avoid re-downloading on each run. If the drivers are not being downloaded, check your internet connection or run the script with elevated permissions.
  
## Additional Notes

- If using Firefox and you encounter issues with missing drivers or geckodriver logs, ensure you have the correct version of Firefox installed.
  
