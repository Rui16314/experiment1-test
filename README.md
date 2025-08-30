# ECON 3310 Auction Experiment (oTree 5)

This repo contains 6 auction apps (10 rounds each) and a minimal results dashboard.
It is compatible across oTree 5.x (requirements are relaxed to avoid Heroku install issues).

## Deploy on Heroku
1) Add **Heroku Redis** (needed for chat apps).
2) Config Vars:
   - `OTREE_ADMIN_PASSWORD` = your password
   - `OTREE_SECRET_KEY` = a long random string
   - (optional) `OTREE_AUTH_LEVEL` = STUDY
3) Deploy. Procfile: `web: otree prodserver 1`