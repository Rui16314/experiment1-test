
from otree.api import *

class C(BaseConstants):
    NAME_IN_URL = 'first_price_auction'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 10
    BID_SECONDS = 60

class Subsession(BaseSubsession):
    def creating_session(self):
        if False:
            if self.round_number == 1:
                self.group_randomly()
            else:
                self.group_like_round(1)
        else:
            self.group_randomly()
        import random
        for p in self.get_players():
            p.valuation = cu(round(random.uniform(0, 100), 2))

class Group(BaseGroup):
    def set_payoffs(self):
        players = self.get_players()
        if len(players) < 2:
            for p in players:
                if p.field_maybe_none('bid') is None:
                    p.bid = cu(0)
                p.opponent_bid = cu(0)
                p.price_paid = cu(0)
                p.won = False
                p.payoff = cu(0)
            return

        p1, p2 = players
        b1 = p1.field_maybe_none('bid') or cu(0)
        b2 = p2.field_maybe_none('bid') or cu(0)

        p1.opponent_bid = b2
        p2.opponent_bid = b1

        if b1 > b2:
            winner, loser = p1, p2
            winner_bid, loser_bid = b1, b2
        elif b2 > b1:
            winner, loser = p2, p1
            winner_bid, loser_bid = b2, b1
        else:
            tie_price = b1
            p1.won = False; p2.won = False
            p1.price_paid = cu(0); p2.price_paid = cu(0)
            p1.payoff = max(cu(0), (p1.valuation - tie_price) / 2)
            p2.payoff = max(cu(0), (p2.valuation - tie_price) / 2)
            return

        winner.won = True
        loser.won = False

        price = winner_bid if 'first' == 'first' else loser_bid

        winner.price_paid = price
        loser.price_paid = cu(0)

        winner.payoff = max(cu(0), winner.valuation - price)
        loser.payoff = cu(0)

class Player(BasePlayer):
    valuation = CurrencyField(initial=0)
    bid = CurrencyField(min=0, initial=0)
    opponent_bid = CurrencyField(initial=0)
    price_paid = CurrencyField(initial=0)
    won = BooleanField(initial=False)
