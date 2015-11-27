from unittest import TestCase
from django.test import TestCase as DjangoTestCase

from quits_users.forms import EditProfileForm, EMAIL_ADDRESS_ERROR
from quits_users.models import User, QuitsUser
from allauth.account.models import EmailAddress

INVALID_EMAILS = ['not_an_email', '@toosoon', 'incomplete@']

class EditProfileFormTest(TestCase):
    def setUp(self):
        email = 'user@email.com'
        self.user = User.objects.create_user(username=email, email=email)

    def tearDown(self):
        User.objects.all().delete()
        QuitsUser.objects.all().delete()

    def test_form_renders_first_name_input(self):
        form = EditProfileForm()
        self.assertIn('id="id_first_name"', form.as_p())

    def test_form_renders_last_name_input(self):
        form = EditProfileForm()
        self.assertIn('id="id_last_name"', form.as_p())

    def test_first_name_required(self):
        form = EditProfileForm(data={
            'first_name': '',
            'last_name': 'Beech',
        })
        self.assertFalse(form.is_valid())

    def test_last_name_required(self):
        form = EditProfileForm(data={
            'first_name': 'Amy',
            'last_name': '',
        })
        self.assertFalse(form.is_valid())
