
from os import environ

SESSION_CONFIGS = [
    dict(
        name="all_in_one",
        display_name="All-in-One: 6 Sessions in One Link",
        num_demo_participants=2,
        app_sequence=["auction_all"],
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.0,
    participation_fee=0.0,
    doc="",
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

LANGUAGE_CODE = "en"
REAL_WORLD_CURRENCY_CODE = "USD"
USE_POINTS = True
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = environ.get("OTREE_ADMIN_PASSWORD", "admin")
SECRET_KEY = environ.get("OTREE_SECRET_KEY", "r7y9d-4XTlWn9z1fWc5GsXMEM-bJgCRtiLlNFsS59tw")

DEMO_PAGE_INTRO_HTML = "<p>ECON 3310 Auction Experiments</p>"
