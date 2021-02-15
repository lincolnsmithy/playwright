from slugify import slugify
from pathlib import Path
import pytest
from datetime import datetime

def pytest_runtest_makereport(item, call) -> None:
    #print("INREPORT")
    if call.when == "call":
        if call.excinfo is not None and "page" in item.funcargs:
            page = item.funcargs["page"]
            screenshot_dir = Path(".playwright-screenshots")
            screenshot_dir.mkdir(exist_ok=True)
            errorfile = "error" + datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

            page.screenshot(path=str(screenshot_dir / errorfile))
            print("After Screenshot Report")

