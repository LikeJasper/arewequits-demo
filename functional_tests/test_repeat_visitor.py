from .base import FunctionalTest
from unittest import skip
import re

from selenium.common.exceptions import NoSuchElementException

UNWRITTEN_COMPLAINT = 'write me!'

def process_sign_up_form(self):
    self.form = self.assert_element_exists('sign_up_form')
    self.email_box = self.assert_element_exists('id_email')
    self.email_box.clear()
    self.password1_box = self.assert_element_exists('id_password1')
    self.password1_box.clear()
    self.submit_button = self.assert_element_exists('signup_submit')

def valid_sign_up(self):
    process_sign_up_form(self)
    self.email_box.send_keys('amy@beech.com')
    self.password1_box.send_keys('password12345')
    self.submit_button.click()

def valid_login(self):
    self.browser.get(self.server_url + '/')
    self.assert_element_exists('cta_log_in_button').click()

    self.assert_element_exists('login_form')
    email_box = self.assert_element_exists('id_login')
    password_box = self.assert_element_exists('id_password')
    submit_button = self.assert_element_exists('login_submit')

    email_box.send_keys('amy@beech.com')
    password_box.send_keys('password12345')
    submit_button.click()

class RepeatVisitorGroupsTest(FunctionalTest):
    def setUp(self):
        super().setUp()
        self.browser.get(self.server_url + '/users/new/')
        valid_sign_up(self)
        self.browser.find_element_by_id('create_new_group_button').click()
        self.valid_group_creation()

    def assert_element_exists(self, id_):
        element = self.browser.find_element_by_id(id_)
        self.assertIsNotNone(element)
        return element

    def process_group_creation_form(self):
        self.form = self.assert_element_exists('create_group_form')
        self.group_name_box = self.assert_element_exists('input_group_name')
        self.assert_element_exists('input_emails')
        self.email_box = self.assert_element_exists('input_emails_0')
        self.assert_element_exists('input_emails_1')
        self.assert_element_exists('input_emails_2')
        self.assert_element_exists('input_emails_3')
        self.assert_element_exists('input_emails_4')
        self.currency_box = self.assert_element_exists('input_currency')
        self.submit_button = self.assert_element_exists('input_submit')

    def valid_group_creation(self, name='Household expenses', email='chandler@friends.com'):
        self.process_group_creation_form()
        self.group_name_box.send_keys(name)
        self.email_box.send_keys(email)
        self.submit_button.click()

    def test_login_with_two_groups(self):
        self.browser.find_element_by_id('logo').click()
        self.browser.find_element_by_id('create_new_group_button').click()
        self.valid_group_creation(name='Second group')
        self.hover_over('menu')
        self.browser.find_element_by_id('logout').click()
        valid_login(self)
        self.assertEqual(self.browser.current_url, self.server_url + '/?source=login')

    def test_login_with_one_group(self):
        self.hover_over('menu')
        self.browser.find_element_by_id('logout').click()
        valid_login(self)
        group_url = '^' + self.server_url + '/groups/' + '(\d+)' + '/view_group/$'
        group_regex = re.compile(group_url)
        self.assertRegexpMatches(self.browser.current_url, group_regex)

class RepeatVisitorTest(FunctionalTest):
    def setUp(self):
        super().setUp()
        self.browser.get(self.server_url + '/users/new/')
        valid_sign_up(self)
        self.hover_over('menu')
        self.browser.find_element_by_id('logout').click()

    def assert_element_exists(self, id_):
        element = self.browser.find_element_by_id(id_)
        self.assertIsNotNone(element)
        return element

    def assert_element_does_not_exist(self, id_):
        self.assertRaises(
            NoSuchElementException,
            self.browser.find_element_by_id,
            id_
        )

    def test_login_with_no_groups(self):
        valid_login(self)

        self.assertEqual(self.browser.current_url, self.server_url + '/?source=login')
        self.hover_over('menu')
        self.assert_element_exists('logout')
        self.assert_element_does_not_exist('cta_sign_up_button')

    def test_attempted_signup(self):
        self.browser.get(self.server_url + '/')
        self.assert_element_exists('cta_sign_up_button').click()

        process_sign_up_form(self)
        self.email_box.send_keys('amy@beech.com')
        self.password1_box.send_keys('password12345')
        self.submit_button.click()

        self.assertEqual(self.browser.current_url, self.server_url + '/users/new/')

    def test_unauthorized_home_page(self):
        # http://www.arewequits.com/ - **homepage** with **logo**, **tagline**, 
        # a **welcome message**, a **brief description** of the service, and an 
        # invitation to **log in** or **sign up**.
        # There are also links to an **about page** and a **contact page** in a **menu bar**.
        # **No account information**.
        self.browser.get(self.server_url + '/')
        self.assert_element_exists('cta_sign_up_button')
        self.assert_element_does_not_exist('group_list')
        self.assert_element_does_not_exist('contacts_list')

    def test_unauthorized_about_page(self):
        # http://www.arewequits.com/about/ - as **normal**. **No account information**.
        self.browser.get(self.server_url + '/about/')
        self.assert_element_exists('long_description')
        self.assert_element_does_not_exist('profile')

    def test_unauthorized_users_page(self):
        # http://www.arewequits.com/users/ - **404** page not found.
        self.browser.get(self.server_url + '/users/')
        self.assert_element_does_not_exist('logo')

    def test_unauthorized_specific_user_page(self):
        # http://www.arewequits.com/users/xxxxxx/ - **404** page not found.
        self.browser.get(self.server_url + '/users/1/')
        self.assert_element_does_not_exist('logo')

    def test_unauthorized_confirm_email_page(self):
        # http://www.arewequits.com/users/confirm_email - **404** page not found.
        self.browser.get(self.server_url + '/users/confirm_email')
        self.assert_element_does_not_exist('logo')

    def test_unauthorized_groups_page(self):
        # http://www.arewequits.com/groups/ - **404** page not found.
        self.browser.get(self.server_url + '/groups/')
        self.assert_element_does_not_exist('logo')

    def test_unauthorized_new_group_page(self):
        # http://www.arewequits.com/groups/new/ - **redirection** to http://www.arewequits.com/
        self.browser.get(self.server_url + '/groups/new/')
        self.assertEqual(self.browser.current_url, self.server_url + '/?next=/groups/new/')
        self.assert_element_exists('cta_sign_up_button')
        self.assert_element_does_not_exist('profile')

    def test_unauthorized_specific_group_page(self):
        # http://www.arewequits.com/groups/xxxxxx/ - **404** page not found.
        self.browser.get(self.server_url + '/groups/1/')
        self.assert_element_does_not_exist('logo')

    def test_unauthorized_view_group_page(self):
        # http://www.arewequits.com/groups/xxxxxx/view_group/ - 
        # **redirection** to http://www.arewequits.com/
        self.browser.get(self.server_url + '/groups/1/view_group/')
        self.assertEqual(self.browser.current_url, self.server_url + '/?next=/groups/1/view_group/')
        self.assert_element_exists('cta_sign_up_button')
        self.assert_element_does_not_exist('profile')

    def test_unauthorized_edit_payment_page(self):
        # http://www.arewequits.com/groups/xxxxxx/payments/xxxxxx/edit/ -
        # **redirection** to http://www.arewequits.com/
        self.browser.get(self.server_url + '/groups/1/payments/1/edit/')
        self.assertEqual(self.browser.current_url, self.server_url + '/?next=/groups/1/payments/1/edit/')
        self.assert_element_exists('cta_sign_up_button')
        self.assert_element_does_not_exist('profile')

    def test_unauthorized_delete_payment_page(self):
        # http://www.arewequits.com/groups/xxxxxx/payments/delete -
        # **redirection** to http://www.arewequits.com/
        self.browser.get(self.server_url + '/groups/1/payments/delete')
        self.assertEqual(self.browser.current_url, self.server_url + '/?next=/groups/1/payments/delete')
        self.assert_element_exists('cta_sign_up_button')
        self.assert_element_does_not_exist('profile')

    def test_unauthorized_view_profile_page(self):
        # http://www.arewequits.com/users/profile/ - **redirection** to
        # http://www.arewequits.com/
        self.browser.get(self.server_url + '/users/profile/')
        self.assertEqual(self.browser.current_url, self.server_url + '/?next=/users/profile/')
        self.assert_element_exists('cta_sign_up_button')
        self.assert_element_does_not_exist('profile')

    def test_unauthorized_edit_profile_page(self):
        # http://www.arewequits.com/users/profile/ - **redirection** to
        # http://www.arewequits.com/
        self.browser.get(self.server_url + '/users/profile/edit/')
        self.assertEqual(self.browser.current_url, self.server_url + '/?next=/users/profile/edit/')
        self.assert_element_exists('cta_sign_up_button')
        self.assert_element_does_not_exist('profile')

    def test_unauthorized_confirm_email_success_page(self):
        # http://www.arewequits.com/users/confirm_email_success/ - as **normal**.
        # **No account information**.

        self.fail(UNWRITTEN_COMPLAINT)

    def test_unauthorized_profile_page(self):
        # http://www.arewequits.com/profile/ - **redirection** to http://www.arewequits.com/

        self.fail(UNWRITTEN_COMPLAINT)

    def test_unauthorized_cancel_email_page(self):
        # http://www.arewequits.com/users/cancel_email - **404** page not found.

        self.fail(UNWRITTEN_COMPLAINT)

    def test_unauthorized_cancel_email_change_page(self):
        # http://www.arewequits.com/users/cancel_email_change/ - as **normal**.
        # **No account information**.

        self.fail(UNWRITTEN_COMPLAINT)
