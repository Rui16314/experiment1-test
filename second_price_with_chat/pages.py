from otree.api import *
from .models import C, Subsession, Group, Player
import random

def _ensure_valuation(player: Player):
    if player.field_maybe_none('valuation') is None:
        val = round(random.uniform(0, 100), 2)
        player.valuation = cu(val)

class Introduction(Page):
    def vars_for_template(self):
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

    def before_next_page(self, timeout_happened=False, **kwargs):
        timeout = (timeout_happened or getattr(self, 'timeout_happened', False) or kwargs.get('timeout_happened', False))
        if timeout and self.player.field_maybe_none('bid') is None:
            self.player.bid = cu(0)

class WaitForBids(WaitPage):
    after_all_players_arrive = 'set_payoffs'

class Results(Page):
    pass

page_sequence = [Introduction, Chat, Bid, WaitForBids, Results]
