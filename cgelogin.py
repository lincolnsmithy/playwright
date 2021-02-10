#Sample automation for initial Post Deployment Verfication
#Simple Login and visit a number of TAVS screens
#Simple Travel View
#Based on Python/Playwright framework with py-test

from playwright.sync_api import sync_playwright
import os
import pytest
#Using Preview for now
testenv = "https:\\cgepreview.concursolutions.com"

#Login Fixture - gets login/session for rest of the tests
@pytest.fixture(scope='module')
def cge_session():
    p = sync_playwright().start()

    browser_type = p.chromium
    browser = browser_type.launch(headless=False)
#Setup directory to store videos of runs
    page = browser.new_page(record_video_dir="videos/")
    testenv = "https:\\cgepreview.concursolutions.com"

    #Goto Preview -  and login
    page.goto(testenv)
    assert page.wait_for_selector("data-test=app-footer-links"), "TEST RESULT"
    page.wait_for_load_state()
    un = os.environ['USERNAME']
    pw = os.environ['PW']
    page.fill("id=userid", un)
    page.fill("id=password", pw)
    page.click("id=btnSubmit")

#Yield connection to rest of tests / includes session info
    yield page

#Logout after all tests are run and close down session and browsers
    page.click("data-test=menu-profile")
    page.click("data-test=user-profile-menu-signout-link")
    assert page.wait_for_selector("id=btnSubmit")  # check logout worked
    page.close()
    p.stop()

def test_travel_screen(cge_session):
    print("Test Travel Screen Shows Up")
    cge_session.goto(testenv + "/travelhome.asp")
    assert cge_session.wait_for_selector("id=TMAIR_searchRefPoint0")

def _test_travel_perdiem_location(cge_session):
    cge_session.goto(testenv + "/travelhome.asp")
    assert cge_session.wait_for_selector("id=TMAIR_searchRefPoint0")

#Choose PerDiem Location
    cge_session.type("[id=TMAIR_searchRefPoint0]", "Boston")
    cge_session.click("[id=TMAIR_TM_Findlocation0]")
    cge_session.click("[id=geocodechoosebutton]")
    cge_session.click("[id=fltArrCityDisplay0]")
    cge_session.keyboard.press('Enter')

    #Select From
    cge_session.focus("[id=fltDepCityDisplay0]")
    cge_session.type("[id=fltDepCityDisplay0]", "LAX",timeout=5000)
    cge_session.keyboard.press('Enter')
    cge_session.dblclick("[id=fltDepCityDisplay0]")

    print(cge_session.get_attribute("[id=fltDepCityDisplay0]", name="text"))

    #Date Picker:)
    cge_session.fill("[id=fltDate0]", "02/10/2021")
    cge_session.keyboard.press('Tab')

    cge_session.fill("[id=fltDate1]", "02/27/2021")
    cge_session.keyboard.press('Tab')

    #cge_session.type("[id=fltArrCityDisplay0]","BOS - Boston Logan Intl Airport - Boston, MA", timeout=5000)
    #cge_session.keyboard.press('Tab')

    cge_session.click("[id=btnAirLaunchWizard]")

    cge_session.screenshot(path=f'exampleTravel.png')

def test_auth_screen(cge_session):
    cge_session.goto(testenv + "/TravelManagerFrame.asp?MenuClicked=Authorization&MenuItem=View")
    assert cge_session.wait_for_selector("data-test=menu__anchor-travelmanagerauthorization_0")
    cge_session.frames[2].wait_for_load_state('networkidle',timeout=30000)
    cge_session.screenshot(path=f'exampleauth.png')

def test_voucher_screen(cge_session):
    cge_session.goto(testenv + "/TravelManagerFrame.asp?MenuClicked=Voucher&MenuItem=View")
    assert cge_session.wait_for_selector("data-test=menu__anchor-travelmanagervoucher_0")
    cge_session.frames[2].wait_for_load_state('networkidle')
    cge_session.screenshot(path=f'examplevoucher.png')

def test_approval_screen(cge_session):
    cge_session.goto(testenv + "/TravelManagerFrame.asp?MenuClicked=Approval&MenuItem=All")
    assert cge_session.wait_for_selector("data-test=menu__anchor-travelmanagervoucher")
    cge_session.frames[2].wait_for_load_state('networkidle')
    cge_session.screenshot(path=f'exampleapprovals.png')

def test_new_auth_screen(cge_session):
    cge_session.goto(testenv + "/TravelManagerFrame.asp?MenuClicked=Authorization&MenuItem=New")
    cge_session.frames[2].wait_for_load_state('networkidle')
    cge_session.screenshot(path=f'newauth.png')