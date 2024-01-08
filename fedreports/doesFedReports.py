#DOES REPORTS
# Based on Python/Playwright framework with
from playwright.sync_api import sync_playwright
from models.does_claim_examiner import ClaimExaminer
import pytest
import time

fname = ""

referer = "review-app-vos11000000-ui.geosolinc.com/vosnet/Default.aspx?enc=Xdm8Yw+m50AOnLNjcWnUPg=="
list_of_fed_ETA_reports = ""
class PageError(Exception):
    """Bad Request –- Incorrect parameters."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

# Report Lists

# hooks for console, request and response
def log_console(msg):
   print("in console: " + msg.type + " " + msg.text)

def handle_download(download):
    print("DOWNLOAD:  ")
    mypdf = 'pdf/' + download.suggested_filename
    #download.save_as("pdf/" + download.suggested_filename)
    download.save_as("pdf/" + fname)
def log_request_finished(requestfinished):
    print("IN REQUEST FINISHED")

# MyTest Fixture - gets login/session for rest of the tests
@pytest.fixture(scope='module')
def myTest():
    p = sync_playwright().start()
    browser_type = p.chromium
    #browser_type = p.firefox
    # browser_type = p.webkit

    browser = browser_type.launch(channel="chrome", headless=False, slow_mo=100, devtools=False, )
    #browser = browser_type.launch(headless=False, slow_mo=100)
    page = browser.new_page(record_video_size={'width': 1280, 'height': 720 }, record_video_dir="../videos/", viewport={'width': 1280, 'height': 720})


    page.on("console", lambda msg: print(f"error: {msg.text}") if msg.type == "error" else None)
    page.on("download", handle_download)
    myTest = ClaimExaminer(page)
    return myTest
def test_federal_ETA_9021(myTest):
    report_name = "ETA_9021"
    versions = ['Continued Weeks Compensated', 'Partial/Part Total Payments']
    reports_url = "https://review-app-vos11000000-ui.geosolinc.com/vosnet/Reports/SSRS/UIFederalReports/UIFederalSearch.aspx?enc=QKBLL9RoPXllnPZmU/Iw11pffxq6X0TTX8Y9I12Ffwc55AohAK/9V7PLCghBpiRKLtuXwAtRl+RnPGHiXCz5TbY4rLjW0cvhLGo3XArZ6rj6oY97yLNM1sPCSANUuly1"

    for each_version in versions:
        try:
            myTest.does_claim.goto(reports_url, referer=referer)
            time.sleep(5)
        except:
            print("WFT HAPPENED")
            return False
        try:
            report_version = myTest.does_claim.locator("id=ctl00_Main_content_ucDWUIMainFilters_ddReportVersion")
            print(versions[1])
            report_version.select_option(label=each_version)
        except:
            print("VERSION MESSED UP")
            return False
        try:
            date_range = myTest.does_claim.locator("id=ctl00_Main_content_ucDWUIMainFilters_ddReportingPeriod")
            date_range.select_option(label="October, 2023 (10/01/2023 - 10/31/2023)")
        except:
            print("no date range found")

        try:
            myTest.does_claim.click("id=ctl00_Main_content_btnSubmit",timeout=30000)
        except:
            print("---------------------------------------") #do nothing if report has no Run Report Button

        time.sleep(10)

        global fname
        fname = report_name + '-' + each_version + '.PDF'
        for char in fname:
            if char in "/":
                fname = fname.replace(char, '-')
        mypdfprint = myTest.does_claim.wait_for_selector("[aria-label=\"Export drop down menu\"]", timeout=120000)
        myTest.does_claim.locator("[aria-label=\"Export drop down menu\"]").click()
        with myTest.does_claim.expect_download() as download_info:
            with myTest.does_claim.expect_popup() as popup_info:
                myTest.does_claim.locator("text=PDF").click()


