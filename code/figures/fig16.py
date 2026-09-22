import sys; sys.path.insert(0,'.')
from figstyle import *
import numpy as np, csv, os
BASE=os.path.expanduser('~/mnt/RAINFALL PAPER B/reanalysis_2026-09-18')
rows=[r for r in csv.DictReader(open(f'{BASE}/wetseason_matrix_n33.csv')) if r['dT_uae'] not in ('','nan')]
cells=[('Rx1day','uae','dT_uae','UAE'),('R95p','uae','dT_uae','UAE'),('Rx1day','east','dT_east','East'),('R95p','east','dT_east','East')]
fig,axes=plt.subplots(2,2,figsize=(7.1,5.6))
for ax,(idx,reg,tc,rn),ltr in zip(axes.ravel(),cells,'abcd'):
    y=np.array([float(r[f'{idx}_{reg}_futpct']) for r in rows]); T=np.array([float(r[tc]) for r in rows])
    r_=np.corrcoef(T,y)[0,1]; n=len(T); t=r_*np.sqrt((n-2)/(1-r_**2))
    import math; p_=math.erfc(abs(t)/math.sqrt(2))
    b,a=np.polyfit(T,y,1)
    ax.scatter(T,y,s=34,color=BLUE,zorder=3,edgecolor='white',linewidth=0.9)
    xx=np.linspace(T.min(),T.max(),50); ax.plot(xx,a+b*xx,color=BLUE,lw=1.8,label='least-squares fit')
    cc=100*((1.07)**xx-1); cc=cc-cc.mean()+ (a+b*xx).mean()
    ax.plot(xx,cc,color=ORANGE,lw=1.5,ls='--',label='Clausius-Clapeyron slope (7 % per K)')
    ax.axhline(0,color=MUTED,lw=0.7,ls=':')
    ax.set_xlabel('projected regional warming (K)'); ax.set_ylabel(f'projected {idx} change (%)')
    ax.set_title(f'{idx}, {rn}',fontsize=8,color=MUTED,pad=5)
    ps = 'p < 0.001' if p_ < 0.001 else f'p = {p_:.3f}'
    ax.text(0.04,0.95,f'r = {r_:+.2f}, {ps}',transform=ax.transAxes,fontsize=7.6,va='top',color=INK)
    ax.text(0.97,0.05,f'{b:+.1f} % per K',transform=ax.transAxes,fontsize=7.6,ha='right',va='bottom',color=BLUE,fontweight='bold')
    panel(ax,ltr)
h,l=axes[0,0].get_legend_handles_labels()
fig.legend(h,l,loc='lower center',ncol=2,fontsize=7.4,bbox_to_anchor=(0.5,-0.02))
fig.tight_layout(w_pad=2.4,h_pad=2.6,rect=(0,0.035,1,1)); save(fig,'Figure16_warming_scaling')
