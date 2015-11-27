from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from unittest import skip
from datetime import date, datetime
from decimal import Decimal

from django.db.utils import IntegrityError

from quits.models import Edit, Payment, QuitsGroup, Group, User

class PaymentModelTest(TestCase):
    def setUp(self):
        self.payment = Payment()

    def test_default_icon(self):
        self.assertEqual(self.payment.icon, 'person_pin')

    def test_default_date(self):
        self.assertEqual(self.payment.date, '{dt:%d} {dt:%B} {dt:%Y}'.format(dt = date.today()))

    def test_default_creation_date(self):
        payment = Payment.objects.create(date=date.today(), amount=10.00)
        self.assertEqual(payment.creation_date.date(), date.today())

    def test_default_amount(self):
        self.assertEqual(self.payment.amount, None)

    def test_default_description(self):
        self.assertEqual(self.payment.description, '')

    def test_default_who_paid(self):
        self.assertEqual(self.payment.who_paid, None)

    def test_default_is_active(self):
        self.assertTrue(self.payment.is_active)

class EditTest(TestCase):
    def setUp(self):
        try:
            self.user = User.objects.get(username='edit@model.com')
        except:
            self.user = User.objects.create_user(username="edit@model.com")
        self.payment = Payment.objects.create(date=date.today(), amount=10.00)
        self.group = Group.objects.create(name='Test group')
        self.edit = Edit.objects.create(payment=self.payment, user=self.user, group=self.group)

    def tearDown(self):
        self.edit.delete()
        self.payment.delete()
        self.user.delete()
        self.group.delete()

    def test_default_date(self):
        self.assertEqual(self.edit.date.date(), date.today())

    def test_default_change(self):
        self.assertEqual(self.edit.change, 'edit')

class QuitsGroupModelTest(DjangoTestCase):
    def setUp(self):
        self.group = Group.objects.create(name='Test Group')
        self.quits_group = QuitsGroup(group=self.group)

    def test_group_required(self):
        quits_group = QuitsGroup()
        self.assertRaises(IntegrityError,
            quits_group.save)

    def test_default_currency(self):
        self.assertEqual(self.quits_group.currency, '£')

    def test_default_owner(self):
        self.assertEqual(self.quits_group.owner, None)

    def test_default_creation_date(self):
        quits_group = QuitsGroup.objects.create(group=self.group)
        self.assertEqual(quits_group.creation_date.date(), date.today())
