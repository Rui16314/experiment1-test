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
    "fp_random": "SESSION 1: FIRST-PRICE SEALED BID AUCTION INSTRUCTIONS\n\n(Instructions as provided; unchanged.)",
    "fp_fixed": "SESSION 2: REPEATED FIRST-PRICE SEALED BID AUCTION INSTRUCTIONS\n\n(Instructions as provided; unchanged.)",
    "fp_comm": "SESSION 3: REPEATED FIRST-PRICE SEALED BID AUCTION WITH COMMUNICATION INSTRUCTIONS\n\n(Instructions as provided; unchanged.)",
    "sp_random": "SESSION 4: SECOND-PRICE SEALED BID AUCTION INSTRUCTIONS\n\n(Instructions as provided; unchanged.)",
    "sp_fixed": "SESSION 5: REPEATED SECOND-PRICE SEALED BID AUCTION INSTRUCTIONS\n\n(Instructions as provided; unchanged.)",
    "sp_comm": "SESSION 6: REPEATED SECOND-PRICE SEALED BID AUCTION WITH COMMUNICATION INSTRUCTIONS\n\n(Instructions as provided; unchanged.)",
}

def current_phase(subsession):
    return PHASES[subsession.phase_index]

class PhaseIntro(Page):
    def is_displayed(self):
        # rounds 1,11,21,31,41,51
        return (self.player.round_number - 1) % PHASE_SIZE == 0

    def vars_for_template(self):
        subsess = self.player.subsession
        phase = current_phase(subsess)
        key = phase["key"]
        return dict(
            general_instructions=GENERAL_INSTR if self.player.round_number == 1 else "",
            session_instructions=PHASE_INSTR.get(key, ""),
            phase_label=phase["label"],
        )

class Chat(Page):
    live_method = "live_chat"

    def is_displayed(self):
        return self.player.subsession.chat_enabled

    @staticmethod
    def live_chat(player: Player, data):
        txt = (data or {}).get("text", "").strip()
        if not txt:
            return
        entry = {"p": player.id_in_group, "text": txt}
        return {0: dict(msg=entry)}

class BidPage(Page):
    form_model = "player"
    form_fields = ["bid"]
    timeout_seconds = 60

class Compute(WaitPage):
    after_all_players_arrive = 'set_winner_and_payoffs'

class Results(Page):
    def vars_for_template(self):
        other = self.player.get_others_in_group()[0]
        return dict(
            my_v=float(self.player.valuation),
            my_b=float(self.player.bid or 0),
            other_v=float(other.valuation),
            other_b=float(other.bid or 0),
            won=self.player.won,
            price=float(self.player.winning_price or 0),
        )

class SessionSummary(Page):
    def is_displayed(self):
        return self.player.round_number % PHASE_SIZE == 0

    def vars_for_template(self):
        subs = self.player.subsession
        start, end = subs.phase_bounds()
        rows = []
        for r in range(start, end + 1):
            for g in subs.in_round(r).get_groups():
                for p in g.get_players():
                    rows.append(dict(
                        round=r, pid=p.participant.code,
                        valuation=float(p.valuation or 0),
                        bid=float(p.bid or 0),
                        price=float(p.winning_price or 0),
                    ))
        bins = defaultdict(list)
        for rr in rows:
            bins[int(rr["valuation"])].append(rr["bid"])
        s1 = [{"x": k, "y": sum(v) / len(v)} for k, v in sorted(bins.items()) if v]

        indiv = {}
        for rr in rows:
            pid = rr["pid"]
            indiv.setdefault(pid, {})
            indiv[pid].setdefault(int(rr["valuation"]), []).append(rr["bid"])
        indiv_series = []
        for pid, mp in indiv.items():
            pts = [{"x": k, "y": sum(v) / len(v)} for k, v in sorted(mp.items())]
            indiv_series.append(dict(pid=pid, points=pts))

        rev = defaultdict(list)
        for rr in rows:
            rev[rr["round"] - (start - 1)].append(rr["price"])
        s3 = [{"x": k, "y": sum(v) / len(v)} for k, v in sorted(rev.items()) if v]

        prices = [rr["price"] for rr in rows]
        overall = (sum(prices) / len(prices)) if prices else 0

        return dict(
            avg_bid_by_val=json.dumps(s1),
            indiv_series=json.dumps(indiv_series),
            rev_by_round=json.dumps(s3),
            overall_rev=overall,
            phase_label=current_phase(subs)["label"],
        )

class AllDashboard(Page):
    def is_displayed(self):
        return self.player.round_number == TOTAL_ROUNDS

    def vars_for_template(self):
        all_series1, all_series3, bar, pooled = {}, {}, [], []
        over = under = equal = 0
        for idx, phase in enumerate(PHASES):
            start = idx * PHASE_SIZE + 1
            end = start + PHASE_SIZE - 1
            rows = []
            for r in range(start, end + 1):
                subs = self.player.subsession.in_round(r)
                for g in subs.get_groups():
                    for p in g.get_players():
                        rows.append(dict(
                            valuation=float(p.valuation or 0),
                            bid=float(p.bid or 0),
                            price=float(p.winning_price or 0),
                            round=r - start + 1,
                        ))
                        pooled.append({"x": float(p.valuation or 0), "y": float(p.bid or 0)})
                        if p.bid is not None:
                            if float(p.bid) > float(p.valuation or 0):
                                over += 1
                            elif float(p.bid) < float(p.valuation or 0):
                                under += 1
                            else:
                                equal += 1
            bins = defaultdict(list)
            for rr in rows:
                bins[int(rr["valuation"])].append(rr["bid"])
            s1 = [{"x": k, "y": sum(v) / len(v)} for k, v in sorted(bins.items()) if v]
            all_series1[phase["label"]] = s1

            rev = defaultdict(list)
            for rr in rows:
                rev[int(rr["round"])].append(rr["price"])
            s3 = [{"x": k, "y": sum(v) / len(v)} for k, v in sorted(rev.items()) if v]
            all_series3[phase["label"]] = s3

            prices = [rr["price"] for rr in rows]
            overall = (sum(prices) / len(prices)) if prices else 0
            bar.append({"label": phase["label"], "value": overall})

        pie = [
            {"label": "Over-bid (bid > value)", "value": over},
            {"label": "Under-bid (bid < value)", "value": under},
            {"label": "Equal (bid = value)", "value": equal},
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