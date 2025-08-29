import os, sys
from otree.cli import otree as otree_cli

port = os.environ.get("PORT", "8000")
# Equivalent to: otree prodserver 1 0.0.0.0:<PORT>
args = ["prodserver", "1", f"0.0.0.0:{port}"]
sys.argv = ["otree"] + args
otree_cli(standalone_mode=True)
