from django.test import TestCase
from django.utils.html import escape
from django.contrib.auth import SESSION_KEY

from allauth.account.forms import SignupForm, AddEmailForm
from quits_users.forms import EditProfileForm
from allauth.account.models import EmailAddress
from quits_users.models import User, QuitsUser

UNWRITTEN_COMPLAINT = 'write me!'
INVALID_EMAILS = ['', 'not_an_email', '@toosoon', 'incomplete@']
INVALID_PASSWORDS = ['', 'pass123']

EMAIL_ADDRESS_ERROR = "Give that email address another go."
PASSWORD_INCOMPLETE_ERROR = "Give those passwords another go."
PASSWORD_MISMATCH_ERROR = "Give those passwords another go."
PASSWORD_TOO_SHORT_ERROR = "Give those passwords another go."

class QuitsUsersTestCase(TestCase):
    pass

class NewUserPageTest(QuitsUsersTestCase):

    def send_post_data(self,
        email='billy@bob.co.uk', password='lovely69',
        first_name='Billy', last_name='Bob'):
        return self.client.post('/users/new/', data={
            'email': email,
            'password1': password,
            'first_name': first_name,
            'last_name': last_name,
            'terms_agree': "checked",
        })

    def create_inactive_user(self,
            username='billy@bob.co.uk', email='billy@bob.co.uk'):
        inactive_user = User.objects.create(
            username=username, email=email)
        inactive_user.is_active = False
        inactive_user.save(update_fields=['is_active'])
        return inactive_user

    def test_logged_in_user_redirects_to_home_page(self):
        user = User.objects.create_user(
            username='test@email.com',email='test@email.com',password='password')
        self.client.login(email='test@email.com',password='password')

        response = self.client.get('/users/new/')
        self.assertRedirects(response, '/')

    def test_new_user_page_renders_new_user_template(self):
        response = self.client.get('/users/new/')
        self.assertTemplateUsed(response, 'account/signup.html')

    def test_new_user_page_uses_new_user_form(self):
        response = self.client.get('/users/new/')
        self.assertIsInstance(response.context['form'], SignupForm)

    def test_post_request_redirects_to_confirm_email_page(self):
        response = self.send_post_data()
        self.assertRedirects(response, '/users/confirm-email/')

    def test_post_saves_new_user(self):
        self.send_post_data()
        new_user = User.objects.first()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(new_user.email, 'billy@bob.co.uk')
        self.assertEqual(new_user.first_name, 'Billy')
        self.assertEqual(new_user.last_name, 'Bob')

    def test_user_string_before_email_verification(self):
        self.send_post_data()
        self.assertEqual(str(User.objects.last()), 'billy@bob.co.uk')

    def test_new_user_not_logged_in(self):
        self.send_post_data()
        self.assertFalse(SESSION_KEY in self.client.session)

    def test_signup_activates_inactive_user(self):
        self.create_inactive_user()

        self.send_post_data()

        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.email, 'billy@bob.co.uk')
        self.assertEqual(user.first_name, 'Billy')
        self.assertEqual(user.last_name, 'Bob')
        self.assertTrue(user.is_active)

    def test_signup_redirects_inactive_user_to_confirm_email_page(self):
        self.create_inactive_user()
        response = self.send_post_data()
        self.assertRedirects(response, '/users/confirm-email/')

    def test_inactive_user_not_logged_in(self):
        user = self.create_inactive_user()
        response = self.send_post_data()
        self.assertFalse(SESSION_KEY in self.client.session)

    def test_invalid_email_nothing_saved_to_db(self):
        for email in INVALID_EMAILS:
            self.send_post_data(email=email)
        self.assertEqual(User.objects.count(), 0)

    def test_invalid_passwords_nothing_saved_to_db(self):
        i = 1
        for password in INVALID_PASSWORDS:
            self.send_post_data(password=password)
            i += 1

        self.assertEqual(User.objects.count(), 0)

    def test_invalid_email_renders_new_user_template(self):
        for email in INVALID_EMAILS:
            response = self.send_post_data(email=email)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed('account/signup.html')

    def test_invalid_passwords_render_new_user_template(self):
        i = 1
        for password in INVALID_PASSWORDS:
            response = self.send_post_data(password=password)
            i += 1
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed('account/signup.html')

    def test_invalid_email_passes_form_to_template(self):
        for email in INVALID_EMAILS:
            response = self.send_post_data(email=email)
            self.assertIsInstance(response.context['form'], SignupForm)

    def test_invalid_passwords_pass_form_to_template(self):
        i = 1
        for password in INVALID_PASSWORDS:
            response = self.send_post_data(password=password)
            i += 1
            self.assertIsInstance(response.context['form'], SignupForm)

class LogoutTest(QuitsUsersTestCase):

    def test_logout_redirects_to_home_page(self):
        response = self.client.get('/users/logout')
        self.assertRedirects(response, '/')

class ViewProfileTest(QuitsUsersTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test@email.com', password='password')
        QuitsUser.objects.create(user=self.user)

    def login_user(self):
        login_successful = self.client.login(username='test@email.com', password='password')
        self.assertTrue(login_successful)

    def test_login_required(self):
        response = self.client.get('/users/profile/')
        self.assertRedirects(response,
            '/?next=/users/profile/'
        )

    def test_view_profile_page_renders_profile_template(self):
        self.login_user()
        response = self.client.get('/users/profile/')
        self.assertTemplateUsed(response, 'quits_users/profile.html')

class EditProfileTest(QuitsUsersTestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test@email.com', email='test@email.com', password='password')
        QuitsUser.objects.create(user=self.user)

    def login_user(self):
        login_successful = self.client.login(email='test@email.com', password='password')
        self.assertTrue(login_successful)

    def send_post_data(self, first_name='Amy', last_name='Beech', email='amy@beech.com'):
        return self.client.post('/users/profile/edit/', data={
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
        })

    def test_login_required(self):
        response = self.client.get('/users/profile/edit/')
        self.assertRedirects(response,
            '/?next=/users/profile/edit/'
        )

    def test_edit_profile_page_renders_profile_template(self):
        self.login_user()
        response = self.client.get('/users/profile/edit/')
        self.assertTemplateUsed(response, 'quits_users/edit_profile.html')

    def test_edit_profile_page_uses_edit_profile_form(self):
        self.login_user()
        response = self.client.get('/users/profile/edit/')
        self.assertIsInstance(response.context['edit_profile_form'], EditProfileForm)

    def test_edit_profile_page_uses_add_email_form(self):
        self.login_user()
        response = self.client.get('/users/profile/edit/')
        self.assertIsInstance(response.context['add_email_form'], AddEmailForm)

    def test_edit_profile_page_edit_profile_form_instance_is_user(self):
        self.login_user()
        response = self.client.get('/users/profile/edit/')
        self.assertEqual(response.context['edit_profile_form'].instance, self.user)

    def test_edit_profile_page_add_email_form_instance_is_user(self):
        self.login_user()
        response = self.client.get('/users/profile/edit/')
        self.assertEqual(response.context['add_email_form'].user, self.user)

    def test_invalid_post_empty_first_name_returns_edit_profile_page(self):
        self.login_user()
        response = self.send_post_data(first_name='')
        self.assertTemplateUsed(response, 'quits_users/edit_profile.html')

    def test_invalid_post_empty_email_returns_edit_profile_page(self):
        self.login_user()
        response = self.send_post_data(email='')
        self.assertTemplateUsed(response, 'quits_users/edit_profile.html')

    def test_invalid_post_invalid_email_returns_edit_profile_page(self):
        self.login_user()
        response = self.send_post_data(email='notanemail')
        self.assertTemplateUsed(response, 'quits_users/edit_profile.html')

    def test_valid_post_same_email_redirects_to_view_profile_page(self):
        self.login_user()
        response = self.send_post_data(email='test@email.com')
        self.assertRedirects(response, '/users/profile/')

    def test_valid_post_new_email_redirects_to_verification_sent_page(self):
        self.login_user()
        response = self.send_post_data()
        self.assertRedirects(response, '/users/confirm-email/')

    def test_valid_post_saves_name_changes_to_db(self):
        self.login_user()
        self.send_post_data()
        user = User.objects.first()
        self.assertEqual(user.first_name, 'Amy')
        self.assertEqual(user.last_name, 'Beech')

    def test_valid_post_saves_new_email_address(self):
        pre_user = self.login_user()
        pre_emails = EmailAddress.objects.filter(user=pre_user)
        self.send_post_data()
        
        user = User.objects.first()
        emails = EmailAddress.objects.filter(user=user)
        self.assertEqual(len(emails), len(pre_emails) + 1)

    def test_valid_post_does_not_set_new_email_address_as_primary(self):
        self.login_user()
        self.send_post_data()
        user = User.objects.first()
        self.assertEqual(user.email, 'test@email.com')
