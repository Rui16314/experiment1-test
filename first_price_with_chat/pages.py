from otree.api import *
from .models import C,Subsession,Group,Player
class Introduction(Page):
    @staticmethod
    def vars_for_template(p): return dict(bid_seconds=C.BID_SECONDS)
class Bid(Page): timeout_seconds=C.BID_SECONDS; form_model='player'; form_fields=['bid']
    
    @staticmethod
    def vars_for_template(p): return dict(valuation=p.valuation)
    
    @staticmethod
    def before_next_page(p,timeout_happened):
        if timeout_happened: p.bid=cu(0)
class WaitForBids(WaitPage): after_all_players_arrive='set_payoffs'
class Results(Page): pass
page_sequence=[Introduction, Bid, WaitForBids, Results]
