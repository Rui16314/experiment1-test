
from otree.api import *
import random
from decimal import Decimal

PHASES = [
    dict(key="fp_random",  label="Exp1: First-Price (Random)",  auction_format="first",  partner="random", chat=False),
    dict(key="fp_fixed",   label="Exp2: First-Price (Fixed)",   auction_format="first",  partner="fixed",  chat=False),
    dict(key="fp_comm",    label="Exp3: First-Price (Fixed + Chat)", auction_format="first",  partner="fixed",  chat=True),
    dict(key="sp_random",  label="Exp4: Second-Price (Random)", auction_format="second", partner="random", chat=False),
    dict(key="sp_fixed",   label="Exp5: Second-Price (Fixed)",  auction_format="second", partner="fixed",  chat=False),
    dict(key="sp_comm",    label="Exp6: Second-Price (Fixed + Chat)", auction_format="second", partner="fixed",  chat=True),
]
PHASE_SIZE = 10
TOTAL_ROUNDS = PHASE_SIZE * len(PHASES)

class C(BaseConstants):
    NAME_IN_URL = "auction_all"
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = TOTAL_ROUNDS

class Subsession(BaseSubsession):
    auction_format = models.StringField()
    partner = models.StringField()
    chat_enabled = models.BooleanField(initial=False)
    phase_index = models.IntegerField()

    def phase_bounds(self):
        start = self.phase_index * PHASE_SIZE + 1
        end = start + PHASE_SIZE - 1
        return start, end

    def creating_session(self):
        self.phase_index = (self.round_number - 1) // PHASE_SIZE
        phase = PHASES[self.phase_index]
        self.auction_format = phase["auction_format"]
        self.partner = phase["partner"]
        self.chat_enabled = phase["chat"]

        start, end = self.phase_bounds()
        if self.partner == "random":
            self.group_randomly()
        else:
            if self.round_number == start:
                self.group_randomly()
            else:
                self.group_like_round(start)

        for p in self.get_players():
            cents = random.randint(0, 10000)
            p.valuation = Decimal(cents) / Decimal(100)

class Group(BaseGroup):
    def set_winner_and_payoffs(self):
        p1, p2 = self.get_players()

        b1 = p1.get_effective_bid()
        b2 = p2.get_effective_bid()

        if b1 > b2:
            winner, loser = p1, p2
            price = b1 if self.subsession.auction_format == "first" else b2
        elif b2 > b1:
            winner, loser = p2, p1
            price = b2 if self.subsession.auction_format == "first" else b1
        else:
            import random as _r
            winner, loser = _r.choice([(p1,p2),(p2,p1)])
            price = b1 if self.subsession.auction_format == "first" else b2

        # highest bid came from an auto/default bid -> both zero
        def raw_bid(pl):
            try:
                return pl.bid
            except TypeError:
                return None

        auto_highest = False
        if (((raw_bid(p1) is None) or p1.timed_out) and b1 >= b2 and b1 > 0) or \
           (((raw_bid(p2) is None) or p2.timed_out) and b2 >= b1 and b2 > 0):
            auto_highest = True

        if auto_highest:
            for pl in [p1,p2]:
                pl.payoff = cu(0)
                pl.won = False
                pl.winning_price = 0
            return

        winner.won, loser.won = True, False
        winner.winning_price = Decimal(price).quantize(Decimal("0.01"))
        loser.winning_price = Decimal(price).quantize(Decimal("0.01"))
        winner.payoff = (Decimal(winner.valuation) - Decimal(price)).quantize(Decimal("0.01"))
        loser.payoff = Decimal("0.00")

class Player(BasePlayer):
    valuation = models.CurrencyField()
    bid = models.CurrencyField(min=0, max=100, blank=True)
    won = models.BooleanField(initial=False)
    winning_price = models.CurrencyField(initial=0)
    timed_out = models.BooleanField(initial=False)

    def get_effective_bid(self):
        # oTree raises TypeError if None; guard it
        try:
            b = self.bid
        except TypeError:
            b = None
        if b is not None:
            return Decimal(b)
        v = Decimal(self.valuation or 0)
        if self.subsession.auction_format == "first":
            return (v/2).quantize(Decimal("0.01"))
        else:
            return v.quantize(Decimal("0.01"))
