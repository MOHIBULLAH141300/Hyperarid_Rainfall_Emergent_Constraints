import sys; sys.path.insert(0,'.')
from figstyle import *
import numpy as np, csv, os
from collections import defaultdict
rng=np.random.default_rng(20260918)
BASE=os.path.expanduser('~/mnt/RAINFALL PAPER B/reanalysis_2026-09-18')
DROP={'GFDL-CM4_gr2','GFDL-ESM41'}
D=defaultdict(dict)
for r in csv.DictReader(open(f'{BASE}/seasons_all.csv')):
    if r['model'] in DROP: continue
    D[(r['model'],r['region'])].setdefault(r['period'],[]).append((int(r['season']),float(r['rx1day']),float(r['r95p'])))
models=sorted({k[0] for k in D})
cells=[('Rx1day','uae',0),('R95p','uae',1),('Rx1day','east',0),('R95p','east',1)]
obs={};noise={};split={}
for idx,reg,vi in cells:
    H={};F={}
    for m in models:
        h=sorted(D[(m,reg)]['hist']); f=sorted(D[(m,reg)]['fut'])
        H[m]=np.array([r[1+vi] for r in h]); F[m]=np.array([r[1+vi] for r in f])
    x=np.array([H[m].mean() for m in models])
    y=np.array([100*(F[m].mean()-H[m].mean())/H[m].mean() for m in models])
    obs[(idx,reg)]=np.corrcoef(x,y)[0,1]
    nl=np.empty(2000)
    for i in range(2000):
        xa=[];ya=[]
        for m in models:
            h=H[m];f=F[m]; hb=h[rng.integers(0,len(h),len(h))]; fb=f[rng.integers(0,len(f),len(f))]
            xa.append(hb.mean()); ya.append(100*(fb.mean()-hb.mean())/hb.mean())
        nl[i]=np.corrcoef(xa,ya)[0,1]
    noise[(idx,reg)]=(nl.mean(),np.percentile(nl,2.5),np.percentile(nl,97.5))
    xs=[H[m][0::2].mean() for m in models]
    ys=[F[m].mean()-H[m][1::2].mean() for m in models]
    split[(idx,reg)]=np.corrcoef(xs,ys)[0,1]
lab=[f'{i}\n{"UAE" if r=="uae" else "East"}' for i,r,_ in cells]
fig,axes=plt.subplots(1,3,figsize=(9.4,3.0))
ax=axes[0]; x=np.arange(4); w=0.30
o=[obs[(i,r)] for i,r,_ in cells]
nm_=[noise[(i,r)][0] for i,r,_ in cells]
nlo=[noise[(i,r)][0]-noise[(i,r)][1] for i,r,_ in cells]; nhi=[noise[(i,r)][2]-noise[(i,r)][0] for i,r,_ in cells]
sv=[split[(i,r)] for i,r,_ in cells]
ax.bar(x-w,o,w*0.94,color=BLUE,label='observed',edgecolor='white',linewidth=1.2)
ax.bar(x,nm_,w*0.94,color=MUTED,label='expected from sampling noise',edgecolor='white',linewidth=1.2)
ax.errorbar(x,nm_,yerr=[nlo,nhi],fmt='none',ecolor=INK,elinewidth=0.9,capsize=2.5)
ax.bar(x+w,sv,w*0.94,color=GREEN,label='split-sample (disjoint seasons)',edgecolor='white',linewidth=1.2)
ax.axhline(0,color=INK,lw=0.8)
ax.set_xticks(x); ax.set_xticklabels(lab); ax.set_ylabel('correlation with projected change')
ax.set_ylim(-0.95,0.95); ax.legend(loc='lower center',bbox_to_anchor=(0.5,-0.02),fontsize=6.6); panel(ax,'a')
idx,reg,vi='R95p','uae',1
H={};F={}
for m in models:
    h=sorted(D[(m,reg)]['hist']); f=sorted(D[(m,reg)]['fut'])
    H[m]=np.array([r[1+vi] for r in h]); F[m]=np.array([r[1+vi] for r in f])
xo=np.array([H[m].mean() for m in models]); yo=np.array([100*(F[m].mean()-H[m].mean())/H[m].mean() for m in models])
xs=np.array([H[m][0::2].mean() for m in models]); ys=np.array([F[m].mean()-H[m][1::2].mean() for m in models])
for ax,(xv,yv,col,mk,xl,yl,ttl,rr) in zip(axes[1:],[
    (xo,yo,BLUE,'o','present-day R95p, all seasons (mm)','projected change (%)','predictor and baseline share seasons',obs[('R95p','uae')]),
    (xs,ys,GREEN,'s','present-day R95p, odd seasons (mm)','projected change (mm)','disjoint seasons, absolute change',split[('R95p','uae')])]):
    ax.scatter(xv,yv,s=36,color=col,marker=mk,zorder=3,edgecolor='white',linewidth=0.9)
    b,a=np.polyfit(xv,yv,1); xx=np.linspace(xv.min(),xv.max(),50); ax.plot(xx,a+b*xx,color=col,lw=1.8)
    ax.axhline(0,color=MUTED,lw=0.7,ls=':')
    ax.set_xlabel(xl); ax.set_ylabel(yl); ax.set_title(ttl,fontsize=7.6,color=MUTED,pad=6)
    ax.text(0.04,0.95,f'r = {rr:+.2f}',transform=ax.transAxes,color=col,fontsize=8.5,va='top',fontweight='bold')
panel(axes[1],'b'); panel(axes[2],'c')
fig.tight_layout(w_pad=2.2)
save(fig,'Figure13_confound_split_sample')
