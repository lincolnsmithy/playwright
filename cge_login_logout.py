#from playwright import sync_playwright
from playwright.sync_api import sync_playwright
import os
import pytest

testenv = "https:\\cgepreview.concursolutions.com"

def log_request(intercepted_request):
    print("Request:", intercepted_request.url)

def log_failed_request(intercepted_request):
    print("FAILED Request: ",intercepted_request.url)

def test_cge_session(page):
    page.set_default_timeout(125000) #Set to handle gateway time out
    page.on("request", log_request)
    page.on("failedrequest", log_failed_request)
    page.goto(testenv)
    assert page.wait_for_selector("data-test=app-footer-links"), "TEST RESULT"
    page.wait_for_load_state()
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

    page.type("id=userid", un)
    page.type("id=password", pw)
    page.click("id=btnSubmit")

    print("logout")
    page.set_default_timeout(30000) #set back to 30 seconds
#Logout
    page.click("data-test=menu-profile")
    page.click("data-test=user-profile-menu-signout-link")
