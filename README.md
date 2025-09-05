
# All-in-One oTree Auction (6 sessions)

**App:** `auction_all` — plays 6 sessions (10 rounds each) in a single link.

## Heroku Config Vars
- `OTREE_SECRET_KEY` — a long random string
- `OTREE_ADMIN_PASSWORD` — your admin password
- `OTREE_PRODUCTION=1`
- Attach **Heroku Postgres** (sets `DATABASE_URL`)
- Attach **Heroku Redis** (sets `REDIS_URL`) for chat/live

## Run locally
```
pip install -r requirements.txt
otree devserver
```

## Deploy
Push to Heroku and deploy. In the Admin, create a session for **all_in_one**.
