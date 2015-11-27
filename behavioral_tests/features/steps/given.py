from behave import *
from django.core.management import call_command
from django.test import Client

from constants import *
from django.contrib.auth.models import User

def load_fixtures(fixtures):
    fixtures = [FIXTURES_PATH + fixture for fixture in fixtures]
    call_command('loaddata', *fixtures, verbosity=0)

@given('I have not already signed up')
def impl(context):
    pass

@given('I have already signed up')
def impl(context):
    fixtures = ['signed_up_user_fixture']
    load_fixtures(fixtures)

@given('someone else has already signed up')
def impl(context):
    fixtures = ['signed_up_other_fixture']
    load_fixtures(fixtures)    

@given('there are a number of signed up users in or out of various groups')
def impl(context):
    fixtures = ['users_groups_fixture']
    load_fixtures(fixtures)

@given('a number of payments have been created')
def impl(context):
    fixtures = ['payments_fixture']
    load_fixtures(fixtures)

@given('there are a number of signed up users')
def impl(context):
    fixtures = ['several_signed_up_users_fixture']
    load_fixtures(fixtures)

@given('some but not all users are in a group')
def impl(context):
    fixtures = ['main_group_fixture']
    load_fixtures(fixtures)

@given('I am in a group with someone else')
def impl(context):
    fixtures = ['member_group_fixture']
    load_fixtures(fixtures)

@given('another member is in a group with someone else')
def impl(context):
    fixtures = ['nonmember_group_fixture']
    load_fixtures(fixtures)

@given('some but not all users are already contacts')
def impl(context):
    fixtures = ['contact_connections_fixture']
    load_fixtures(fixtures)

@given('I am not logged in')
def impl(context):
    pass

@given('I am logged in')
def impl(context):
    client = Client()
    client.login(email='amy@beech.com', password='password123')

    cookie = client.cookies['sessionid']

    b = context.browser
    b.get(context.server_url + '/404-loads-fastest/') # selenium will set cookie domain based on current page domain
    b.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})

@given('I am a logged-in user with no existing contacts')
def impl(context):
    client = Client()
    client.login(email='creepy@weirdo.com', password='password123')

    cookie = client.cookies['sessionid']

    b = context.browser
    b.get(context.server_url + '/404-loads-fastest/') # selenium will set cookie domain based on current page domain
    b.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})

@given('I have been added to a group')
def impl(context):
    fixtures = ['group_fixture', 'nonmember_added_to_group_fixture']
    load_fixtures(fixtures)

@given('I am a member of "{number}" group(s)')
def impl(context, number):
    if number == "1":
        fixtures = ['group_fixture']
        load_fixtures(fixtures)
        user = User.objects.get(email='amy@beech.com')
        user.groups.add(1)
    elif number == "2":
        fixtures = ['group_fixture', 'second_group_fixture']
        load_fixtures(fixtures)
        user = User.objects.get(email='amy@beech.com')
        user.groups.add(*[1,2])

@given('I am a robot')
def impl(context):
    pass

@given('I am interested in the humans')
def impl(context):
    pass
