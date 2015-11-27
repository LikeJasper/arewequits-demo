from behave import *
from django.core import mail

from constants import *
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait

@then('I will see the "{page}" page')
def impl(context, page):
    b = context.browser
    current_url = b.current_url.split('?',1)[0]
    suffix = URL_SUFFIXES[page]
    if context.feature.name == "Create group":
        suffix = suffix.replace('1', '4', 1)
    page_url = context.server_url + suffix

    identifier = IDENTIFIERS[page]
    page_source = b.page_source

    assert current_url == page_url, \
        '%r does not match target url %r' % (current_url, page_url)
    assert identifier in page_source, \
        '%r not found in page source %r' % (identifier, page_source)

@then('I will see the "{message}" message')
def impl(context, message):
    assert "Email address confirmed" in context.browser.page_source, \
        "Email confirmed not found in page source"

@then('I will see the "{element}"')
def impl(context, element):
    id_ = 'id="{}"'.format(ELEMENT_IDS[element])
    assert id_ in context.browser.page_source, \
        "%r not found in page source" % id_

@then('I will not see the "{element}"')
def impl(context, element):
    id_ = 'id="{}"'.format(ELEMENT_IDS[element])
    assert id_ not in context.browser.page_source, \
        "%r unexpectedly found in page source" % id_

@then('I will receive an email confirmation email')
def impl(context):
    emails = len(mail.outbox)
    assert emails == 1, \
        'Found %d emails, should be 1' % emails

    subject = mail.outbox[0].subject
    assert subject == '[AreWeQuits?] Confirm Email Address', \
        'Email subject %r is not [AreWeQuits?] Confirm Email Address' % subject

@then('I will see the signup form')
def impl(context):
    b = context.browser
    assert b.find_element_by_id('sign_up_form'), \
        'Signup form not found'

@then('I will see the login form')
def impl(context):
    b = context.browser
    assert b.find_element_by_id('login_form'), \
        'Login form not found'

@then('I will see an error message')
def impl(context):
    b = context.browser
    error_msg = "Give that email address another go"
    assert error_msg in b.page_source, \
        "%r not found in page source" % error_msg

@then('It will tell me to get started')
def impl(context):
    b = context.browser
    msg = "Get started by creating a group."
    assert msg in b.page_source, \
        "%r not found in page source" % msg

@then('It will list my group in the my groups table')
def impl(context):
    b = context.browser
    group_name = "Test group"
    assert group_name in b.page_source, \
        "%r not found in page source" % group_name

@then('I will see the "{datum}" I gave when I signed up')
def impl(context, datum):
    datum = PERSONAL_DATA[datum]
    assert datum in context.browser.page_source, \
        "%r not found in page source" % datum

@then('I will see the "{datum}" I gave when creating the group')
def impl(context, datum):
    if datum == "members":
        context.execute_steps('''
            Then I will see the "contact" I gave when creating the group
            Then I will see the "member email" I gave when creating the group
        ''')
        return
    datum = GROUP_DATA[datum]
    assert datum in context.browser.page_source, \
        "%r not found in page source" % datum

@then('I will see the "{datum}" I gave when editing the group')
def impl(context, datum):
    datum = EDITED_GROUP_DATA[datum]
    assert datum in context.browser.page_source, \
        "%r not found in page source" % datum

@then('I will not see the group I deleted')
def impl(context):
    assert "Test group" not in context.browser.page_source, \
        "Test group unexpectedly found in page source"

@then('I will not see the payment I deleted')
def impl(context):
    assert "BILL" not in context.browser.page_source, \
        "BILL unexpectedly found in page source"

@then('I will see the payment I restored')
def impl(context):
    assert "BILL" in context.browser.page_source, \
        "BILL not found in page source"

@then('I will see the "tos" modal')
def impl(context):
    try:
        context.browser.find_element_by_id('modal-tos')
    except NoSuchElementException:
        assert False

@then('my new account details will be displayed')
def impl(context):
    for value in [EDITED_PERSONAL_DATA['first name'], EDITED_PERSONAL_DATA['last name']]:
        assert value in context.browser.page_source, \
            "%r not found in page_source" % value

@then('I will see "no existing users" as options')
def impl(context):
    users = ['Amy Beech', 'Monica Geller', 'Ross Geller', 'Creepy Weirdo', 'Privacy Freak']
    for user in users:
        assert user not in context.browser.page_source, \
            "Unexpectedly found %r in page source" % user

@then('I will see "my contacts" as options')
def impl(context):
    contacts = ['Monica Geller', 'Ross Geller']
    for user in contacts:
        assert user in context.browser.page_source, \
            "%r not found in page source" % user

@then('I will see "no other users" as options')
def impl(context):
    not_contacts = ['Creepy Weirdo']
    if hasattr(context, 'added_member'):
        if context.added_member in not_contacts:
            not_contacts.remove(context.added_member)
    for user in not_contacts:
        assert user not in context.browser.page_source, \
            "Unexpectedly found %r in page source" % user

@then('I will see "the group members" as options')
def impl(context):
    members = ['Amy Beech', 'Monica Geller', 'Ross Geller']
    for user in members:
        assert user in context.browser.page_source, \
            "%r not found in page source" % user        

@then('I will not see any users who were not given when creating the group')
def impl(context):
    non_members = ['Ross Geller', 'Creepy Weirdo', 'Privacy Freak']
    for user in non_members:
        assert user not in context.browser.page_source, \
            "Unexpectedly found %r in page source" % user

@then('I will see the added member\'s "{detail}"')
def impl(context, detail):
    assert context.added_member in context.browser.page_source, \
        "Member %r not found in page source"

@then('I will see the member\'s balance is "{number}"')
def impl(context, number):
    b = context.browser
    tds = b.find_elements_by_tag_name('td')
    member_td = [i for i,td in enumerate(tds) if td.text == context.added_member][0]
    amount_td = tds[member_td+1]
    assert number in amount_td.text

@then('the added member will receive an email inviting them to sign up')
def impl(context):
    emails = len(mail.outbox)
    assert emails == 1, \
        'Found %d emails, should be 1' % emails

@then('I will see the original "group name"')
def impl(context):
    assert "Test group" in context.browser.page_source, \
        "Test group not found in page source"

@then('I will see the "{datum}" I gave when "{action}" the payment')
def impl(context, datum, action):
    if action == "creating":
        data = DATA_SETS["Create payment"]
    elif action == "editing":
        data = DATA_SETS["Edit payment"]
    if datum == 'receivers':
        for receiver in data[datum]:
            assert receiver in context.browser.page_source, \
                "%r not found in page source" % receiver
            return
    datum = data[datum]
    assert datum in context.browser.page_source, \
        "%r not found in page source" % datum

@then('I will see the details I gave when "{action}" the payment')
def impl(context, action):
    context.execute_steps('''
        Then I will see the "icon" I gave when "{0}" the payment
        Then I will see the "date" I gave when "{0}" the payment
        Then I will see the "amount" I gave when "{0}" the payment
        Then I will see the "description" I gave when "{0}" the payment
        Then I will see the "payer" I gave when "{0}" the payment
        Then I will see the "receivers" I gave when "{0}" the payment
    '''.format(action))

@then('I will see when "{event}"')
def impl(context, event):
    entry = LOG_ENTRIES[event]
    assert entry in context.browser.find_element_by_id('id_log_table').text, \
        "%r not found in log table" % entry

@then('I will see who "{action}"')
def impl(context, action):
    assert "Amy Beech" in context.browser.find_element_by_class_name('log-entry').text, \
        "Amy Beech not found in log table"

@then('I will not see the group summary table')
def impl(context):
    assert 'id="overview_table"' not in context.browser.page_source, \
        'id="overview_table" unexpectedly found in page source'

@then('the group summary table will show my group name "{name}"')
def impl(context, name):
    assert name in context.browser.find_element_by_id('overview_table').text, \
        "%r not found in group summary table" % name

@then('the group summary table will show my other groups')
def impl(context):
    groups = ["Test group", "Second group"]
    for group in groups:
        assert group in context.browser.find_element_by_id('overview_table').text, \
            "%r not found in group summary table" % group

@then('the group summary table will not show any other groups')
def impl(context):
    table = context.browser.find_element_by_id('overview_table')
    rows = len(table.find_elements_by_xpath('tbody/tr'))
    assert rows == 1, \
        '%d rows found, expected to find 1' % rows

@then('the group summary table will show an empty balance for my new group')
def impl(context):
    assert "0.00" in context.browser.find_element_by_id('overview_table').text, \
        "0.00 not found in group summary table"

@then('the group summary table will show an updated balance for my group')
def impl(context):
    assert "16.00" in context.browser.find_element_by_id('overview_table').text, \
        "16.00 not found in group summary table"

@then('the group summary table will show an unchanged balance for each other group')
def impl(context):
    unchanged = len(context.browser.find_elements_by_xpath('//td[contains(text(), "0.00")]'))
    assert unchanged == 1, \
        "Found %d instances of 0.00 in group summary table, expected 1" % unchanged

@then('I will see the get started card for "groups"')
def impl(context):
    assert 'id="id_group_help_card"' in context.browser.page_source, \
        'id="id_group_help_card" not found in page source'

@then('I will see the member balances have changed to incorporate the "{change}"')
def impl(context, change):
    b = context.browser
    if change == "new payment":
        amy_total = "16.00"
        other_totals = ["-8.00", "-8.00"]
    elif change == "additional payment":
        amy_total = "-2.67"
        other_totals = ["-129.67", "132.33"]
    elif change == "edited payment":
        amy_total = "53.33"
        other_totals = ["-49.67", "-3.67"]
    elif change == "deleted payment":
        amy_total = "61.33"
        other_totals = ["-41.67", "-19.67"]
    else:    
        assert False

    amy_row = b.find_element_by_xpath(
        '//table[@id="members_table"]//td[@class="member" and contains(text(), "Amy Beech")]/..'
    )
    other_rows = b.find_elements_by_xpath(
        '//table[@id="members_table"]//td[@class="member" and not(contains(text(), "Amy Beech"))]/..'
    )

    assert amy_total in amy_row.text
    for total in other_totals:
        assert any(total in row.text for row in other_rows)

@then('I will get a 404')
def impl(context):
    assert "Page not found" in context.browser.page_source, \
        "404 page not found"

@then('I should see the help message(s)')
def impl(context):
    assert context.browser.find_element_by_class_name('tooltipster-base'), \
        "tooltipster-base div not found"

@then('I should not see the help message(s)')
def impl(context):
    assert len(context.browser.find_elements_by_class_name('tooltipster-base')) == 0, \
        "tooltipster-base div unexpectedly found"

@then('fail')
def impl(context):
    assert false, "Scenario not yet complete"
