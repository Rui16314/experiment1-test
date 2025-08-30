# run_otree.py
import os

print("Starting: otree prodserver", flush=True)
# Let oTree read the Heroku $PORT internally; no extra args.
os.execvp("otree", ["otree", "prodserver"])


