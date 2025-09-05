
from otree.api import *
from .models import C, Subsession, Group, Player, PHASES, PHASE_SIZE, TOTAL_ROUNDS
import json
from collections import defaultdict

GENERAL_INSTR = """Welcome to the ECON 3310 Experiment Platform.

This experiment has two parts. Each part includes three separate sessions. In each session, you'll complete 10 rounds. Therefore, you will play an auction game over 6 sessions, totaling 60 rounds. Each round is expected to take about 1 minute or less. Overall, the experiment should take no more than 75 minutes, including review of instructions.

Participating in this experiment will earn you 100 POINTS.

You can earn extra points in each round, and these points are mostly affected by your choices and those of your opponents. Points earned in each round and session will be added up. Therefore, each round matters, and it's important to make the most of each one.

The instructions for each session will appear on the computer screen before you start each session.
"""

PHASE_INSTR = {
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

def current_phase(subsession):
    return PHASES[subsession.phase_index]

def phase_key(subsession):
    return PHASES[subsession.phase_index]["key"]

class PhaseIntro(Page):
    def is_displayed(player):
        # rounds 1,11,21,31,41,51
        return (player.round_number-1) % PHASE_SIZE == 0

    def vars_for_template(player):
        subsess = player.subsession
        phase = current_phase(subsess)
        key = phase["key"]
        return dict(
            general_instructions=GENERAL_INSTR if player.round_number == 1 else "",
            session_instructions=PHASE_INSTR.get(key, ""),
            phase_label=phase["label"],
        )

class Chat(Page):
    live_method = "live_chat"
    def is_displayed(player):
        return player.subsession.chat_enabled
    @staticmethod
    def live_chat(player: Player, data):
        txt = (data or {}).get("text","").strip()
        if not txt: return
        entry = {"p": player.id_in_group, "text": txt}
        return {0: dict(msg=entry)}

class BidPage(Page):
    form_model = "player"
    form_fields = ["bid"]
    timeout_seconds = 60
    class Compute(WaitPage):
    after_all_players_arrive = 'set_winner_and_payoffs'

class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        other = player.get_others_in_group()[0]
        return dict(
            my_v=float(player.valuation),
            my_b=float(player.bid or 0),
            other_v=float(other.valuation),
            other_b=float(other.bid or 0),
            won=player.won,
            price=float(player.winning_price or 0),
        )

class SessionSummary(Page):
    def is_displayed(player):
        # show at end of each phase: 10,20,...,60
        return player.round_number % PHASE_SIZE == 0
    @staticmethod
    def vars_for_template(player: Player):
        subs = player.subsession
        start, end = subs.phase_bounds()
        # collect rows within this phase
        rows = []
        for r in range(start, end+1):
            for g in subs.in_round(r).get_groups():
                for p in g.get_players():
                    rows.append(dict(
                        round=r, pid=p.participant.code,
                        valuation=float(p.valuation or 0),
                        bid=float(p.bid or 0),
                        price=float(p.winning_price or 0),
                    ))
        # 1) avg bid vs valuation
        bins = defaultdict(list)
        for r in rows: bins[int(r["valuation"])].append(r["bid"])
        s1 = [{"x":k,"y":sum(v)/len(v)} for k,v in sorted(bins.items()) if v]
        # 2) per-participant
        indiv = {}
        for r in rows:
            pid = r["pid"]
            indiv.setdefault(pid, {})
            indiv[pid].setdefault(int(r["valuation"]), []).append(r["bid"])
        indiv_series = []
        for pid, mp in indiv.items():
            pts = [{"x":k, "y":sum(v)/len(v)} for k,v in sorted(mp.items())]
            indiv_series.append(dict(pid=pid, points=pts))
        # 3) avg revenue by round (within phase)
        rev = defaultdict(list)
        for r in rows: rev[r["round"] - (start-1)].append(r["price"])
        s3 = [{"x":k, "y":sum(v)/len(v)} for k,v in sorted(rev.items()) if v]
        # 4) overall avg revenue number
        prices = [r["price"] for r in rows]
        overall = (sum(prices)/len(prices)) if prices else 0

        return dict(
            avg_bid_by_val=json.dumps(s1),
            indiv_series=json.dumps(indiv_series),
            rev_by_round=json.dumps(s3),
            overall_rev=overall,
            phase_label=current_phase(subs)["label"],
        )

class AllDashboard(Page):
    def is_displayed(player):
        return player.round_number == TOTAL_ROUNDS
    @staticmethod
    def vars_for_template(player: Player):
        # Build per-phase series across the single session
        all_series1 = {}   # key -> avg bid vs val
        all_series3 = {}   # key -> avg revenue by round
        bar = []           # overall avg revenue by phase
        pooled = []
        over=under=equal=0

        for idx, phase in enumerate(PHASES):
            start = idx*PHASE_SIZE + 1
            end = start + PHASE_SIZE - 1
            rows = []
            for r in range(start, end+1):
                subs = player.subsession.in_round(r)
                for g in subs.get_groups():
                    for p in g.get_players():
                        rows.append(dict(
                            valuation=float(p.valuation or 0),
                            bid=float(p.bid or 0),
                            price=float(p.winning_price or 0),
                            round=r-start+1,
                        ))
                        pooled.append({"x": float(p.valuation or 0), "y": float(p.bid or 0)})
                        if p.bid is not None:
                            if float(p.bid) > float(p.valuation or 0): over += 1
                            elif float(p.bid) < float(p.valuation or 0): under += 1
                            else: equal += 1

            # 5) avg bid vs valuation (by phase)
            bins = defaultdict(list)
            for rr in rows: bins[int(rr["valuation"])].append(rr["bid"])
            s1 = [{"x":k,"y":sum(v)/len(v)} for k,v in sorted(bins.items()) if v]
            all_series1[phase["label"]] = s1

            # 6) avg revenue by round (by phase)
            rev = defaultdict(list)
            for rr in rows: rev[int(rr["round"])].append(rr["price"])
            s3 = [{"x":k,"y":sum(v)/len(v)} for k,v in sorted(rev.items()) if v]
            all_series3[phase["label"]] = s3

            # 7) overall avg revenue (by phase)
            prices = [rr["price"] for rr in rows]
            overall = (sum(prices)/len(prices)) if prices else 0
            bar.append({"label": phase["label"], "value": overall})

        pie = [
            {"label":"Over-bid (bid > value)", "value": over},
            {"label":"Under-bid (bid < value)", "value": under},
            {"label":"Equal (bid = value)", "value": equal},
        ]

        return dict(
            series1=json.dumps(all_series1),
            series3=json.dumps(all_series3),
            bar_overall=json.dumps(bar),
            pooled_points=json.dumps(pooled),
            pie=json.dumps(pie),
            labels=[ph["label"] for ph in PHASES],
        )

page_sequence = [PhaseIntro, Chat, BidPage, Compute, Results, SessionSummary, AllDashboard]
