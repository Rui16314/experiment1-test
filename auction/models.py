
from otree.api import *
import random
from decimal import Decimal

class C(BaseConstants):
    NAME_IN_URL = "auction"
    PLAYERS_PER_GROUP = 2
    ROUNDS_PER_SESSION = 10

class Subsession(BaseSubsession):
    auction_format = models.StringField()
    partner = models.StringField()
    chat_enabled = models.BooleanField(initial=False)

    def creating_session(self):
        cfg = self.session.config
        self.auction_format = cfg.get("auction_format", "first")
        self.partner = cfg.get("partner", "random")
        self.chat_enabled = cfg.get("chat_enabled", False)
        if self.round_number == 1 or self.partner == "random":
            self.group_randomly()
        # assign valuations
        for p in self.get_players():
            cents = random.randint(0, 10000)
            p.valuation = Decimal(cents) / Decimal(100)

class Group(BaseGroup):
    def set_winner_and_payoffs(self):
        p1, p2 = self.get_players()
        b1 = p1.get_effective_bid()
        b2 = p2.get_effective_bid()
        # tie-break randomly
        if b1 > b2:
            winner, loser = p1, p2
            win_price = b1 if self.subsession.auction_format == "first" else b2
        elif b2 > b1:
            winner, loser = p2, p1
            win_price = b2 if self.subsession.auction_format == "first" else b1
        else:
            import random as _r
            winner, loser = _r.choice([(p1, p2), (p2, p1)])
            win_price = b1 if self.subsession.auction_format == "first" else b2

        # if any auto-bid was highest → both zero
        auto_highest = False
        if (p1.timed_out and b1 >= b2 and b1 > 0) or (p2.timed_out and b2 >= b1 and b2 > 0):
            auto_highest = True
        if auto_highest:
            for pl in [p1, p2]:
                pl.payoff = cu(0)
                pl.won = False
                pl.winning_price = 0
            return

        for pl in [p1, p2]:
            pl.won = (pl == winner)
        winner.payoff = (winner.valuation - Decimal(win_price)).quantize(Decimal("0.01"))
        loser.payoff = Decimal("0.00")
        winner.winning_price = Decimal(win_price).quantize(Decimal("0.01"))
        loser.winning_price = Decimal(win_price).quantize(Decimal("0.01"))

class Player(BasePlayer):
    valuation = models.CurrencyField()
    bid = models.CurrencyField(min=0, max=100, blank=True)
    won = models.BooleanField(initial=False)
    winning_price = models.CurrencyField(initial=0)
    timed_out = models.BooleanField(initial=False)

    def get_effective_bid(self):
        if self.bid is not None:
            return Decimal(self.bid)
        v = Decimal(self.valuation or 0)
        if self.subsession.auction_format == "first":
            return (v / 2).quantize(Decimal("0.01"))
        else:
            return v.quantize(Decimal("0.01"))
