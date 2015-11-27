from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from allauth.account.utils import perform_login

from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from allauth.account.views import signup as allauth_signup
from allauth.account.forms import SetPasswordForm as AllauthSetPasswordForm, AddEmailForm
from quits_users.forms import EditProfileForm

def authenticate_and_login(request, user=None):
    user = authenticate(email=user.email, password=request.POST['password1'])
    if user is not None:
        if user.is_active:
            login(request, user)
            return True
    return False

def valid_email(email):
    if len(email) > 2:
        return '@' in email and email[0] != '@' and email[-1] != '@'
    return False

def signup(request):
    request.session['inactive_user'] = False
    if request.user.is_authenticated():
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password1')
        terms_agree = request.POST.get('terms_agree')

        user = None
        if valid_email(email):
            user = User.objects.filter(email=email).first()
        if user:
            if not user.is_active:
                request.session['inactive_user'] = True
                if password and first_name and last_name and terms_agree:
                    data = {
                        'password1': password,
                        'password2': password,
                    }
                    form = AllauthSetPasswordForm(user=user, data=data)
                    if form.is_valid():
                        form.save()
                        user.first_name = first_name
                        user.last_name = last_name
                        user.is_active = True
                        user.save(update_fields=['is_active', 'first_name', 'last_name'])

                        return perform_login(request, user, email_verification='mandatory')
    return allauth_signup(request)

@login_required
def view_profile(request):
    return render(request, 'quits_users/profile.html')

@login_required
def edit_profile(request):
    profile_form = None
    email_form = None
    user = request.user
    if request.method == 'POST':
        post_email = request.POST.get('email')
        profile_form = EditProfileForm(instance=user, data=request.POST)
        if post_email != user.email:
            email_form = AddEmailForm(user=user, data=request.POST)
        if profile_form.is_valid() and (not email_form or email_form.is_valid()):
            profile_form.save()
            if email_form:
                email_form.save(request=request)
                return redirect('account_email_verification_sent')
            return redirect('view_profile')

    if not profile_form:
        profile_form = EditProfileForm(instance=user)
    if not email_form:
        email_form = AddEmailForm(user=user, initial={'email': user.email})
    context = {'edit_profile_form': profile_form, 'add_email_form': email_form}
    return render(request, 'quits_users/edit_profile.html', context)
