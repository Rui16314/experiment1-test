from otree.api import *

class C(BaseConstants):
    NAME_IN_URL = 'second_price_auction'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 10
    BID_SECONDS = 60


class Subsession(BaseSubsession):
    def creating_session(self):
        # Grouping
        if False:
            if self.round_number == 1:
                self.group_randomly()
            else:
                self.group_like_round(1)
        else:
            # reshuffle every round
            self.group_randomly()

        # Assign valuations independently each round, uniform on [0,100] with 2 decimals
        import random
        for p in self.get_players():
            val = round(random.uniform(0, 100), 2)
            p.valuation = cu(val)


class Group(BaseGroup):
    def set_payoffs(self):
        # Two-player comparison
        p1, p2 = self.get_players()

        # Use 0 as default if a bid is missing due to timeout
        b1 = p1.field_maybe_none('bid') or cu(0)
        b2 = p2.field_maybe_none('bid') or cu(0)

        # record opponent bids
        p1.opponent_bid = b2
        p2.opponent_bid = b1

        # Determine winner/price/payoffs according to second-price rule (pays opponent's bid)
        if b1 > b2:
            # Player 1 wins
            winner, loser = p1, p2
            winner_bid, loser_bid = b1, b2
        elif b2 > b1:
            winner, loser = p2, p1
            winner_bid, loser_bid = b2, b1
        else:
            # Tie: each gets expected payoff of 0.5*(valuation - price)
            # Winner is not selected; both 'won' False, price 0 for display.
            p1.won = False
            p2.won = False
            tie_price = b1  # equal
            if 'second' == 'first':
                p1.payoff = max(cu(0), (p1.valuation - tie_price) / 2)
                p2.payoff = max(cu(0), (p2.valuation - tie_price) / 2)
            else:
                # second-price: price is opponent's bid (same in tie)
                p1.payoff = max(cu(0), (p1.valuation - tie_price) / 2)
                p2.payoff = max(cu(0), (p2.valuation - tie_price) / 2)
            p1.price_paid = cu(0)
            p2.price_paid = cu(0)
            return

        # Non-tie cases
        winner.won = True
        loser.won = False

        if 'second' == 'first':
            price = winner_bid
        else:
            price = loser_bid

        winner.price_paid = price
        loser.price_paid = cu(0)

        # Payoffs cannot be negative
        winner.payoff = max(cu(0), winner.valuation - price)
        loser.payoff = cu(0)


class Player(BasePlayer):
    valuation = CurrencyField(initial=0)
    bid = CurrencyField(min=0, initial=0)
    opponent_bid = CurrencyField(initial=0)
    price_paid = CurrencyField(initial=0)
    won = BooleanField(initial=False)