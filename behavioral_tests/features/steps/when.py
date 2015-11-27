from behave import *
from django.core import mail
import re

from constants import *

@when('I visit the "{page}" page')
def impl(context, page):
    suffix = URL_SUFFIXES[page]
    context.browser.get(context.server_url + suffix)

@when('I go to "{location}"')
def impl(context, location):
    if location == "the add members page":
        context.execute_steps('''
            When I visit the "add members" page
        ''')
    elif location == "the add members tab of the edit group page":
        context.execute_steps('''
            When I visit the "edit group" page
            When I click on the "add members tab"
        ''')

@when('I visit the "{page}" page for a group I am not a member of')
def impl(context, page):
    suffix = URL_SUFFIXES[page]
    suffix = suffix.replace('1', '3')
    context.browser.get(context.server_url + suffix)    

@when('I click on the "{element}"')
def impl(context, element):
    if element == "first payment row":
        context.browser.find_element_by_class_name('collapsible-header').click()
    elif element == "edit payment icon":
        row = context.browser.find_element_by_class_name('collapsible-body')
        icon = row.find_element_by_tag_name('a').click()
    elif element == "payment link":
        context.browser.find_element_by_class_name('payment').click()
    elif element == "Test group link":
        context.browser.find_element_by_link_text('Test group').click()
    else:
        id_ = ELEMENT_IDS[element]
        context.browser.find_element_by_id(id_).click()

@when('I input an invalid email ("{email_address}")')
def impl(context, email_address):
    if email_address == "NONE":
        email_address = ""
    b = context.browser
    f = context.feature.name
    if f == "Signup":
        email_box = b.find_element_by_id('id_email')
    elif f == "Login":
        email_box = b.find_element_by_id('id_login')
    elif f == "Add members to group":
        email_box = b.find_element_by_id('input_emails_0')
    email_box.send_keys(email_address)

@when('I input an invalid password ("{password}")')
def impl(context, password):
    if password == "NONE":
        password = ""
    b = context.browser
    f = context.feature.name
    if f == "Signup":
        password_box = b.find_element_by_id('id_password1')
    elif f == "Login":
        password_box = b.find_element_by_id('id_password')
    password_box.send_keys(password)

@when('I input an invalid first name')
def impl(context):
    b = context.browser
    password_box = b.find_element_by_id('id_first_name')
    password_box.send_keys("")

@when('I input an invalid last name')
def impl(context):
    b = context.browser
    password_box = b.find_element_by_id('id_last_name')
    password_box.send_keys("")

@when('I input a valid "{entry}"')
def impl(context, entry):
    b = context.browser
    f = context.feature.name
    s = context.scenario.name

    if f == "Activity log" and s == "Add a payment":
        data = DATA_SETS["Create payment"]
    elif f == "Activity log" and s == "Edit a payment":
        data = DATA_SETS["Edit payment"]
    elif f == "My groups" and s == "Payments added to groups":
        data = DATA_SETS["Create payment"]
    else:
        data = DATA_SETS[f]

    if f == "Signup" and entry == "password":
        entry = "password1"
    elif f == "Login" and entry == "email":
        entry = "login"

    id_ = INPUT_IDS[entry]
    input_box = b.find_element_by_id(id_)
    input_box.clear()
    input_box.send_keys(data[entry])

@when('I check the terms of service box')
def impl(context):
    b = context.browser
    box = b.find_element_by_xpath('//label[@for="id_terms_agree"]').click()

@when('I select an existing user from another group')
def impl(context):
    b = context.browser
    b.find_element_by_xpath("//label[@for='input_contacts_0']").click()
    context.added_member = "Monica Geller"

@when('I enter the email address of "{person}"')
def impl(context, person):
    if person == "an existing user":
        email = "creepy@weirdo.com"
        context.added_member = "Creepy Weirdo"
    elif person == "a non-user":
        email = "non@user.com"
        context.added_member = "non@user.com"

    b = context.browser
    email_box = b.find_element_by_id('input_emails_0')
    email_box.clear()
    email_box.send_keys(email)

@when('I select an "icon"')
def impl(context):
    b = context.browser
    f = context.feature.name
    s = context.scenario.name

    icon_box = b.find_element_by_class_name('select-dropdown')
    icon_box.click()
    if f == "Create payment" or (f == "Activity log" and s == "Add a payment"):
        icon_box.find_element_by_xpath('//span[text()="shopping_cart SHOPPING"]').click()
    elif f == "Edit payment" or (f == "Activity log" and s == "Edit a payment"):
        icon_box.find_element_by_xpath('//span[text()="cake PARTIES"]').click()

@when('I input a valid date')
def impl(context):
    f = context.feature.name
    s = context.scenario.name

    if f == "Edit payment" or (f == "Activity log" and s == "Edit a payment"):
        b = context.browser
        date = DATA_SETS["Edit payment"]['date']
        day = date.partition(' ')[0]

        date_box = b.find_element_by_id('input_date')
        date_box.click()
        b.find_element_by_xpath(
            '//table[@id="input_date_table"]//td/div[text()="{}"]'.format(day)
        ).click()
        b.find_element_by_class_name("picker__close").click()

@when('I press submit')
def impl(context):
    b = context.browser
    f = context.feature.name
    if f == "Signup":
        btn_id = 'signup_submit'
    elif f == "Login":
        btn_id = 'login_submit'
    elif f == "Edit group":
        btn_id = 'input_edit_group_submit'
    else:
        btn_id = 'input_submit'
    b.find_element_by_id(btn_id).click()

@when('I input valid signup details')
def impl(context):
    context.execute_steps('''
        When I input a valid "email"
        When I input a valid "password"
        When I input a valid "first name"
        When I input a valid "last name"
        When I check the terms of service box
        When I press submit
    ''')

@when('I input valid login details')
def impl(context):
    context.execute_steps('''
        When I input a valid "email"
        When I input a valid "password"
        When I press submit
    ''')

@when('I input valid edit account details')
def impl(context):
    context.execute_steps('''
        When I input a valid "first name"
        When I input a valid "last name"
        When I press submit
    ''')

@when('I input valid group details')
def impl(context):
    context.execute_steps('''
        When I input a valid "group name"
        When I input a valid "member email"
    ''')
    if context.feature.name != "My groups":
        context.execute_steps('''
            When I select an existing user from another group
        ''')
    context.execute_steps('''
        When I press submit
    ''')

@when('I input valid payment details')
def impl(context):
    context.execute_steps('''
        When I select an "icon"
        When I input a valid date
        When I input a valid "amount"
        When I input a valid "description"
        When I press submit
    ''')

@when('I put "{entry}" in "{input_box}"')
def impl(context, entry, input_box):
    if input_box == "all member inputs":
        return
    if entry == "NONE":
        entry = ""
    b = context.browser

    if input_box == "who_for" and entry == "":
        b.find_element_by_link_text("Uncheck all").click()
        return

    box = b.find_element_by_id(INPUT_IDS[input_box])
    box.clear()
    box.send_keys(entry)

@when('I clear the "{input_box}"')
def impl(context, input_box):
    b = context.browser
    box = b.find_element_by_id(INPUT_IDS[input_box])
    box.clear()

@when('I select a new currency')
def impl(context):
    b = context.browser
    currency_box = b.find_element_by_class_name('select-dropdown')
    currency_box.click()
    currency_box.find_element_by_xpath('//span[text()="$"]').click()

@when('I click on the verification link in the email confirm email')
def impl(context):
    email = mail.outbox[0]
    pattern = 'http://localhost:8081/users/confirm-email/[a-z0-9]+/'

    specific_link = re.findall(pattern, email.body)[0]
    context.browser.get(specific_link)
