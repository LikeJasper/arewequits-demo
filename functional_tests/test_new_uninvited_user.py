# -*- coding: utf-8 -*-
from .base import FunctionalTest
from unittest import skip
import re
from datetime import date

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

UNWRITTEN_COMPLAINT = 'write me!'
NOT_EMAILS = [
    '',
    '12345678',
    '*$%(*&£%',
    'abcdefgh',
]

class NewUninvitedUserTest(FunctionalTest):

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

    def check_menu_bar_present(self):
        # Logo
        self.assert_element_exists('logo')

        # Tagline
        tagline = self.browser.find_element_by_id('tagline')
        correct_tagline = "AreWeQuits? is the easy way to share bills with your \
housemates, friends and colleagues."
        self.assertEqual(correct_tagline, tagline.text)

        # Menu bar
        self.assert_element_exists('menu_bar')

        # About
        about_link = self.assert_element_exists('footer_about_page')
        self.assertIsNotNone(about_link)

        # Contact
        contact_link = self.assert_element_exists('footer_contact_page')
        self.assertIsNotNone(contact_link)

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def process_sign_up_form(self):
        self.form = self.assert_element_exists('sign_up_form')
        self.email_box = self.assert_element_exists('id_email')
        self.email_box.clear()
        self.password1_box = self.assert_element_exists('id_password1')
        self.password1_box.clear()
        self.submit_button = self.assert_element_exists('signup_submit')

    def valid_sign_up(self, email='amy@beech.com', password='password12345'):
        self.process_sign_up_form()
        self.email_box.send_keys(email)
        self.password1_box.send_keys(password)
        self.submit_button.click()

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

    def process_new_contacts_form(self):
        self.form = self.assert_element_exists('new_contacts_form')
        self.assert_element_exists('input_emails')
        self.email_boxes = []
        for i in range(5):
            self.email_boxes.append(
                self.assert_element_exists('input_emails_{}'.format(str(i))))
        for email_box in self.email_boxes:
            email_box.clear()
        self.submit_button = self.assert_element_exists('input_submit')

    def process_new_payment_form(self, id_='create_payment_form', members=2):
        self.form = self.assert_element_exists(id_)
        self.date_box = self.assert_element_exists('input_date')
        self.amount_box = self.assert_element_exists('input_amount')
        self.description_box = self.assert_element_exists('input_description')
        self.assert_element_exists('input_who_paid_0')
        self.who_paid_0 = self.browser.find_element_by_css_selector('label[for="input_who_paid_0"]')
        self.assertIn('amy@beech.com', self.who_paid_0.text)
        self.who_paid_1 = self.browser.find_element_by_css_selector('label[for="input_who_paid_1"]')
        self.assertIn('chandler@friends.com', self.who_paid_1.text)
        self.assertRaises(
            NoSuchElementException,
            self.browser.find_element_by_id,
            'input_who_paid_{}'.format(str(members))
        )
        self.who_for_0 = self.browser.find_element_by_css_selector('label[for="input_who_for_0"]')
        self.assertIn('amy@beech.com', self.who_for_0.text)
        self.who_for_1 = self.browser.find_element_by_css_selector('label[for="input_who_for_1"]')
        self.assertIn('chandler@friends.com', self.who_for_1.text)
        self.submit_button = self.assert_element_exists('input_submit')

        # self.date_box.clear()
        self.amount_box.click()
        self.amount_box.send_keys(Keys.COMMAND, 'a')
        self.amount_box.send_keys(Keys.DELETE)
        self.description_box.clear()
        if self.who_for_0.is_selected():
            self.who_for_0.click()
        if self.who_for_1.is_selected():
            self.who_for_1.click()

    def process_edit_profile_form(self):
        self.assert_element_exists('edit_profile_form')
        self.first_name_box = self.assert_element_exists('input_first_name')
        self.last_name_box = self.assert_element_exists('input_last_name')
        self.email_box = self.assert_element_exists('input_email')
        self.submit_button = self.assert_element_exists('input_submit')

    def sign_up_with_group_and_payment(self):
        # Amy signs up for an account and creates a group
        self.browser.get(self.server_url + '/users/new/')
        self.valid_sign_up()
        self.browser.find_element_by_id('create_new_group_button').click()
        self.valid_group_creation()

        # She creates a payment
        self.browser.find_element_by_id('create_new_payment_button').click()
        self.process_new_payment_form()
        self.amount_box.send_keys('10.00')
        self.description_box.send_keys('First group payment')
        self.who_paid_0.click()
        self.who_for_1.click()
        self.submit_button.click()
        self.browser.find_element_by_id('logo').click()
        overview_table = self.assert_element_exists('overview_table')
        self.assertIn('£5.00', overview_table.text)

    def test_delete_group(self):
        # Amy signs up for an account and creates a group
        self.browser.get(self.server_url + '/users/new/')
        self.valid_sign_up()
        self.browser.find_element_by_id('create_new_group_button').click()
        self.valid_group_creation()

        # She realises she didn't need to make that one
        self.browser.find_element_by_id('edit_group_button').click()
        self.browser.find_element_by_id('input_delete').click()

        # She finds herself on the "My groups" page and the group is not there
        self.assertEqual(self.browser.current_url, self.server_url + '/')
        self.assertNotIn('Household expenses', self.browser.page_source)

    def test_edit_group_page(self):
        # Amy signs up for an account and creates a group
        self.browser.get(self.server_url + '/users/new/')
        self.valid_sign_up()
        self.browser.find_element_by_id('create_new_group_button').click()
        self.valid_group_creation()

        # She realises that she gave the group the wrong name, and clicks on 
        # the "Edit Group Details" button to correct it
        self.browser.find_element_by_id('edit_group_button').click()

        expected_url = '^' + self.server_url + \
            '/groups/' + '(\d+)' + '/edit_group/$'
        group_regex = re.compile(expected_url)
        group_url = self.browser.current_url
        self.assertRegexpMatches(group_url, group_regex)

        self.assertIn('Household expenses', self.browser.page_source)
        self.assertIn('£', self.browser.page_source)

        # She renames it "Travel expenses" and puts the currency into $
        group_name_box = self.browser.find_element_by_id('id_name')
        group_name_box.clear()
        group_name_box.send_keys('Travel expenses')

        self.browser.find_element_by_class_name('select-dropdown').click()
        self.browser.find_element_by_xpath('//div[@class="select-wrapper"]/ul/li[3]').click()

        self.browser.find_element_by_id('input_submit').click()

        self.assertIn('Travel expenses', self.browser.page_source)
        self.assertNotIn('Household expenses', self.browser.page_source)

        self.assertIn('€0.00', self.browser.page_source)
        self.assertNotIn('£0.00', self.browser.page_source)

    def test_group_activity_log(self):
        self.sign_up_with_group_and_payment()
        self.browser.find_element_by_link_text('Household expenses').click()
        self.browser.find_element_by_id('add_group_members_button').click()
        self.browser.find_element_by_id('input_emails_0').send_keys('ross@friends.com')
        self.browser.find_element_by_id('input_emails_1').send_keys('rachel@friends.com')
        self.browser.find_element_by_id('input_submit').click()

        self.browser.find_element_by_id('id_activity_log').click()
        log_table = self.browser.find_element_by_id('id_log_table')

        self.assertIn('(amy@beech.com) created the group.', log_table.text)
        self.assertIn('(amy@beech.com) created a payment.', log_table.text)
        self.assertIn('(amy@beech.com) added (ross@friends.com) to the group.', log_table.text)
        self.assertIn('(amy@beech.com) added (rachel@friends.com) to the group.', log_table.text)

        self.browser.find_element_by_link_text('a payment').click()
        payment_url = '^' + self.server_url + \
            '/groups/' + '(\d+)' + '/payments/' + '(\d+)' + '/edit/$'
        payment_regex = re.compile(payment_url)
        self.assertRegexpMatches(self.browser.current_url, payment_regex)

        self.process_new_payment_form(id_='edit_payment_form', members=4)
        self.amount_box.send_keys('444.44')
        self.description_box.send_keys('Edited')
        self.submit_button.click()
        self.browser.find_element_by_id('id_activity_log').click()
        log_table = self.browser.find_element_by_id('id_log_table')

        self.assertIn('(amy@beech.com) created the group.', log_table.text)
        self.assertIn('(amy@beech.com) created a payment.', log_table.text)
        self.assertIn('(amy@beech.com) edited a payment.', log_table.text)

        self.browser.find_element_by_link_text('a payment').click()
        self.browser.find_element_by_id('input_delete').click()
        self.browser.find_element_by_id('id_activity_log').click()
        log_table = self.browser.find_element_by_id('id_log_table')

        self.assertIn('(amy@beech.com) created the group.', log_table.text)
        self.assertIn('(amy@beech.com) created a payment.', log_table.text)
        self.assertIn('(amy@beech.com) edited a payment.', log_table.text)
        self.assertIn('(amy@beech.com) deleted a payment.', log_table.text)

    def test_two_groups_with_the_same_name(self):
        self.sign_up_with_group_and_payment()

        # If she clicks on "Create new group" again, the process is **the same** even
        # if she uses the same group name.
        self.browser.find_element_by_id('create_new_group_button').click()
        self.valid_group_creation()
        self.browser.find_element_by_id('logo').click()
        overview_table = self.assert_element_exists('overview_table')
        self.assertIn('£5.00', overview_table.text)
        self.assertIn('£0.00', overview_table.text)

        self.browser.find_element_by_link_text('£0.00').click()
        self.browser.find_element_by_id('create_new_payment_button').click()
        self.process_new_payment_form()
        self.amount_box.send_keys('12.00')
        self.description_box.send_keys('First group payment')
        self.who_paid_0.click()
        self.who_for_1.click()
        self.submit_button.click()
        self.browser.find_element_by_id('logo').click()
        overview_table = self.assert_element_exists('overview_table')
        self.assertIn('£5.00', overview_table.text)
        self.assertIn('£6.00', overview_table.text)

    def test_second_group_creation(self):
        self.sign_up_with_group_and_payment()

        # If she clicks on "Create new group" again, the process is **the same** except 
        # when it comes to adding members to the group she can both **add email 
        # addresses** or **select users from her Contacts list** using a **checkbox** 
        # system.
        self.browser.find_element_by_id('create_new_group_button').click()
        self.valid_group_creation(name='Work stuff', email='gunther@friends.com')
        self.browser.find_element_by_id('logo').click()
        overview_table = self.assert_element_exists('overview_table')
        self.assertIn('£5.00', overview_table.text)
        self.assertIn('£0.00', overview_table.text)

    def test_second_payment_creation(self):
        # Amy signs up for an account and creates a group

        self.browser.get(self.server_url + '/users/new/')
        self.valid_sign_up()
        self.browser.find_element_by_id('create_new_group_button').click()
        self.valid_group_creation()

        # She is **taken** to 
        # http://www.arewequits.com/groups/xxxxxx/view_group/ where she can 
        # add a new payment.
        specific_group_url = self.browser.current_url
        self.browser.find_element_by_id('create_new_payment_button').click()
        self.process_new_payment_form()
        self.amount_box.send_keys('8.02')
        self.description_box.send_keys('First')
        self.who_paid_0.click()
        self.who_for_1.click()
        self.submit_button.click()

        # She adds a second payment
        self.browser.find_element_by_id('create_new_payment_button').click()
        self.process_new_payment_form()
        self.amount_box.send_keys('16.50')
        self.description_box.send_keys('Second')
        self.who_paid_1.click()
        self.who_for_1.click()
        self.submit_button.click()

        # The payments are listed in reverse order of creation since they have
        # the same date.
        payments_table = self.assert_element_exists('id_payments_ul').text
        self.assertIn('£16.50', payments_table)
        payments_table_end = payments_table.split('£16.50', 1)[1]
        self.assertIn('£8.02', payments_table_end)

    def test_first_payment_creation(self):
        # Amy signs up for an account and creates a group

        self.browser.get(self.server_url + '/users/new/')
        self.valid_sign_up()
        new_group_link = self.browser.find_element_by_id('create_new_group_button')
        new_group_link.click()
        self.valid_group_creation()

        # She is **taken** to 
        # http://www.arewequits.com/groups/xxxxxx/view_group/ .
        group_url = '^' + self.server_url + '/groups/' + '(\d+)' + '/view_group/$'
        group_regex = re.compile(group_url)
        specific_group_url = self.browser.current_url
        self.assertRegexpMatches(specific_group_url, group_regex)

        # The page shows an **empty table** called **"Payments"** and a 
        # **button** saying **"Add new payment"**.
        self.assert_element_exists('payments_list')
        new_payment_link = self.browser.find_element_by_id('create_new_payment_button')

        # There is another **table** at the side called **"Group members"** which lists 
        # the **email addresses** of the people she added to the group (and their 
        # **names** if they are registered users).
        members_table = self.assert_element_exists('members_table')
        self.assertIn('amy@beech.com', members_table.text)
        self.assertIn('chandler@friends.com', members_table.text)

        # Next to each member is a **balance** which shows **0.00** in the **currency** 
        # specified when the group was created.
        self.assertIn('£0.00', members_table.text)

        # There is a **button** saying **"Add new group members"**.
        self.browser.find_element_by_id('add_group_members_button')

        # If she clicks on "Add new payment", she is **taken** to
        # http://www.arewequits.com/groups/xxxxxx/new_payment/ where there is a **form** 
        # which asks her for a **date** (default **today**), an **amount** (default 
        # **0.00**) in the **currency** specified for the group, and a **description** 
        # of the item.
        # She is asked to select **who paid** using **radio buttons** next to **each of 
        # the group members' names** (defaulted to select **her**).
        # She is also asked to select **who gained** using **checkboxes** next to **each 
        # of the group members' names** (all defaulted to **unchecked**).
        # There is a **button** saying **"Add payment"**. She is selected under "Who paid"
        # and "Who for".
        new_payment_link.click()
        expected_url = specific_group_url.replace('view_group', 'new_payment')
        self.assertEqual(self.browser.current_url, expected_url)

        who_paid_radio = self.browser.find_element_by_id('input_who_paid_0')
        self.assertTrue(who_paid_radio.is_selected())

        who_for_checkbox = self.browser.find_element_by_id('input_who_for_0')
        self.assertTrue(who_for_checkbox.is_selected())

        # If she tries to submit the form without supplying a **date**, an **amount**, or a 
        # **description**, or without checking at least **one person who gained**, the 
        # page asks her to **correct it**.

        # No amount
        self.process_new_payment_form()
        # self.date_box.send_keys('2015-05-02')
        self.description_box.send_keys('Blah')
        self.who_paid_0.click()
        self.who_for_1.click()
        self.submit_button.click()
        self.assertEqual(self.browser.current_url, expected_url)

        # Amount is not a number
        self.process_new_payment_form()
        # self.date_box.send_keys('2000-01-01')
        self.amount_box.send_keys('Not numbers')
        self.description_box.send_keys('Blah')
        self.who_paid_0.click()
        self.who_for_1.click()
        self.submit_button.click()
        self.assertEqual(self.browser.current_url, expected_url)

        # Amount is invalid number
        self.process_new_payment_form()
        # self.date_box.send_keys('2015-05-02')
        self.amount_box.send_keys('12.345')
        self.description_box.send_keys('Blah')
        self.who_paid_0.click()
        self.who_for_1.click()
        self.submit_button.click()
        self.assertEqual(self.browser.current_url, expected_url)

        # No description
        self.process_new_payment_form()
        # self.date_box.send_keys('2015-05-02')
        self.amount_box.send_keys('65.43')
        self.who_paid_0.click()
        self.who_for_1.click()
        self.submit_button.click()
        self.assertEqual(self.browser.current_url, expected_url)

        # No who_for
        self.process_new_payment_form()
        # self.date_box.send_keys('1999-12-31')
        self.amount_box.send_keys('8.02')
        self.description_box.send_keys('Blah')
        self.who_paid_0.click()
        self.who_for_0.click() # Deselects preselected box
        self.submit_button.click()
        self.assertEqual(self.browser.current_url, expected_url)

        # If she successfully adds a new entry she is **redirected** to 
        # http://www.arewequits.com/groups/xxxxxx/view_group/ which looks the **same as before** 
        # except there is a "That's it! Now add more entries as you need." 
        # **success message** and the Payments table is **no longer empty**.

        self.process_new_payment_form()
        # self.date_box.send_keys('2012-03-01') - Invalid due to date picker
        self.amount_box.send_keys('8.02')
        self.description_box.send_keys('Blah')
        self.who_paid_0.click()
        self.who_for_1.click()
        self.submit_button.click()
        self.assertEqual(self.browser.current_url, specific_group_url)

        # The **entry she just added is listed in the table**, showing the **date**, 
        # **cost**, **name of the person who paid**, and **names** or **email addresses 
        # of the people who gained**, depending on whether they are **registered users**.
        payments_table = self.assert_element_exists('id_payments_ul')
        payment_data = ['{dt:%b}. {dt.day}, {dt:%Y}'.format(dt = date.today()), 
            '£8.02', 'amy@beech.com']
        for datum in payment_data:
            self.assertIn(datum, payments_table.text)

        # In the "Group members table" the **balance** now shows **appropriate values** 
        # next to **each member** (whoever paid will have a **positive** number and 
        # anyone who gained but did not pay will have a **negative** number; 
        # anyone who was not involved will still have a balance of **0.00**).
        members_table = self.assert_element_exists('members_table')
        self.assertIn('4.01', members_table.text)
        self.assertIn('-4.01', members_table.text)

        # When she goes back to the homepage, her balance is displayed in the group table
        self.browser.find_element_by_id('logo').click()
        overview_table = self.assert_element_exists('overview_table')
        self.assertIn('4.01', overview_table.text)

    def test_user_profile(self):
        # Amy signs up
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('cta_sign_up_button').click()
        self.valid_sign_up()

        # She clicks on her name in the menu bar and is taken to her profile page
        self.hover_over('menu')
        self.browser.find_element_by_id('account_details').click()
        self.assertEqual(self.browser.current_url, self.server_url + '/users/profile/')

        # She can see her first name, last name, and email address there.
        self.assertIn('amy@beech.com', self.browser.page_source)

        # She clicks a big button that says "Edit" and is taken to an edit page
        self.browser.find_element_by_id('edit_profile_button').click()
        self.assertEqual(self.browser.current_url, self.server_url + '/users/profile/edit/')

        # She sees a form with fields for her first name, last name and email address.
        self.process_edit_profile_form()

        # Her existing information is already there.
        self.assertIn('amy@beech.com', self.browser.page_source)

        # If she tries to submit the form with a blank first name, it takes her 
        # back to the same page
        self.first_name_box.clear()
        self.submit_button.click()
        self.assertEqual(self.browser.current_url, self.server_url + '/users/profile/edit/')

        # If she tries to submit the form with a blank last name, it takes her 
        # back to the same page
        self.process_edit_profile_form()
        self.last_name_box.clear()
        self.submit_button.click()
        self.assertEqual(self.browser.current_url, self.server_url + '/users/profile/edit/')

        # If she tries to submit the form with a blank email address, it takes her
        # back to the same page
        self.process_edit_profile_form()
        self.email_box.clear()
        self.submit_button.click()
        self.assertEqual(self.browser.current_url, self.server_url + '/users/profile/edit/')

        # If she tries to submit the form with an invalid email address, it takes her
        # back to the same page
        self.process_edit_profile_form()
        self.email_box.clear()
        self.email_box.send_keys('not an email')
        self.submit_button.click()
        self.assertEqual(self.browser.current_url, self.server_url + '/users/profile/edit/')

        # If she succesfully types in her details, she is taken to her profile page
        self.process_edit_profile_form()
        self.first_name_box.clear()
        self.first_name_box.send_keys('Amelie')
        self.last_name_box.clear()
        self.last_name_box.send_keys('Beecham')
        self.email_box.clear()
        self.email_box.send_keys('amelie@beecham.com')
        self.submit_button.click()
        self.assertEqual(self.browser.current_url, self.server_url + '/users/profile/')

        # Her new details appear there
        self.assertIn('Amelie', self.browser.page_source)
        self.assertIn('Beecham', self.browser.page_source)
        self.assertIn('amelie@beecham.com', self.browser.page_source)

    def test_payment_deletion(self):
        # Amy signs up
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('cta_sign_up_button').click()
        self.valid_sign_up()

        # Amy creates a new group using a new contact, Chandler
        self.browser.find_element_by_id('create_new_group_button').click()
        self.valid_group_creation()

        # Amy adds a payment
        self.browser.find_element_by_id('create_new_payment_button').click()
        self.process_new_payment_form()
        self.amount_box.send_keys('8.02')
        self.description_box.send_keys('Amy stuff')
        self.who_paid_0.click()
        self.who_for_1.click()
        self.submit_button.click()

        # She decides she shouldn't have added that payment after all and goes to delete it
        self.browser.find_element_by_xpath('//ul[@id="id_payments_ul"]/li/div/div[1]').click()
        self.browser.find_element_by_link_text('Edit').click()
        payment_url = '^' + self.server_url + \
            '/groups/' + '(\d+)' + '/payments/' + '(\d+)' + '/edit/$'
        payment_regex = re.compile(payment_url)
        self.assertRegexpMatches(self.browser.current_url, payment_regex)
        self.browser.find_element_by_id('input_delete').click()

        # She finds herself back on the group page
        group_url = '^' + self.server_url + \
            '/groups/' + '(\d+)' + '/view_group/'
        group_regex = re.compile(group_url)
        self.assertRegexpMatches(self.browser.current_url, group_regex)

        # Her payment has disappeared
        self.assertNotIn('8.02', self.browser.page_source)
        self.assertNotIn('Amy stuff', self.browser.page_source)

    def test_payment_editing(self):
        # Amy signs up
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('cta_sign_up_button').click()
        self.valid_sign_up()

        # Amy creates a new group using a new contact, Chandler
        self.browser.find_element_by_id('create_new_group_button').click()
        self.valid_group_creation()

        # Amy adds a payment
        self.browser.find_element_by_id('create_new_payment_button').click()
        self.process_new_payment_form()
        self.amount_box.send_keys('8.02')
        self.description_box.send_keys('Amy stuff')
        self.who_paid_0.click()
        self.who_for_0.click()
        self.who_for_1.click()
        self.submit_button.click()

        # She realises she made a mistake so she clicks on the description to edit the 
        # details of the payment. The page she is taken to shows a form with the existing
        # details already in place.
        self.browser.find_element_by_xpath('//ul[@id="id_payments_ul"]/li/div/div[1]').click()
        self.browser.find_element_by_link_text('Edit').click()
        payment_url = '^' + self.server_url + \
            '/groups/' + '(\d+)' + '/payments/' + '(\d+)' + '/edit/$'
        payment_regex = re.compile(payment_url)
        expected_url = self.browser.current_url
        self.assertRegexpMatches(expected_url, payment_regex)
        self.assertIn('{dt:%d} {dt:%B}, {dt:%Y}'.format(dt=date.today()), self.browser.page_source)
        self.assertIn('Amy stuff', self.browser.page_source)
        self.assertIn('8.02', self.browser.page_source)
        self.assertTrue(self.browser.find_element_by_id('input_who_paid_0').is_selected())
        self.assertFalse(self.browser.find_element_by_id('input_who_paid_1').is_selected())
        # form processing deselects first who_for...
        self.assertFalse(self.browser.find_element_by_id('input_who_for_0').is_selected())
        self.assertTrue(self.browser.find_element_by_id('input_who_for_1').is_selected())

        # If she tries to submit the form without supplying a **date**, an **amount**, or a 
        # **description**, or without checking at least **one person who gained**, the 
        # page asks her to **correct it**.

        # No amount
        self.process_new_payment_form(id_='edit_payment_form')
        # self.date_box.send_keys('2015-05-02')
        self.description_box.send_keys('Blah')
        self.who_paid_1.click()
        self.submit_button.click()
        self.assertEqual(self.browser.current_url, expected_url)

        # Amount is not a number
        self.process_new_payment_form(id_='edit_payment_form')
        # self.date_box.send_keys('2000-01-01')
        self.amount_box.send_keys('Not numbers')
        self.description_box.send_keys('Blah')
        self.who_paid_1.click()
        self.submit_button.click()
        self.assertEqual(self.browser.current_url, expected_url)

        # Amount is invalid number
        self.process_new_payment_form(id_='edit_payment_form')
        # self.date_box.send_keys('2015-05-02')
        self.amount_box.send_keys('12.345')
        self.description_box.send_keys('Blah')
        self.who_paid_1.click()
        self.submit_button.click()
        self.assertEqual(self.browser.current_url, expected_url)

        # No description
        self.process_new_payment_form(id_='edit_payment_form')
        # self.date_box.send_keys('2015-05-02')
        self.amount_box.send_keys('65.43')
        self.who_paid_1.click()
        self.submit_button.click()
        self.assertEqual(self.browser.current_url, expected_url)

        # No who_for
        self.process_new_payment_form(id_='edit_payment_form')
        # self.date_box.send_keys('1999-12-31')
        self.amount_box.send_keys('8.02')
        self.description_box.send_keys('Blah')
        self.who_paid_1.click()
        self.who_for_1.click()
        self.submit_button.click()
        self.assertEqual(self.browser.current_url, expected_url)

        # If she successfully saves the edited payment she is **redirected** to 
        # http://www.arewequits.com/groups/xxxxxx/view_group/ which looks the **same as before**
        # except the details are changed to match what she entered.

        self.process_new_payment_form(id_='edit_payment_form')
        # self.date_box.send_keys('2012-03-01') - Invalid due to date picker
        self.amount_box.send_keys('81.02')
        self.description_box.send_keys('Blah')
        self.who_paid_1.click()
        self.who_for_0.click()
        self.submit_button.click()
        group_url = '^' + self.server_url + \
            '/groups/' + '(\d+)' + '/view_group/'
        group_regex = re.compile(group_url)
        self.assertRegexpMatches(self.browser.current_url, group_regex)

        # The **entry she just added is listed in the table**, showing the **date**, 
        # **cost**, **name of the person who paid**, and **names** or **email addresses 
        # of the people who gained**, depending on whether they are **registered users**.
        payments_table = self.assert_element_exists('id_payments_ul')
        payment_data = ['{dt:%b}. {dt.day}, {dt:%Y}'.format(dt = date.today()), 
            '£81.02', 'chandler@friends.com']
        for datum in payment_data:
            self.assertIn(datum, payments_table.text)

        # In the "Group members table" the **balance** now shows **appropriate values** 
        # next to **each member** (whoever paid will have a **positive** number and 
        # anyone who gained but did not pay will have a **negative** number; 
        # anyone who was not involved will still have a balance of **0.00**).
        members_table = self.assert_element_exists('members_table')
        self.assertIn('81.02', members_table.text)
        self.assertIn('-81.02', members_table.text)

        # When she goes back to the homepage, her balance is displayed in the group table
        self.browser.find_element_by_id('logo').click()
        overview_table = self.assert_element_exists('overview_table')
        self.assertIn('-81.02', overview_table.text)

    def test_add_members_to_group(self):
        # Amy signs up
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('cta_sign_up_button').click()
        self.valid_sign_up()

        # Amy creates a new group using a new contact, Chandler
        self.browser.find_element_by_id('create_new_group_button').click()
        self.valid_group_creation()

        # If she clicks on "Add new group members" from the Group members table on an 
        # account page then she will be **taken** to 
        # http://www.arewequits.com/groups/xxxxxx/new_members/ where there will be a 
        # **form** where she can enter **up to 5 email addresses**.
        members_table = self.browser.find_element_by_id('members_table')
        self.assertNotIn('gunther@friends.com', members_table.text)
        self.assertNotIn('monica@friends.com', members_table.text)
        self.browser.find_element_by_id('add_group_members_button').click()
        group_url = '^' + self.server_url + \
            '/groups/' + '(\d+)' + '/add_members/'
        group_regex = re.compile(group_url)
        self.assertRegexpMatches(self.browser.current_url, group_regex)
        self.assertIn('Add members to Household expenses', self.browser.page_source)

        # If she has contacts who are not already members of the group they are also 
        # **listed here** with a **checkbox** next to their name (default **unchecked**).
        # Existing group members are not shown.
        self.assertNotIn('chandler@friends.com', self.browser.page_source)

        # There is a **button** that says **"Add people to group"**.
        submit_button = self.browser.find_element_by_id('input_submit')

        # If she tries to submit the form without having entered any **email addresses** 
        # or having checked any **checkboxes** then the page **asks her to**.
        submit_button.click()
        self.assertEqual(self.browser.current_url, self.server_url + '/groups/1/add_members/')

        # If she tries to submit the form with an email address which is obviously 
        # invalid then it asks her to **correct it**.
        self.browser.find_element_by_id('input_emails_0').send_keys('not_an_email')
        self.browser.find_element_by_id('input_submit').click()
        self.assertEqual(self.browser.current_url, self.server_url + '/groups/1/add_members/')

        # If she clicks on "Add people to group" she is **redirected** to the group page.
        email_input = self.browser.find_element_by_id('input_emails_0')
        email_input.clear()
        email_input.send_keys('monica@friends.com')
        self.browser.find_element_by_id('input_submit').click()
        self.assertEqual(self.browser.current_url, self.server_url + '/groups/1/view_group/')

        # Now the **people she added** are visible in the **Group members table** with a 
        # balance of **0.00**.
        members_table = self.browser.find_element_by_id('members_table')
        self.assertIn('monica@friends.com', members_table.text)
        self.assertEqual(members_table.text.count('0.00'), 3)

        # If she then tries to add an entry to that group (but **not any other group** 
        # unless they were **already added** to it) they also **appear as options** for 
        # the **paid**/**gained** sections of the form.
        self.browser.find_element_by_id('create_new_payment_button').click()
        self.assertIn('monica@friends.com', self.browser.page_source)

    def test_new_uninvited_visitors_have_similar_experiences_with_nobody_elses_info(self):
        # Any subsequent new uninvited users should have an experience that 
        # **corresponds exactly** to Amy's.

        # In particular, they should not see any information **relating to Amy**.

        # Amy signs up
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('cta_sign_up_button').click()
        self.valid_sign_up()

        # Amy creates a new group
        self.browser.find_element_by_id('create_new_group_button').click()
        self.valid_group_creation()

        # Amy adds a payment
        self.browser.find_element_by_id('create_new_payment_button').click()
        self.process_new_payment_form()
        self.amount_box.send_keys('8.02')
        self.description_box.send_keys('Amy stuff')
        self.who_paid_0.click()
        self.who_for_0.click()
        self.who_for_1.click()
        self.submit_button.click()

        # Amy logs out
        self.hover_over('menu')
        self.browser.find_element_by_id('logout').click()

        # Brian signs up
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('cta_sign_up_button').click()
        self.valid_sign_up(email='brian@jonesing.com')

        # He tries to visit Amy's group page, but ends up at a 404
        self.browser.get(self.server_url + '/groups/1/view_group/')
        self.assertEqual(self.browser.title, 'Page Not Found')

        # He tries to add a new payment to Amy's group, but ends up at a 404
        self.browser.get(self.server_url + '/groups/1/new_payment/')
        self.assertEqual(self.browser.title, 'Page Not Found')

        # The home page is empty of groups and contacts
        self.browser.get(self.server_url + '/')
        self.assertNotIn('Household expenses', self.browser.page_source)
        self.assertNotIn('amy@beech.com', self.browser.page_source)
        self.assertNotIn('chandler@friends.com', self.browser.page_source)

        # Brian goes to create a group. There are no suggestions for group members to add.
        self.browser.find_element_by_id('create_new_group_button').click()
        self.assertNotIn('amy@beech.com', self.browser.page_source)
        self.assertNotIn('chandler@friends.com', self.browser.page_source)

        self.valid_group_creation(name='Unrelated', email='richard@friends.com')

        # Brian views the group. There are no payments, his information is there, 
        # but none of Amy's information is present.
        self.assertIn('brian@jonesing.com', self.browser.page_source)
        self.assertIn('richard@friends.com', self.browser.page_source)
        self.assertNotIn('amy@beech.com', self.browser.page_source)
        self.assertNotIn('chandler@friends.com', self.browser.page_source)
        self.assertNotIn('Amy stuff', self.browser.page_source)
        self.assertNotIn('8.02', self.browser.page_source)
        self.assertNotIn('4.01', self.browser.page_source)

        # Brian goes to create a payment. His contact is an option there, but none of Amy's
        # information is present.
        self.browser.find_element_by_id('create_new_payment_button').click()
        self.assertIn('brian@jonesing.com', self.browser.page_source)
        self.assertIn('richard@friends.com', self.browser.page_source)
        self.assertNotIn('amy@beech.com', self.browser.page_source)
        self.assertNotIn('chandler@friends.com', self.browser.page_source)

    def test_home_page_displays_welcome_message_and_ctas(self):
        # Amy hears about the app and visits the [homepage].
        self.browser.get(self.server_url)

        # Because she is not an existing user she is **not logged in** and cannot 
        # access any **account features**.

        # The title of the webpage is "Are we quits?".
        self.assertIn('AreWeQuits?', self.browser.title)

        # She sees a **logo**, a **tagline**, a **welcome message**, and an invitation to 
        # **log in** or **sign up**.
        # There are also links to an **about page** and a **contact page** in a 
        # **menu bar**.
        self.check_menu_bar_present()
        self.assert_element_exists('welcome_message')
        self.assert_element_exists('cta_sign_up_button')
        self.assert_element_exists('cta_log_in_button')

        # Clicking on the logo (from the **homepage** or **anywhere else** on the site) 
        # **takes** her back to the [homepage][homepage].
        logo = self.browser.find_element_by_id('logo')
        logo.click()
        self.assertEqual(self.browser.current_url, self.server_url + '/')        

    def test_about_page_has_long_description(self):
        # Amy hears about the app and visits the [homepage].
        self.browser.get(self.server_url)

        # Clicking on the about page link (from the **homepage** or **anywhere else** 
        # on the site) **takes** her to the [about page][about page] where there are more 
        # **extensive details** on what the service involves and how to use it. 
        about_link = self.browser.find_element_by_id('footer_about_page')
        about_link.click()
        self.assertEqual(self.browser.current_url, self.server_url + '/about/')

        self.assert_element_exists('long_description')

        # She can still see the **logo**, **tagline**, and links to the **about** and 
        # **contact** pages, and there are links to **log in** or **sign up** in the 
        # **menu bar**.
        self.check_menu_bar_present()

    def test_first_group_creation(self):
        # If she clicks on "Create new group" she is **taken** to the [new group page]
        # [new group] where there is a **form** which asks for a **name for the group** 
        # and the **email addresses of the other people** who should be in that group.

        # There is a **drop-down menu listing currencies**, with the **default** being 
        # the currency used in the location associated with her IP address.

        # There is a big "Save group" **button**.

        self.browser.get(self.server_url + '/users/new/')
        self.valid_sign_up()
        new_group_link = self.browser.find_element_by_id('create_new_group_button')
        new_group_link.click()

        self.assertEqual(self.browser.current_url, self.server_url + '/groups/new/')

        self.process_group_creation_form()
        # self.assertRaises(
        #     NoSuchElementException,
        #     self.browser.find_element_by_id,
        #     'input_members'
        # )

        # There should be some **explanatory text** saying something like "For example, 
        # if this is to keep track of your household expenses, you could call it 
        # 'Household expenses' and enter the email addresses of your housemates."
        self.assert_element_exists('input_submit')

        # The page will ask her to **change any email addresses that are obviously 
        # invalid** before allowing her to submit the form.


        # The form will provide a **relevant prompt** if **no name** is given to the 
        # group, or if **no email** addresses are given.

        # If she clicks on "Save group" she is taken to the group page for her
        # newly created group.
        self.valid_group_creation()
        new_group_url = '^' + self.server_url + '/groups/' + '(\d+)' + '/view_group/$'
        new_group_regex = re.compile(new_group_url)
        specific_new_group_url = self.browser.current_url
        self.assertRegexpMatches(specific_new_group_url, new_group_regex)

        # If she clicks on the logo she is **taken** to the [homepage][homepage] 
        # where she again sees the **Overview** and **Contacts** tables.
        self.browser.find_element_by_id('logo').click()
        self.assertEqual(self.browser.current_url, self.server_url + '/')

        # This time the Overview table has the **name of the group** she just created 
        # and a **balance value of 0.00**. The value is in the **currency she specified**
        # when she created the group.
        table = self.assert_element_exists('overview_table')
        self.assertIn('Household expenses', table.text)
        self.assertIn('£0.00', table.text)

        # The name of the group she created is a **link**.
        group_link = self.browser.find_element_by_link_text('Household expenses')

        # Under that group there is still the **button** that says **"Create new 
        # group"**.
        self.assert_element_exists('create_new_group_button')

    def test_signup(self):
        # Clicking on the sign up button (from the **homepage** or **anywhere else** 
        # on the site) reveals a **form** with fields for her **first** and **last** 
        # names, **email address** and **password**.

        self.browser.get(self.server_url)
        button = self.assert_element_exists('cta_sign_up_button')
        button.click()

        for not_email in NOT_EMAILS:
            self.process_sign_up_form()

            # If she tries to enter an **email address that is obviously not valid** then 
            # she will be asked to use a **real one**.
            self.password1_box.send_keys('password12345')
            self.email_box.send_keys(not_email)
            self.submit_button.click()

            self.assertEqual(self.browser.current_url, self.server_url + '/users/new/')

        # If she tries to enter a **password that is less than 8 characters long** 
        # she will be asked to enter a **longer one**.
        self.process_sign_up_form()
        self.email_box.send_keys('amy@beech.com')
        self.password1_box.send_keys('abcdefg')
        self.submit_button.click()

        self.assertEqual(self.browser.current_url, self.server_url + '/users/new/')

        # If she successfully signs up for an account she will be **redirected** to the 
        # [homepage][homepage] as a **logged-in user**.
        self.valid_sign_up()

        self.assertEqual(self.browser.current_url, self.server_url + '/?source=login')
        self.assert_element_exists('logout')

    def test_logout(self):
        # Amy signs up for an account

        self.browser.get(self.server_url + '/users/new/')
        self.valid_sign_up()

        # She decides to come back later and logs out
        self.hover_over('menu')
        self.browser.find_element_by_id('logout').click()

        # She ends up at the homepage but is no longer logged in.
        self.assertEqual(self.browser.current_url, self.server_url + '/')
        self.assert_element_does_not_exist('profile')

    # @skip
    # def test_signup_emails(self):
    #     # If she successfully signs up for an account she will receive an **email** 
    #     # asking her to **confirm her email address** by clicking on a link or copying 
    #     # it into her web browser.

    #     # The **link will look like this**:
    #     # http://www.arewequits.com/users/confirm_email?user_id=xxxxxx&code=xxxxxx .

    #     # The email will tell her that **if she did not intend to sign up for an account 
    #     # then she can simply ignore the email**.

    #     # If she clicks on the link she will be **redirected** to [a success page]
    #     # where the webpage will **thank her** for confirming her email.

    #     # If she is not already logged in it will **suggest that she logs in**.

    #     # If she is already logged in it will **suggest that she visits the homepage**.

    #     self.fail(UNWRITTEN_COMPLAINT)
