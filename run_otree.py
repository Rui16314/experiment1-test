# run_otree.py
import os, sys
from otree.main import execute_from_command_line

port = os.environ.get("PORT", "8000")
# Start oTree like:  otree prodserver 0.0.0.0:<PORT>
sys.argv = ["otree", "prodserver", f"0.0.0.0:{port}"]
execute_from_command_line()

