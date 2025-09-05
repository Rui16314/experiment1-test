
from otree.api import *
from .models import C, Subsession, Group, Player
import json
from decimal import Decimal

GENERAL_INSTR = """Welcome to the ECON 3310 Experiment Platform.

This experiment has two parts. Each part includes three separate sessions. In each session, you'll complete 10 rounds. Therefore, you will play an auction game over 6 sessions, totaling 60 rounds. Each round is expected to take about 1 minute or less. Overall, the experiment should take no more than 75 minutes, including review of instructions.

Participating in this experiment will earn you 100 POINTS.

You can earn extra points in each round, and these points are mostly affected by your choices and those of your opponents. Points earned in each round and session will be added up. Therefore, each round matters, and it's important to make the most of each one.

The instructions for each session will appear on the computer screen before you start each session.
"""

SESSION_TEXT = {
"fp_random": """SESSION 1: FIRST-PRICE SEALED BID AUCTION INSTRUCTIONS

You will play 10 rounds of this game. At the start of each round, you'll be randomly paired with a different participant. This means your matches will change from round to round, and you'll never know who you'll be paired with in any given round.

The seller is auctioning an indivisible item, and two buyers—yourself and your opponent, whom we match randomly—are interested in purchasing it. In each round, you'll participate in an auction to buy the good.

In each round, your valuation and your opponent’s will be assigned randomly. Therefore, your and your opponent’s valuations will probably differ in each round. You will always know your own valuation but won’t learn your opponent’s until the round ends. Valuations are chosen independently and uniformly from 0 to 100, in increments of cents. As a result, your valuation will be 0.01n with a probability of 1/10,000, where n ranges from 0 to 10,000.

In each round, after learning your valuation, you have 1 minute to place your bid. Once you submit your bid, the round will end. You will not see your opponent’s bid until after the round ends, when you learn the winning bid and how many points you earned that round.

POINTS YOU EARN IN EACH ROUND WILL DEPEND ON THESE THREE FACTORS

Your bid
Your opponent’s bid
Your valuation 

More specifically, 

If your bid is less than your opponent’s bid, then you lose the auction and receive 0 points.

If your bid is higher than your opponent’s bid, then you win the auction. Thus, your points will be 

If your bid is equal to your opponent’s bid, then your points will be determined according to the following:

If you do not submit your bid within the 1-minute window, you lose the auction and receive 0 points.

At the end of each round, you will find out whether you win the auction, your opponent’s valuation, bid, and your points.
""",
"fp_fixed": """SESSION 2: REPEATED FIRST-PRICE SEALED BID AUCTION INSTRUCTIONS

You will play 10 rounds of the same game you played in the previous session. The only difference is that you will play all 10 rounds against the same opponent. So, your opponent will stay the same throughout the rounds.

In the experimental instructions, the bold sections highlight the only new parts compared to the previous session.

To be more specific, you'll be randomly paired with a participant at the beginning of this session and remain paired throughout 10 rounds.

In each round, your valuation and your opponent’s will be assigned randomly. Therefore, your and your opponent’s valuations will probably differ in each round. You will always know your own valuation but won’t learn your opponent’s until the round ends. Valuations are chosen independently and uniformly from 0 to 100, in increments of cents. As a result, your valuation will be 0.01n with a probability of 1/10,000, where n ranges from 0 to 10,000.

In each round, after learning your valuation, you have 1 minute to place your bid. Once you submit your bid, the round will end. You will not see your opponent’s bid until after the round ends, when you learn the winning bid and how many points you earned that round.

POINTS YOU EARN IN EACH ROUND WILL DEPEND ON THESE THREE FACTORS

Your bid
Your opponent’s bid
Your valuation 

More specifically, 

If your bid is less than your opponent’s bid, then you lose the auction and receive 0 points.

If your bid is higher than your opponent’s bid, then you win the auction. Thus, your points will be 

If your bid is equal to your opponent’s bid, then your points will be determined according to the following:

If you do not submit your bid within the 1-minute window, you lose the auction and receive 0 points.

At the end of each round, you will find out whether you win the auction, your opponent’s valuation, bid, and your points.
""",
"fp_comm": """SESSION 3: REPEATED FIRST-PRICE SEALED BID AUCTION WITH COMMUNICATION INSTRUCTIONS

You will play 10 rounds of the same game you played in the previous session. The only difference is that you will now be able to communicate with your opponent through the chatbox.

In the experimental instructions, the bold sections highlight the only new parts compared to the previous session.

To be more specific, you'll be randomly paired with a participant at the beginning of this session and remain paired throughout 10 rounds.

In each round, your valuation and your opponent’s will be assigned randomly. Therefore, your and your opponent’s valuations will probably differ in each round. You will always know your own valuation but won’t learn your opponent’s until the round ends. Valuations are chosen independently and uniformly from 0 to 100, in increments of cents. As a result, your valuation will be 0.01n with a probability of 1/10,000, where n ranges from 0 to 10,000.

In each round, after learning your valuation, you have 1 minute to place your bid. You may communicate with your opponent before submitting your bid. Feel free to discuss any matter, but please keep your identity confidential. Once you submit your bid, the round will end. You will not see your opponent’s bid until after the round ends, when you learn the winning bid and how many points you earned that round.

POINTS YOU EARN IN EACH ROUND WILL DEPEND ON THESE THREE FACTORS

Your bid
Your opponent’s bid
Your valuation 

More specifically, 

If your bid is less than your opponent’s bid, then you lose the auction and receive 0 points.

If your bid is higher than your opponent’s bid, then you win the auction. Thus, your points will be 

If your bid is equal to your opponent’s bid, then your points will be determined according to the following:

If you do not submit your bid within the 1-minute window, you lose the auction and receive 0 points.

At the end of each round, you will find out whether you win the auction, your opponent’s valuation, bid, and your points.
""",
"sp_random": """SESSION 4: SECOND-PRICE SEALED BID AUCTION INSTRUCTIONS

You will play 10 rounds of this game. At the start of each round, you'll be randomly paired with a different participant. This means your matches will change from round to round, and you'll never know who you'll be paired with in any given round.

The seller is auctioning an indivisible item, and two buyers—yourself and your opponent, whom we match randomly—are interested in purchasing it. In each round, you'll participate in an auction to buy the good.

In each round, your valuation and your opponent’s will be assigned randomly. Therefore, your and your opponent’s valuations will probably differ in each round. You will always know your own valuation but won’t learn your opponent’s until the round ends. Valuations are chosen independently and uniformly from 0 to 100, in increments of cents. As a result, your valuation will be 0.01n with a probability of 1/10,000, where n ranges from 0 to 10,000.

In each round, after learning your valuation, you have 1 minute to place your bid. Once you submit your bid, the round will end. You will not see your opponent’s bid until after the round ends, when you learn the winning bid and how many points you earned that round.

[Second-price format: the highest bidder wins and pays the second-highest bid.]
""",
"sp_fixed": """SESSION 5: REPEATED SECOND-PRICE SEALED BID AUCTION INSTRUCTIONS

You will play 10 rounds of the same game you played in the previous session. The only difference is that you will play all 10 rounds against the same opponent. So, your opponent will stay the same throughout the rounds.

[Second-price format as above.]
""",
"sp_comm": """SESSION 6: REPEATED SECOND-PRICE SEALED BID AUCTION WITH COMMUNICATION INSTRUCTIONS

You will play 10 rounds of the same game you played in the previous session. The only difference is that you will now be able to communicate with your opponent through the chatbox.

[Second-price format as above.]
""",
}

class Intro(Page):
    def is_displayed(player):
        return player.round_number == 1

    def vars_for_template(player):
        session_key = player.session.config["name"]
        return dict(
            session_instructions=SESSION_TEXT.get(session_key, ""),
            session_name=session_key
        )

class Chat(Page):
    live_method = "live_chat"
    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.chat_enabled
    @staticmethod
    def live_chat(player: Player, data):
        txt = (data or {}).get("text", "").strip()
        if not txt:
            return
        entry = {"p": player.id_in_group, "text": txt}
        others = player.get_others_in_group()
        return {0: dict(msg=entry)}

class BidPage(Page):
    form_model = "player"
    form_fields = ["bid"]
    timeout_seconds = 60
    @staticmethod
    def error_message(player, values):
        b = values.get("bid")
        if b is None:
            return None
        if b < 0 or b > 100:
            return "Bid must be between 0 and 100."
    class Compute(WaitPage):
    after_all_players_arrive = 'set_winner_and_payoffs'

class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        other = player.get_others_in_group()[0]
        return dict(
            my_v=float(player.valuation),
            my_b=float(player.bid if player.bid is not None else 0),
            other_v=float(other.valuation),
            other_b=float(other.bid if other.bid is not None else 0),
            won=player.won,
            price=float(player.winning_price or 0),
        )

class SessionSummary(Page):
    def is_displayed(player):
        return player.round_number == C.ROUNDS_PER_SESSION
    @staticmethod
    def vars_for_template(player: Player):
        subsess = player.subsession
        data = []
        for r in range(1, C.ROUNDS_PER_SESSION + 1):
            for g in subsess.in_round(r).get_groups():
                p1, p2 = g.get_players()
                for p in [p1, p2]:
                    data.append(dict(
                        round=r, pid=p.participant.code,
                        valuation=float(p.valuation), bid=float(p.bid or 0),
                        won=p.won, price=float(p.winning_price or 0),
                    ))
        from collections import defaultdict
        bins = defaultdict(list)
        for row in data: bins[int(row["valuation"])].append(row["bid"])
        avg_bid_by_val = [{"x": k, "y": (sum(v)/len(v))} for k, v in sorted(bins.items()) if v]

        indiv = {}
        for row in data:
            pid = row["pid"]
            indiv.setdefault(pid, {})
            indiv[pid].setdefault(int(row["valuation"]), []).append(row["bid"])
        indiv_series = []
        for pid, mp in indiv.items():
            pts = [{"x": k, "y": sum(v)/len(v)} for k, v in sorted(mp.items())]
            indiv_series.append(dict(pid=pid, points=pts))

        rev_by_round = []
        for r in range(1, C.ROUNDS_PER_SESSION + 1):
            prices = []
            for g in subsess.in_round(r).get_groups():
                p1, p2 = g.get_players()
                prices.append(float(p1.winning_price or 0))
            if prices: rev_by_round.append(dict(x=r, y=sum(prices)/len(prices)))
        all_prices = [float(g.get_players()[0].winning_price or 0) for g in subsess.get_groups()]
        overall_rev = sum(all_prices)/len(all_prices) if all_prices else 0

        return dict(
            general_instructions=GENERAL_INSTR,
            avg_bid_by_val=json.dumps(avg_bid_by_val),
            indiv_series=json.dumps(indiv_series),
            rev_by_round=json.dumps(rev_by_round),
            overall_rev=overall_rev,
            session_name=subsess.session.config["name"],
        )

page_sequence = [Intro, Chat, BidPage, Compute, Results, SessionSummary]
