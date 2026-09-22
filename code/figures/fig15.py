import sys; sys.path.insert(0,'.')
from figstyle import *
import numpy as np, csv
from pathlib import Path
BASE=Path(__file__).resolve().parents[2]
rows=[r for r in csv.DictReader(open(BASE/'wetseason_matrix_n33.csv')) if r['dT_uae'] not in ('','nan')]
CC=0.07
cells=[('Rx1day','uae','dT_uae'),('R95p','uae','dT_uae'),('Rx1day','east','dT_east'),('R95p','east','dT_east')]
lab=[f'{i}\n{"UAE" if r=="uae" else "East"}' for i,r,_ in cells]
dyn=[]
for idx,reg,tc in cells:
    y=np.array([float(r[f'{idx}_{reg}_futpct']) for r in rows]); T=np.array([float(r[tc]) for r in rows])
    th=100*((1+CC)**T-1); res=y-th
    vt,vd=np.var(th,ddof=1),np.var(res,ddof=1); dyn.append(100*vd/(vt+vd))
fig,axes=plt.subplots(1,2,figsize=(7.1,3.0))
ax=axes[0]; x=np.arange(4)
ax.bar(x,dyn,0.58,color=BLUE,label='residual from Clausius-Clapeyron',edgecolor='white',linewidth=1.2)
ax.bar(x,[100-d for d in dyn],0.58,bottom=dyn,color=ORANGE,label='thermodynamic (7 % per K)',edgecolor='white',linewidth=1.2)
for xi,d in zip(x,dyn): ax.text(xi,d-4,f'{d:.1f} %',ha='center',va='top',fontsize=7.4,color='white',fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels(lab); ax.set_ylabel('share of summed component variance (%)')
ax.set_ylim(0,100); ax.legend(loc='lower center',bbox_to_anchor=(0.5,1.01),fontsize=7); panel(ax,'a')
ax=axes[1]
y=np.array([float(r['Rx1day_uae_futpct']) for r in rows]); T=np.array([float(r['dT_uae']) for r in rows])
th=100*((1+CC)**T-1)
ax.scatter(th,y,s=38,color=BLUE,zorder=3,edgecolor='white',linewidth=0.9)
lo=min(th.min(),y.min()); hi=max(th.max(),y.max()); pad=0.08*(hi-lo); lim=[lo-pad,hi+pad]
ax.plot(lim,lim,color=MUTED,lw=0.9,ls='--'); ax.text(lim[1]-0.04*(lim[1]-lim[0]),lim[1]-0.10*(lim[1]-lim[0]),'1:1',fontsize=7,color=MUTED,ha='right')
ax.axhline(0,color=MUTED,lw=0.7,ls=':')
ax.set_xlim(lim); ax.set_ylim(lim)
ax.set_xlabel('Clausius-Clapeyron expectation (%)'); ax.set_ylabel('projected Rx1day change, UAE (%)')
ax.set_title('projected change against its thermodynamic expectation',fontsize=7.6,color=MUTED,pad=6); panel(ax,'b')
fig.tight_layout(w_pad=2.4); save(fig,'Figure15_thermodynamic_dynamic')
