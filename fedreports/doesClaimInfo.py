#DOES REPORTS
# Based on Python/Playwright framework with py-test
import os

import bs4
from playwright.sync_api import sync_playwright
from models.does_claim_examiner import ClaimExaminer
import pytest
import time
from urllib.parse import urlparse

#referer = "https://uat-app-vos11000000-ui.geosolinc.com/vosnet/"
referer = "https://review-app-vos11000000-ui.geosolinc.com/vosnet/"
#referer ="https://review-app-vos11000000-ui.geosolinc.com/vosnet/Reports/ReportMenu.aspx?enc=5sxDU1ufe4mY7HvrDnhvag=="


class PageError(Exception):
    """Bad Request –- Incorrect parameters."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


# hooks for console, request and response
def log_console(msg):
   print("in console: " + msg.type + " " + msg.text)

def handle_download(download):
    print("DOWNLOAD:  ")
    mypdf = 'pdf/' + download.suggested_filename
    download.save_as("pdf/" + download.suggested_filename)


def log_request_finished(requestfinished):
    print("IN REQUEST FINISHED")

# MyTest Fixture - gets login/session for rest of the tests
@pytest.fixture(scope='module')
def myTest():
    p = sync_playwright().start()
    browser_type = p.chromium
    #browser_type = p.firefox
    # browser_type = p.webkit

    browser = browser_type.launch(channel="chrome", headless=False, slow_mo=100, devtools=True, )
    #browser = browser_type.launch(headless=False, slow_mo=100)

    #context = browser.new_context(viewport={'width': 2048, 'height': 2048 })

    #page = context.new_page()

    page = browser.new_page(record_video_size={'width': 2048, 'height': 2048 }, record_video_dir="../videos/", viewport={'width': 2048, 'height': 2048})

    #page.video.save_as("videos/register.webm")
    #page.on('response', log_response)
    #page.on('load', log_response)
    #page.on('requestfinished',log_request_finished)
    # Listen for all console events and handle errors
    #page.on("console", lambda msg: print(f"error: {msg.text}") if msg.type == "error" else None)
    page.on("download", handle_download)

    myTest = ClaimExaminer(page)

    return myTest

def log_response(response):
    try:
        body = response.body()

        txtbody = body.decode('UTF-8','ignore')
        #print(txtbody)
        if "You have encountered an error in the system" in txtbody:
            print("ERROR FIELD")
    except:
        assert False

def test_get_info(myTest):
    print("WHAT")
    myTest.does_claim.goto("https://review-app-vos11000000-ui.geosolinc.com/vosnet/MenuLandingPage.aspx?enc=JCztPGRxiYcCr5ufgMs/8G23v6r6uxOzE8346srCMgI=",referer=referer)

    myTest.does_claim.


