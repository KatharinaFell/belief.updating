from os import environ
SESSION_CONFIG_DEFAULTS = dict(participation_fee=0.0, real_world_currency_per_point=None)
SESSION_CONFIGS = [dict(name='belief_updating_session', num_demo_participants=6, app_sequence=['belief_updating', 'estimation_tasks'], monitor_participant_fields=['main_estimate', 'filler_estimate', 'main_justification', 'filler_justification'])]
LANGUAGE_CODE = 'en'
DEMO_PAGE_INTRO_HTML = ''
THOUSAND_SEPARATOR = ''
CURRENCY_UNIT = 'units.EUR'
ENABLE_ADMIN_CHAT = False
ROOMS = [dict(name='Test', display_name='Test')]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = environ.get('OTREE_SECRET_KEY', 'blahblahblah')

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']


