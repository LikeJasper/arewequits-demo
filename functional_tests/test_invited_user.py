from .base import FunctionalTest
from unittest import skip

UNWRITTEN_COMPLAINT = 'write me!'

class UserAddedAsContactTest(FunctionalTest):
    def setUp(self):
        super().setUp()
        # Amy signs up
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('cta_sign_up_button').click()
        self.signup(
            email='amy@beech.com',
        )
        # She adds Chandler to a group
        self.browser.find_element_by_id('create_new_group_button').click()
        self.browser.find_element_by_id('input_group_name').send_keys('Friends')
        self.browser.find_element_by_id('input_emails_0').send_keys('chandler@friends.com')
        self.browser.find_element_by_id('input_submit').click()
        # Then she logs out
        self.hover_over('menu')
        self.browser.find_element_by_id('logout').click()

    def assert_element_exists(self, id_):
        element = self.browser.find_element_by_id(id_)
        self.assertIsNotNone(element)
        return element

    def process_sign_up_form(self):
        self.form = self.assert_element_exists('sign_up_form')
        self.email_box = self.assert_element_exists('id_email')
        self.email_box.clear()
        self.password1_box = self.assert_element_exists('id_password1')
        self.password1_box.clear()
        self.submit_button = self.assert_element_exists('signup_submit')

    def signup(self,
            email='chandler@friends.com',
            password1='password12345'):
        self.process_sign_up_form()
        self.email_box.send_keys(email)
        self.password1_box.send_keys(password1)
        self.submit_button.click()

    def test_registration_when_already_added_to_a_group(self):
        # Chandler ignores his verification email, but hears about the site from Amy
        # He decides to sign up directly.
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('cta_sign_up_button').click()
        self.signup()

        # He finds himself on the homepage as a logged-in user
        self.assertEqual(self.browser.current_url, self.server_url + '/')
        self.hover_over('menu')
        self.browser.find_element_by_id('account_details').click()
        self.browser.find_element_by_id('edit_profile_button').click()
        self.browser.find_element_by_id('input_first_name').send_keys('Chandler')
        self.browser.find_element_by_id('input_submit').click()
        self.hover_over('menu')
        self.browser.find_element_by_id('logout').click()

        # Amy logs in again
        self.browser.find_element_by_id('cta_log_in_button').click()
        self.browser.find_element_by_id('id_login').send_keys('amy@beech.com')
        self.browser.find_element_by_id('id_password').send_keys('password12345')
        self.browser.find_element_by_id('login_submit').click()

        # She now sees Chandler's name next to his email address
        self.assertIn('Chandler (chandler@friends.com)', self.browser.page_source)
