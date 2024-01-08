from pathlib import Path
import pytest
from datetime import datetime
import os
from urllib.parse import urlparse

# conftest.py





def pytest_collection_modifyitems(items):
    """Modifies test items in place to ensure test modules run in a given order."""
    print("IN COLLECTION")
    MODULE_ORDER = ["test_register_privacy", "test_claim", "test_verify_ssn", "test_work_history", "test_states_worked", "test_federal_service", "test_military_service", "test_login_information","test_elegibility", "test_address", "test_phone", "test_notification"]
    module_mapping = {item: item.module.__name__ for item in items}

    sorted_items = items.copy()
    # Iteratively move tests of each module to the end of the test queue
    for module in MODULE_ORDER:
        sorted_items = [it for it in sorted_items if module_mapping[it] != module] + [
            it for it in sorted_items if module_mapping[it] == module
        ]
    items[:] = sorted_items



def pytest_html_report_title(report):
    report.title = os.environ['PYTEST_BASE_URL'] + ": Post Deploy Test"

def pytest_runtest_makereport(item, call):
#Reporting
    ss = False #need to command line this option for pass/fail/all
    sspass = False
    if call.when == "call":
        #If error (excinfo and page is in item then get screen shot of page
        #Screen shot is taken of failed page with test name and datetime stamp
        if call.excinfo is not None and ("myTest" in item.funcargs):
            try:
                os.environ['PYTEST_CURRENT_TEST']
                testname = os.environ["PYTEST_CURRENT_TEST"]
                #testname = testname.split(':')[-1].split(' ')[0]
                #testname = urlparse(testname).path

                print("TESTNAME " + testname)
            except:
                pass
            myTest = item.funcargs["myTest"]

            if ss:
                screenshot_dir = Path("playwright-screenshots")
                screenshot_dir.mkdir(exist_ok=True)
                errorfile = "FAIL: " + testname + "-" + datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + ".png"
                myTest.does_claim.screenshot(path=str(screenshot_dir / errorfile))
        else:
            try:
                os.environ['PYTEST_CURRENT_TEST']
                testname = os.environ["PYTEST_CURRENT_TEST"]
                #testname = testname.split(':')[-1].split(' ')[0]
                #testname = urlparse(testname).path
                #print("TESTNAME " + testname)
            except:
                pass
            myTest = item.funcargs['myTest']

            if sspass:
                screenshot_dir = Path("playwright-screenshots")
                screenshot_dir.mkdir(exist_ok=True)

                errorfile = "PASS: "+ testname + "-" + datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + ".png"
                myTest.does_claim.screenshot(path=str(screenshot_dir / errorfile))
