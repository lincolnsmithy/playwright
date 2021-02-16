from slugify import slugify
from pathlib import Path
import pytest
from datetime import datetime
import os


def pytest_runtest_makereport(item, call) -> None:
#Reporting
    ss = True
    if call.when == "call":
        for items in item.funcargs:
            print(items)
        print(dir(item.funcargs['cge_session']))
        #If error (excinfo and page is in item then get screen shot of page
        #Screen shot is taken of failed page with test name and datetime stamp
        if call.excinfo is not None and "cge_session" in item.funcargs:
            try:
                os.environ['PYTEST_CURRENT_TEST']
                testname = os.environ["PYTEST_CURRENT_TEST"]
                testname = testname.split(':')[-1].split(' ')[0]
                print("TESTNAME " + testname)
            except:
                print("NOTTATEST")
            page = item.funcargs["cge_session"]

            if ss:
                screenshot_dir = Path(".playwright-screenshots")
                screenshot_dir.mkdir(exist_ok=True)

                errorfile = testname + "-error" + datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + ".png"


                page.screenshot(path=str(screenshot_dir / errorfile))

        else:
            try:
                os.environ['PYTEST_CURRENT_TEST']
                testname = os.environ["PYTEST_CURRENT_TEST"]
                testname = testname.split(':')[-1].split(' ')[0]
                print("TESTNAME " + testname)
            except:
                print("NOTTATEST")
            page = item.funcargs['cge_session']

            if ss:
                screenshot_dir = Path(".playwright-screenshots")
                screenshot_dir.mkdir(exist_ok=True)

                errorfile = testname + "-PASS" + datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + ".png"

                page.screenshot(path=str(screenshot_dir / errorfile))
