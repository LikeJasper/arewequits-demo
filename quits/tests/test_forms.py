from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from unittest import skip
from unittest.mock import Mock, patch

from datetime import date, datetime

from quits.forms import (NewPaymentForm, DeletePaymentForm,
    GroupForm, QuitsGroupForm, AddMembersForm, EditGroupForm,
    ValidationError)
from quits.models import Group, Payment
from quits_users.models import User, QuitsUser

UNWRITTEN_COMPLAINT = 'write me!'

class GroupFormIntegratedTest(DjangoTestCase):
    def create_owner(self):
        return User.objects.create_user(
            username='owner@email.com', email='owner@email.com')

    def create_users(self, number=3):
        return [
            User.objects.create_user(
            username='member{}@a.de'.format(str(i)),
            email='member{}@a.de'.format(str(i))
            ) for i in range(number)
        ]

    def create_quits_users(self, number=3):
        users = self.create_users(number)
        return [QuitsUser.objects.create(user=user) for user in users]

    def create_member_ids(self, number=3):
        members = self.create_users(number=3)
        return [member.id for member in members]

    def create_group_with_email_members(self, number=5):
        emails = ['test_{}@email.com'.format(str(i)) for i in range(number)]
        data = {'name': 'Emails group'}
        for i in range(len(emails)):
            data['emails_{}'.format(str(i))] = emails[i]
        form = GroupForm(owner=self.create_owner(), data=data)
        return {'group': form.save(), 'emails': emails}

    def test_form_renders_group_name_input(self):
        form = GroupForm(owner=self.create_owner())
        self.assertIn('placeholder="Group name"', form.as_p())
        self.assertIn('id="input_group_name"', form.as_p())

    def test_form_validation_for_blank_group_name(self):
        form = GroupForm(owner=self.create_owner(), data={
            'name': '',
            'contacts': self.create_member_ids()
            })
        self.assertFalse(form.is_valid())

    def test_form_renders_contacts_input(self):
        form = GroupForm(owner=self.create_owner())
        self.assertIn('id="input_contacts"', form.as_p())

    def test_form_renders_only_fellow_group_members_as_member_input(self):
        contacts = self.create_users()
        owner = User.objects.create_user(username='owner@email.com')
        members = list(contacts)
        members.append(owner)
        other_group = Group.objects.create(name="Other")
        other_group.user_set.add(*members)
        not_contact = User.objects.create_user(username='not_me@email.com')

        form = GroupForm(owner=owner)
        for contact in contacts:
            self.assertIn(contact.username, form.as_p())
        self.assertNotIn(not_contact.username, form.as_p())

    def test_form_renders_email_input(self):
        form = GroupForm(owner=self.create_owner())
        self.assertIn('placeholder="Email address"',
            form.as_p())
        for i in range(5):
            self.assertIn(
                'id="input_emails_{}'.format(str(i)),
                form.as_p()
            )

    def test_form_validation_for_valid_data_members_and_email(self):
        owner = self.create_owner()
        members = self.create_users(3)
        gang = list(members)
        gang.append(owner)
        other_group = Group.objects.create(name="Other")
        other_group.user_set.add(*gang)
        form = GroupForm(owner=owner, data={
            'name': 'Household expenses',
            'contacts': [member.id for member in members],
            'emails_0': 'new_member_1@email.com',
            'emails_1': 'new_member_2@email.com',
            'emails_2': 'new_member_3@email.com',
            'emails_3': 'new_member_4@email.com',
            'emails_4': 'new_member_5@email.com',
            })
        self.assertTrue(form.is_valid())

    def test_form_validation_for_valid_data_members_no_email(self):
        owner = self.create_owner()
        members = self.create_users(1)
        gang = list(members)
        gang.append(owner)
        other_group = Group.objects.create(name="Other")
        other_group.user_set.add(*gang)
        form = GroupForm(owner=owner, data={
            'name': 'Household expenses',
            'contacts': [member.id for member in members],
            'emails_0': '',
            'emails_1': '',
            'emails_2': '',
            'emails_3': '',
            'emails_4': '',
            })
        self.assertTrue(form.is_valid())

    def test_form_validation_for_valid_data_email_no_members(self):
        form = GroupForm(owner=self.create_owner(), data={
            'name': 'Household expenses',
            'contacts': [],
            'emails_0': 'new_member_1@email.com',
            })
        self.assertTrue(form.is_valid())

    def test_form_validation_for_no_members_and_no_email(self):
        form = GroupForm(owner=self.create_owner(), data={
            'name': 'Household expenses',
            'contacts': [],
            'emails_0': '',
            'emails_1': '',
            'emails_2': '',
            'emails_3': '',
            'emails_4': '',
            })
        self.assertFalse(form.is_valid())
        self.assertRaises(
            ValidationError,
            form.clean
        )

    def test_form_validation_for_bad_email(self):
        form = GroupForm(owner=self.create_owner(), data={
            'name': 'Household expenses',
            'emails_0': 'not_an_email',
            })
        self.assertFalse(form.is_valid())

    def test_form_save_adds_members_to_group(self):
        owner = self.create_owner()
        members = self.create_users()
        gang = list(members)
        gang.append(owner)
        other_group = Group.objects.create(name="Other")
        other_group.user_set.add(*gang)
        member_ids = [member.id for member in members]
        form = GroupForm(owner=owner, data={
            'name': 'Household expenses',
            'contacts': member_ids,
            })
        group = form.save()
        self.assertEqual(list(group.user_set.exclude(username='owner@email.com')), members)

    def test_form_save_adds_owner_as_member(self):
        owner = self.create_owner()
        members = self.create_users()
        gang = list(members)
        gang.append(owner)
        other_group = Group.objects.create(name="Other")
        other_group.user_set.add(*gang)
        member_ids = [member.id for member in members]
        form = GroupForm(owner=owner, data={
            'name': 'Household expenses',
            'contacts': member_ids,
            })
        group = form.save()
        self.assertIn(owner, group.user_set.all())

    def test_form_save_creates_inactive_members_for_each_email(self):
        emails = self.create_group_with_email_members()['emails']
        user_emails = [user.email for user in User.objects.exclude(username='owner@email.com')]
        self.assertListEqual(user_emails, emails)
        for user in User.objects.exclude(username='owner@email.com'):
            self.assertFalse(user.is_active)

    def test_form_save_does_not_recreate_existing_users_by_email(self):
        existing_users = self.create_users()
        form = GroupForm(owner=self.create_owner(), data={
            'name': 'Duplicate existing members',
            'emails_0': 'member1@a.de',
            })
        form.save()
        self.assertListEqual(list(User.objects.exclude(username='owner@email.com')), existing_users)

    def test_form_save_adds_members_to_group_by_email(self):
        group_emails = self.create_group_with_email_members()
        group = group_emails['group']
        emails = group_emails['emails']
        user_emails = [user.email for user in group.user_set.exclude(username='owner@email.com')]
        self.assertListEqual(user_emails, emails)

class QuitsGroupFormIntegratedTest(DjangoTestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner@email.com')

    def test_form_invalid_without_group(self):
        form = QuitsGroupForm(owner=self.owner,data={
            'currency': '£',
            })
        self.assertFalse(form.is_valid())

    def test_form_invalid_without_owner(self):
        group = Group.objects.create(name='Testing')
        self.assertRaises(
            TypeError,
            QuitsGroupForm,
            data={'currency': '£', 'group': group.id}
        )

    def test_form_renders_currency_input(self):
        form = QuitsGroupForm(owner=self.owner)
        self.assertIn('id="input_currency"', form.as_p())

    def test_form_validation_for_blank_currency(self):
        group = Group.objects.create(name='Testing')
        form = QuitsGroupForm(owner=self.owner, data={
            'currency': '',
            'group': group.id,
            })
        self.assertFalse(form.is_valid())

    def test_form_validation_for_valid_data(self):
        group = Group.objects.create(name='Testing')
        form = QuitsGroupForm(owner=self.owner, data={
            'currency': '£',
            'group': group.id,
            })
        self.assertTrue(form.is_valid())

class EditGroupFormTest(DjangoTestCase):
    def setUp(self):
        group = Group.objects.create(name='Test')
        self.form = EditGroupForm(instance=group)

    def test_form_renders_name_input(self):
        self.assertIn('value="Test"', self.form.as_p())

class NewPaymentFormIntegratedTest(DjangoTestCase):
    def setUp(self):
        group = Group.objects.create(name='Test')
        self.form = NewPaymentForm(group_id=group.id)

    def test_form_renders_icon_input(self):
        self.assertIn('id="input_icon"', self.form.as_p())

    def test_form_renders_date_input(self):
        today = '{dt:%d} {dt:%B} {dt:%Y}'.format(dt = date.today())
        self.assertIn('value="{}"'.format(today), self.form.as_p())
        self.assertIn('id="input_date"', self.form.as_p())

    def test_form_renders_amount_input(self):
        self.assertIn('placeholder="0.00"', self.form.as_p())
        self.assertIn('id="input_amount"', self.form.as_p())

    def test_form_renders_description_input(self):
        self.assertIn('placeholder="E.g. electricity bill"', self.form.as_p())
        self.assertIn('id="input_description"', self.form.as_p())

    def test_form_renders_who_paid_input(self):
        self.assertIn('id="input_who_paid"', self.form.as_p())

    def test_form_renders_who_for_input(self):
        self.assertIn('id="input_who_for"', self.form.as_p())

    def test_does_not_offer_none_as_who_paid_choice(self):
        self.assertNotIn('---------', self.form.as_p())

    def test_form_save_adds_payment_to_group(self):
        users = [User.objects.create_user(
            username='user{}@email.com'.format(str(i)),
            email='user{}@email.com'.format(str(i))
            ) for i in range(3)]
        group = Group.objects.create(name='Test Group')
        group.user_set.add(*users)
        form = NewPaymentForm(group_id=group.id, data={
            'icon': 'person_pin',
            'date': datetime.strptime('02 February 2011', '%d %B %Y'),
            'amount': '99.99',
            'description': 'bill',
            'who_paid': 1,
            'who_for': [1, 2],
        })
        form.save()
        payment = Payment.objects.first()
        self.assertEqual(payment.group, group)

    def test_form_only_renders_who_paid_and_who_for_options_for_group(self):
        owner = User.objects.create_user(
            username='owner@g.co', email='owner@g.co')
        member = User.objects.create_user(
            username='member@g.co', email='member@g.co')
        not_member = User.objects.create_user(
            username='not_member@g.co', email='not_member@g.co')
        group = Group.objects.create(name='Members only')
        group.user_set.add(owner, member)
        form = NewPaymentForm(group_id=group.id)

        self.assertIn('owner@g.co', form.as_p())
        self.assertEqual(form.as_p().count('owner@g.co'), 2)
        self.assertIn('member@g.co', form.as_p())
        self.assertEqual(form.as_p().count('member@g.co'), 2)

        self.assertNotIn('not_member@g.co', form.as_p())

    def test_form_save_does_not_add_new_payment_when_given_instance(self):
        users = [User.objects.create_user(
            username='user{}@email.com'.format(str(i))) for i in range(3)]
        group = Group.objects.create(name='Test Group')
        group.user_set.add(*users)
        payment = Payment.objects.create(
            date=datetime.strptime('02 February 2011', '%d %B %Y'),
            amount='99.99',
            description='bill',
            who_paid=users[0],
        )
        payment.who_for.add(*users)

        form = NewPaymentForm(group_id=group.id, instance=payment, data={
            'icon': 'person_pin',
            'date': datetime.strptime('11 March 2014', '%d %B %Y'),
            'amount': '22.50',
            'description': 'New Info',
            'who_paid': 3,
            'who_for': [2, 3],
        })
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(Payment.objects.count(), 1)

    def test_form_save_changes_attributes_for_existing_payment(self):
        users = [User.objects.create_user(
            username='user{}@email.com'.format(str(i))) for i in range(3)]
        group = Group.objects.create(name='Test Group')
        group.user_set.add(*users)
        payment = Payment.objects.create(
            date=datetime.strptime('02 February 2011', '%d %B %Y'),
            amount='99.99',
            description='bill',
            who_paid=users[0],
        )
        payment.who_for.add(*users)

        form = NewPaymentForm(group_id=group.id, instance=payment, data={
            'icon': 'person_pin',
            'date': datetime.strptime('11 March 2014', '%d %B %Y'),
            'amount': '22.50',
            'description': 'New Info',
            'who_paid': 3,
            'who_for': [2, 3],
        })
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(payment.date, datetime.strptime('11 March 2014', '%d %B %Y').date())
        self.assertEqual(payment.amount, 22.50)
        self.assertEqual(payment.description, 'New Info')
        self.assertEqual(payment.who_paid, users[2])
        self.assertListEqual(list(payment.who_for.all()), [users[1], users[2]])

class DeletePaymentFormTest(DjangoTestCase):

    def test_form_save_makes_payment_inactive(self):
        users = [User.objects.create_user(
            username='user{}@email.com'.format(str(i))) for i in range(3)]
        group = Group.objects.create(name='Test Group')
        group.user_set.add(*users)
        payment = Payment.objects.create(
            date=datetime.strptime('02 February 2011', '%d %B %Y'),
            amount='99.99',
            description='bill',
            who_paid=users[0],
        )
        payment.who_for.add(*users)
        payment.group = group
        payment.save()

        form = DeletePaymentForm(group_id=group.id, data={'payment': 1})
        form.save()
        self.assertFalse(Payment.objects.get(id=payment.id).is_active)

    def test_form_save_does_not_make_payment_from_wrong_group_inactive(self):
        users = [User.objects.create_user(
            username='user{}@email.com'.format(str(i))) for i in range(3)]
        group = Group.objects.create(name='Test Group')
        group.user_set.add(*users)
        payment = Payment.objects.create(
            date=datetime.strptime('02 February 2011', '%d %B %Y'),
            amount='99.99',
            description='bill',
            who_paid=users[0],
        )
        payment.who_for.add(*users)
        payment.group = group
        payment.save()

        wrong_group = Group.objects.create(name='Wrong Group')
        wrong_group.user_set.add(*users)

        form = DeletePaymentForm(group_id=wrong_group.id, data={'payment': 1})
        form.save()
        self.assertTrue(Payment.objects.get(id=payment.id).is_active)

class AddMembersFormTest(DjangoTestCase):
    def create_owner(self):
        return User.objects.create_user(username='owner@email.com')

    def create_users(self, number=3):
        return [
            User.objects.create_user(
            username='member{}@a.de'.format(str(i)),
            email='member{}@a.de'.format(str(i))
            ) for i in range(number)
        ]

    def create_quits_users(self, number=3):
        users = self.create_users(number)
        return [QuitsUser.objects.create(user=user) for user in users]

    def add_email_members(self, number=5):
        emails = ['test_{}@email.com'.format(str(i)) for i in range(number)]
        data = {}
        for i in range(len(emails)):
            data['emails_{}'.format(str(i))] = emails[i]
        group = Group.objects.create(name='Existing')
        form = AddMembersForm(group_id=group.id, user=self.create_owner(), data=data)
        form.save()
        return {'group': group, 'emails': emails}

    def test_form_renders_contact_input(self):
        group = Group.objects.create(name='Existing')
        form = AddMembersForm(group_id=1, user=self.create_owner())
        self.assertIn('id="input_contacts"', form.as_p())

    def test_form_renders_only_fellow_group_members_as_contact_input(self):
        contacts = self.create_users()
        owner = User.objects.create_user(username='owner@email.com')
        members = list(contacts)
        members.append(owner)
        other_group = Group.objects.create(name="Other")
        other_group.user_set.add(*members)
        not_contact = User.objects.create_user(username='not_me@email.com')

        group = Group.objects.create(name='Existing')

        form = AddMembersForm(group_id=group.id, user=owner)
        for contact in contacts:
            self.assertIn(contact.username, form.as_p())
        self.assertNotIn(not_contact.username, form.as_p())

    def test_form_does_not_render_existing_members_as_contact_input(self):
        contacts = self.create_users()
        owner = User.objects.create_user(username='owner@email.com')
        members = list(contacts)
        members.append(owner)
        other_group = Group.objects.create(name="Other")
        other_group.user_set.add(*members)
        not_contact = User.objects.create_user(username='not_me@email.com')

        group = Group.objects.create(name='Existing')
        group.user_set.add(*[owner] + contacts[1:])

        form = AddMembersForm(group_id=group.id, user=owner)
        for contact in contacts[1:]:
            self.assertNotIn(contact.username, form.as_p())
        self.assertIn(contacts[0].username, form.as_p())

    def test_form_renders_email_input(self):
        user = User.objects.create_user(username='owner@email.com')

        group = Group.objects.create(name='Existing')
        # group.user_set.add(user)

        form = AddMembersForm(group_id=group.id, user=user)
        self.assertIn('placeholder="Email address"',
            form.as_p())
        for i in range(5):
            self.assertIn(
                'id="input_emails_{}'.format(str(i)),
                form.as_p()
            )

    def test_form_save_adds_contacts_to_group(self):
        user = self.create_owner()
        contacts = self.create_users()
        gang = list(contacts)
        gang.append(user)
        other_group = Group.objects.create(name="Other")
        other_group.user_set.add(*gang)
        contact_ids = [contact.id for contact in contacts]

        group = Group.objects.create(name='Existing')

        form = AddMembersForm(group_id=group.id, user=user, data={
            'name': 'Household expenses',
            'contacts': contact_ids,
            })
        form.save()
        self.assertEqual(list(group.user_set.exclude(username='owner@email.com')), contacts)

    def test_form_save_creates_inactive_users_for_each_email(self):
        emails = self.add_email_members()['emails']
        user_emails = [user.email for user in User.objects.exclude(username='owner@email.com')]
        self.assertListEqual(user_emails, emails)
        for user in User.objects.exclude(username='owner@email.com'):
            self.assertFalse(user.is_active)

    def test_form_save_does_not_recreate_existing_users_by_email(self):
        existing_users = self.create_users()
        group = Group.objects.create(name='Existing')
        form = AddMembersForm(group_id=group.id, user=self.create_owner(), data={
            'emails_0': 'member1@a.de',
            })
        form.save()
        self.assertListEqual(list(User.objects.exclude(username='owner@email.com')), existing_users)

    def test_form_save_creates_quits_user_for_each_email(self):
        emails = self.add_email_members()['emails']
        user_emails = [quits_user.user.username for quits_user in QuitsUser.objects.exclude(
            user__username='owner@email.com')]
        self.assertListEqual(user_emails, emails)

    def test_form_save_does_not_recreate_existing_quits_users_by_email(self):
        existing_quits_users = self.create_quits_users()
        group = Group.objects.create(name='Existing')
        form = AddMembersForm(group_id=group.id, user=self.create_owner(), data={
            'emails_0': 'member1@a.de',
            })
        form.save()
        self.assertListEqual(list(QuitsUser.objects.exclude(user__username='owner@email.com')),
            existing_quits_users)

    def test_form_save_adds_members_to_group_by_email(self):
        group_emails = self.add_email_members()
        group = group_emails['group']
        emails = group_emails['emails']
        group_emails = [user.username for user in group.user_set.exclude(username='owner@email.com')]
        self.assertListEqual(group_emails, emails)

    def test_form_validation_for_no_contacts_no_emails(self):
        user = self.create_owner()
        contacts = self.create_users()
        other_group = Group.objects.create(name="Other")
        other_group.user_set.add(user)
        other_group.user_set.add(*contacts)
        contact_ids = [contact.id for contact in contacts]

        group = Group.objects.create(name='Existing')

        data = {}
        for i in range(5):
            data['emails_{}'.format(str(i))] = ''
        form = AddMembersForm(group_id=group.id, user=user, data=data)
        self.assertFalse(form.is_valid())
