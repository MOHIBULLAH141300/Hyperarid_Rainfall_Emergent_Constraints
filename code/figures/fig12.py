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
    D[(r['model'],r['region'])].setdefault(r['period'],[]).append((float(r['rx1day']),float(r['r95p'])))
models=sorted({k[0] for k in D}); N=len(models)
cells=[('Rx1day','uae',0),('R95p','uae',1),('Rx1day','east',0),('R95p','east',1)]
frac={}; cross={}
for idx,reg,vi in cells:
    for mode in ('mm','pct'):
        samp=[];act=[];nz=0
        for m in models:
            d=D[(m,reg)]; h=np.array([x[vi] for x in d['hist']]); f=np.array([x[vi] for x in d['fut']])
            act.append(f.mean()-h.mean() if mode=='mm' else 100*(f.mean()-h.mean())/h.mean())
            nh,nf=len(h),len(f); bs=np.empty(3000)
            for b in range(3000):
                hh=h[rng.integers(0,nh,nh)]; ff=f[rng.integers(0,nf,nf)]
                bs[b]= ff.mean()-hh.mean() if mode=='mm' else 100*(ff.mean()-hh.mean())/hh.mean()
            samp.append(bs.std(ddof=1))
            lo,hi=np.percentile(bs,[2.5,97.5])
            if lo<0<hi: nz+=1
        samp=np.array(samp); act=np.array(act)
        frac[(idx,reg,mode)]=np.mean(samp**2)/np.var(act,ddof=1); cross[(idx,reg,mode)]=nz
lab=[f'{i}\n{"UAE" if r=="uae" else "East"}' for i,r,_ in cells]
fig,axes=plt.subplots(1,2,figsize=(7.1,3.0))
x=np.arange(4); w=0.36
ax=axes[0]
for k,(mode,col,nm) in enumerate([('mm',BLUE,'absolute change (mm)'),('pct',VERM,'fractional change (%)')]):
    v=[frac[(i,r,mode)] for i,r,_ in cells]
    ax.bar(x+(k-0.5)*w,v,w*0.94,color=col,label=nm,edgecolor='white',linewidth=1.2)
    for xi,vv in zip(x+(k-0.5)*w,v):
        ax.text(xi,vv+0.025,f'{vv:.2f}',ha='center',va='bottom',fontsize=7,color=INK)
ax.axhline(1.0,color=MUTED,lw=0.9,ls='--')
ax.text(3.62,1.035,'parity',fontsize=7,color=MUTED,va='bottom',ha='left')
ax.set_xlim(-0.6,4.05)
ax.set_xticks(x); ax.set_xticklabels(lab)
ax.set_ylabel('sampling variance / inter-model variance'); ax.set_ylim(0,1.42)
ax.legend(loc='upper left'); panel(ax,'a')
ax=axes[1]
for k,(mode,col,nm) in enumerate([('mm',BLUE,'absolute change (mm)'),('pct',VERM,'fractional change (%)')]):
    v=[100*cross[(i,r,mode)]/N for i,r,_ in cells]
    ax.bar(x+(k-0.5)*w,v,w*0.94,color=col,label=nm,edgecolor='white',linewidth=1.2)
    for xi,vv,c in zip(x+(k-0.5)*w,v,[cross[(i,r,mode)] for i,r,_ in cells]):
        ax.text(xi,vv+1.2,f'{c}',ha='center',va='bottom',fontsize=7,color=INK)
ax.set_xticks(x); ax.set_xticklabels(lab)
ax.set_ylabel(f'models whose own 95 % interval\nincludes zero (% of {N})'); ax.set_ylim(0,104)
ax.set_xlim(-0.6,3.6); ax.legend(loc='upper left'); panel(ax,'b')
fig.tight_layout(w_pad=2.6)
save(fig,'Figure12_sampling_partition')
