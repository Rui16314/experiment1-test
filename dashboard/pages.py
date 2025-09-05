
from otree.api import *
from .models import C, Subsession, Group, Player
from auction.models import Player as AuctionPlayer, Subsession as AuctionSubsession
from otree.models import Session as OTreeSession
import json
from collections import defaultdict

LABELS = [
    ("fp_random", "Exp1: FP Random"),
    ("fp_fixed", "Exp2: FP Fixed"),
    ("fp_comm", "Exp3: FP w/ Chat"),
    ("sp_random", "Exp4: SP Random"),
    ("sp_fixed", "Exp5: SP Fixed"),
    ("sp_comm", "Exp6: SP w/ Chat"),
]

class Dash(Page):
    @staticmethod
    def is_displayed(player):
        return True

    @staticmethod
    def vars_for_template(player: Player):
        # pick the most recent session for each named config
        latest_by_name = {}
        for s in OTreeSession.objects.order_by("-id"):
            cfg = s.config or {}
            name = cfg.get("name")
            if name in [k for k, _ in LABELS] and name not in latest_by_name:
                latest_by_name[name] = s
        series1 = {}   # avg bid vs valuation (per session)
        series3 = {}   # avg revenue by round (per session)
        bar_overall = []  # overall avg revenue by session
        pooled_points = []  # for scatter
        over = under = equal = 0

        for key, label in LABELS:
            sess = latest_by_name.get(key)
            if not sess:
                continue

            # collect rows from this session
            rows = []
            subs = AuctionSubsession.objects.filter(session=sess).order_by("round_number")
            for sub in subs:
                groups = sub.get_groups()
                for g in groups:
                    players = g.get_players()
                    for p in players:
                        rows.append(dict(
                            round=sub.round_number,
                            valuation=float(p.valuation or 0),
                            bid=float(p.bid or 0),
                            price=float(p.winning_price or 0),
                        ))
                        # pooled stats
                        pooled_points.append({"x": float(p.valuation or 0), "y": float(p.bid or 0)})
                        if p.bid is not None:
                            if float(p.bid) > float(p.valuation or 0): over += 1
                            elif float(p.bid) < float(p.valuation or 0): under += 1
                            else: equal += 1

            # (1) avg bid vs valuation for this session
            bins = defaultdict(list)
            for r in rows: bins[int(r["valuation"])].append(r["bid"])
            s1 = [{"x": k, "y": sum(v)/len(v)} for k, v in sorted(bins.items()) if v]
            series1[label] = s1

            # (3) avg revenue by round for this session
            rev = defaultdict(list)
            for r in rows: rev[int(r["round"])].append(r["price"])
            s3 = [{"x": r, "y": (sum(v)/len(v))} for r, v in sorted(rev.items()) if v]
            series3[label] = s3

            # (4) overall avg revenue number for the session
            prices = [r["price"] for r in rows if r["price"] is not None]
            overall = (sum(prices)/len(prices)) if prices else 0
            bar_overall.append({"label": label, "value": overall})

        totals = over + under + equal
        pie = [
            {"label": "Over-bid (bid > value)", "value": over},
            {"label": "Under-bid (bid < value)", "value": under},
            {"label": "Equal (bid = value)", "value": equal},
        ]

        return dict(
            series1=json.dumps(series1),
            series3=json.dumps(series3),
            bar_overall=json.dumps(bar_overall),
            pooled_points=json.dumps(pooled_points),
            pie=json.dumps(pie),
            labels=[lbl for _, lbl in LABELS],
        )

page_sequence = [Dash]
