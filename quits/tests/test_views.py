from django.test import TestCase
from django.http import HttpRequest, Http404
from decimal import Decimal
from datetime import date, datetime

from quits.views import new_group, delete_payment, delete_group
from quits.models import Group, QuitsGroup, Payment, Edit
from quits_users.models import User, QuitsUser
from quits.forms import (NewPaymentForm, DeletePaymentForm, GroupForm, QuitsGroupForm, 
    AddMembersForm, EditGroupForm, EditQuitsGroupForm)
from allauth.account.forms import SignupForm, LoginForm

UNWRITTEN_COMPLAINT = 'write me!'

def create_members(number=3):
    users =  [
        User.objects.create_user(
        username='member{}@email.com'.format(str(i)),
        email='member{}@email.com'.format(str(i)),
        ) for i in range(number)
    ]
    return users

def create_and_login_user(self, email='user@email.com'):
    user = User.objects.create_user(
        username=email, email=email, password='password12345'
    )
    login_successful = self.client.login(
        username=email, password='password12345'
    )
    self.assertTrue(login_successful)
    return user

def create_new_group(owner=None, members=None, name='Cool group', currency='£'):
    if not owner:
        owner = User.objects.create_user(
            username='owner@email.com', email='owner@email.com', password='testing123')
    group = Group.objects.create(
        name=name,
    )
    if not members:
        members = create_members()
    group.user_set.add(owner)
    group.user_set.add(*members)
    group.save()
    quits_group = QuitsGroup.objects.create(
        owner=owner,
        group=group,
        currency=currency,
    )
    return group

class QuitsTestCase(TestCase):
    pass

class HomePageTest(QuitsTestCase):

    def test_home_page_renders_base_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'quits/home.html')

    def test_home_page_shows_no_account_information_if_not_logged_in(self):
        response = self.client.get('/')
        self.assertNotIn('Log out', response)

    def test_home_page_passes_signup_form_if_not_logged_in(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['signup_form'], SignupForm)

    def test_home_page_passes_login_form_if_not_logged_in(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['login_form'], LoginForm)

    def test_home_page_redirects_if_only_one_group(self):
        test_group = create_new_group()
        self.client.login(email='owner@email.com', password='testing123')
        response = self.client.get('/?source=login')
        self.assertRedirects(response, '/groups/' + str(test_group.id) + '/view_group/')

    def test_home_page_does_not_redirect_if_no_groups(self):
        create_and_login_user(self)
        response = self.client.get('/?source=login')
        self.assertEqual(response.status_code, 200)

    def test_home_page_does_not_redirect_if_more_than_one_group(self):
        test_group = create_new_group()
        owner = User.objects.get(email='owner@email.com')
        member = User.objects.get(email='member0@email.com')
        second_group = create_new_group(owner=owner, members=[member], name='Second group')
        self.client.login(email='owner@email.com', password='testing123')
        response = self.client.get('/?source=login')
        self.assertEqual(response.status_code, 200)

    def test_home_page_passes_only_member_groups_to_template(self):
        test_group = create_new_group()
        create_and_login_user(self)
        response = self.client.get('/')
        self.assertNotIn(test_group, response.context['user'].groups.all())

    def test_home_page_does_not_pass_inactive_groups_to_template(self):
        user = create_and_login_user(self)
        members = create_members()
        active_group = create_new_group(owner=user, members=members)
        inactive_group = create_new_group(owner=user, members=members)
        qg = inactive_group.quitsgroup
        qg.is_active = False
        qg.save(update_fields=['is_active'])

        response = self.client.get('/')
        self.assertEqual(len(response.context['group_balances']), 1)

    def test_home_page_passes_group_balance_list_to_template(self):
        test_group = create_new_group()
        self.client.login(username='owner@email.com', password='testing123')
        response = self.client.get('/')
        self.assertEqual(
            response.context['group_balances'][0],
            (test_group, Decimal(0), '£')
        )

    def test_group_balance_list_has_correct_balances(self):
        test_group_1 = create_new_group()
        owner = User.objects.get(email='owner@email.com')
        member = User.objects.get(email='member0@email.com')
        test_group_2 = create_new_group(
            owner=owner, members=[member],
            name="Second cool group")
        payment = Payment.objects.create(
            group=test_group_1, amount=10.00,
            date='2015-07-13', who_paid=owner,
        )
        payment.who_for.add(member)

        self.client.login(email='owner@email.com', password='testing123')
        response = self.client.get('/')
        group_balances = [(test_group_1, Decimal('10.00'), '£'), (test_group_2, Decimal('0.00'), '£')]
        self.assertEqual(response.context['group_balances'], group_balances)

class AboutPageTest(QuitsTestCase):
    
    def test_about_page_renders_about_template(self):
        response = self.client.get('/about/')
        self.assertTemplateUsed(response, 'quits/about.html')

class NewGroupPageTest(QuitsTestCase):

    def create_member_ids(self, number=3):
        members = create_members(number)
        return [member.id for member in members]

    def test_new_group_page_redirects_for_unauthenticated_users(self):
        response = self.client.get('/groups/new/')
        self.assertRedirects(response, '/?next=/groups/new/')

    def test_new_group_page_renders_new_group_template(self):
        create_and_login_user(self)
        response = self.client.get('/groups/new/')
        self.assertTemplateUsed(response, 'quits/new_group.html')

    def test_new_group_page_uses_group_form(self):
        create_and_login_user(self)
        response = self.client.get('/groups/new/')
        self.assertIsInstance(response.context['group_form'], GroupForm)

    def test_new_group_page_uses_quits_group_form(self):
        create_and_login_user(self)
        response = self.client.get('/groups/new/')
        self.assertIsInstance(response.context['quits_group_form'], QuitsGroupForm)

    def test_new_group_page_only_displays_user_contacts(self):
        user = create_and_login_user(self)
        contacts = create_members()
        other_group = Group.objects.create(name="Other group")
        other_group.user_set.add(user)
        other_group.user_set.add(*contacts)
        not_contact = User.objects.create_user(username="not@contact.com", email="not@contact.com")

        response = self.client.get('/groups/new/')
        for contact in contacts:
            self.assertContains(response, contact.email)
        self.assertNotContains(response, not_contact.email)

    def test_valid_post_request_redirects_to_group_page(self):
        contacts = create_members()
        owner = create_and_login_user(self)
        other_group = Group.objects.create(name="Other group")
        other_group.user_set.add(owner)
        other_group.user_set.add(*contacts)

        response = self.client.post('/groups/new/', data={
            'name': 'New group',
            'currency': '£',
            'contacts': [contact.id for contact in contacts],
            })
        self.assertRedirects(response, '/groups/2/view_group/')

    def test_post_adds_new_group_to_group_list(self):
        User.objects.create_user(
            username='not_the_owner@email.com', password='testing123')
        user = create_and_login_user(self)
        contacts = create_members()
        other_group = Group.objects.create(name="Other group")
        other_group.user_set.add(user)
        other_group.user_set.add(*contacts)

        redirect = self.client.post('/groups/new/', data={
            'name': 'New group',
            'currency': '£',
            'contacts': [contact.id for contact in contacts],
            })
        response = self.client.get(redirect.url)
        group = response.context['user'].groups.get(name="New group")
        self.assertEqual(group.name, 'New group')
        self.assertEqual(group.quitsgroup.currency, '£')
        group_members = group.user_set.all()
        group_ids = [member.id for member in group_members]
        self.assertListEqual(group_ids, [member.id for member in [user] + contacts])

    def test_groups_with_same_name_can_be_created(self):
        user = create_and_login_user(self)
        members = create_members()
        other_group = Group.objects.create(name="Other group")
        other_group.user_set.add(user)
        other_group.user_set.add(*members)

        self.client.post('/groups/new/', data={
            'name': 'Group name',
            'currency': '£',
            'contacts': [member.id for member in members],
            })
        response = self.client.post('/groups/new/', data={
            'name': 'Group name',
            'currency': '£',
            'contacts': [member.id for member in members],
            })
        self.assertEqual(user.groups.count(), 3)
        group_id = user.groups.last().id
        self.assertRedirects(response, '/groups/' + str(group_id) + '/view_group/')

    def test_post_adds_current_user_as_owner(self):
        User.objects.create_user(
            username='not_the_owner@email.com', password='testing123')
        user = create_and_login_user(self)
        contacts = create_members()
        other_group = Group.objects.create(name="Other group")
        other_group.user_set.add(user)
        other_group.user_set.add(*contacts)

        redirect = self.client.post('/groups/new/', data={
            'name': 'New group',
            'currency': '£',
            'contacts': [contact.id for contact in contacts],            
        })
        response = self.client.get(redirect.url)
        group = response.context['user'].groups.get(name="New group")
        self.assertEqual(group.quitsgroup.owner.username, 'user@email.com')

    def test_post_adds_current_user_as_member(self):
        User.objects.create_user(
            username='not_the_owner@email.com', password='testing123')
        user = create_and_login_user(self)
        contacts = create_members()
        other_group = Group.objects.create(name="Other group")
        other_group.user_set.add(user)
        other_group.user_set.add(*contacts)

        redirect = self.client.post('/groups/new/', data={
            'name': 'New group',
            'currency': '£',
            'contacts': [contact.id for contact in contacts],            
        })
        response = self.client.get(redirect.url)
        group = response.context['user'].groups.first()
        self.assertIn(user, group.user_set.all())

    def test_post_adds_email_users_as_members(self):
        user = create_and_login_user(self)
        emails = ['test_{}@email.com'.format(str(i)) for i in range(5)]
        data = {'name': 'Email members', 'currency': '£'}
        for i in range(len(emails)):
            data['emails_{}'.format(str(i))] = emails[i]
        redirect = self.client.post('/groups/new/', data=data)
        response = self.client.get(redirect.url)
        group = response.context['user'].groups.first()
        member_emails = [user.email for user in group.user_set.all()]
        for email in emails:
            self.assertIn(email, member_emails)

class ViewGroupPageTest(QuitsTestCase):

    def test_view_group_page_redirects_for_unauthenticated_users(self):
        id_ = create_new_group().id
        url = '/groups/' + str(id_) + '/view_group/'
        response = self.client.get(url)
        self.assertRedirects(response, '/?next=' + url)

    def test_view_group_page_404s_for_non_members(self):
        id_ = create_new_group().id
        url = '/groups/' + str(id_) + '/view_group/'
        create_and_login_user(self)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_view_group_page_renders_view_group_template(self):
        id_ = create_new_group().id
        self.client.login(username='owner@email.com', password='testing123')
        response = self.client.get('/groups/' + str(id_) + '/view_group/')
        self.assertTemplateUsed(response, 'quits/view_group.html')

    def test_view_group_page_passes_group_to_template(self):
        id_ = create_new_group().id
        self.client.login(username='owner@email.com', password='testing123')
        response = self.client.get('/groups/' + str(id_) + '/view_group/')
        self.assertIsInstance(response.context['group'], Group)

    def test_view_group_page_passes_active_payments_to_template(self):
        group = create_new_group()
        payment = Payment.objects.create(
            group=group,
            date='2015-05-05',
            amount='20.00',
            description='blah',
            who_paid=User.objects.get(id=1),
        )
        payment.who_for.add(
            *[User.objects.get(id=i) for i in [1,2]]
        )
        payment.save()

        self.client.login(username='owner@email.com', password='testing123')
        response = self.client.get('/groups/' + str(group.id) + '/view_group/')

        self.assertIn(Payment.objects.get(id=payment.id), response.context['payments'])

    def test_view_group_page_does_not_pass_inactive_payments_to_template(self):
        group = create_new_group()
        payment = Payment.objects.create(
            group=group,
            date='2015-05-05',
            amount='20.00',
            description='blah',
            who_paid=User.objects.get(id=1),
        )
        payment.who_for.add(
            *[User.objects.get(id=i) for i in [1,2]]
        )
        payment.is_active = False
        payment.save()

        self.client.login(username='owner@email.com', password='testing123')
        response = self.client.get('/groups/' + str(group.id) + '/view_group/')

        self.assertNotIn(Payment.objects.get(id=payment.id), response.context['payments'])

    def test_view_group_gets_default_group_totals(self):
        id_ = create_new_group().id
        self.client.login(username='owner@email.com', password='testing123')
        response = self.client.get('/groups/' + str(id_) + '/view_group/')
        self.assertContains(response, '£0.00')

    def test_view_group_gets_group_total_for_each_member(self):
        group = create_new_group()
        member_set = group.user_set.all()

        payment_data_sets = [
            {
                # Somebody else paid -> -10.00
                'group': group,
                'date': '2015-05-05',
                'amount': '20.00',
                'description': 'blah',
                'who_paid': 2,
                'who_for': [1, 2],
            },
            {
                # Paid but did not benefit (1 did) -> +11.11
                'group': group,
                'date': '2015-05-05',
                'amount': '11.11',
                'description': 'blah',
                'who_paid': 1,
                'who_for': [2],
            },
            {
                # Paid but did not benefit (2 did) -> +24.50
                'group': group,
                'date': '2015-05-05',
                'amount': '24.50',
                'description': 'blah',
                'who_paid': 1,
                'who_for': [2, 3],
            },
            {
                # Paid and benefited (1 other did) -> +6.00
                'group': group,
                'date': '2015-05-05',
                'amount': '12.00',
                'description': 'blah',
                'who_paid': 1,
                'who_for': [1, 2],
            },
            {
                # Paid and benefited (2 others did) -> +22.44
                'group': group,
                'date': '2015-05-05',
                'amount': '33.66',
                'description': 'blah',
                'who_paid': 1,
                'who_for': [1, 2, 3],
            },
        ]

        for data_set in payment_data_sets:
            payment = Payment.objects.create(
                group=data_set['group'],
                date=data_set['date'],
                amount=data_set['amount'],
                description=data_set['description'],
                who_paid=User.objects.get(id=data_set['who_paid']),
            )
            payment.who_for.add(
                *[User.objects.get(id=i) for i in data_set['who_for']]
            )
            payment.save()

        totals = [54.05, -30.58, -23.47, 0]

        self.client.login(email='owner@email.com', password='testing123')
        response = self.client.get('/groups/' + str(group.id) + '/view_group/')
        entries = response.context['member_balances']
        for i in range(len(totals)):
            self.assertEqual(
                entries[i]['group_total'], 
                Decimal(totals[i]).quantize(Decimal('0.01'))
            )

class EditGroupPageTest(QuitsTestCase):

    def create_group_url_stub(self):
        id_ = create_new_group(currency='€').id
        self.client.login(username='owner@email.com', password='testing123')
        return '/groups/' + str(id_)

    def get_post_response(self, name='New name', currency=None, url=None):
        if not url:
            url_stub = self.create_group_url_stub()
            url = url_stub + '/edit_group/'
        data = {'name': name}
        if currency:
            data['currency'] = currency
        return self.client.post(url, data=data)

    def test_edit_group_page_redirects_for_unauthenticated_users(self):
        id_ = create_new_group().id
        url = '/groups/' + str(id_) + '/edit_group/'
        response = self.client.get(url)
        self.assertRedirects(response, '/?next=' + url)

    def test_new_payment_page_404s_for_non_members(self):
        url = self.create_group_url_stub() + '/edit_group/'
        create_and_login_user(self)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_edit_group_page_renders_edit_group_template(self):
        url = self.create_group_url_stub() + '/edit_group/'
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'quits/edit_group.html')

    def test_edit_group_page_passes_group_id_to_template(self):
        id_ = create_new_group().id
        url = '/groups/' + str(id_) + '/edit_group/'
        self.client.login(username='owner@email.com', password='testing123')
        response = self.client.get(url)
        self.assertEqual(response.context['group_id'], str(id_))

    def test_edit_group_page_uses_edit_group_form(self):
        url = self.create_group_url_stub() + '/edit_group/'
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        response = self.client.get(url)
        self.assertIsInstance(response.context['group_form'], EditGroupForm)

    def test_edit_group_page_uses_edit_quits_group_form(self):
        url = self.create_group_url_stub() + '/edit_group/'
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        response = self.client.get(url)
        self.assertIsInstance(response.context['quits_group_form'], EditQuitsGroupForm)

    def test_edit_group_page_uses_add_members_form(self):
        url = self.create_group_url_stub() + '/edit_group/'
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        response = self.client.get(url)
        self.assertIsInstance(response.context['add_members_form'], AddMembersForm)        

    def test_edit_group_page_sets_default_group_name(self):
        url = self.create_group_url_stub() + '/edit_group/'
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        response = self.client.get(url)
        self.assertContains(response, 'Cool group')

    def test_edit_group_page_sets_default_group_currency(self):
        url = self.create_group_url_stub() + '/edit_group/'
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        response = self.client.get(url)
        self.assertContains(
            response, 'value="€" selected="selected"'
        )

    def test_post_redirects_to_group_page(self):
        id_ = create_new_group().id
        self.assertTrue(self.client.login(
            username='owner@email.com', password='testing123'
        ))
        url = '/groups/' + str(id_)
        response = self.get_post_response(url=url + '/edit_group/')
        self.assertRedirects(response, url + '/view_group/')

    def test_post_does_not_add_new_group_to_db(self):
        precount = Group.objects.count()
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        response = self.get_post_response()
        self.assertEqual(Payment.objects.count(), precount)

    def test_post_changes_group_name(self):
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        response = self.get_post_response()
        group = Group.objects.last()

        self.assertEqual(group.name, 'New name')

    def test_post_changes_group_currency(self):
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        response = self.get_post_response(currency='$')
        group = Group.objects.last()

        self.assertEqual(group.quitsgroup.currency, '$')

    def test_valid_post_adds_edit_for_group_name_change(self):
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        precount = Edit.objects.count()
        response = self.get_post_response()
        self.assertEqual(Edit.objects.count(), precount + 1)

    def test_valid_post_adds_edit_for_group_currency_change(self):
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        precount = Edit.objects.count()
        response = self.get_post_response(name="", currency='$')
        self.assertEqual(Edit.objects.count(), precount + 1)

    def test_invalid_post_does_not_add_edit_for_group(self):
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        precount = Edit.objects.count()
        response = self.get_post_response(name='')
        self.assertEqual(Edit.objects.count(), precount)

class DeleteGroupPageTest(QuitsTestCase):

    def get_url(self, group):
        return '/groups/' + str(group.id) + '/delete'

    def test_get_404s(self):
        user = create_and_login_user(self)
        group = create_new_group(owner=user)
        url = self.get_url(group)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_delete_group_page_redirects_for_unauthenticated_users(self):
        group = create_new_group()
        url = self.get_url(group)
        response = self.client.post(url)
        self.assertRedirects(response, '/?next=' + url)

    def test_delete_group_page_404s_for_non_members(self):
        group = create_new_group()
        url = self.get_url(group)
        create_and_login_user(self)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    def test_post_redirects_to_home_page(self):
        group = create_new_group()
        url = self.get_url(group)
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        response = self.client.post(url)
        self.assertRedirects(response, '/')

    def test_post_makes_group_inactive(self):
        group = create_new_group()
        url = self.get_url(group)
        self.assertTrue(group.quitsgroup.is_active)
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        response = self.client.post(url)
        self.assertFalse(Group.objects.get(id=group.id).quitsgroup.is_active)

class NewPaymentPageTest(QuitsTestCase):

    def create_group_url_stub(self):
        id_ = create_new_group().id
        self.client.login(username='owner@email.com', password='testing123')
        return '/groups/' + str(id_)

    def get_post_response(self, icon='today',
            date='02 February, 2014', amount='200.99', description='blah',
            who_paid=1, who_for=[1,2]):
        url_stub = self.create_group_url_stub()
        new_payment_url = url_stub + '/new_payment/'
        return self.client.post(new_payment_url, data={
            'icon': icon,
            'date': date,
            'amount': amount,
            'description': description,
            'who_paid': who_paid,
            'who_for': who_for,
        })

    def test_new_payment_page_redirects_for_unauthenticated_users(self):
        id_ = create_new_group().id
        url = '/groups/' + str(id_) + '/new_payment/'
        response = self.client.get(url)
        self.assertRedirects(response, '/?next=' + url)

    def test_new_payment_page_404s_for_non_members(self):
        id_ = create_new_group().id
        url = '/groups/' + str(id_) + '/new_payment/'
        create_and_login_user(self)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_new_payment_page_renders_new_payment_template(self):
        id_ = create_new_group().id
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        response = self.client.get('/groups/' + str(id_) + '/new_payment/')
        self.assertTemplateUsed(response, 'quits/new_payment.html')

    def test_new_payment_page_uses_new_payment_form(self):
        id_ = create_new_group().id
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        response = self.client.get('/groups/' + str(id_) + '/new_payment/')
        self.assertIsInstance(response.context['form'], NewPaymentForm)

    def test_new_payment_page_only_displays_group_members(self):
        owner = create_and_login_user(self)
        contacts = create_members()
        not_contact = User.objects.create_user(username="Not a contact")
        not_member = User.objects.create_user(username="Not a member")
        other_group = Group.objects.create(name="Other")
        other_group.user_set.add(*contacts + [owner, not_contact])
        group = Group.objects.create(name='Members group')
        group.user_set.add(*[owner] + contacts)
        response = self.client.get('/groups/' + str(group.id) + '/new_payment/')
        for contact in contacts:
            self.assertContains(response, contact.username)
        self.assertNotContains(response, not_contact.username)
        self.assertNotContains(response, not_member.username)

    def test_new_payment_page_sets_user_as_default_who_paid(self):
        user = create_and_login_user(self)
        contacts = create_members()
        other_group = Group.objects.create(name="Other")
        other_group.user_set.add(*contacts + [user])
        group = Group.objects.create(name='Members group')
        group.user_set.add(*[user] + contacts)
        response = self.client.get('/groups/' + str(group.id) + '/new_payment/')
        self.assertContains(response, 'checked="checked" id="input_who_paid_0"')

    def test_new_payment_page_sets_all_as_default_who_for(self):
        user = create_and_login_user(self)
        contacts = create_members()
        other_group = Group.objects.create(name="Other")
        other_group.user_set.add(*contacts + [user])
        group = Group.objects.create(name='Members group')
        group.user_set.add(*[user] + contacts)
        response = self.client.get('/groups/' + str(group.id) + '/new_payment/')
        for i in range(4):
            self.assertContains(response,
                'checked="checked" id="input_who_for_{}"'.format((str(i))))

    def test_valid_post_redirects_to_group_page(self):
        url_stub = self.create_group_url_stub()
        group_page_url = url_stub + '/view_group/'
        new_payment_url = url_stub + '/new_payment/'
        response = self.client.post(new_payment_url, data={
            'icon': 'local_dining',
            'date': '02 February, 2014',
            'amount': '99.99',
            'description': 'bill',
            'who_paid': 1,
            'who_for': [1, 2],
            })
        self.assertRedirects(response, group_page_url)

    def test_valid_post_saves_payment_to_db(self):
        response = self.get_post_response()
        payments = Payment.objects.all()
        self.assertEqual(len(payments), 1)
        payment = payments[0]
        self.assertEqual(str(payment.date), '2014-02-02')
        self.assertEqual(str(payment.amount), '200.99')
        self.assertEqual(payment.description, 'blah')
        self.assertEqual(payment.who_paid.username, 'owner@email.com')
        who_for_emails = [who_for.username for who_for in payment.who_for.all()]
        self.assertListEqual(who_for_emails, ['owner@email.com', 'member0@email.com'])

    def test_valid_post_adds_payment_to_group(self):
        response = self.get_post_response()
        payment = Payment.objects.first()
        self.assertEqual(payment.group, Group.objects.first())

    def test_invalid_post_no_date_redirects_to_group_page(self):
        group_page_url = '/groups/1/view_group/'
        response = self.get_post_response(date='')
        self.assertRedirects(response, group_page_url)

    def test_invalid_post_date_not_date_redirects_to_group_page(self):
        # invalid date is replaced by today's date
        group_page_url = '/groups/1/view_group/'
        response = self.get_post_response(date='not a date')
        self.assertRedirects(response, group_page_url)

    def test_invalid_post_invalid_date_redirects_to_group_page(self):
        # invalid date is replaced by today's date
        group_page_url = '/groups/1/view_group/'
        response = self.get_post_response(date='30 February, 2014')
        self.assertRedirects(response, group_page_url)

    def test_invalid_post_no_amount_shows_new_payment_page(self):
        response = self.get_post_response(amount='')
        self.assertTemplateUsed(response, 'quits/new_payment.html')

    def test_invalid_post_amount_not_amount_shows_new_payment_page(self):
        response = self.get_post_response(amount='not an amount')
        self.assertTemplateUsed(response, 'quits/new_payment.html')

    def test_invalid_post_invalid_amount_shows_new_payment_page(self):
        response = self.get_post_response(amount='20.199')
        self.assertTemplateUsed(response, 'quits/new_payment.html')

    def test_invalid_post_no_description_shows_new_payment_page(self):
        response = self.get_post_response(description='')
        self.assertTemplateUsed(response, 'quits/new_payment.html')

    def test_invalid_post_no_who_paid_shows_new_payment_page(self):
        response = self.get_post_response(who_paid=None)
        self.assertTemplateUsed(response, 'quits/new_payment.html')

    def test_invalid_post_no_who_for_shows_new_payment_page(self):
        response = self.get_post_response(who_for=None)
        self.assertTemplateUsed(response, 'quits/new_payment.html')

    def test_valid_post_adds_edit_for_group(self):
        pre_count = Edit.objects.count()
        response = self.get_post_response()
        self.assertEqual(Edit.objects.count(), pre_count + 1)

    def test_invalid_post_does_not_add_edit_for_group(self):
        pre_count = Edit.objects.count()
        response = self.get_post_response(who_for=None)
        self.assertEqual(Edit.objects.count(), pre_count)

class AddMembersPageTest(QuitsTestCase):

    def test_add_members_page_redirects_for_unauthenticated_users(self):
        id_ = create_new_group().id
        url = '/groups/' + str(id_) + '/add_members/'
        response = self.client.get(url)
        self.assertRedirects(response, '/?next=' + url)

    def test_add_members_page_404s_for_non_members(self):
        id_ = create_new_group().id
        url = '/groups/' + str(id_) + '/add_members/'
        create_and_login_user(self)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_add_members_page_renders_add_members_template(self):
        id_ = create_new_group().id
        self.assertTrue(self.client.login(
            username='owner@email.com', password='testing123'
        ))
        response = self.client.get('/groups/' + str(id_) + '/add_members/')
        self.assertTemplateUsed(response, 'quits/add_members.html')

    def test_add_members_page_passes_group_name_to_template(self):
        id_ = create_new_group().id
        self.client.login(username='owner@email.com', password='testing123')
        response = self.client.get('/groups/' + str(id_) + '/add_members/')
        self.assertEqual(response.context['group_name'], 'Cool group')

    def test_add_members_page_passes_group_id_to_template(self):
        id_ = create_new_group().id
        self.client.login(username='owner@email.com', password='testing123')
        response = self.client.get('/groups/' + str(id_) + '/add_members/')
        self.assertEqual(response.context['group_id'], str(id_))

    def test_add_members_page_uses_add_members_form(self):
        id_ = create_new_group().id
        self.assertTrue(self.client.login(
            username='owner@email.com', password='testing123'
        ))
        response = self.client.get('/groups/' + str(id_) + '/add_members/')
        self.assertIsInstance(response.context['form'], AddMembersForm)

    def test_post_redirects_to_group_page(self):
        id_ = create_new_group().id
        self.assertTrue(self.client.login(
            username='owner@email.com', password='testing123'
        ))
        response = self.client.post('/groups/' + str(id_) + '/add_members/', data={
                'emails_0': 'hello@you.com',
                'emails_1': '',
                'emails_2': '',
                'emails_3': '',
                'emails_4': '',
            })
        self.assertRedirects(response, '/groups/' + str(id_) + '/view_group/')

    def test_post_saves_contacts_as_members(self):
        group = create_new_group()
        owner = User.objects.get(username='owner@email.com')
        self.assertTrue(self.client.login(
            username='owner@email.com', password='testing123'
        ))
        new_user = User.objects.create_user(username="new@member.com")
        other_group = Group.objects.create(name="Other group")
        other_group.user_set.add(*[owner, new_user])

        response = self.client.post('/groups/' + str(group.id) + '/add_members/', data={
                'contacts': [5],
                'emails_0': '',
                'emails_1': '',
                'emails_2': '',
                'emails_3': '',
                'emails_4': '',
            })
        self.assertIn(new_user, group.user_set.all())

    def test_post_saves_email_users_as_members(self):
        group = create_new_group()
        owner = User.objects.get(username='owner@email.com')
        self.client.login(
            username='owner@email.com', password='testing123'
        )

        response = self.client.post('/groups/' + str(group.id) + '/add_members/', data={
                'emails_0': 'new_user@email.com',
                'emails_1': '',
                'emails_2': '',
                'emails_3': '',
                'emails_4': '',
            })
        self.assertIn(User.objects.get(email='new_user@email.com'), group.user_set.all())

    def test_post_with_empty_fields_shows_add_members_page(self):
        id_ = create_new_group().id
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        response = self.client.post(
            '/groups/' + str(id_) + '/add_members/', data={
                'emails_0': '',
                'emails_1': '',
                'emails_2': '',
                'emails_3': '',
                'emails_4': '',
            })
        self.assertTemplateUsed(response, 'quits/add_members.html')

    def test_valid_post_adds_edits_for_group(self):
        pre_count = Edit.objects.count()
        id_ = create_new_group().id
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        response = self.client.post(
            '/groups/' + str(id_) + '/add_members/', data={
                'emails_0': 'first@add.com',
                'emails_1': 'second@add.com',
                'emails_2': '',
                'emails_3': '',
                'emails_4': '',
            })
        self.assertEqual(Edit.objects.count(), pre_count + 2)

    def test_invalid_post_does_not_add_edit_for_group(self):
        pre_count = Edit.objects.count()
        pre_count = Edit.objects.count()
        id_ = create_new_group().id
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        response = self.client.post(
            '/groups/' + str(id_) + '/add_members/', data={
                'emails_0': '',
                'emails_1': '',
                'emails_2': '',
                'emails_3': '',
                'emails_4': '',
            })
        self.assertEqual(Edit.objects.count(), pre_count)

class EditPaymentPageTest(QuitsTestCase):

    def setUp(self):
        self.group = create_new_group()
        self.payment = self.create_new_payment(group=self.group)

    def create_new_payment(self, 
            group=None, dt=date.today(), amount=20.00, description='Blah', who_paid=1, who_for=[1,2]):
        payment = Payment.objects.create(
            group=group,
            date=dt,
            amount=amount,
            description=description,
            who_paid=User.objects.get(id=who_paid),
        )
        payment.who_for.add(*[User.objects.get(id=id_) for id_ in who_for])
        return payment

    def get_payment_url(self):
        return '/groups/' + str(self.group.id) + '/payments/' + str(self.payment.id) + '/edit/'

    def get_post_response(self, icon='local_dining',
            date='04 February, 2014', amount='20.50', description='Something new',
            who_paid=2, who_for=[2,3]):
        url = self.get_payment_url()
        return self.client.post(url, data={
            'icon': icon,
            'date': date,
            'amount': amount,
            'description': description,
            'who_paid': who_paid,
            'who_for': who_for,
        })

    def test_edit_payment_page_redirects_for_unauthenticated_users(self):
        url = self.get_payment_url()
        response = self.client.get(url)
        self.assertRedirects(response, '/?next=' + url)

    def test_edit_payment_page_404s_for_non_members(self):
        create_and_login_user(self)
        response = self.client.get(self.get_payment_url())
        self.assertEqual(response.status_code, 404)

    def test_edit_payment_page_renders_view_group_template(self):
        self.client.login(username='owner@email.com', password='testing123')
        response = self.client.get(self.get_payment_url())
        self.assertTemplateUsed(response, 'quits/edit_payment.html')

    def test_edit_payment_page_uses_new_payment_form(self):
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        response = self.client.get(self.get_payment_url())
        self.assertIsInstance(response.context['form'], NewPaymentForm)

    def test_edit_payment_page_uses_delete_payment_form(self):
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        response = self.client.get(self.get_payment_url())
        self.assertIsInstance(response.context['delete_form'], DeletePaymentForm)

    def test_edit_payment_page_passes_group_id_to_form(self):
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        response = self.client.get(self.get_payment_url())
        self.assertEqual(response.context['group_id'], str(self.group.id))

    def test_edit_payment_page_passes_payment_active_status_to_form(self):
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        response = self.client.get(self.get_payment_url())
        self.assertTrue(response.context['active'])

    def test_edit_payment_page_prepopulates_form_with_payment_data(self):
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        response = self.client.get(self.get_payment_url())
        self.assertContains(response, '20.00')
        self.assertContains(response, 'Blah')
        self.assertContains(response, 'owner@email.com')
        self.assertContains(response, 'member0@email.com')

    def test_post_does_not_add_new_payment_to_db(self):
        precount = Payment.objects.count()
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        response = self.get_post_response()
        self.assertEqual(Payment.objects.count(), precount)

    def test_post_changes_payment_attributes(self):
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        response = self.get_post_response()
        payment = Payment.objects.last()

        self.assertEqual(payment.date, datetime.strptime('04 February, 2014', '%d %B, %Y').date())
        self.assertEqual(payment.amount, Decimal('20.50'))
        self.assertEqual(payment.description, 'Something new')
        self.assertEqual(payment.who_paid.username, 'member0@email.com')
        self.assertListEqual(
            [who_for.username for who_for in payment.who_for.all()],
            ['member0@email.com', 'member1@email.com']
        )

    def test_post_redirects_to_group_page(self):
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        response = self.get_post_response()
        self.assertRedirects(response, '/groups/' + str(self.group.id) + '/view_group/')

    def test_valid_post_adds_edit_for_group(self):
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        precount = Edit.objects.count()
        response = self.get_post_response()
        self.assertEqual(Edit.objects.count(), precount + 1)

    def test_invalid_post_does_not_add_edit_for_group(self):
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        precount = Edit.objects.count()
        response = self.get_post_response(who_for=None)
        self.assertEqual(Edit.objects.count(), precount)

class DeletePaymentTest(QuitsTestCase):

    def create_new_payment(self, 
            group=None, dt=date.today(), amount=20.00, description='Blah', who_paid=1, who_for=[1,2]):
        payment = Payment.objects.create(
            group=group,
            date=dt,
            amount=amount,
            description=description,
            who_paid=User.objects.get(id=who_paid),
        )
        payment.who_for.add(*[User.objects.get(id=id_) for id_ in who_for])
        return payment

    def test_get_404s(self):
        request = HttpRequest
        request.method = 'GET'
        request.user = create_and_login_user(self)
        self.assertRaises(Http404, delete_payment, request, 1)

    def test_delete_payment_page_redirects_for_unauthenticated_users(self):
        group = create_new_group()
        url = '/groups/' + str(group.id) + '/payments/delete'
        response = self.client.post(url)
        self.assertRedirects(response, '/?next=' + url)

    def test_delete_payment_page_404s_for_non_members(self):
        group = create_new_group()
        url = '/groups/' + str(group.id) + '/payments/delete'
        create_and_login_user(self)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    def test_post_redirects_to_group_page(self):
        group = create_new_group()
        payment = self.create_new_payment(group=group)
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        response = self.client.post(
            '/groups/1/payments/delete',
            data={'payment': payment.id}
        )
        self.assertRedirects(response, '/groups/' + str(group.id) + '/view_group/')

    def test_post_makes_payment_inactive(self):
        group = create_new_group()
        payment = self.create_new_payment(group=group)
        self.assertTrue(payment.is_active)
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        response = self.client.post(
            '/groups/1/payments/delete',
            data={'payment': payment.id}
        )
        self.assertFalse(Payment.objects.get(id=payment.id).is_active)

    def test_valid_post_adds_edit_for_group(self):
        precount = Edit.objects.count()
        group = create_new_group()
        payment = self.create_new_payment(group=group)
        self.assertTrue(payment.is_active)
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        response = self.client.post(
            '/groups/1/payments/delete',
            data={'payment': payment.id}
        )
        self.assertEqual(Edit.objects.count(), precount + 1)

    def test_invalid_post_does_not_add_edit_for_group(self):
        precount = Edit.objects.count()
        group = create_new_group()
        payment = self.create_new_payment(group=group)
        self.assertTrue(payment.is_active)
        self.client.login(
            username='owner@email.com', password='testing123'
        )
        response = self.client.post(
            '/groups/1/payments/delete',
            data={'payment': 'payment'}
        )
        self.assertEqual(Edit.objects.count(), precount)

class ActivityLogTest(QuitsTestCase):

    def setUp(self):
        super().setUp()
        self.user = create_and_login_user(self)
        self.group = create_new_group(owner=self.user)
        self.group_url = '/groups/' + str(self.group.id) + '/activity_log/'

    def test_activity_log_renders_activity_log_template(self):
        response = self.client.get(self.group_url)
        self.assertTemplateUsed(response, 'quits/activity_log.html')

    def test_activity_log_passes_group_to_template(self):
        response = self.client.get(self.group_url)
        self.assertEqual(response.context['group'], self.group)

    def test_activity_log_passes_quits_group_to_template(self):
        response = self.client.get(self.group_url)
        self.assertEqual(response.context['quits_group'], self.group.quitsgroup)

    def test_activity_log_passes_edits_to_template(self):
        payment = Payment.objects.create(date=date.today(), amount=10.00)
        Edit.objects.create(payment=payment, user=self.user, group=self.group)
        response = self.client.get(self.group_url)
        edits = Edit.objects.filter(group=self.group).all()
        self.assertListEqual(list(response.context['edits']), list(edits))

    def test_activity_log_page_404s_for_non_members(self):
        create_and_login_user(self, email="not@member.com")
        response = self.client.get(self.group_url)
        self.assertEqual(response.status_code, 404)
