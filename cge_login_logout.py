#from playwright import sync_playwright
from playwright.sync_api import sync_playwright
import os
import pytest

testenv = "https:\\cgepreview.concursolutions.com"
#testenv = os.environ['ENV']
#@pytest.fixture(scope='module')
#@pytest.fixture()

def log_request(intercepted_request):
    print("a request was made:", intercepted_request.url)

def log_failed_request(intercepted_request):
    print("FAILED REQUEST: ",intercepted_request.url)

#def log_requestinfo(intercepted_requestinfo):
    #print("requestinfo: ", intercepted_requestinfo.headers["x-edgeconnect-origin-mex-latency"])
#    if "x-edgeconnect-origin-mex-latency" in intercepted_requestinfo.headers.keys():
#        print("x-edgeconnect-origin-mex-latency: ",intercepted_requestinfo.headers["x-edgeconnect-origin-mex-latency"])

def test_cge_session(page):
    #p = sync_playwright().start()
    page.set_default_timeout(125000) #Set to handle gateway time out

    page.on("request", log_request)
    page.on("failedrequest", log_failed_request)
    #page.on("response", log_requestinfo)

    page.goto(testenv)
    assert page.wait_for_selector("data-test=app-footer-links"), "TEST RESULT"
    page.wait_for_load_state()
    un = os.environ['USERNAME']
    pw = os.environ['PW']
    #print(un)

    page.type("id=userid", un)
    page.type("id=password", pw)
    page.click("id=btnSubmit")

    #assert page.wait_for_selector("id=sidebar1")
    print(page.context.cookies())

    print("logout")
    page.set_default_timeout(10000) #Set to handle gateway time out

    page.click("data-test=menu-profile")
    page.click("data-test=user-profile-menu-signout-link")
    #p.stop
    #page.remove_listener("request", log_request)
   # page.remove_listener("failedrequest", log_failed_request)