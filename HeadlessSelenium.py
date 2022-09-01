import unittest
from selenium import webdriver
import requests
from PIL import Image
from Screenshot import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class NestleWF(unittest.TestCase):
    def setUp(self):

        # Put your username and authey below
        # You can find your authkey at crossbrowsertesting.com/account
        self.username = "m@nextuser.com"
        self.authkey = "uccdc07c229a7f6a"

        self.api_session = requests.Session()
        self.api_session.auth = (self.username, self.authkey)

        self.test_result = None

        caps = {}

        caps['name'] = 'Nestle WF Initial Headless'
        caps['browser_api_name'] = 'Chrome93'
        caps['platform'] = 'Headless'
        #caps['screen_resolution'] = '1024x768'
        caps['record_network'] = 'true'
        caps['record_video'] = 'true'

        self.driver = webdriver.Remote(
            desired_capabilities=caps,
            command_executor="http://%s:%s@hub-cloud.crossbrowsertesting.com:80/wd/hub" % (self.username, self.authkey)
        )

        self.driver.implicitly_wait(20)

    def test_CBT(self):

        try:
            self.driver.get("https://www.nestlebabyandme.com.mx/?wf=engagement_tracker_test&nu_prev=1&var=1")
            #self.driver.get('http://crossbrowsertesting.github.io/selenium_example_page.html')
            self.driver.maximize_window()
            self.driver.save_screenshot('singletake.png')
            #self.assertEqual("Regístrate en Baby and Me | Nestlé Baby and Me", self.driver.title)

            print("Taking snapshot")
            snapshot_hash = self.api_session.post(
                'https://crossbrowsertesting.com/api/v3/selenium/' + self.driver.session_id + '/snapshots').json()[
                'hash']

            self.test_result = 'pass'

        except AssertionError as e:
            # log the error message, and set the score to "during tearDown()".
            self.api_session.put(
                'https://crossbrowsertesting.com/api/v3/selenium/' + self.driver.session_id + '/snapshots/' + snapshot_hash,
                data={'description': "AssertionError: " + str(e)})
            self.test_result = 'fail'
            raise

    def tearDown(self):
        print("Done with session %s" % self.driver.session_id)
        self.driver.quit()
        # Here we make the api call to set the test's score.
        # Pass it passes, fail if an assertion fails, unset if the test didn't finish
        if self.test_result is not None:
            self.api_session.put('https://crossbrowsertesting.com/api/v3/selenium/' + self.driver.session_id,
                                 data={'action': 'set_score', 'score': self.test_result})


if __name__ == '__main__':
    unittest.main()