from django import forms
from django.forms import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from datetime import date, datetime

from quits.models import Payment, QuitsGroup, Group
from quits_users.models import User, QuitsUser
from allauth.account.forms import SignupForm

class NewPaymentForm(forms.models.ModelForm):
    def __init__(self, group_id, *args, **kwargs):
        super(NewPaymentForm, self).__init__(*args, **kwargs)
        self.fields['who_paid'].empty_label = None
        self.group = Group.objects.get(id=group_id)
        self.fields['who_paid'].queryset = User.objects.filter(
            groups=self.group
        )
        self.fields['who_for'].queryset = User.objects.filter(
            groups=self.group
        )        
    
    class Meta:
        model = Payment
        fields = ('icon', 'date', 'amount', 'description', 'who_paid', 'who_for')
        widgets = {
            'icon': forms.Select(attrs={
                'id': 'input_icon',
                }),
            'date': forms.DateInput(attrs={
                'id': 'input_date',
                'class': 'datepicker',
                }),
            'amount': forms.NumberInput(attrs={
                'placeholder': '0.00',
                'id': 'input_amount',
                }),
            'description': forms.TextInput(attrs={
                'placeholder': 'E.g. electricity bill',
                'id': 'input_description',
                }),
            'who_paid': forms.RadioSelect(attrs={
                'id': 'input_who_paid',
                }),
            'who_for': forms.CheckboxSelectMultiple(attrs={
                'id': 'input_who_for',
                }),
        }

    def save(self, commit=True):
        instance = super(NewPaymentForm, self).save(commit=True)
        instance.group = self.group
        if commit:
            instance.save()
        return instance

class DeletePaymentForm(forms.Form):
    def __init__(self, group_id, *args, **kwargs):
        super(DeletePaymentForm, self).__init__(*args, **kwargs)
        self.group = Group.objects.get(id=group_id)
        self.fields['payment'].queryset = Payment.objects.filter(group=self.group)

    payment = forms.ModelChoiceField(
        queryset=Payment.objects.none(),
        widget=forms.HiddenInput(),
    )

    def save(self, commit=True):
        if self.is_valid():
            payment = self.cleaned_data.get('payment')
            if payment not in Payment.objects.filter(group=self.group):
                raise ValidationError('Payment does not belong to this group.',
                    'wrong_group')
            payment.is_active = False
            if commit:
                payment.save(update_fields=['is_active'])
            return payment

class RestorePaymentForm(forms.Form):
    def __init__(self, group_id, *args, **kwargs):
        super(RestorePaymentForm, self).__init__(*args, **kwargs)
        self.group = Group.objects.get(id=group_id)
        self.fields['payment'].queryset = Payment.objects.filter(group=self.group)

    payment = forms.ModelChoiceField(
        queryset=Payment.objects.none(),
        widget=forms.HiddenInput()
    )

    def save(self, commit=True):
        if self.is_valid():
            payment = self.cleaned_data.get('payment')
            if payment not in Payment.objects.filter(group=self.group):
                raise ValidationError('Payment does not belong to this group.',
                    'wrong_group')
            payment.is_active = True
            if commit:
                payment.save(update_fields=['is_active'])
            return payment

class GroupForm(forms.models.ModelForm):
    def __init__(self, owner, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        self.owner = owner
        self.fields['contacts'].queryset = User.objects.exclude(id=owner.id).filter(
            groups=owner.groups.all()).distinct().extra(
            select={'no_name': 'CASE WHEN auth_user.first_name IS "" THEN 0 ELSE 1 END'}
            ).order_by('-no_name', 'first_name', 'last_name', 'email')
    
    class Meta:
        model = Group
        fields = ('name',)
        labels = {
            'name': "Group name",
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Group name',
                'id': 'input_group_name',
                }),
        }

    contacts = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        required=False,
        label="Add members from other groups",
        widget=forms.CheckboxSelectMultiple(attrs={
            'id': 'input_contacts',
            }),
        )

    emails_0 = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'placeholder': 'Email address',
        'id': 'input_emails_0'
        }))
    emails_1 = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'placeholder': 'Email address',
        'id': 'input_emails_1'
        }))
    emails_2 = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'placeholder': 'Email address',
        'id': 'input_emails_2'
        }))
    emails_3 = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'placeholder': 'Email address',
        'id': 'input_emails_3'
        }))
    emails_4 = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'placeholder': 'Email address',
        'id': 'input_emails_4'
        }))

    def clean(self):
        cleaned_data = super(GroupForm, self).clean()
        members = cleaned_data.get('contacts')
        emails = []
        for i in range(5):
            email = cleaned_data.get('emails_{}'.format(str(i)))
            if email != '':
                emails.append(email)
                
        if not members and not emails:
            raise ValidationError("You must add at least one other person to the group.",
                code='no_contacts_or_emails')
        return cleaned_data

    def save(self, commit=True):
        instance = super(GroupForm, self).save(commit=True)
        instance.user_set.add(self.owner)
        for member in self.cleaned_data.get('contacts'):
            instance.user_set.add(member)
        for i in range(5):
            email = self.cleaned_data.get('emails_{}'.format(str(i)))
            if email != '':
                try:
                    email_user = User.objects.get(email=email)
                except ObjectDoesNotExist:
                    email_user = User.objects.create_user(username=email, email=email)
                    email_user.is_active = False
                    email_user.save()
                instance.user_set.add(email_user)
        if commit:
            instance.save()
        return instance

class QuitsGroupForm(forms.models.ModelForm):
    def __init__(self, owner, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner = owner

    class Meta:
        model = QuitsGroup
        fields = ('currency', 'group')
        widgets = {
            'currency': forms.Select(attrs={
                'id': 'input_currency',
                }),
        }

    def save(self, commit=True):
        instance = super(QuitsGroupForm, self).save(commit=commit)
        instance.owner = self.owner
        if commit:
            instance.save()
        return instance

class EditGroupForm(forms.models.ModelForm):

    class Meta:
        model = Group
        fields = ('name',)

class EditQuitsGroupForm(forms.models.ModelForm):

    class Meta:
        model = QuitsGroup
        fields = ('currency',)

class AddMembersForm(forms.Form):
    def __init__(self, group_id, user, *args, **kwargs):
        super(AddMembersForm, self).__init__(*args, **kwargs)
        self.group = Group.objects.get(id=group_id)
        self.fields['contacts'].queryset = User.objects.exclude(
            groups=self.group).filter(groups=user.groups.all()
            ).distinct().extra(
            select={'no_name': 'CASE WHEN auth_user.first_name IS "" THEN 0 ELSE 1 END'}
            ).order_by('-no_name', 'first_name', 'last_name', 'email')

    contacts = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        required=False,
        label="Add members from other groups",
        widget=forms.CheckboxSelectMultiple(attrs={
            'id': 'input_contacts',
            }),
        )

    emails_0 = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'placeholder': 'Email address',
        'id': 'input_emails_0'
        }))
    emails_1 = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'placeholder': 'Email address',
        'id': 'input_emails_1'
        }))
    emails_2 = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'placeholder': 'Email address',
        'id': 'input_emails_2'
        }))
    emails_3 = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'placeholder': 'Email address',
        'id': 'input_emails_3'
        }))
    emails_4 = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'placeholder': 'Email address',
        'id': 'input_emails_4'
        }))

    def clean(self):
        cleaned_data = super(AddMembersForm, self).clean()
        contacts = cleaned_data.get('contacts')
        emails = []
        for i in range(5):
            email = cleaned_data.get('emails_{}'.format(str(i)))
            if email != '':
                emails.append(email)
                
        if not contacts and not emails:
            raise ValidationError("You didn't add anyone to the group.",
                code='no_contacts_or_emails')
        return cleaned_data

    def save(self, commit=True):
        if self.is_valid():
            for contact in self.cleaned_data.get('contacts'):
                self.group.user_set.add(contact)
            emails = [self.cleaned_data.get('emails_{}'.format(str(i))) for i in range(5)]
            self.email_users = []
            for email in emails:
                if email != '' and email is not None:
                    try:
                        email_user = User.objects.get(email=email)
                    except ObjectDoesNotExist:
                        try:
                            email_user = User.objects.get(username=email)
                        except ObjectDoesNotExist:
                            email_user = User.objects.create_user(username=email, email=email)
                            email_user.is_active = False
                            email_user.save()
                            quits_user = QuitsUser.objects.create(user=email_user)
                    self.email_users.append(email_user)
            for email_user in self.email_users:
                self.group.user_set.add(email_user)
