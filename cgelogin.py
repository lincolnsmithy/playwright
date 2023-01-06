#Sample automation for initial Post Deployment Verfication
#Simple Login and visit a number of TAVS screens
#Simple Travel View
#Based on Python/Playwright framework with py-test

from playwright.sync_api import sync_playwright
import pytest
import os
import json


testenv = os.environ['PYTEST_BASE_URL'] #Global Test BASE URL - note:pytest_base_url not really working

#hooks for console, request and response
def log_console(msg):
    print("in console: " + msg.type + " " +msg.text)

def log_request(requestfinished):
    print("REQUEST: ")
    headers = requestfinished.headers
    print(headers)

def log_response(response):
    print("REPSONSE: ")
    respheader = response.headers
    print(respheader)

#Pull TAVSSESSIONID our of Cookies
#Useful for Kibana search  session_id:"TAVSSESSIONID"
def get_tavs_sessionid(page):
    mycookies = page.context.cookies()
    for stuff in mycookies:
        tavssessionid = None
        try:
            #print(stuff)
            if (stuff["name"] == 'TAVSSESSION'):
                tavssessionid = stuff["value"]
                #print("Tavs Session:{0}".format(stuff["value"]))
                return (tavssessionid)
        except:
            print("Not a TAVSSESSION")

    return(tavssessionid)


#Login Fixture - gets login/session for rest of the tests
@pytest.fixture(scope='module')

def cge_session():
    """Create Concur Login Session for use with additional tests

    Sets up Playwright browser and new_page for use with additional tests"""

    p = sync_playwright().start()
    browser_type = p.chromium
    #browser_type = p.firefox
    #browser_type = p.webkit

    browser = browser_type.launch(headless=True,devtools=True)
    # browser.start_tracing(path='/Users/i857921/trace.json')

    #browser = browser.new_context(record_har_path='/Users/i857921/har')
    page = browser.new_page(record_har_path='/Users/johnraymond/har/test.har')

# Turn on hooks for response, console and request
# Set Headers x-abmb-concur so that test traffic is not flagged.

    page.context.set_extra_http_headers({"x-abmb-concur":"b132d9a0cfc7f5784706f46d8a4f41aaa4d460c5"})
    #page.on('console', log_console) #send page console messages to log_console
    #page.on('requestfinished', log_request)
    #page.on('response', log_response)
    #page.on("response", lambda response: print("<<", response.status, response.url, response.all_headers().get("date")))
    page.on("requestfailed ", lambda request: print(request.url + ":" + request.failure))

    if testenv == "https://integration.concursolutions.com":
        #Add nui login until cge login is replaced
        #print(testenv)
        page.goto(testenv)
        page.wait_for_load_state()
        un = os.environ['USERNAME']
        pw = os.environ['PW']
        page.fill("id=username-input", un)
        page.click("id=btnSubmit")

        page.wait_for_load_state()
        page.fill("id=password", pw)
        page.click("id=btnSubmit")
    else:

        page.goto(testenv) #testenv set globally above
    #assert page.wait_for_selector("data-test=app-footer-links"), "TEST RESULT"
        page.wait_for_load_state()
        un = os.environ['USERNAME']
        pw = os.environ['PW']
        page.fill("id=userid", un)
        page.fill("id=password", pw)
        page.click("id=btnSubmit")

        #page.set_extra_http_headers({"TAVSSESSION": ""})

#Yield connection to rest of tests / includes session info
    yield page

   #Get TAVSSESSIONID
    try:
        print(get_tavs_sessionid(page))
        page.click('text=Profile')
        page.click('text=Sign Out')
        #page.click("data-test=user-profile-menu-signout-link")
        assert page.wait_for_selector("id=btnSubmit")  # check logout worked
        #browser.stop_tracing()
        #browser.close()
        page.close()
        p.stop()
    except:
        page.close()
        p.stop()

def test_travel_screen(cge_session):
    """Simple Travel Screen Rendered Test

    Goto /travel.asp
    Asserts: id=id=TMAIR_searchRefPoint0 is found on page"""

    #print("Test Travel Screen Shows Up")
    cge_session.click("data-test=menu__anchor-travel")
    #cge_session.goto(testenv + "/travelhome.asp")
    assert cge_session.wait_for_selector("id=TMAIR_searchRefPoint0")
    cge_session.wait_for_load_state('networkidle',timeout=121000)


def test_travel_perdiem_location(cge_session):
    cge_session.click("data-test=menu__anchor-travel")
    #cge_session.goto(testenv + "/travelhome.asp")
    assert cge_session.wait_for_selector("id=TMAIR_searchRefPoint0")
    #Choose PerDiem Location
    cge_session.fill("[id=TMAIR_searchRefPoint0]", "Boston")
    cge_session.click("[id=TMAIR_TM_Findlocation0]")
    cge_session.click("[id=geocodechoosebutton]")
    cge_session.type("[id=fltDepCityDisplay0]", "LAX")
    cge_session.keyboard.press("Tab")
    #cge_session.click("[id=fltDepCityDisplay0_airAC0]",timeout=5000)
    #cge_session.dblclick("[id=fltDepCityDisplay0]")
    #print(cge_session.get_attribute("[id=fltDepCityDisplay0]", name="text"))

    #Date Picker:)
    cge_session.fill("[id=fltDate0]", "08/27/2022")
    cge_session.keyboard.press('Tab')

    cge_session.fill("[id=fltDate1]", "08/30/2022")
    cge_session.keyboard.press('Tab')

    cge_session.click("[id=btnAirLaunchWizard]")
    cge_session.wait_for_load_state('domcontentloaded', timeout=120000)
    cge_session.wait_for_selector("[id=shopbyfare_content]",timeout=30000)

def test_auth_screen(cge_session):
    '''Auth Screen Renders'''

    cge_session.click("data-test=menu__anchor-travelmanagerauthorization")
    #cge_session.goto(testenv + "/TravelManagerFrame.asp?MenuClicked=Authorization&MenuItem=View")
    #cge_session.wait_for_load_state('networkidle',timeout=121000)
    #assert cge_session.wait_for_selector("data-test=menu__anchor-travelmanagerauthorization_0")
    #assert cge_session.frames[2].wait_for_selector("id=DocumentFrame")

def test_voucher_screen(cge_session):
    cge_session.click("data-test=menu__anchor-travelmanagervoucher")

    #cge_session.goto(testenv + "/TravelManagerFrame.asp?MenuClicked=Voucher&MenuItem=View")
    cge_session.wait_for_load_state('networkidle',timeout=121000)
    assert cge_session.frames[2].wait_for_selector("id=DocumentFrame")

def test_voucher_search(cge_session):
    cge_session.click("data-test=menu__anchor-travelmanagervoucher")
    cge_session.wait_for_load_state('networkidle', timeout=121000)
    cge_session.click("data-test=menu__anchor-travelmanagervoucher_2")
    cge_session.wait_for_load_state('networkidle', timeout=121000)

def test_approval_screen(cge_session):
    #cge_session.goto(testenv + "/TravelManagerFrame.asp?MenuClicked=Approval&MenuItem=All")

    try:
        print(get_tavs_sessionid(cge_session))
        cge_session.click("data-test=menu__anchor-travelmanagerapproval")
        #print(cge_session.context.cookies())

        cge_session.wait_for_load_state('domcontentloaded', timeout=120000)
        print("Dom Content Loaded")
        #print(cge_session.main_frame.content())
        #print("-----------------------------")
        cge_session.main_frame.wait_for_load_state()
        #dump_frame_tree(cge_session.main_frame, "")

        #assert cge_session.wait_for_selector('//*[@id="approvals-list-cards"]/div')
        cge_session.wait_for_load_state('networkidle',timeout=120000)
        print("Network Idle Reached")
        #assert cge_session.wait_for_selector("data-test=menu__anchor-travelmanagervoucher")
        #assert cge_session.frames[2].wait_for_selector("id=DocumentFrame")

        test_travel_screen(cge_session)
        test_voucher_search(cge_session)
    except:
        print("BYPASS approval wait")

def test_new_auth_screen(cge_session):
    cge_session.click("data-test=menu__anchor-travelmanagerauthorization")
    # cge_session.goto(testenv + "/TravelManagerFrame.asp?MenuClicked=Authorization&MenuItem=View")

#    cge_session.wait_for_load_state('networkidle', timeout=121000)
#    cge_session.wait_for_load_state('networkidle')

    cge_session.wait_for_load_state('domcontentloaded')
    cge_session.click("data-test=menu__anchor-travelmanagerauthorization_1")
    cge_session.wait_for_load_state('domcontentloaded')

#    cge_session.wait_for_load_state('networkidle', timeout=121000)
#    cge_session.wait_for_load_state('networkidle')

def test_frame(cge_session):
    #print(cge_session.main_frame.content())
    print("-----------------------------")
    dump_frame_tree(cge_session.main_frame,"")

def dump_frame_tree(frame, indent):
    print(indent + frame.name + '@' + frame.url)
    #print(frame.content())
    for child in frame.child_frames:
        dump_frame_tree(child, indent + "    ")

