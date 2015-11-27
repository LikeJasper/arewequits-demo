from selenium import webdriver
from django.core.management import call_command
from django.core import mail

FIXTURES_PATH = 'arewequits/fixtures/'

def load_fixtures(fixtures):
    fixtures = [FIXTURES_PATH + fixture for fixture in fixtures]
    call_command('loaddata', *fixtures)

def before_all(context):
    context.browser = webdriver.Firefox()
    context.browser.implicitly_wait(2)
    context.browser.maximize_window()
    context.server_url = 'http://localhost:8081'
    fixtures = ['allauth_fixture']
    load_fixtures(fixtures)

# def before_feature(context, feature):
#     fixtures = []
#     load_fixtures(fixtures)

# def before_scenario(context, scenario):
#     fixtures = []
#     load_fixtures(fixtures)

def after_scenario(context, scenario):
    context.browser.delete_all_cookies()
    call_command('flush', interactive=False, verbosity=0)
    mail.outbox = []

def after_all(context):
    context.browser.quit()
