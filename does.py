#Sample automation for initial Post Deployment Verfication
#Simple Login and visit a number of TAVS screens
#Simple Travel View
#Based on Python/Playwright framework with py-test
from faker import Faker
from playwright.sync_api import sync_playwright
import pytest
import os
import json

testenv = os.environ['PYTEST_BASE_URL'] #Global Test BASE URL - note:pytest_base_url not really working
fake = Faker()


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


#Login Fixture - gets login/session for rest of the tests
@pytest.fixture(scope='module')

def does_claim():
    """Create UI Claim and or Login

    Sets up Playwright browser and new_page for use with additional tests"""
    p = sync_playwright().start()
    #browser_type = p.chromium
    browser_type = p.firefox
    #browser_type = p.webkit

    browser = browser_type.launch(headless=False, slow_mo=100)

    #browser = browser_type.launch(channel="chrome", headless=False, devtools=False)
    #browser = browser.new_context(record_har_path='/Users/johnraymond/har')


    page = browser.new_page()

# Turn on hooks for response, console and request
    #page.on('console', log_console) #send page console messages to log_console
    #page.on('requestfinished', log_request)
    #page.on('response', log_response)
    #page.on("response", lambda response: print("<<", response.status, response.url, response.all_headers().get("date")))
    #page.on("requestfailed ", lambda request: print(request.url + ":" + request.failure))


    page.goto(testenv)

    yield page



def test_create_claim(does_claim):
    #Create Simple Claim

    #Create Fake Profile
    profile = fake.profile()
    print(profile)

    print("HELLO DOES")
    does_claim.wait_for_selector("id=btnguestlogina")
    does_claim.click("id=btnguestlogina")

    does_claim.wait_for_selector("id=btnIndRegistration")
    does_claim.click("id=btnIndRegistration")

    #test_frame(does_claim)
    does_claim.wait_for_selector("text=I certify that the information I have provided in this claim is true to the best")
    does_claim.click("text=I certify that the information I have provided in this claim is true to the best")


    does_claim.wait_for_selector("text=I authorize the exchange of information relating to prior assessment(s) for trai")
    does_claim.click("text=I authorize the exchange of information relating to prior assessment(s) for trai")

    does_claim.wait_for_selector("text=I Agree")
    does_claim.click("text=I Agree")
    does_claim.wait_for_load_state("load")

    does_claim.wait_for_selector("id=ctl00_Main_content_radFilingUI_0")
    does_claim.click("id=ctl00_Main_content_radFilingUI_0")

    does_claim.wait_for_selector("id=ctl00_Main_content_btnNext")
    does_claim.click("id=ctl00_Main_content_btnNext")

    does_claim.wait_for_selector("id=ctl00_Main_content_Wizard1_StartNavigationTemplateContainerID_StartNextButton")
    does_claim.click("id=ctl00_Main_content_Wizard1_StartNavigationTemplateContainerID_StartNextButton")
    does_claim.wait_for_load_state("networkidle")
    does_claim.screenshot(path="screenshot", full_page=True)
    #Enter SSN
    #ssn = fake.ssn().replace("-","")
    #print(ssn)
    ssn = profile['ssn'].replace("-", "")

    does_claim.type("id=ctl00_Main_content_Wizard1_ucSSN_txtSSN", ssn)
    does_claim.type("id=ctl00_Main_content_Wizard1_ucSSN_txtSSNReenter", ssn)

    #Next
    does_claim.click("id=ctl00_Main_content_Wizard1_StepNavigationTemplateContainerID_StepNextButton")

    #Verify Work Time Frame
    does_claim.click("id=ctl00_Main_content_Wizard1_rblWorkHistoryVerify_0")

    #Next
    does_claim.click("id=ctl00_Main_content_Wizard1_StepNavigationTemplateContainerID_StepNextButton")

    #States you have worked in
    #No
    does_claim.click("id=ctl00_Main_content_Wizard1_rblStatesWorkedIn_1")
    does_claim.click("id=ctl00_Main_content_Wizard1_rblAppliedUCPast12Months_1")

    #Yes
    #does_claim.click("id=ctl00_Main_content_Wizard1_rblStatesWorkedIn")
    #does_claim.click("id=ctl00_Main_content_Wizard1_rblAppliedUCPast12Months")

    #Next
    does_claim.click("id=ctl00_Main_content_Wizard1_StepNavigationTemplateContainerID_StepNextButton")

    #Federal Service
    #No
    does_claim.click("id=ctl00_Main_content_Wizard1_rblFederalCivilianEmployee_1")

    #Yes
    #does_claim.click("id=ctl00_Main_content_Wizard1_rblFederalCivilianEmployee")

    #Next
    does_claim.click("id=ctl00_Main_content_Wizard1_StepNavigationTemplateContainerID_StepNextButton")

    #Military Service
    #No
    does_claim.click("id=ctl00_Main_content_Wizard1_rblMilitaryService_1")
    #Yes
    #does_claim.click("id=ctl00_Main_content_Wizard1_rblMilitaryService")

    #Next
    does_claim.click("id=ctl00_Main_content_Wizard1_StepNavigationTemplateContainerID_StepNextButton")

    #Create User
    un = does_claim.locator("id=ctl00_Main_content_ucLogin_txtUsername")
    un.fill("myusername1")
    un.fill(profile['username'])
    #does_claim.type("id=ctl00_Main_content_ucLogin_txtUsername", "myusername")

    # Password
    #does_claim.type("id=ctl00_Main_content_ucLogin_ucPassword_txtPwd", "PASSPASS1!")
    pw = does_claim.locator("id=ctl00_Main_content_ucLogin_ucPassword_txtPwd")
    pw.fill("PASSpASS1!")

    #does_claim.type("id=ctl00_Main_content_ucLogin_ucPassword_txtPwdConfirm", "PASSPASS1!")
    pwc = does_claim.locator("id=ctl00_Main_content_ucLogin_ucPassword_txtPwdConfirm")
    pwc.fill("PASSpASS1!")

    does_claim.select_option("id=ctl00_Main_content_ucLogin_ddlSecurityQuestion", value="1")
    does_claim.type("id=txtSecurityQuestionResponse", "mother")
    does_claim.type("id=txtPINID", "2404")

    #Enter Zip
    does_claim.type("id=ctl00_Main_content_txtZip", "20005")


    #Enter Email
    #does_claim.type("id=ctl00_Main_content_ucEmailTextBox_txtEmail", "email@email.com")
    email = profile['mail']

    emailtxt = does_claim.locator("id=ctl00_Main_content_ucEmailTextBox_txtEmail")
    emailtxt.fill(email)



    confirmemailtxt = does_claim.locator("id=ctl00_Main_content_ucEmailTextBox_txtEmailConfirm")
    confirmemailtxt.fill(email)


    #Auth to work US
    does_claim.click("id=ctl00_Main_content_radAuthorizedToWork_0")

    does_claim.type("id=ctl00_Main_content_ucRegDemographics_txtDOB", "07/19/1966")
    does_claim.click("id=ctl00_Main_content_ucRegDemographics_rblArrested_1")


 #Enter Demographics --- This selection does a post of somesort so do at the end`
    #does_claim.click("id=ctl00_Main_content_ucRegDemographics_rblGender_2")  #rather not say
    #does_claim.click("id=ctl00_Main_content_ucRegDemographics_rblGender_0")  #female
    does_claim.click("id=ctl00_Main_content_ucRegDemographics_rblGender_1")  #male

    #Wait for network traffic to stop to handle the widget spinner completion
    does_claim.wait_for_load_state("networkidle")


    # Selective Service
    does_claim.select_option("id=ctl00_Main_content_ucRegDemographics_ddlDraftStatus", value="2")

    #Next
    does_claim.click("id=ctl00_Main_content_btnNext")

    #Eligibility
    #Name
    fName = does_claim.locator("id=ctl00_Main_content_ucName_txtFirstName")
    fName.fill(profile["name"].split(" ")[0])

    lname = does_claim.locator("id=ctl00_Main_content_ucName_txtLastName")
    lname.fill(profile['name'].split(" ")[1])
    #Next
    does_claim.click("id=ctl00_Main_content_btnNext")

    #Residential Address



