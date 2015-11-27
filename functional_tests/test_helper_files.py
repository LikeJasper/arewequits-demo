from .base import FunctionalTest
from unittest import skip

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

UNWRITTEN_COMPLAINT = 'write me!'

class HelperTest(FunctionalTest):

    def test_robots(self):
        self.browser.get(self.live_server_url + "/robots.txt")
        self.assertNotIn("Not Found", self.browser.title)

    def test_humans(self):
        self.browser.get(self.live_server_url + "/humans.txt")
        self.assertNotIn("Not Found", self.browser.title)
