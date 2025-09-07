
from otree.api import *
from .models import C, Subsession, Group, Player, PHASES, PHASE_SIZE, TOTAL_ROUNDS
import json

GENERAL_INSTR = """
<h3 style="text-align:center;">GENERAL INSTRUCTIONS</h3>
<p>Welcome to the ECON 3310 Experiment Platform.</p>
<p>This experiment has two parts. Each part includes three separate sessions. In each session, you'll complete 10 rounds. Therefore, you will play an auction game over 6 sessions, totaling 60 rounds. Each round is expected to take about 1 minute or less. Overall, the experiment should take no more than 75 minutes, including review of instructions.</p>
<p>Participating in this experiment will earn you <strong>100 POINTS</strong>.</p>
<p>You can earn extra points in each round, and these points are mostly affected by your choices and those of your opponents. Points earned in each round and session will be added up. Therefore, each round matters, and it's important to make the most of each one.</p>
<p>The instructions for each session will appear on the computer screen before you start each session.</p>
"""

SESSION_1_HTML = """
<h4 style="text-align:center;">SESSION 1: FIRST-PRICE SEALED BID AUCTION INSTRUCTIONS</h4>
<p>You will play 10 rounds of this game. At the start of each round, you'll be randomly paired with a different participant. This means your matches will change from round to round, and you'll never know who you'll be paired with in any given round.</p>
<p>The seller is auctioning an indivisible item, and two buyers—yourself and your opponent, whom we match randomly—are interested in purchasing it. In each round, you'll participate in an auction to buy the good.</p>
<p>In each round, your valuation and your opponent’s will be assigned randomly. Therefore, your and your opponent’s valuations will probably differ in each round. You will always know your own valuation but won’t learn your opponent’s until the round ends. Valuations are chosen independently and uniformly from 0 to 100, in increments of cents. As a result, your valuation will be 0.01n with a probability of 1/10,000, where n ranges from 0 to 10,000.</p>
<p>In each round, after learning your valuation, you have 1 minute to place your bid. Once you submit your bid, the round will end. You will not see your opponent’s bid until after the round ends, when you learn the winning bid and how many points you earned that round.</p>
<p><strong>POINTS YOU EARN IN EACH ROUND WILL DEPEND ON THESE THREE FACTORS</strong></p>
<ol><li>Your bid</li><li>Your opponent’s bid</li><li>Your valuation</li></ol>
<p><em>More specifically,</em></p>
<ul>
<li>If your bid is less than your opponent’s bid, then you lose the auction and receive 0 points.</li>
<li>If your bid is higher than your opponent’s bid, then you win the auction. Thus, your points will be <em>Your points = Your valuation − Your bid</em>.</li>
<li>If your bid is equal to your opponent’s bid, then your points will be determined according to the following: <em>Your points = (Your valuation − Your bid) / 2</em>.</li>
<li>If you do not submit your bid within the 1-minute window, you lose the auction and receive 0 points.</li>
</ul>
<p>At the end of each round, you will find out whether you win the auction, your opponent’s valuation, bid, and your points.</p>
"""

SESSION_2_HTML = """
<h4 style="text-align:center;">SESSION 2: REPEATED FIRST-PRICE SEALED BID AUCTION INSTRUCTIONS</h4>
<p>You will play 10 rounds of the same game you played in the previous session. The only difference is that you will play all 10 rounds against the same opponent. So, your opponent will stay the same throughout the rounds.</p>
<p>In the experimental instructions, the bold sections highlight the only new parts compared to the previous session.</p>
<p><strong>To be more specific, you'll be randomly paired with a participant at the beginning of this session and remain paired throughout 10 rounds.</strong></p>
<p>In each round, your valuation and your opponent’s will be assigned randomly. Therefore, your and your opponent’s valuations will probably differ in each round. You will always know your own valuation but won’t learn your opponent’s until the round ends. Valuations are chosen independently and uniformly from 0 to 100, in increments of cents. As a result, your valuation will be 0.01n with a probability of 1/10,000, where n ranges from 0 to 10,000.</p>
<p>In each round, after learning your valuation, you have 1 minute to place your bid. Once you submit your bid, the round will end. You will not see your opponent’s bid until after the round ends, when you learn the winning bid and how many points you earned that round.</p>
<p><strong>POINTS YOU EARN IN EACH ROUND WILL DEPEND ON THESE THREE FACTORS</strong></p>
<ol start="4"><li>Your bid</li><li>Your opponent’s bid</li><li>Your valuation</li></ol>
<p><em>More specifically,</em></p>
<ul>
<li>If your bid is less than your opponent’s bid, then you lose the auction and receive 0 points.</li>
<li>If your bid is higher than your opponent’s bid, then you win the auction. Thus, your points will be <em>Your points = Your valuation − Your bid</em>.</li>
<li>If your bid is equal to your opponent’s bid, then your points will be determined according to the following: <em>Your points = (Your valuation − Your bid) / 2</em>.</li>
<li>If you do not submit your bid within the 1-minute window, you lose the auction and receive 0 points.</li>
</ul>
<p>At the end of each round, you will find out whether you win the auction, your opponent’s valuation, bid, and your points.</p>
"""

SESSION_3_HTML = """
<h4 style="text-align:center;">SESSION 3: REPEATED FIRST-PRICE SEALED BID AUCTION WITH COMMUNICATION INSTRUCTIONS</h4>
<p>You will play 10 rounds of the same game you played in the previous session. The only difference is that you will now be able to communicate with your opponent through the chatbox.</p>
<p>In the experimental instructions, the bold sections highlight the only new parts compared to the previous session.</p>
<p><strong>To be more specific, you'll be randomly paired with a participant at the beginning of this session and remain paired throughout 10 rounds.</strong></p>
<p>In each round, your valuation and your opponent’s will be assigned randomly. Therefore, your and your opponent’s valuations will probably differ in each round. You will always know your own valuation but won’t learn your opponent’s until the round ends. Valuations are chosen independently and uniformly from 0 to 100, in increments of cents. As a result, your valuation will be 0.01n with a probability of 1/10,000, where n ranges from 0 to 10,000.</p>
<p><strong>You may communicate with your opponent before submitting your bid. Feel free to discuss any matter, but please keep your identity confidential.</strong></p>
<p>In each round, after learning your valuation, you have 1 minute to place your bid. Once you submit your bid, the round will end. You will not see your opponent’s bid until after the round ends, when you learn the winning bid and how many points you earned that round.</p>
<p><strong>POINTS YOU EARN IN EACH ROUND WILL DEPEND ON THESE THREE FACTORS</strong></p>
<ol start="4"><li>Your bid</li><li>Your opponent’s bid</li><li>Your valuation</li></ol>
<p><em>More specifically,</em></p>
<ul>
<li>If your bid is less than your opponent’s bid, then you lose the auction and receive 0 points.</li>
<li>If your bid is higher than your opponent’s bid, then you win the auction. Thus, your points will be <em>Your points = Your valuation − Your bid</em>.</li>
<li>If your bid is equal to your opponent’s bid, then your points will be determined according to the following: <em>Your points = (Your valuation − Your bid) / 2</em>.</li>
<li>If you do not submit your bid within the 1-minute window, you lose the auction and receive 0 points.</li>
</ul>
<p>At the end of each round, you will find out whether you win the auction, your opponent’s valuation, bid, and your points.</p>
"""

SESSION_TEXT = {
    "fp_random": SESSION_1_HTML,
    "fp_fixed":  SESSION_2_HTML,
    "fp_comm":   SESSION_3_HTML,
    "sp_random": "<h4>SESSION 4</h4><p>(Paste the exact text from your document here.)</p>",
    "sp_fixed":  "<h4>SESSION 5</h4><p>(Paste the exact text from your document here.)</p>",
    "sp_comm":   "<h4>SESSION 6</h4><p>(Paste the exact text from your document here.)</p>",
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
        phase = current_phase(self.player.subsession)
        key = phase["key"]
        return dict(
            general_instructions=GENERAL_INSTR if self.player.round_number == 1 else "",
            session_instructions=SESSION_TEXT[key],
            phase_label=phase["label"],
        )

class Chat(Page):
    live_method = 'live_chat'

    @staticmethod
    def vars_for_template(player: Player):
        # use your actual field name here: 'valuation', 'value_points', etc.
        val = getattr(player, 'valuation', None)
        if val is None:
            val = player.participant.vars.get('valuation')
        text = '' if val in (None, '') else f'{val} POINTS'
        return dict(my_value=text)

    @staticmethod
    def live_chat(player: Player, data):
        text = (data or {}).get('text', '').strip()
        if not text:
            return
        # broadcast to both players; also send a "me" copy so your own line is marked
        payload_all = dict(sender=player.id_in_group, text=text, me=False)
        payload_me  = dict(sender=player.id_in_group, text=text, me=True)
        return {0: payload_all, player.id_in_group: payload_me}


class BidPage(Page):
    form_model = "player"
    form_fields = ["bid"]
    timeout_seconds = 60

class Compute(WaitPage):
    after_all_players_arrive = 'set_winner_and_payoffs'

class Results(Page):
    def vars_for_template(self):
        other = self.player.get_others_in_group()[0]
        def _c(x): 
            try: return float(x)
            except TypeError: return 0.0
        return dict(
            my_v=_c(self.player.valuation),
            my_b=_c(getattr(self.player, "bid", None)),
            other_v=_c(other.valuation),
            other_b=_c(getattr(other, "bid", None)),
            won=self.player.won,
            price=_c(getattr(self.player, "winning_price", None)),
        )

class SessionSummary(Page):
    def is_displayed(self):
        return self.player.round_number % PHASE_SIZE == 0
    def vars_for_template(self):
        subs = self.player.subsession
        start = subs.phase_index * PHASE_SIZE + 1
        end = start + PHASE_SIZE - 1
        rows = []
        for r in range(start, end+1):
            for g in subs.in_round(r).get_groups():
                for p in g.get_players():
                    def _c(x):
                        try: return float(x)
                        except TypeError: return 0.0
                    rows.append(dict(
                        round=r, pid=p.participant.code,
                        valuation=_c(getattr(p, "valuation", None)),
                        bid=_c(getattr(p, "bid", None)),
                        price=_c(getattr(p, "winning_price", None)),
                        payoff=_c(getattr(p, "payoff", None)),
                    ))
        bins = {}
        for rr in rows:
            k = int(rr["valuation"])
            bins.setdefault(k, []).append(rr["bid"])
        s1 = [{"x":k,"y":sum(v)/len(v)} for k,v in sorted(bins.items()) if v]
        indiv = {}
        for rr in rows:
            pid = rr["pid"]; k = int(rr["valuation"])
            indiv.setdefault(pid, {}).setdefault(k, []).append(rr["bid"])
        indiv_series = []
        for pid, mp in indiv.items():
            pts = [{"x":k,"y":sum(v)/len(v)} for k,v in sorted(mp.items())]
            indiv_series.append(dict(pid=pid, points=pts))
        rev = {}
        for rr in rows:
            k = rr["round"] - (start-1)
            rev.setdefault(k, []).append(rr["price"])
        s3 = [{"x":k,"y":sum(v)/len(v)} for k,v in sorted(rev.items()) if v]
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
            start = idx*PHASE_SIZE + 1; end = start + PHASE_SIZE - 1
            rows = []
            for r in range(start, end+1):
                subs = self.player.subsession.in_round(r)
                for g in subs.get_groups():
                    for p in g.get_players():
                        def _c(x):
                            try: return float(x)
                            except TypeError: return 0.0
                        rows.append(dict(
                            valuation=_c(getattr(p, "valuation", None)),
                            bid=_c(getattr(p, "bid", None)),
                            price=_c(getattr(p, "winning_price", None)),
                            round=r-start+1,
                        ))
                        pooled.append({"x": _c(getattr(p, "valuation", None)),
                                       "y": _c(getattr(p, "bid", None))})
                        if getattr(p, "bid", None) is not None:
                            b = _c(getattr(p, "bid", None)); v = _c(getattr(p, "valuation", None))
                            if b > v: over += 1
                            elif b < v: under += 1
                            else: equal += 1
            bins = {}
            for rr in rows:
                k = int(rr["valuation"])
                bins.setdefault(k, []).append(rr["bid"])
            s1 = [{"x":k,"y":sum(v)/len(v)} for k,v in sorted(bins.items()) if v]
            all_series1[phase["label"]] = s1
            rev = {}
            for rr in rows:
                k = int(rr["round"])
                rev.setdefault(k, []).append(rr["price"])
            s3 = [{"x":k,"y":sum(v)/len(v)} for k,v in sorted(rev.items()) if v]
            all_series3[phase["label"]] = s3
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
