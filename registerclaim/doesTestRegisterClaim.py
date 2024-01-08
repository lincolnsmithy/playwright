# Sample automation for initial Post Deployment Verfication
# Simple Login and visit a number of TAVS screens
# Simple Travel View
# Based on Python/Playwright framework with py-test
from faker import Faker
from playwright.sync_api import sync_playwright
from models.does_register_claim import DoesFrontPage
import pytest

fake = Faker()

# hooks for console, request and response
#def log_console(msg):
#   print("in console: " + msg.type + " " + msg.text)
def log_dialog(dialog):
    print("WFT Dialgo")
    print(dialog.title())

def log_popup(popup):
    print("WFT POPUP")
    print(popup.title())

def log_request(requestfinished):
    print("REQUEST: ")
    headers = requestfinished.headers
    print(headers)

def log_response(response):
    print("REPSONSE: ")
    respheader = response.headers
    print(respheader)

def myRegistration():
    p = sync_playwright().start()
    #browser_type = p.chromium
    #browser_type = p.firefox
    browser_type = p.webkit
    #browser = browser_type.launch(channel="chrome",headless=False, slow_mo=100)

    browser = browser_type.launch(headless=False, slow_mo=100)

    context = browser.new_context(viewport={'width': 1024, 'height': 768 })

    context = browser.new_context()
    # Create Fake Profile
    profile = fake.profile()

    #page = context.new_page()
    #page = browser.new_page(record_video_dir=".videos/")

    page = browser.new_page(record_video_size={'width': 1024, 'height': 768 }, record_video_dir=".videos/", viewport={'width': 2048, 'height': 2048})

    #page.video.save_as("videos/register.webm")
    #page.on('response', log_response)
    page.on('popup', log_popup)
    page.on("dialog", log_dialog)

    myTest = DoesFrontPage(page)

    myTest.register_privacy()
    #page.pause()

    myTest.claim()
    #page.pause()

    myTest.verify_ssn()
    #page.pause()

    myTest.work_history(True)
    #page.pause()

    myTest.states_worked()
    #page.pause()

    myTest.federal_service()
    #page.pause()

    myTest.military_service()
    #page.pause()

    myTest.login_information()
    #page.pause()

    myTest.elegibility()
    #page.pause()

    myTest.address()
    #page.pause()


    myTest.phone()
    #page.pause()

    myTest.notification()
    #page.pause()

    myTest.wft()
    page.pause




# Login Fixture - gets login/session for rest of the tests
@pytest.fixture(scope='module')
def myTest():
    p = sync_playwright().start()
    browser_type = p.chromium
    #browser_type = p.firefox
    # browser_type = p.webkit
    browser = browser_type.launch(channel= "chrome",headless=False, slow_mo=100)

    context = browser.new_context(viewport={'width': 2048, 'height': 2048 })

    context = browser.new_context()
    # Create Fake Profile
    profile = fake.profile()

    #page = context.new_page()
    #page = browser.new_page(record_video_dir=".videos/")

    page = browser.new_page(record_video_size={'width': 2048, 'height': 2048 }, record_video_dir=".videos/", viewport={'width': 2048, 'height': 2048})

    #page.video.save_as("videos/register.webm")
    #page.on('response', log_response)
    #page.on('request', log_request)

    myTest = DoesFrontPage(page)

    yield myTest

def test_register_privacy(myTest):

    assert (myTest.register_privacy()) == True

def test_claim(myTest):

   assert (myTest.claim()) == True


def test_verify_ssn(myTest):
    assert (myTest.verify_ssn()) == True

def test_work_history(myTest):
    assert (myTest.work_history(work=True)) == True

def test_states_worked(myTest):
    assert (myTest.states_worked()) == True

def test_federal_service(myTest):
    assert (myTest.federal_service()) == True

def test_military_service(myTest):
    assert (myTest.military_service()) == True

def test_login_information(myTest):
    assert (myTest.login_information()) == True

def test_elegibility(myTest):
    assert (myTest.elegibility()) == True

def test_address(myTest):
    assert (myTest.address()) == True

def test_phone(myTest):
    assert (myTest.phone()) == True

def test_notification(myTest):
    assert (myTest.notification()) == True


myRegistration()


