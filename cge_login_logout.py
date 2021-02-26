#from playwright import sync_playwright
from playwright.sync_api import sync_playwright
import os
import pytest
from pytest_html import extras

testenv = "https:\\cgepreview.concursolutions.com"

def log_request(intercepted_request):
    print("Request:", intercepted_request.url)

def log_failed_request(intercepted_request):
    print("FAILED Request: ",intercepted_request.url)

def log_console(msg):
    print("in console: " + msg.text)

@pytest.fixture(scope='module')
def cge_session():
    p = sync_playwright().start()
    browser_type = p.chromium
    browser = browser_type.launch(headless=True) #,slow_mo=500

    # Setup directory to store videos of runs
    # page = browser.new_page(record_video_dir="videos/")
    page = browser.new_page()

    yield page

    page.close()
    p.stop()


def test_cge_login(cge_session):
    cge_session.set_default_timeout(125000) #Set to handle gateway time out
    #cge_session.on("request", log_request)
    #cge_session.on("failedrequest", log_failed_request)
    #cge_session.on('console', log_console)

    cge_session.goto(testenv)

    assert cge_session.wait_for_selector("data-test=app-footer-links"), "TEST RESULT"
    cge_session.wait_for_load_state()
    try:
        un = os.environ['USERNAME']
    except:
        print("USERNAME environment variable not set")
        print("export USERNAME=testusername")
    try:
        pw = os.environ['PW']
    except:
        print("PW environment variable not set")
        print("export PW=testpassword")

    cge_session.fill("id=userid", un)
    cge_session.fill("id=password", pw)
    cge_session.click("id=btnSubmit")

    #print("logout")
    cge_session.set_default_timeout(30000)  # set back to 30 seconds
    # Logout
    cge_session.click("data-test=menu-profile")
    cge_session.click("data-test=user-profile-menu-signout-link")

