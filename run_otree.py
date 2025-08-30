# run_otree.py
import os, sys
# Classic oTree entrypoint available in all v5 releases
from otree.main import execute_from_command_line

port = os.environ.get("PORT", "8000")
# Equivalent to:  otree prodserver 1 0.0.0.0:<PORT>
sys.argv = ["otree", "prodserver", "1", f"0.0.0.0:{port}"]
execute_from_command_line()

