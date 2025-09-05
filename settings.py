
from os import environ

SESSION_CONFIGS = [

    dict(
        name="dashboard_all", display_name="Dashboard: All Sessions (5–8)",
        num_demo_participants=1, app_sequence=["dashboard"],
    ),

    dict(
        name="fp_random", display_name="Exp 1: First-Price (Random Opponent)",
        num_demo_participants=2, app_sequence=["auction"],
        auction_format="first", partner="random", chat_enabled=False,
    ),
    dict(
        name="fp_fixed", display_name="Exp 2: First-Price (Fixed Opponent)",
        num_demo_participants=2, app_sequence=["auction"],
        auction_format="first", partner="fixed", chat_enabled=False,
    ),
    dict(
        name="fp_comm", display_name="Exp 3: First-Price (Fixed Opponent with Chat)",
        num_demo_participants=2, app_sequence=["auction"],
        auction_format="first", partner="fixed", chat_enabled=True,
    ),
    dict(
        name="sp_random", display_name="Exp 4: Second-Price (Random Opponent)",
        num_demo_participants=2, app_sequence=["auction"],
        auction_format="second", partner="random", chat_enabled=False,
    ),
    dict(
        name="sp_fixed", display_name="Exp 5: Second-Price (Fixed Opponent)",
        num_demo_participants=2, app_sequence=["auction"],
        auction_format="second", partner="fixed", chat_enabled=False,
    ),
    dict(
        name="sp_comm", display_name="Exp 6: Second-Price (Fixed Opponent with Chat)",
        num_demo_participants=2, app_sequence=["auction"],
        auction_format="second", partner="fixed", chat_enabled=True,
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.0,
    participation_fee=0.0,
    doc="",
    rounds_per_session=10,
)

PARTICIPANT_FIELDS = ["chat_log"]
SESSION_FIELDS = []

LANGUAGE_CODE = "en"
REAL_WORLD_CURRENCY_CODE = "USD"
USE_POINTS = True
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = environ.get("OTREE_ADMIN_PASSWORD", "admin")

DEMO_PAGE_INTRO_HTML = """
<p>ECON 3310 Auction Experiments</p>
"""

SECRET_KEY = environ.get("OTREE_SECRET_KEY", "CCYuBmuit2mkU6DtmlLR6ku1sSCSHnUweJYsRy751mQ")
