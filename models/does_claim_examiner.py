# Sample automation for initial Post Deployment Verfication
# Simple Login and visit a number of TAVS screens
from faker import Faker
import time



class ClaimExaminer():
    def __init__(self, page):
        self.does_claim = page
        #testenv = 'https://uat-app-vos11000000-ui.geosolinc.com/vosnet/'  # Global Test BASE URL - note:pytest_base_url not really working
        testenv = 'https://review-app-vos11000000-ui.geosolinc.com/vosnet/Default.aspx?enc=Xdm8Yw+m50AOnLNjcWnUPg=='


        self.does_claim.goto(testenv)

        self.does_claim.wait_for_selector("id=btnguestlogina")
        self.does_claim.click("id=btnguestlogina")
        un = self.does_claim.locator("id=txtUserName")
        un.fill("JRaymond")
        pw = self.does_claim.locator("id=txtPassword")
        pw.fill("Twin99flex!")
        time.sleep(5)
        self.does_claim.click("id=ctl00_Main_content_cmdLoginButt")
        #Staff Sign-in Notice
        print("LOGIN")
        #agreebtn = self.does_claim.locator("id=ctl00_Main_content_ucStaffSignNotice_btnAgree")
        #agreebtn.click()




