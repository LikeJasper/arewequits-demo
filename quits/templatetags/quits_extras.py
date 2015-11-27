from django import template

register = template.Library()

@register.filter
def print_thing(thing, arg=None):
    print(str(thing))
    return thing

@register.filter
def html_placeholder(field, arg=""):
    field.field.widget.attrs.update({
        "placeholder": arg
        })
    return field

@register.filter
def html_class(field, arg=""):
    field.field.widget.attrs.update({
        "class": arg
        })
    return field

@register.filter
def minlength(field, arg="8"):
    field.field.widget.attrs.update({
        "minlength": arg
        })
    return field

@register.filter
def blur(field):
    field.field.widget.attrs.update({
        "autofocus": False
        })
    return field

ERROR_MESSAGE_MAP = (
    # General
    ("This field is required.",
        "This field is required."),
    ("Enter a valid email address.",
        "Try that email address again."),
    # Signup
    ("A user is already registered with this e-mail address.",
        "A user already exists with this email address. Did you mean to log in instead?"),
    ("Password must be a minimum of 8 characters.",
        "Password must be at least 8 characters."),
    # Login
    ("The e-mail address and/or password you specified are not correct.",
        "The email address and password didn't match. Did you mean to sign up instead?"),
    ("The login and/or password you specified are not correct.",
        "The email address and password didn't match. Did you mean to sign up instead?"),
    # Reset password
    ("The e-mail address is not assigned to any user account",
        "That email address doesn't belong to any AreWeQuits? account."),
    ("You must type the same password each time.",
        "Those passwords need to match."),
    ("",
        "Try that one again."),
    # Edit profile
    ("This e-mail address is already associated with this account.",
        "This email address is already used by this account."),
    ("This e-mail address is already associated with another account.",
        "This email address is already used by another account."),
)

@register.filter
def customise_error_message(error_list):
    for i in range(len(error_list)):
        for m in ERROR_MESSAGE_MAP:
            if error_list[i] == m[0]:
                error_list[i] = m[1]
    return error_list

@register.filter
def customise_who_for_error_message(error_list):
    for i in range(len(error_list)):
        if error_list[i] == "This field is required.":
            error_list[i] = "You must select at least one person."
    return error_list
