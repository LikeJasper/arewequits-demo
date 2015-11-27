from datetime import date, timedelta

FIXTURES_PATH = 'arewequits/fixtures/'

URL_SUFFIXES = {
    'home': '/',
    'landing': '/',
    'my groups': '/',
    'new group': '/groups/new/',
    'view group': '/groups/1/view_group/',
    'edit group': '/groups/1/edit_group/',
    'add members': '/groups/1/add_members/',
    'add payment': '/groups/1/new_payment/',
    'edit payment': '/groups/1/payments/8/edit/',
    'activity log': '/groups/1/activity_log/',
    'account details': '/users/profile/',
    'edit details': '/users/profile/edit/',
    'about': '/about/',
    'signup': '/users/new/',
    'login': '/users/login/',
    'logout': '/users/logout',
    'confirm email': '/users/confirm-email/',
    'email confirmed': '/users/confirm-email/',
    'robots': '/robots.txt',
    'humans': '/humans.txt',
}

IDENTIFIERS = {
    'landing': "Keep track - Stick to your budget - Stay friendly",
    'my groups': "My groups</h2>",
    'new group': "Create a new group</h2>",
    'view group': "Activity log",
    'edit group': "Edit group</h2>",
    'add members': ">Add members to",
    'add payment': "Add a new payment</h2>",
    'edit payment': "Edit existing payment</h2>",
    'activity log': "created the group",
    'account details': "Account details</h2>",
    'edit details': "Edit your details</h2>",
    'about': "How does it work?",
    'signup': "Sign up</h2>",
    'login': "Log in</h2>",
    'logout': "Log out</h2>",
    'confirm email': "Just one more thing...</h2>",
    'email confirmed': "Email address confirmed!</h1>",
    'robots': 'www.robotstxt.org',
    'humans': 'humanstxt.org/',
}

INPUT_IDS = {
    'first name': 'id_first_name',
    'last name': 'id_last_name',
    'email': 'id_email',
    'login': 'id_login',
    'password': 'id_password',
    'password1': 'id_password1',
    'group name': 'input_group_name',
    'member email': 'input_emails_0',
    'edited group name': 'id_name',
    'amount': 'input_amount',
    'description': 'input_description',
}

ELEMENT_IDS = {
    'Sign up button': 'cta_sign_up_button',
    'Log in button': 'cta_log_in_button',
    'Create new group button': 'create_new_group_button',
    'menu icon': 'menu',
    'Log out': 'logout',
    'about page link': 'footer_about_page',
    'contact link': 'footer_contact_page',
    'tos link': 'footer_tos',
    'add members tab': 'id_add_members_tab',
    'delete tab': 'id_delete_group_tab',
    'enable delete button switch': 'id_enable_delete',
    'delete button': 'input_delete',
    'Add new payment button': 'create_new_payment_button',
    'activity log button': 'id_activity_log',
    'group summary table': 'overview_table',
    'members summary table': 'members_table',
    'help button': 'id_help_button',
    'restore payment button': 'input_restore',
}

PERSONAL_DATA = {
    'first name': "Amy",
    'last name': "Beech",
    'email': "amy@beech.com",
    'login': "amy@beech.com",
    'password': "password123",
    'password1': "password123",
}

EDITED_PERSONAL_DATA = {
    'first name': "Avery",
    'last name': "Beecham",
    'email': "avery@beecham.com",
}

GROUP_DATA = {
    'group name': 'New group',
    'currency': '£',
    'contact': 'Monica Geller',
    'member email': 'new@person.com',
}

EDITED_GROUP_DATA = {
    'edited group name': 'Edited group name',
    'currency': '$',
}

PAYMENT_DATA = {
    'icon': '>shopping_cart</i>',
    'amount': '24.00',
    'description': 'Test payment',
    'date': '{dt:%-d} {dt:%b} {dt:%Y}'.format(dt=date.today()),
    'payer': 'Amy Beech',
    'receivers': ['Amy Beech', 'Monica Geller', 'Ross Geller']
}

EDITED_PAYMENT_DATA = {
    'icon': '>cake</i>',
    'amount': '32.57',
    'description': 'Edited payment',
    'date': '{dt:%-d} {dt:%b} {dt:%Y}'.format(dt=date.today() - timedelta(days=1)),
    'payer': 'Monica Geller',
    'receivers': ['Amy Beech', 'Monica Geller']
}

LOG_ENTRIES = {
    "the group was created": "created the group",
    "the payment was created": "created a payment",
    "the payment was edited": "edited a payment",
    "the payment was deleted": "deleted a payment",
    "the payment was restored": "restored a payment",
    "the user was added to the group": "to the group",
}

DATA_SETS = {
    'Signup': PERSONAL_DATA,
    "Login": PERSONAL_DATA,
    "Edit details": EDITED_PERSONAL_DATA,
    "Create group": GROUP_DATA,
    "My groups": GROUP_DATA,
    "Edit group": EDITED_GROUP_DATA,
    "Create payment": PAYMENT_DATA,
    "Edit payment": EDITED_PAYMENT_DATA,
    "Group summary": PAYMENT_DATA,
}
