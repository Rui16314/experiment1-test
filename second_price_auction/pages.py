
from otree.api import *
from .models import C, Subsession, Group, Player
import random

def _ensure_valuation(player: Player):
    if player.valuation is None:
        player.valuation = cu(random.randint(0, 10000)) / 100

class Introduction(Page):
    def vars_for_template(self):
        return dict(bid_seconds=C.BID_SECONDS)

class Bid(Page):
    timeout_seconds = C.BID_SECONDS
    form_model = 'player'
    form_fields = ['bid']

    def vars_for_template(self):
        _ensure_valuation(self.player)
        return dict(valuation=self.player.valuation)

    def before_next_page(self, timeout_happened):
        if timeout_happened:
            self.player.bid = cu(0)

class WaitForBids(WaitPage):
    after_all_players_arrive = 'set_payoffs'

class Results(Page):
    pass

page_sequence = [Introduction, Bid, WaitForBids, Results]
    