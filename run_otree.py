# run_otree.py
import os, os, sys

port = os.environ.get("PORT", "8000")

# Run the real oTree CLI and REPLACE the current process,
# so Heroku sees a long-running web process.
cmd = ["otree", "prodserver", "1", f"0.0.0.0:{port}"]

print("Starting:", " ".join(cmd), flush=True)
os.execvp("otree", ["otree", "prodserver"])

