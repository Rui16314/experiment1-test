
from otree.api import *
from .models import C, Subsession, Group, Player
import random

def _ensure_valuation(player: Player):
    # Avoid raising by using field_maybe_none rather than direct attribute access.
    if player.field_maybe_none('valuation') is None:
        val = round(random.uniform(0, 100), 2)
        player.valuation = cu(val)

class Introduction(Page):
    def vars_for_template(self):
        # don't touch valuation here
        return dict(bid_seconds=C.BID_SECONDS)

class Chat(Page):
    pass

class Bid(Page):
    timeout_seconds = C.BID_SECONDS
    form_model = 'player'
    form_fields = ['bid']

    def vars_for_template(self):
        _ensure_valuation(self.player)
        return dict(valuation=self.player.field_maybe_none('valuation'))

    def before_next_page(self, timeout_happened):
        if timeout_happened:
            self.player.bid = cu(0)

class WaitForBids(WaitPage):
    after_all_players_arrive = 'set_payoffs'

class Results(Page):
    pass

page_sequence = [Introduction, Chat, Bid, WaitForBids, Results]
