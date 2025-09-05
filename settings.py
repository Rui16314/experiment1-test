
import os

SESSION_CONFIGS = [
    dict(
        name='all_in_one',
        display_name='All-in-One: 6 Sessions (60 rounds)',
        app_sequence=['auction_all'],
        num_demo_participants=2,
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=0.00,
    doc="",
)

LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
POINTS_CUSTOM_NAME = 'POINTS'

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = os.environ.get('OTREE_ADMIN_PASSWORD', 'admin')

DEMO_PAGE_INTRO_HTML = """
<h3>ECON 3310 Auction Experiments</h3>
<p>Click "Create session" in the Admin to launch the 6-in-1 game.</p>
"""

SECRET_KEY = os.environ.get('OTREE_SECRET_KEY', 'dev-secret')

INSTALLED_APPS = ['otree']

OTREE_PRODUCTION = os.environ.get('OTREE_PRODUCTION', '') == '1'
DEBUG = not OTREE_PRODUCTION

AUTH_LEVEL = os.environ.get('OTREE_AUTH_LEVEL', 'STUDY')
