from django.db import models
from quits.models import User, Group
from decimal import Decimal
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
import hashlib

from django.dispatch import receiver
from allauth.account.signals import email_confirmed

class QuitsUser(models.Model):
    user = models.OneToOneField(User, unique=True)

    def __str__(self):
        return "QuitsUser object for User {}".format(str(self.user))

    def get_group_total(self, group):
        active_payments = group.payment_set.filter(is_active=True)
        who_paid_payments = active_payments.filter(who_paid=self.user)
        paid_total = sum([payment.amount for payment in who_paid_payments])

        who_for_payments = active_payments.filter(who_for=self.user)
        benefits = [(payment.amount / payment.who_for.count())
            for payment in who_for_payments]
        for_total = sum(benefits)
        group_total = Decimal(paid_total - for_total).quantize(Decimal('.01'))

        return group_total

    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False

    def profile_image_url(self):
        fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')
        if len(fb_uid):
            return "http://graph.facebook.com/{}/picture?width=50&height=50".format(fb_uid[0].uid)
        return "http://www.gravatar.com/avatar/{}?s=50".format(hashlib.md5(self.user.email.encode('utf-8')).hexdigest())

User.quitsuser = property(lambda u: QuitsUser.objects.get_or_create(user=u)[0])
User.__str__ = lambda self: self.first_name + " " + self.last_name \
if self.first_name and self.emailaddress_set.filter(verified=True) \
else self.email

@receiver(email_confirmed)
def update_user_email(sender, request, email_address, **kwargs):
    # Once the email address is confirmed, make new email_address primary.
    # This also sets user.email to the new email address.
    # email_address is an instance of allauth.account.models.EmailAddress
    email_address.set_as_primary()
    # Get rid of old email addresses
    stale_addresses = EmailAddress.objects.filter(
        user=email_address.user).exclude(primary=True).delete()
