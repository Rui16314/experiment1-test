from otree.api import *; import random
class C(BaseConstants): NAME_IN_URL='first_price_with_chat'; PLAYERS_PER_GROUP=2; NUM_ROUNDS=10; BID_SECONDS=60; MAX_V=10000; MIN_V=0
class Subsession(BaseSubsession): pass
class Group(BaseGroup): price=CurrencyField(initial=0)
class Player(BasePlayer): valuation=CurrencyField(); bid=CurrencyField(min=0,max=100); opponent_bid=CurrencyField(initial=0); opponent_valuation=CurrencyField(initial=0); price_paid=CurrencyField(initial=0); won=models.BooleanField(initial=False)
def draw_valuation(): return cu(random.randint(C.MIN_V,C.MAX_V))/100
def set_bids_and_outcomes(group:Group,*,price_rule:str):
    p1,p2=group.get_players()
    for a,b in ((p1,p2),(p2,p1)):
        a.opponent_bid=b.bid; a.opponent_valuation=b.valuation
    if p1.bid>p2.bid:
        w,l=p1,p2; price = w.bid if price_rule=='first' else l.bid
        group.price=price; w.won=True; w.price_paid=price; l.won=False; l.price_paid=cu(0); w.payoff=w.valuation-price; l.payoff=cu(0)
    elif p2.bid>p1.bid:
        w,l=p2,p1; price = w.bid if price_rule=='first' else l.bid
        group.price=price; w.won=True; w.price_paid=price; l.won=False; l.price_paid=cu(0); w.payoff=w.valuation-price; l.payoff=cu(0)
    else:
        price=p1.bid; group.price=price; p1.price_paid=p2.price_paid=price; p1.payoff=(p1.valuation-price)/2; p2.payoff=(p2.valuation-price)/2
    s=group.session; rev=s.vars.get('revenue',{}); rev.setdefault(C.NAME_IN_URL,[]).append(float(group.price)); s.vars['revenue']=rev
    obs=s.vars.get('observations',[])
    for pl in group.get_players(): obs.append(dict(app=C.NAME_IN_URL,round=group.round_number,participant=pl.participant.code,valuation=float(pl.valuation),bid=float(pl.bid),opponent_bid=float(pl.opponent_bid),price=float(group.price),won=bool(pl.won)))
    s.vars['observations']=obs

def creating_session(subsession: Subsession):
    if True:
        if subsession.round_number==1: subsession.group_randomly()
        else: subsession.group_like_round(1)
    else: subsession.group_randomly()
    for p in subsession.get_players(): p.valuation=draw_valuation()
def set_payoffs(group:Group): set_bids_and_outcomes(group, price_rule='first')
