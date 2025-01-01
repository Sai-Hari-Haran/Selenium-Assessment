def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     help="Type of browser to use for testing (chrome or firefox or edge)")
