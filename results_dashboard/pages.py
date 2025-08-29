from otree.api import *
from .models import C,Subsession,Group,Player
import json,random

def _avg(xs): return sum(xs)/len(xs) if xs else None
class ResultsDashboard(Page):
    form_model='player'; form_fields=['bin_size','target_v']
    @staticmethod
    def vars_for_template(p:Player):
        s=p.session; obs=s.vars.get('observations',[])
        data=[dict(v=float(o['valuation']),b=float(o['bid']),pr=o.get('participant')) for o in obs]
        tv=float(p.target_v); at=[d['b'] for d in data if round(d['v'],2)==round(tv,2)]; avg=_avg(at)
        bs=max(1,min(100,int(p.bin_size))); edges=list(range(0,100,bs))+[100]
        labels=[]; means=[]
        for i in range(len(edges)-1):
            lo,hi=edges[i],edges[i+1]
            vals=[d['b'] for d in data if d['v']>=lo and (d['v']<hi if hi<100 else d['v']<=hi)]
            labels.append(f"{lo}–{hi}"); means.append(_avg(vals) or 0)
        rev=s.vars.get('revenue',{}); rlabels=list(rev.keys()); rdata=[sum(v)/len(v) for v in rev.values()] if rev else []
        return dict(labels_json=json.dumps(labels), bin_means_json=json.dumps(means), target_v=p.target_v, avg_at_target=avg, rev_labels_json=json.dumps(rlabels), rev_data_json=json.dumps(rdata))
page_sequence=[ResultsDashboard]
