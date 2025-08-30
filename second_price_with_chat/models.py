from otree.api import *
import random

class C(BaseConstants):
    NAME_IN_URL = 'second_price_with_chat'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 10
    BID_SECONDS = 60
    MAX_V = 10000
    MIN_V = 0

class Subsession(BaseSubsession): pass

class Group(BaseGroup):
    price = models.CurrencyField(initial=0)

class Player(BasePlayer):
    valuation = models.CurrencyField(doc='Your valuation (0.00–100.00)')
    bid = models.CurrencyField(min=0, max=100)
    opponent_bid = models.CurrencyField(initial=0)
    opponent_valuation = models.CurrencyField(initial=0)
    price_paid = models.CurrencyField(initial=0)
    won = models.BooleanField(initial=False)

def draw_valuation():
    n = random.randint(C.MIN_V, C.MAX_V)
    return cu(n) / 100

def creating_session(subsession: Subsession):
    if True:
        if subsession.round_number == 1:
            subsession.group_randomly()
        else:
            subsession.group_like_round(1)
    else:
        subsession.group_randomly()
    for p in subsession.get_players():
        p.valuation = draw_valuation()

def set_bids_and_outcomes(group: Group, *, price_rule: str):
    p1, p2 = group.get_players()
    p1.opponent_bid = p2.bid
    p2.opponent_bid = p1.bid
    p1.opponent_valuation = p2.valuation
    p2.opponent_valuation = p1.valuation

    if p1.bid > p2.bid:
        winner, loser = p1, p2
        price = winner.bid if price_rule == 'second' else loser.bid
        group.price = price
        winner.won = True
        winner.price_paid = price
        loser.won = False
        loser.price_paid = cu(0)
        winner.payoff = winner.valuation - price
        loser.payoff = cu(0)
    elif p2.bid > p1.bid:
        winner, loser = p2, p1
        price = winner.bid if price_rule == 'second' else loser.bid
        group.price = price
        winner.won = True
        winner.price_paid = price
        loser.won = False
        loser.price_paid = cu(0)
        winner.payoff = winner.valuation - price
        loser.payoff = cu(0)
    else:
        tie_price = p1.bid
        group.price = tie_price
        p1.price_paid = tie_price
        p2.price_paid = tie_price
        p1.payoff = (p1.valuation - tie_price) / 2
        p2.payoff = (p2.valuation - tie_price) / 2

    s = group.session
    rev = s.vars.get('revenue', {})
    lst = rev.get(C.NAME_IN_URL, [])
    lst.append(float(group.price))
    rev[C.NAME_IN_URL] = lst
    s.vars['revenue'] = rev

    obs = s.vars.get('observations', [])
    for pl in group.get_players():
        obs.append(dict(
            app=C.NAME_IN_URL,
            round=group.round_number,
            participant=pl.participant.code,
            valuation=float(pl.valuation),
            bid=float(pl.bid),
            opponent_bid=float(pl.opponent_bid),
            price=float(group.price),
            won=bool(pl.won),
        ))
    s.vars['observations'] = obs

def set_payoffs(group: Group):
    set_bids_and_outcomes(group, price_rule='second')
