from django.conf import settings

def subject(user):
    return "Invitation from {} {} to join AreWeQuits?".format(user.first_name, user.last_name)

def message(user, url):
    return """
    Hi there,

    {first_name} {last_name} wants you to sort out your shared expenses together on AreWeQuits?
    
    Click here to sign up and see the group {first_name} made:
    {url}

    If you don't know {first_name}, they probably added you by mistake. You can just ignore this email.

    
    """.format(first_name=user.first_name, last_name=user.last_name, url=url)

FROM_EMAIL = settings.DEFAULT_FROM_USER
