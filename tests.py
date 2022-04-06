from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from django.test.utils import override_settings
from django.conf import settings
 
class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ['testdb.json',]

    ABSOLUTE_PATH_REPO = '/home/vagrant/ClassVRoom/' # MUST END WITH SEPARATOR /
    TEST_FILE = 'testResourceFile.pdf'
    
    SUPERADMIN_USER = 'admin@admin.es';
    ADMIN_CENTRE_USER = 'testAdminCentre@test.test';
    DOCENT_USER = 'testDocent@test.test';
    ALUMNE_USER = 'testAlumne@test.test';

    SUPERADMIN_PASS = '1234';
    NON_SUPERADMIN_PASS = 'P@ssw0rdP@ssw0rd';

    # Centers courses
    COURSE_C1 = 'CursCentre1';
    COURSE_C2 = 'CursCentre2'; 
 
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

    def findElemByName(self, name):
        return self.selenium.find_element_by_name(name)

    def findLinkByText(self, text):
        return self.selenium.find_element_by_xpath("//a[text()='"+text+"']")        

    def findInputByValue(self, value):
        return self.selenium.find_element_by_xpath('//input[@value="'+value+'"]')
 
    def login_admin (self, user, password, hasToLogin):
        # get admin login page
        self.selenium.get('%s%s' % (self.live_server_url, '/admin'))

        # if admin already logged, log out and go login page before continue
        if not (len(self.selenium.find_elements_by_xpath("//a[text()='Log out']")) == 0):
            elemLogout = self.findLinkByText('Log out')
            elemLogout.click()
            self.selenium.get('%s%s' % (self.live_server_url, '/admin'))

        # Write username and password, then click 'Log in'
        username_input = self.findElemByName('username')
        username_input.send_keys(user)
        password_input = self.findElemByName('password')
        password_input.send_keys(password)
        elemLogin = self.findInputByValue('Log in')
        elemLogin.click()
 
        # This function can check if an user can login as admin or if he doesnt,
        # depending on hasToLogin parameter
        if (hasToLogin):
            self.findLinkByText('Log out')
        else:
            self.findInputByValue('Log in')

    def checkCoursesFromAdminPanel(self, seeCourses, nonSeeCourses):
        # Check can open courses window 
        elemCourses = self.findLinkByText('Courses')
        elemCourses.click()
        
        # Check can see courses specified in array seeCourses
        for seeCourse in seeCourses:
            self.findLinkByText(seeCourse)            
        
        # Check can NOT see courses specified in array nonSeeCourses
        for nonSeeCourse in nonSeeCourses:
            assert len(self.selenium.find_elements_by_xpath("//a[text()='"+nonSeeCourse+"']")) == 0
        

    @override_settings(DEBUG=True)    
    def test_superadmin (self): 
        # Login super admin
        self.login_admin(self.SUPERADMIN_USER, self.SUPERADMIN_PASS, True)
        # Check can see both courses of different school
        self.checkCoursesFromAdminPanel([self.COURSE_C1, self.COURSE_C2], [])
                

    @override_settings(DEBUG=True)    
    def test_adminCentre (self): 
        # Login super admin
        self.login_admin(self.ADMIN_CENTRE_USER, self.NON_SUPERADMIN_PASS, True)

        # Check can see courses from school 1 but not 2
        self.checkCoursesFromAdminPanel([self.COURSE_C1], [self.COURSE_C2])


    @override_settings(DEBUG=True)    
    def test_docent (self): 
        # Login docent (suscribed to Centre1)
        self.login_admin(self.DOCENT_USER, self.NON_SUPERADMIN_PASS, True)

        # Check can see courses from school 1 but not from school 2
        self.checkCoursesFromAdminPanel([self.COURSE_C1], [self.COURSE_C2])

        # Click Course1
        elemCourseC1 = self.findLinkByText(self.COURSE_C1)
        elemCourseC1.click()

        # Click Add resource
        elemBrows= self.selenium.find_element_by_name('resource_set-0-file')
        elemBrows.send_keys(self.ABSOLUTE_PATH_REPO + self.TEST_FILE)

        elemName = self.selenium.find_element_by_name('resource_set-0-name')
        elemName.send_keys('ResourceTest1')

        elemSave = self.findInputByValue('Save')
        elemSave.click()

    @override_settings(DEBUG=True)
    def test_login_rols (self):
        # Login super admin
        self.login_admin(self.SUPERADMIN_USER, self.SUPERADMIN_PASS, True)      
        # Login admin centre  
        self.login_admin(self.ADMIN_CENTRE_USER, self.NON_SUPERADMIN_PASS, True)
        # Login docent      
        self.login_admin(self.DOCENT_USER, self.NON_SUPERADMIN_PASS, True)
        # Login alumne
        self.login_admin(self.ALUMNE_USER, self.NON_SUPERADMIN_PASS, False)
   
      
        
