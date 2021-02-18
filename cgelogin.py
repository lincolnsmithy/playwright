#Sample automation for initial Post Deployment Verfication
#Simple Login and visit a number of TAVS screens
#Simple Travel View
#Based on Python/Playwright framework with py-test

from playwright.sync_api import sync_playwright
import pytest
import os
#Using Preview for now
#testenv = "https:\\cgepreview.concursolutions.com"
testenv = os.environ['PYTEST_BASE_URL'] #Global Test BASE URL - note:pytest_base_url not really working

#hook for printing out cosole message
def log_console(msg):
    print("in console: " + msg.type + " " +msg.text)

#Login Fixture - gets login/session for rest of the tests
@pytest.fixture(scope='module')
def cge_session():
    p = sync_playwright().start()
    browser_type = p.firefox
    browser = browser_type.launch(headless=False,slow_mo=500)

    #Setup directory to store videos of runs - another argument needs to be implemented to support
    #
    page = browser.new_page(record_video_dir="videos/")

    page = browser.new_page()
    #print("PAGEURL: " + page.url)
    page.on('console', log_console) #send page console messages to log_console

    page.goto(testenv) #testenv set globally above
    #assert page.wait_for_selector("data-test=app-footer-links"), "TEST RESULT"
    page.wait_for_load_state()
    un = os.environ['USERNAME']
    pw = os.environ['PW']
    page.fill("id=userid", un)
    page.fill("id=password", pw)
    page.click("id=btnSubmit")

#Yield connection to rest of tests / includes session info
    yield page

#Logout after all tests are run and close down session and browsers
    #page.click("data-test=menu-profile")
    page.click('text=Profile')
    page.click('text=Sign Out')
    #page.click("data-test=user-profile-menu-signout-link")
    assert page.wait_for_selector("id=btnSubmit")  # check logout worked
    page.close()
    p.stop()

def test_travel_screen(cge_session):
    #print("Test Travel Screen Shows Up")
    cge_session.goto(testenv + "/travelhome.asp")
    assert cge_session.wait_for_selector("id=TMAIR_searchRefPoint0")

def test_travel_perdiem_location(cge_session):
    cge_session.goto(testenv + "/travelhome.asp")
    assert cge_session.wait_for_selector("id=TMAIR_searchRefPoint0")
    #Choose PerDiem Location
    cge_session.fill("[id=TMAIR_searchRefPoint0]", "Boston")
    cge_session.click("[id=TMAIR_TM_Findlocation0]")
    cge_session.click("[id=geocodechoosebutton]")
    cge_session.type("[id=fltDepCityDisplay0]", "LAX")
    cge_session.keyboard.press("Tab")
    #cge_session.click("[id=fltDepCityDisplay0_airAC0]",timeout=5000)
    #cge_session.dblclick("[id=fltDepCityDisplay0]")
    print(cge_session.get_attribute("[id=fltDepCityDisplay0]", name="text"))

    #Date Picker:)
    cge_session.fill("[id=fltDate0]", "02/27/2021")
    cge_session.keyboard.press('Tab')

    cge_session.fill("[id=fltDate1]", "03/27/2021")
    cge_session.keyboard.press('Tab')

    cge_session.click("[id=btnAirLaunchWizard]")
    #cge_session.screenshot(path=f'exampleTravel.png')
    cge_session.wait_for_selector("[id=resultsSummaryDiv]",timeout=180000)

def test_auth_screen(cge_session):
    cge_session.goto(testenv + "/TravelManagerFrame.asp?MenuClicked=Authorization&MenuItem=View")
    cge_session.wait_for_load_state('networkidle',timeout=30000)
    #assert cge_session.wait_for_selector("data-test=menu__anchor-travelmanagerauthorization_0")
    assert cge_session.frames[2].wait_for_selector("id=DocumentFrame")

def test_voucher_screen(cge_session):
    print(testenv)
    cge_session.goto(testenv + "/TravelManagerFrame.asp?MenuClicked=Voucher&MenuItem=View")
    cge_session.wait_for_load_state()
    assert cge_session.frames[2].wait_for_selector("id=DocumentFrame")

def test_approval_screen(cge_session):
    cge_session.goto(testenv + "/TravelManagerFrame.asp?MenuClicked=Approval&MenuItem=All")
    cge_session.wait_for_load_state('networkidle',timeout=30000)
    #assert cge_session.wait_for_selector("data-test=menu__anchor-travelmanagervoucher")
    assert cge_session.frames[2].wait_for_selector("id=DocumentFrame")
    
def test_new_auth_screen(cge_session):
    cge_session.goto(testenv + "/TravelManagerFrame.asp?MenuClicked=Authorization&MenuItem=New")
    cge_session.wait_for_load_state('networkidle')
    assert cge_session.frames[2].wait_for_selector("id=DocumentFrame")
