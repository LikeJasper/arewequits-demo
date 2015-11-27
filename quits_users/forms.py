from django import forms
from django.core.exceptions import ObjectDoesNotExist

from quits_users.models import User, QuitsUser

EMAIL_ADDRESS_ERROR = "This field is required."
NO_CONTACTS_GIVEN = "Please enter at least one email address."

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    terms_agree = forms.BooleanField(required=True)

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

class EditProfileForm(forms.models.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

        widgets = {
            'first_name': forms.TextInput(attrs={
                'id': 'id_first_name',
                }),
            'last_name': forms.TextInput(attrs={
                'id': 'id_last_name',
                }),
        }
