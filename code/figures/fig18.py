# -*- coding: utf-8 -*-
"""Figure: the two diagnostics. (a) split-half behaviour of the historical record;
(b) scenario dependence of the historical-to-future relationship."""
import csv,os,math,collections
import numpy as np
from figstyle import *
import matplotlib.pyplot as plt
SRC=os.path.expanduser('~/mnt/RAINFALL PAPER B/reanalysis_2026-09-18/multiscenario/seasons_v4.csv')
rows=list(csv.DictReader(open(SRC)))
S=collections.defaultdict(dict)
for r in rows: S[(r['model'],r['exp'],r['region'])][int(r['season'])]={k:float(r[k]) for k in ('rx1day','r95p','r95p_oos')}
def ser(m,e,reg,k):
    d=S.get((m,e,reg));  return [v[k] for _,v in sorted(d.items())] if d else None
def mean(a): return sum(a)/len(a)
def var(a): mu=mean(a); return sum((x-mu)**2 for x in a)/(len(a)-1)
def pear(x,y):
    mx,my=mean(x),mean(y); c=sum((a-mx)*(b-my) for a,b in zip(x,y))/(len(x)-1)
    v=var(x)*var(y); return c/math.sqrt(v) if v>0 else 0.0
EXPS=['ssp126','ssp245','ssp370','ssp585']; SCL=['SSP1-2.6','SSP2-4.5','SSP3-7.0','SSP5-8.5']
allm=sorted({r['model'] for r in rows})
common=[m for m in allm if all(S.get((m,e,'uae')) for e in ['historical']+EXPS)]
hist=[m for m in allm if S.get((m,'historical','uae')) and m!='GFDL-CM4_gr2']

fig,axes=plt.subplots(1,2,figsize=(9.6,3.5))
# ---- (a) split-half ----
ax=axes[0]
cats=[('rx1day','Rx1day\n(no threshold)'),('r95p','R95p, threshold\nestimated in sample'),
      ('r95p_oos','R95p, threshold\nestimated out of sample')]
regs=[('uae','National',BLUE),('east','Eastern',VERM)]
w=0.36; x=np.arange(len(cats))
for t,(reg,rlab,col) in enumerate(regs):
    vals=[]
    for k,_ in cats:
        A=[mean(ser(m,'historical',reg,k)[0::2]) for m in hist]
        Bv=[mean(ser(m,'historical',reg,k)[1::2]) for m in hist]
        vals.append(pear(A,Bv))
    b=ax.bar(x+(t-0.5)*w,vals,w*0.92,color=col,label=rlab,edgecolor='white',linewidth=1.2)
    for xi,v in zip(x+(t-0.5)*w,vals):
        ax.text(xi,v+(0.035 if v>0 else -0.035),'%+.2f'%v,ha='center',
                va='bottom' if v>0 else 'top',fontsize=7,color=INK)
ax.axhline(0,color=MUTED,lw=0.9)
ax.set_xticks(x); ax.set_xticklabels([c[1] for c in cats])
ax.set_ylabel('Correlation between two disjoint\nhalves of the same record')
ax.set_ylim(-0.62,0.66); ax.legend(loc='lower right',ncol=1)
ax.set_title('Independent halves should correlate positively',pad=6); panel(ax,'a')
# ---- (b) scenario dependence ----
ax=axes[1]
combos=[('uae','rx1day','National Rx1day',BLUE,'o','-'),('uae','r95p','National R95p',VERM,'s','-'),
        ('east','rx1day','Eastern Rx1day',BLUE,'o','--'),('east','r95p','Eastern R95p',VERM,'s','--')]
xs=np.arange(4)
for reg,idx,lab,col,mk,ls in combos:
    ys=[]
    for e in EXPS:
        H=[mean(ser(m,'historical',reg,idx)) for m in common]
        F=[mean(ser(m,e,reg,idx)) for m in common]
        ys.append(pear(H,F))
    ax.plot(xs,ys,ls,color=col,marker=mk,ms=5,lw=2,label=lab,
            markeredgecolor='white',markeredgewidth=1.0)
ax.axhline(0,color=INK,lw=1.0)
ax.set_xticks(xs); ax.set_xticklabels(SCL,rotation=20,ha='right')
ax.set_ylabel('r (historical level, future level)')
ax.set_ylim(-0.85,0.72); ax.legend(loc='lower right',ncol=2,columnspacing=1.0,handlelength=3.0)
ax.set_title('Identical 23-model set in every scenario',pad=6); panel(ax,'b')
fig.tight_layout()
save(fig,'Figure18_diagnostics')
