from slugify import slugify
from pathlib import Path
import pytest

def pytest_runtest_makereport(item, call) -> None:
    #print("INREPORT")
    if call.when == "call":
        if call.excinfo is not None and "page" in item.funcargs:
            page = item.funcargs["page"]
            screenshot_dir = Path(".playwright-screenshots")
            screenshot_dir.mkdir(exist_ok=True)
            page.screenshot(path=str(screenshot_dir / "tester.png"))
            print("After Screenshot Report")

