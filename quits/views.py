from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from allauth.account.decorators import verified_email_required
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist

from quits.models import Group, Payment, Edit
from quits.forms import (NewPaymentForm, GroupForm, QuitsGroupForm, AddMembersForm,
    DeletePaymentForm, RestorePaymentForm, EditGroupForm, EditQuitsGroupForm)
from allauth.account.forms import LoginForm, SignupForm

from django.core.mail import send_mail
from quits.templates.quits.emails import invitation_email

def confirm_user_in_group(user, group_id):
    try:
        return Group.objects.filter(user=user).get(id=group_id)
    except ObjectDoesNotExist:
        pass
    return False

def send_invitations(request, user, emails):
    signup_url = request.build_absolute_uri(reverse('account_signup'))
    for email in emails:
        send_mail(
            subject=invitation_email.subject(user),
            message=invitation_email.message(user, signup_url),
            from_email=invitation_email.FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
            )

def home(request):
    context = {}
    if request.user:
        u = request.user
        if u.is_authenticated():
            if request.method == 'GET':
                source = request.GET.get('source')
                if source == 'login':
                    count = u.groups.count()
                    if count == 1:
                        group_id = u.groups.first().id
                        return redirect('view_group', group_id)
                elif source == 'email_confirmed':
                    context['msg'] = 'Email address confirmed!'

            group_balances = []
            for group in u.groups.filter(quitsgroup__is_active=True):
                group_balance = u.quitsuser.get_group_total(group)
                group_balances.append((group, group_balance, group.quitsgroup.currency))
            context['group_balances'] = group_balances
        else:
            context['signup_form'] = SignupForm()
            context['login_form'] = LoginForm()
    return render(request, 'quits/home.html', context)

def about(request):
    return render(request, 'quits/about.html')

# @verified_email_required
@login_required
def new_group(request):
    group_form = None
    quits_group_form = None
    user = request.user
    
    if request.method == 'POST':
        members = [id_ for id_ in request.POST.getlist('contacts')]
        group_data = {
            'name': request.POST['name'],
            'contacts': members,
        }
        emails = []
        for i in range(5):
            key = 'emails_{}'.format(str(i))
            try:
                group_data[key] = request.POST[key]
                emails.append(request.POST[key])
            except:
                pass
        group_form = GroupForm(owner=user, data=group_data)
        if group_form.is_valid() and request.POST.get('currency'):
            group = group_form.save()
            quits_group_data = {
                'currency': request.POST['currency'],
                'group': group.id,
            }
            quits_group_form = QuitsGroupForm(
                owner=user, data=quits_group_data)
            if quits_group_form.is_valid():
                quits_group_form.save()

                emails = [user.email for user in group.user_set.exclude(is_active=True)]
                send_invitations(request=request, user=user, emails=emails)
                
                return redirect('view_group', group.id)

    if not group_form:
        group_form = GroupForm(owner=user)
    if not quits_group_form:
        quits_group_form = QuitsGroupForm(owner=request.user)

    context = {
        'group_form': group_form,
        'quits_group_form': quits_group_form,
    }
    return render(request, 'quits/new_group.html', context)

@login_required
def view_group(request, group_id):
    group = confirm_user_in_group(request.user, group_id)
    if not group:
        raise Http404

    member_balances = []
    for member in group.user_set.all():
        entry = {
            'member': member,
            'group_total': member.quitsuser.get_group_total(group=group)
        }
        member_balances.append(entry)

    payments = Payment.objects.filter(group=group).filter(is_active=True)

    context = {
        'group': group,
        'member_balances': member_balances,
        'payments': payments
    }
    return render(request, 'quits/view_group.html', context)

# @verified_email_required
@login_required
def edit_group(request, group_id):
    group = confirm_user_in_group(request.user, group_id)
    if not group:
        raise Http404

    if request.method == 'POST':
        group_form = EditGroupForm(instance=group, data=request.POST)
        if group_form.is_valid():
            group_form.save()
            Edit.objects.create(
                group=group,
                user=request.user,
                change='name'
                )

        quits_group_form = EditQuitsGroupForm(
            instance=group.quitsgroup, data=request.POST)
        if quits_group_form.is_valid():
            quits_group_form.save()
            Edit.objects.create(
                group=group,
                user=request.user,
                change='curren'
                )

        return redirect('view_group', group_id)

    context = {
        'group_id': group_id,
        'group_form': EditGroupForm(instance=group),
        'quits_group_form': EditQuitsGroupForm(instance=group.quitsgroup),
        'add_members_form': AddMembersForm(group_id=group_id, user=request.user)
    }
    return render(request, 'quits/edit_group.html', context)

# @verified_email_required
@login_required
def add_members(request, group_id):
    group = confirm_user_in_group(request.user, group_id)
    if not group:
        raise Http404
    form = None
    user = request.user

    if request.method == 'POST':
        form = AddMembersForm(group_id=group_id, user=user, data=request.POST)
        if form.is_valid():
            form.save()
            members = [c for c in form.cleaned_data.get('contacts')]
            members += form.email_users
            for member in members:
                Edit.objects.create(
                    group=group,
                    user=user,
                    change='addmem',
                    added_member=member,
                    )
            send_invitations(request=request, user=user,
                emails=[user.email for user in form.email_users])
            return redirect('view_group', group_id)

    if not form:
        form = AddMembersForm(group_id=group_id, user=user)
    context = {
        'group_name': group.name,
        'group_id': group_id,
        'form': form,
    }
    return render(request, 'quits/add_members.html', context)

# @verified_email_required
@login_required
def delete_group(request, group_id):
    group = confirm_user_in_group(request.user, group_id)
    if not group:
        raise Http404

    if request.method == 'POST':
        quits_group = group.quitsgroup
        quits_group.is_active = False
        quits_group.save(update_fields=['is_active'])
        return redirect('home')

    raise Http404

# @verified_email_required
@login_required
def new_payment(request, group_id):
    group = confirm_user_in_group(request.user, group_id)
    if not group:
        raise Http404
    form = None

    if request.method == 'POST':
        who_for = []
        if request.POST.get('who_for'):
            who_for = [user_id for user_id in request.POST.getlist('who_for')]
        try:
            date = datetime.strptime(request.POST.get('date'), '%d %B, %Y')
        except ValueError:
            date = datetime.today()
        form = NewPaymentForm(group_id=group_id, data={
            'icon': request.POST.get('icon'),
            'date': date,
            'amount': request.POST.get('amount'),
            'description': request.POST.get('description'),
            'who_paid': request.POST.get('who_paid'),
            'who_for': who_for
        })
        if form.is_valid():
            payment = form.save()
            Edit.objects.create(
                group=group,
                user=request.user,
                payment=payment,
                change='create'
                )
            return redirect('view_group', group_id)
    if not form:
        form = NewPaymentForm(group_id=group_id, initial={
            'who_paid': request.user,
            'who_for': group.user_set.all(),
        })

    context = {'group_id': group_id,
        'form': form}
    return render(request, 'quits/new_payment.html', context)

# @verified_email_required
@login_required
def edit_payment(request, group_id, payment_id):
    group = confirm_user_in_group(request.user, group_id)
    if not group:
        raise Http404

    try:
        payment = Payment.objects.get(id=payment_id)
    except ObjectDoesNotExist:
        raise Http404
    form = None
    if request.method == 'POST':
        who_for = []
        if request.POST.get('who_for'):
            who_for = [user_id for user_id in request.POST.getlist('who_for')]
        form = NewPaymentForm(group_id=group_id, instance=payment, data={
            'icon': request.POST.get('icon'),
            'date': datetime.strptime(
                request.POST.get('date'), '%d %B, %Y'),
            'amount': request.POST.get('amount'),
            'description': request.POST.get('description'),
            'who_paid': request.POST.get('who_paid'),
            'who_for': who_for
        })
        if form.is_valid():
            payment = form.save()
            Edit.objects.create(
                group=group,
                user=request.user,
                payment=payment,
                change='edit'
                )
            return redirect('view_group', group_id)

    if not form:
        form = NewPaymentForm(group_id=group_id, instance=payment)
    delete_form = DeletePaymentForm(group_id=group_id, initial={'payment': payment})
    restore_form = RestorePaymentForm(group_id=group_id, initial={'payment': payment})

    context = {
        'group_id': group_id,
        'form': form,
        'delete_form': delete_form,
        'restore_form': restore_form,
        'active': payment.is_active
    }
    return render(request, 'quits/edit_payment.html', context)

# @verified_email_required
@login_required
def delete_payment(request, group_id):
    if request.method == 'POST':
        try:
            group = Group.objects.filter(user=request.user).get(id=group_id)
        except ObjectDoesNotExist:
            raise Http404

        form = DeletePaymentForm(group_id=group_id, data=request.POST)
        if form.is_valid():
            payment = form.save()
            Edit.objects.create(
                group=group,
                user=request.user,
                payment=payment,
                change='delete'
            )
            return redirect('view_group', group_id)

    raise Http404

@login_required
def restore_payment(request, group_id):
    if request.method == 'POST':
        try:
            group = Group.objects.filter(user=request.user).get(id=group_id)
        except ObjectDoesNotExist:
            raise Http404
        form = RestorePaymentForm(group_id=group_id, data=request.POST)
        if form.is_valid():
            payment = form.save()
            Edit.objects.create(
                group=group,
                user=request.user,
                payment=payment,
                change='restor'
            )
            return redirect('view_group', group_id)
    raise Http404

# @verified_email_required
@login_required
def activity_log(request, group_id):
    try:
        Group.objects.filter(user=request.user).get(id=group_id)
    except ObjectDoesNotExist:
        raise Http404

    group = Group.objects.get(id=group_id)
    quits_group = group.quitsgroup
    edits = Edit.objects.filter(group=group)
    context = {'group': group, 'quits_group': quits_group, 'edits': edits}
    return render(request, 'quits/activity_log.html', context)

def home_files(request, filename):
    return render(request, filename, {}, content_type="text/plain")
