
from os import environ
from otree.api import Currency as cu

SESSION_CONFIGS = [
    dict(name='first_price_auction', app_sequence=['first_price_auction'], num_demo_participants=2),
    dict(name='repeated_first_price_fixed', app_sequence=['repeated_first_price_fixed'], num_demo_participants=2),
    dict(name='first_price_with_chat', app_sequence=['first_price_with_chat'], num_demo_participants=2),
    dict(name='second_price_auction', app_sequence=['second_price_auction'], num_demo_participants=2),
    dict(name='repeated_second_price_fixed', app_sequence=['repeated_second_price_fixed'], num_demo_participants=2),
    dict(name='second_price_with_chat', app_sequence=['second_price_with_chat'], num_demo_participants=2),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.0,
    participation_fee=0.0,
    doc="",
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = "<h3>ECON 3310 Auction Experiment</h3>"
SECRET_KEY = environ.get('OTREE_SECRET_KEY', 'dev-secret')

ROOMS = []

INSTALLED_APPS = ['otree']
