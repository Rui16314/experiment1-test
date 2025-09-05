# ECON 3310 Auction Experiments (oTree)

Six configured sessions (10 rounds each):

1. First‑price, random opponent
2. First‑price, fixed opponent
3. First‑price, fixed opponent with chat
4. Second‑price, random opponent
5. Second‑price, fixed opponent
6. Second‑price, fixed opponent with chat

- Uses the instructor’s **General Instructions** verbatim on the site.
- Visualizations appear after each session, plus an all‑sessions dashboard.
- Default bids on timeout: first‑price → v/2; second‑price → v. If this default is highest, both players earn zero per the spec.
- Valuations drawn uniformly from 0–100 with cent increments.
- For now, launch sessions with an **even** number of participants.

## Local
```bash
pip install -r requirements.txt
otree devserver
```
## Heroku
1) Create app + Postgres. 2) Set `OTREE_ADMIN_PASSWORD` and `OTREE_PRODUCTION=1`. 3) Deploy the repo. 4) Scale `web=1`.


## All-sessions dashboard (5–8)
- After running the six sessions (Exp1–Exp6), create a new session for **Dashboard: All Sessions (5–8)**.
- Join once as a participant; the page aggregates the **most recent** run of each of the six configs.
- It renders: (5) six avg-bid-vs-valuation charts, (6) six avg-revenue-by-round charts, (7) bars of overall avg revenue, (8) pooled scatter & over/under/equal share.
