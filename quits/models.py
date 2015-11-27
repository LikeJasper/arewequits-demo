from django.db import models
from django.contrib.auth.models import Group, User
from datetime import date
from decimal import Decimal

class Payment(models.Model):
    swap = 'swap_horiz'
    home = 'home'
    bill = 'account_balance'
    shop = 'shopping_cart'
    meal = 'local_dining'
    drinks = 'local_bar'
    tickets = 'local_activity'
    party = 'cake'
    holiday = 'public'
    car = 'directions_car'
    other = 'thumb_up'
    ICON_CHOICES = (
        (swap, 'swap_horiz TRANSFER'),
        (home, 'home HOUSEHOLD'),
        (bill, 'account_balance BILLS'),
        (shop, 'shopping_cart SHOPPING'),
        (meal, 'local_dining MEALS'),
        (drinks, 'local_bar DRINKS'),
        (tickets, 'local_activity TICKETS'),
        (party, 'cake PARTIES'),
        (holiday, 'public HOLIDAYS'),
        (car, 'directions_car TRANSPORT'),
        (other, 'thumb_up OTHER')
    )

    group = models.ForeignKey(Group, null=True)
    icon = models.CharField(max_length=16, choices=ICON_CHOICES, default=swap)
    date = models.DateField(default='{dt:%d} {dt:%B} {dt:%Y}'.format(dt=date.today()))
    creation_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(default=None, max_digits=16, decimal_places=2)
    description = models.CharField(default='', max_length=256, blank=True)
    who_paid = models.ForeignKey(User, null=True)
    who_for = models.ManyToManyField(User, related_name='benefits')
    is_active = models.BooleanField(default=True, null=False)

    class Meta:
        ordering = ['-date', '-creation_date']

class Edit(models.Model):
    ch_create = 'create'
    ch_edit = 'edit'
    ch_delete = 'delete'
    ch_restor = 'restor'
    ch_name = 'name'
    ch_curren = 'curren'
    ch_addmem = 'addmem'
    CHANGE_CHOICES = (
        (ch_create, 'create'),
        (ch_edit, 'edit'),
        (ch_delete, 'delete'),
        (ch_restor, 'restor'),
        (ch_name, 'name'),
        (ch_curren, 'curren'),
        (ch_addmem, 'addmem'),
    )

    group = models.ForeignKey(Group, null=False)
    user = models.ForeignKey(User, null=False)
    date = models.DateTimeField(auto_now_add=True)
    change = models.CharField(max_length=6, choices=CHANGE_CHOICES, default=ch_edit)
    payment = models.ForeignKey(Payment, null=True)
    added_member = models.ForeignKey(User, null=True, related_name="edit_addmem")

    class Meta:
        ordering = ['-date']

class QuitsGroup(models.Model):
    GBP = '£'
    USD = '$'
    EUR = '€'
    CURRENCY_CHOICES = (
        (GBP, '£'),
        (USD, '$'),
        (EUR, '€'),
    )

    group = models.OneToOneField(Group, unique=True, null=False)
    currency = models.CharField(max_length=1, choices=CURRENCY_CHOICES, default=GBP)
    owner = models.ForeignKey(User, null=True, related_name='owned_groups')
    creation_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, null=False)

Group._meta.get_field('name')._unique = False
