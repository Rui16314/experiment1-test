from os import environ
SESSION_CONFIGS=[dict(name='full_experiment',display_name='ECON3310',num_demo_participants=12,app_sequence=['first_price_auction','repeated_first_price_fixed','first_price_with_chat','second_price_auction','repeated_second_price_fixed','second_price_with_chat','results_dashboard'])]
REAL_WORLD_CURRENCY_CODE='USD'
USE_POINTS=True
POINTS_CUSTOM_NAME='points'
ROOMS=[]
ADMIN_USERNAME='admin'
ADMIN_PASSWORD=environ.get('OTREE_ADMIN_PASSWORD')
DEMO_PAGE_INTRO_HTML='ECON3310 auctions.'
SECRET_KEY='econ3310-auction-experiment-secret'
INSTALLED_APPS=['otree','otreechat']
LANGUAGE_CODE = 'en'
