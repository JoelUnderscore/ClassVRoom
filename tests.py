from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
 
class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ['testdb.json',]
 
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        opts.headless = False
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)
 
    @classmethod
    def tearDownClass(cls):
        #cls.selenium.quit()
        super().tearDownClass()
 
    def login_admin (self, user, password, hasToLogin):
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))

        # if admin already logged, log out before continue
        if not (len(self.selenium.find_elements_by_xpath("//a[text()='Log out']")) == 0):
            self.selenium.find_element_by_xpath("//a[text()='Log out']").click()


        # Write username and password, then click 'Log in'
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(user)
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(password)
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()
 
        # This function can check if an user can login as admin or if he doesnt
        # depending on hasToLogin parameter
        if (hasToLogin):
            self.selenium.find_element_by_xpath("//a[text()='Log out']")
        else:
            self.selenium.find_element_by_xpath('//input[@value="Log in"]')
    
    def test_superadmin (self):
        self.login_admin('admin@admin.es', '1234', True)
        self.selenium.find_element_by_xpath("//a[text()='Courses']").click()
        self.selenium.find_element_by_xpath("//a[normalize-space()='Add course']")

    def test_login_rols (self):
        #.login_admin('admin@admin.es', '1234', True)
        #self.login_admin('testAdminCentre@test.test', 'P@ssw0rdP@ssw0rd', True)        
        #self.login_admin('testDocent@test.test', 'P@ssw0rdP@ssw0rd', True)
        self.login_admin('testAlumne@test.test', 'P@ssw0rdP@ssw0rd', False)
   
       
       
