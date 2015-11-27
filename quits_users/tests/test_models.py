from django.test import TestCase as DjangoTestCase
from django.db.utils import IntegrityError
from decimal import Decimal

from quits_users.models import User, QuitsUser
from quits.models import Group, QuitsGroup, Payment

class QuitsUserModelTest(DjangoTestCase):

    def test_user_required(self):
        quits_user = QuitsUser()
        self.assertRaises(IntegrityError, quits_user.save)

    def test_get_group_total_default(self):
        emails = ['test@email.com', 'dope@email.com', 'dupe@email.com']
        members = [User.objects.create_user(username=email, email=email) for
            email in emails]

        group = Group.objects.create(name='Test')
        QuitsGroup.objects.create(group=group)
        group.user_set.add(*members)

        totals = [user.quitsuser.get_group_total(group=group) 
            for user in User.objects.all()]
        targets = [Decimal(0).quantize(Decimal('.01')) for i in range(3)]
        self.assertListEqual(totals, targets)

    def test_get_group_total_ignores_inactive_payments(self):
        emails = ['test@email.com', 'dope@email.com', 'dupe@email.com']
        members = [User.objects.create_user(username=email, email=email) for
            email in emails]

        group = Group.objects.create(name='Test')
        QuitsGroup.objects.create(group=group)
        group.user_set.add(*members)

        active_payment = Payment.objects.create(
            group=group,
            date='2015-05-05',
            amount='30.00',
            description='This one is active',
            who_paid=members[0],
        )
        active_payment.who_for.add(
            *members
        )
        active_payment.save()

        inactive_payment = Payment.objects.create(
            group=group,
            date='2015-05-05',
            amount='30.00',
            description='This one is inactive',
            who_paid=members[0],
        )
        inactive_payment.who_for.add(
            *members
        )
        inactive_payment.is_active = False
        inactive_payment.save()

        group_total = members[0].quitsuser.get_group_total(group)
        self.assertEqual(group_total, Decimal(20.00).quantize(Decimal('.01')))

    def test_get_group_total_returns_group_total_value(self):
        emails = ['test@email.com', 'dope@email.com', 'dupe@email.com']
        members = [User.objects.create_user(username=email, email=email) for
            email in emails]

        group = Group.objects.create(name='Test')
        QuitsGroup.objects.create(group=group)
        group.user_set.add(*members)

        wrong_group = Group.objects.create(name='Wrong')
        QuitsGroup.objects.create(group=wrong_group)
        wrong_group.user_set.add(*members)

        users = User.objects.all()

        payment_data_sets = [
            {
                # Irrelevant group
                'group': wrong_group,
                'date': '2015-05-05',
                'amount': '20.00',
                'description': 'first',
                'who_paid': users[0].id,
                'who_for': [users[0].id, users[1].id],
            },
            {
                # Somebody else paid -> -10.00
                'group': group,
                'date': '2015-05-05',
                'amount': '20.00',
                'description': 'second',
                'who_paid': users[1].id,
                'who_for': [users[0].id, users[1].id],
            },
            {
                # Paid but did not benefit (1 did) -> +11.11
                'group': group,
                'date': '2015-05-05',
                'amount': '11.11',
                'description': 'third',
                'who_paid': users[0].id,
                'who_for': [users[1].id],
            },
            {
                # Paid but did not benefit (2 did) -> +24.50
                'group': group,
                'date': '2015-05-05',
                'amount': '24.50',
                'description': 'fourth',
                'who_paid': users[0].id,
                'who_for': [users[1].id, users[2].id],
            },
            {
                # Paid and benefited (1 other did) -> +6.00
                'group': group,
                'date': '2015-05-05',
                'amount': '12.00',
                'description': 'fifth',
                'who_paid': users[0].id,
                'who_for': [users[0].id, users[1].id],
            },
            {
                # Paid and benefited (2 others did) -> +22.44
                'group': group,
                'date': '2015-05-05',
                'amount': '33.66',
                'description': 'sixth',
                'who_paid': users[0].id,
                'who_for': [users[0].id, users[1].id, users[2].id],
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

        quits_user = members[0].quitsuser

        self.assertEqual(quits_user.get_group_total(group), Decimal(54.05).quantize(Decimal('.01')))
