# Sample automation for initial Post Deployment Verfication
# Simple Login and visit a number of TAVS screens
from faker import Faker
import time


class DoesFrontPage:
    def __init__(self, page):
        self.does_claim = page
        testenv = 'https://uat-app-vos11000000-ui.geosolinc.com/vosnet/'  # Global Test BASE URL - note:pytest_base_url not really working
        #testenv = 'https://review-app-vos11000000-ui.geosolinc.com/vosnet/Default.aspx?enc=Xdm8Yw+m50AOnLNjcWnUPg=='
        self.does_claim.goto(testenv)
        self.fake = Faker()

        # Create Fake Profile
        self.profile = self.fake.profile()
        print(self.profile['name'])
        print(self.profile['ssn'])
        print(self.profile['mail'])
        print(self.profile['username'])

        page.pause()

    def register_privacy(self):
        try:
            self.does_claim.wait_for_load_state("networkidle", timeout=5000)

            self.does_claim.wait_for_selector("id=btnguestlogina")
            self.does_claim.click("id=btnguestlogina")

            self.does_claim.wait_for_selector("id=btnIndRegistration")
            self.does_claim.click("id=btnIndRegistration")

            # test_frame(does_claim)
            self.does_claim.wait_for_selector(
                "text=I certify that the information I have provided in this claim is true to the best")
            self.does_claim.click(
                "text=I certify that the information I have provided in this claim is true to the best")

            self.does_claim.wait_for_selector(
                "text=I authorize the exchange of information relating to prior assessment(s) for trai")
            self.does_claim.click(
                "text=I authorize the exchange of information relating to prior assessment(s) for trai")

            self.does_claim.wait_for_selector("text=I Agree")
            # self.does_claim.click("text=I Agree")
            # self.does_claim.wait_for_load_state("load")
            # self.does_claim.wait_for_selector("id=ctl00_Main_content_radFilingUI_0")
            # self.does_claim.click("id=ctl00_Main_content_radFilingUI_0")
            return True

        except:
            return False

    def claim(self):
        try:
            self.does_claim.wait_for_selector("text=I Agree")
            self.does_claim.click("text=I Agree")
            self.does_claim.wait_for_load_state("load")
            uiclaim = self.does_claim.locator("text=Yes")
            uiclaim.click()
            self.does_claim.wait_for_selector("id=ctl00_Main_content_btnNext")
            return True

        except:
            return False

    def verify_ssn(self):
        try:

            self.does_claim.click("id=ctl00_Main_content_btnNext")
            self.does_claim.wait_for_selector(
                "id=ctl00_Main_content_Wizard1_StartNavigationTemplateContainerID_StartNextButton")
            self.does_claim.click("id=ctl00_Main_content_Wizard1_StartNavigationTemplateContainerID_StartNextButton")
            self.does_claim.wait_for_load_state("networkidle", timeout=5000)
            #self.does_claim.screenshot(path="screenshot", full_page=True)
            # Enter SSN
            # ssn = fake.ssn().replace("-","")
            # print(ssn)
            self.ssn = self.profile['ssn'].replace("-", "")

            self.does_claim.type("id=ctl00_Main_content_Wizard1_ucSSN_txtSSN", self.ssn)
            self.does_claim.type("id=ctl00_Main_content_Wizard1_ucSSN_txtSSNReenter", self.ssn)
            return True
        except:
            return False

    def work_history(self, work):
        try:
            # Next from verify ssn
            self.does_claim.click("id=ctl00_Main_content_Wizard1_StepNavigationTemplateContainerID_StepNextButton")
            self.does_claim.wait_for_load_state("networkidle", timeout=5000)


            # Verify Work Time Frame
            self.does_claim.click("id=ctl00_Main_content_Wizard1_rblWorkHistoryVerify_0")
            self.does_claim.click("text=Yes")
            return True
        except:
            return False

    def states_worked(self):

        try:
            #Next
            self.does_claim.click("id=ctl00_Main_content_Wizard1_StepNavigationTemplateContainerID_StepNextButton")
            self.does_claim.wait_for_load_state("networkidle", timeout=5000)

            #States you have worked in
            #No
            self.does_claim.click("id=ctl00_Main_content_Wizard1_rblStatesWorkedIn_1")
            self.does_claim.click("id=ctl00_Main_content_Wizard1_rblAppliedUCPast12Months_1")
            #self.does_claim.click("[aria-label=\"Have you claimed unemployment insurance benefits within the last 12 months\\?\"] >> text=No")

            #self.does_claim.getByLabel("for=ctl00_Main_content_Wizard1_rblStatesWorkedIn_1").click()
            #self.does_claim.getByText('Have you worked in two or more states between >> text=No').click()
            # self.does_claim.get_by_role("radio", name="ctl00$Main_content$Wizard1$rblStatesWorkedIn", value=0).click()

            #Yes
            #self.does_claim.click("id=ctl00_Main_content_Wizard1_rblStatesWorkedIn")
            #self.does_claim.click("id=ctl00_Main_content_Wizard1_rblAppliedUCPast12Months")
            return True
        except:
            return False

    def federal_service(self):
        try:
            # Next
            self.does_claim.click("id=ctl00_Main_content_Wizard1_StepNavigationTemplateContainerID_StepNextButton")
            self.does_claim.wait_for_load_state("networkidle", timeout=5000)

            # Federal Service
            # No
            fedservice = self.does_claim.locator("id=ctl00_Main_content_Wizard1_rblFederalCivilianEmployee_1")
            fedservice.click()

            # Yes
            # self.does_claim.click("id=ctl00_Main_content_Wizard1_rblFederalCivilianEmployee")
            return True
        except:
            return False

    def military_service(self):
        try:
            # Next
            self.does_claim.click("id=ctl00_Main_content_Wizard1_StepNavigationTemplateContainerID_StepNextButton")
            self.does_claim.wait_for_load_state("networkidle", timeout=5000)

            # Military Service
            # No
            self.does_claim.click("id=ctl00_Main_content_Wizard1_rblMilitaryService_1")
            # Yes
            # self.does_claim.click("id=ctl00_Main_content_Wizard1_rblMilitaryService")
            return True
        except:
            return False

    def login_information(self):
        try:
            # Next
            self.does_claim.click("id=ctl00_Main_content_Wizard1_StepNavigationTemplateContainerID_StepNextButton")
            self.does_claim.wait_for_load_state("networkidle", timeout=5000)

            # Create User
            un = self.does_claim.locator("id=ctl00_Main_content_ucLogin_txtUsername")
            un.fill("myusername1")
            un.fill(self.profile['username'])
            # self.does_claim.type("id=ctl00_Main_content_ucLogin_txtUsername", "myusername")
            self.does_claim.wait_for_load_state("networkidle", timeout=5000)

            # Password
            # does_claim.type("id=ctl00_Main_content_ucLogin_ucPassword_txtPwd", "PASSPASS1!")
            pw = self.does_claim.locator("id=ctl00_Main_content_ucLogin_ucPassword_txtPwd")
            pw.fill("PASSpASS1!")

            # does_claim.type("id=ctl00_Main_content_ucLogin_ucPassword_txtPwdConfirm", "PASSPASS1!")
            pwc = self.does_claim.locator("id=ctl00_Main_content_ucLogin_ucPassword_txtPwdConfirm")
            pwc.fill("PASSpASS1!")
            self.does_claim.wait_for_load_state("networkidle", timeout=5000)

            self.does_claim.select_option("id=ctl00_Main_content_ucLogin_ddlSecurityQuestion", value="1")
            self.does_claim.type("id=txtSecurityQuestionResponse", "mother")
            self.does_claim.type("id=txtPINID", "2404")

            # Enter Zip
            self.does_claim.type("id=ctl00_Main_content_txtZip", "20005")
            self.does_claim.wait_for_load_state("networkidle", timeout=5000)

            # Enter Email
            # does_claim.type("id=ctl00_Main_content_ucEmailTextBox_txtEmail", "email@email.com")
            email = self.profile['mail']
            self.does_claim.wait_for_load_state("networkidle", timeout=5000)

            emailtxt = self.does_claim.locator("id=ctl00_Main_content_ucEmailTextBox_txtEmail")
            emailtxt.fill(email)
            self.does_claim.wait_for_load_state("networkidle", timeout=5000)

            confirmemailtxt = self.does_claim.locator("id=ctl00_Main_content_ucEmailTextBox_txtEmailConfirm")
            confirmemailtxt.fill(email)
            self.does_claim.wait_for_load_state("networkidle", timeout=5000)

            # Auth to work US
            self.does_claim.click("id=ctl00_Main_content_radAuthorizedToWork_0")
            self.does_claim.wait_for_load_state("networkidle", timeout=5000)

            self.does_claim.type("id=ctl00_Main_content_ucRegDemographics_txtDOB", "07/19/1966")
            self.does_claim.click("id=ctl00_Main_content_ucRegDemographics_rblArrested_1")

            # Enter Demographics --- This selection does a post of somesort so do at the end`
            # does_claim.click("id=ctl00_Main_content_ucRegDemographics_rblGender_2")  #rather not say
            self.does_claim.click("id=ctl00_Main_content_ucRegDemographics_rblGender_0")  #female
            #self.does_claim.click("id=ctl00_Main_content_ucRegDemographics_rblGender_1")  # male
            self.does_claim.wait_for_load_state("networkidle",timeout=5000)
            self.does_claim.wait_for_load_state("domcontentloaded")

            #this is a hack for progress indicator reseting the Selective service setting
            #time.sleep(10)

            # Selective Service
            #draft_status = self.does_claim.locator("id=ctl00_Main_content_ucRegDemographics_ddlDraftStatus")
            # draft_status.select_option("id=ctl00_Main_content_ucRegDemographics_ddlDraftStatus", value="2")
            #draft_status.select_option(value="2")

            # Wait for network traffic to stop to handle the widget spinner completion
            self.does_claim.wait_for_load_state("networkidle",timeout=5000)

            return True
        except:
            return False

    def elegibility(self):
        try:
            # Next
            self.does_claim.click("id=ctl00_Main_content_btnNext")
            self.does_claim.wait_for_load_state("networkidle", timeout=5000)


            # Eligibility
            # Name
            fName = self.does_claim.locator("id=ctl00_Main_content_ucName_txtFirstName")
            fName.fill(self.profile["name"].split(" ")[0])

            lname = self.does_claim.locator("id=ctl00_Main_content_ucName_txtLastName")
            lname.fill(self.profile['name'].split(" ")[1])
            # Next
            self.does_claim.click("id=ctl00_Main_content_btnNext")
            return True
        except:
            return False

    def address(self):
        try:
            my_address = self.does_claim.locator("id=ctl00_Main_content_ucAddress_txtAddress1")
            my_address.fill("1224 H St NE")
            self.does_claim.wait_for_load_state("networkidle", timeout=5000)
            my_address.press("Tab")
            time.sleep(5)
            self.does_claim.wait_for_load_state("networkidle", timeout=5000)
            time.sleep(5)
            my_zip = self.does_claim.locator("id=ctl00_Main_content_ucAddress_txtZip")
            my_zip.fill("200024445")
            self.does_claim.wait_for_load_state("networkidle", timeout=5000)
            my_zip.press("Enter")
            self.does_claim.wait_for_load_state("networkidle", timeout=5000)

            time.sleep(5)
            my_city = self.does_claim.locator("id=ctl00_Main_content_ucAddress_txtCity")
            my_city.fill("Washington")
            self.does_claim.wait_for_load_state("networkidle", timeout=5000)
            time.sleep(10)
            my_state = self.does_claim.locator("id=ctl00_Main_content_ucAddress_cboState")
            my_state.select_option("DC")
            self.does_claim.wait_for_load_state("networkidle", timeout=5000)
            time.sleep(10)
            #my_current = self.does_claim.locator("id=ctl00_Main_content_ucAddress_rdoCorrectedResidentialAddress_0")
           # my_current.click()

            my_ward = self.does_claim.locator("id=ctl00_Main_content_ucAddress_ddlAltGeo")
            my_ward.select_option("00")
            self.does_claim.wait_for_load_state("networkidle", timeout=5000)
            time.sleep(10)
            #time.sleep(5)
            my_mailing = self.does_claim.locator("id=ctl00_Main_content_ucAddress_cntPopulateMailAddress")
            my_mailing = self.does_claim.locator("text=Use residential address")

            my_mailing.click()
            self.does_claim.wait_for_load_state("networkidle", timeout=5000)
            time.sleep(5)

            #self.does_claim.click("id=ctl00_Main_content_btnNext")



            return True
        except:
            return False

    def phone(self):
        self.does_claim.click("id=ctl00_Main_content_btnNext")
        self.does_claim.wait_for_load_state("networkidle", timeout=5000)

        pnum = self.does_claim.locator("id=ctl00_Main_content_ucPhone_txtPrimePhone1")
        pnum.type("7034314471")

        ptype = self.does_claim.locator("id=ctl00_Main_content_ucPhone_ddlPrimePhoneType")
        ptype.select_option("1")

    def notification(self):
        self.does_claim.click("id=ctl00_Main_content_btnNext")
        self.does_claim.wait_for_load_state("networkidle", timeout=5000)

        my_prefmethod = self.does_claim.locator("id=ctl00_Main_content_ucNotificationMethod_ddlPrefDelMethods")
        my_prefmethod.select_option("5") #postal

        my_method1099 = self.does_claim.locator("select[name=\"ctl00\\$Main_content\\$ucNotificationMethod\\$ddl1099GNotificationMethod\"]")
        my_method1099.select_option("5") #postal

        my_access = self.does_claim.locator("id=ctl00_Main_content_ucSiteAccess_ddlSiteAccess")
        my_access.select_option("2")

        my_hearabout = self.does_claim.locator("id=ctl00_Main_content_ucSiteAccess_ddlWebsiteReferral")
        #my_hearabout.select_option("")

    def wft(self):
        # Next
        self.does_claim.click("id=ctl00_Main_content_btnNext")
        self.does_claim.wait_for_load_state("networkidle", timeout=5000)
        print("next step")

