# settings.py
from os import environ

# --- Defaults used by all sessions ---
SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=0.00,
    doc="",
)

# --- Sessions you can run from /admin ---
SESSION_CONFIGS = [
    dict(
        name='full_experiment',
        display_name='ECON3310: Full 6-Session Experiment',
        num_demo_participants=12,
        app_sequence=[
            'first_price_auction',
            'repeated_first_price_fixed',
            'first_price_with_chat',
            'second_price_auction',
            'repeated_second_price_fixed',
            'second_price_with_chat',
            'results_dashboard',
        ],
    ),
    # Single-app entries (handy for testing)
    dict(name='first_price_auction', num_demo_participants=4, app_sequence=['first_price_auction']),
    dict(name='repeated_first_price_fixed', num_demo_participants=4, app_sequence=['repeated_first_price_fixed']),
    dict(name='first_price_with_chat', num_demo_participants=4, app_sequence=['first_price_with_chat']),
    dict(name='second_price_auction', num_demo_participants=4, app_sequence=['second_price_auction']),
    dict(name='repeated_second_price_fixed', num_demo_participants=4, app_sequence=['repeated_second_price_fixed']),
    dict(name='second_price_with_chat', num_demo_participants=4, app_sequence=['second_price_with_chat']),
    dict(name='results_dashboard', num_demo_participants=2, app_sequence=['results_dashboard']),
]

# --- Language & currency ---
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
POINTS_CUSTOM_NAME = 'points'

# --- Rooms (optional; you can remove or edit) ---
ROOMS = [
    dict(
        name='econ3310',
        display_name='ECON 3310 Lab',
        
    ),
]

# --- Admin login ---
ADMIN_USERNAME = 'admin'
# Set OTREE_ADMIN_PASSWORD in Heroku Config Vars
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD', 'password')  # do NOT keep the default in production

# --- Security / deployment ---
SECRET_KEY = environ.get('OTREE_SECRET_KEY', 'econ3310-auction-experiment-secret')
# Read STUDY/DEMO from env so you can switch modes without code changes
OTREE_AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')  # e.g., 'STUDY' or 'DEMO'
OTREE_PRODUCTION = environ.get('OTREE_PRODUCTION', '0')  # '1' on Heroku

DEMO_PAGE_INTRO_HTML = "ECON3310 auction experiment."

# --- Installed apps (chat requires Redis and channels-redis) ---
INSTALLED_APPS = ['otree', 'otreechat']

# --- Channels / WebSocket backend ---
# Uses Heroku Redis if REDIS_URL is present; falls back to in-memory (OK for local dev).
REDIS_URL = environ.get('REDIS_URL')
if REDIS_URL:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {'hosts': [REDIS_URL]},
        }
    }
else:
    CHANNEL_LAYERS = {
        'default': {'BACKEND': 'channels.layers.InMemoryChannelLayer'}
    }

# --- Optional: participant/session field storage (not required for session.vars) ---
PARTICIPANT_FIELDS = []
SESSION_FIELDS = []
