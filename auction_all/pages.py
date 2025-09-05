from otree.api import *
from .models import C, Subsession, Group, Player, PHASES, PHASE_SIZE, TOTAL_ROUNDS
import json

# === GENERAL INSTRUCTIONS (verbatim) ===
GENERAL_INSTR = """<h3 style="text-align:center;">GENERAL INSTRUCTIONS</h3>
<p>Welcome to the ECON 3310 Experiment Platform.</p>
<p>This experiment has two parts. Each part includes three separate sessions. In each session, you'll complete 10 rounds. Therefore, you will play an auction game over 6 sessions, totaling 60 rounds. Each round is expected to take about 1 minute or less. Overall, the experiment should take no more than 75 minutes, including review of instructions.</p>
<p>Participating in this experiment will earn you <strong>100 POINTS</strong>.</p>
<p>You can earn extra points in each round, and these points are mostly affected by your choices and those of your opponents. Points earned in each round and session will be added up. Therefore, each round matters, and it's important to make the most of each one.</p>
<p>The instructions for each session will appear on the computer screen before you start each session.</p>"""

# Session headers with highlighted bits
SESSION_1 = "<strong>SESSION 1: FIRST-PRICE SEALED BID AUCTION</strong><br/>You are <strong>randomly paired</strong> with a new opponent each round."
SESSION_2 = "<strong>SESSION 2: REPEATED FIRST-PRICE SEALED BID AUCTION</strong><br/>You play the <strong>same opponent</strong> for all 10 rounds (fixed pairing)."
SESSION_3 = "<strong>SESSION 3: REPEATED FIRST-PRICE WITH COMMUNICATION</strong><br/>Same as Session 2, but <strong>chat is enabled</strong> before bidding."
SESSION_4 = "<strong>SESSION 4: SECOND-PRICE SEALED BID AUCTION</strong><br/>Random pairing each round. Winner pays the <strong>second-highest</strong> bid."
SESSION_5 = "<strong>SESSION 5: REPEATED SECOND-PRICE</strong><br/>Same as Session 4, but with a <strong>fixed opponent</strong> across all rounds."
SESSION_6 = "<strong>SESSION 6: REPEATED SECOND-PRICE WITH COMMUNICATION</strong><br/>Fixed opponent + <strong>chat</strong> before bidding."

PHASE_INSTR = {
    "fp_random": SESSION_1,
    "fp_fixed":  SESSION_2,
    "fp_comm":   SESSION_3,
    "sp_random": SESSION_4,
    "sp_fixed":  SESSION_5,
    "sp_comm":   SESSION_6,
}

def _cfloat(x):
    try:
        return float(x)
    except TypeError:
        return 0.0

def current_phase(subsession): 
    return PHASES[subsession.phase_index]

class PhaseIntro(Page):
    def is_displayed(self):
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
        txt = (data or {}).get("text","").strip()
        if not txt: 
            return
        entry = {"p": player.id_in_group, "text": txt}
        return {0: dict(msg=entry), player.id_in_group: dict(msg=entry)}
    def vars_for_template(self):
        return dict(my_valuation=self.player.valuation)

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
            my_v=_cfloat(self.player.valuation),
            my_b=_cfloat(getattr(self.player, "bid", None)),
            other_v=_cfloat(other.valuation),
            other_b=_cfloat(getattr(other, "bid", None)),
            won=self.player.won,
            price=_cfloat(getattr(self.player, "winning_price", None)),
        )

class SessionSummary(Page):
    def is_displayed(self):
        return self.player.round_number % PHASE_SIZE == 0
    def vars_for_template(self):
        subs = self.player.subsession
        start, end = subs.phase_bounds()
        rows = []
        for r in range(start, end+1):
            for g in subs.in_round(r).get_groups():
                for p in g.get_players():
                    rows.append(dict(
                        round=r, pid=p.participant.code,
                        valuation=_cfloat(getattr(p, "valuation", None)),
                        bid=_cfloat(getattr(p, "bid", None)),
                        price=_cfloat(getattr(p, "winning_price", None)),
                        payoff=_cfloat(getattr(p, "payoff", None)),
                    ))

        # (1) Avg bid by valuation (all players)
        bins = {}
        for rr in rows:
            k = int(rr["valuation"])
            bins.setdefault(k, []).append(rr["bid"])
        s1 = [{"x":k, "y":sum(v)/len(v)} for k,v in sorted(bins.items()) if v]

        # (2) Individual avg bid by valuation
        indiv = {}
        for rr in rows:
            pid = rr["pid"]
            k = int(rr["valuation"])
            indiv.setdefault(pid, {}).setdefault(k, []).append(rr["bid"])
        indiv_series = []
        for pid, mp in indiv.items():
            pts = [{"x":k,"y":sum(v)/len(v)} for k,v in sorted(mp.items())]
            indiv_series.append(dict(pid=pid, points=pts))

        # (3) Avg revenue by round (within session)
        rev = {}
        for rr in rows:
            k = rr["round"] - (start-1)
            rev.setdefault(k, []).append(rr["price"])
        s3 = [{"x":k,"y":sum(v)/len(v)} for k,v in sorted(rev.items()) if v]

        # (4) YOUR overall average payoff (individual)
        my_pid = self.player.participant.code
        my_payoffs = [rr["payoff"] for rr in rows if rr["pid"] == my_pid]
        my_avg_payoff_str = f"{(sum(my_payoffs)/len(my_payoffs) if my_payoffs else 0):.2f}"

        return dict(
            avg_bid_by_val=json.dumps(s1),
            indiv_series=json.dumps(indiv_series),
            rev_by_round=json.dumps(s3),
            my_avg_payoff_str=my_avg_payoff_str,
            phase_label=current_phase(subs)["label"],
        )

class AllDashboard(Page):
    def is_displayed(self):
        return self.player.round_number == TOTAL_ROUNDS
    def vars_for_template(self):
        all_series1, all_series3, bar, pooled = {}, {}, [], []
        over = under = equal = 0
        for idx, phase in enumerate(PHASES):
            start = idx*PHASE_SIZE + 1
            end   = start + PHASE_SIZE - 1
            rows = []
            for r in range(start, end+1):
                subs = self.player.subsession.in_round(r)
                for g in subs.get_groups():
                    for p in g.get_players():
                        rows.append(dict(
                            valuation=_cfloat(getattr(p, "valuation", None)),
                            bid=_cfloat(getattr(p, "bid", None)),
                            price=_cfloat(getattr(p, "winning_price", None)),
                            round=r-start+1,
                        ))
                        pooled.append({"x": _cfloat(getattr(p, "valuation", None)),
                                       "y": _cfloat(getattr(p, "bid", None))})
                        if getattr(p, "bid", None) is not None:
                            b = _cfloat(getattr(p, "bid", None))
                            v = _cfloat(getattr(p, "valuation", None))
                            if b > v: over += 1
                            elif b < v: under += 1
                            else: equal += 1

            # avg bid by valuation
            bins = {}
            for rr in rows:
                k = int(rr["valuation"])
                bins.setdefault(k, []).append(rr["bid"])
            s1 = [{"x":k,"y":sum(v)/len(v)} for k,v in sorted(bins.items()) if v]
            all_series1[phase["label"]] = s1

            # avg revenue by round
            rev = {}
            for rr in rows:
                k = int(rr["round"])
                rev.setdefault(k, []).append(rr["price"])
            s3 = [{"x":k,"y":sum(v)/len(v)} for k,v in sorted(rev.items()) if v]
            all_series3[phase["label"]] = s3

            # bar: overall avg revenue for phase
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