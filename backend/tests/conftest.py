import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--run-openai", 
        action="store_true", 
        default=False,
        help="run tests that require the OpenAI API"
    )

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "external_api: mark test as requiring an external API call (e.g., OpenAI)"
    )

def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-openai"):
        # if the flag is set, do not skip external API tests
        return
    skip_openai = pytest.mark.skip(reason="need --run-openai option to run")
    for item in items:
        if "external_api" in item.keywords:
            item.add_marker(skip_openai)
