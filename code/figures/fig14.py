import sys; sys.path.insert(0,'.')
from figstyle import *
import numpy as np, csv, os, re, glob
BASE=os.path.expanduser('~/mnt/RAINFALL PAPER B/reanalysis_2026-09-18')
norm=lambda s: re.sub(r'[^a-z0-9]','',s.lower())
raw={}
for f in sorted(glob.glob(f'{BASE}/raw_*.csv')):
    for r in csv.DictReader(open(f)): raw[norm(r['model'])]=(float(r['rx1day']),float(r['r95p']))
nex={}
for r in csv.DictReader(open(f'{BASE}/wetseason_matrix_n33.csv')):
    nex[norm(r['model'])]=(float(r['Rx1day_uae_histlevel']),float(r['R95p_uae_histlevel']))
com=sorted(set(raw)&set(nex))
R=np.array([raw[m][0] for m in com]); N=np.array([nex[m][0] for m in com])
R9=np.array([raw[m][1] for m in com]); N9=np.array([nex[m][1] for m in com])
fig,axes=plt.subplots(1,3,figsize=(9.4,3.05))
for ax,(r,n,nm,col,ltr) in zip(axes[:2],[(R,N,'Rx1day',BLUE,'a'),(R9,N9,'R95p',VERM,'b')]):
    ax.scatter(r,n,s=38,color=col,zorder=3,edgecolor='white',linewidth=0.9)
    lim=[0,max(r.max(),n.max())*1.08]
    ax.plot(lim,lim,color=MUTED,lw=0.9,ls='--'); ax.text(lim[1]*0.80,lim[1]*0.86,'1:1',fontsize=7,color=MUTED)
    ax.set_xlim(lim); ax.set_ylim(lim)
    ax.set_xlabel(f'raw CMIP6 {nm} (mm)'); ax.set_ylabel(f'NEX-GDDP {nm} (mm)')
    ax.text(0.04,0.95,f'r = {np.corrcoef(r,n)[0,1]:+.2f}',transform=ax.transAxes,color=col,fontsize=8.5,va='top',fontweight='bold')
    ax.set_title(f'present-day {nm}, {len(com)} matched models',fontsize=7.6,color=MUTED,pad=6); panel(ax,ltr)
ax=axes[2]; x=np.arange(2); w=0.34
cvr=[R.std(ddof=1)/R.mean(), R9.std(ddof=1)/R9.mean()]
cvn=[N.std(ddof=1)/N.mean(), N9.std(ddof=1)/N9.mean()]
ax.bar(x-w/2,cvr,w*0.94,color=MUTED,label='raw CMIP6',edgecolor='white',linewidth=1.2)
ax.bar(x+w/2,cvn,w*0.94,color=GREEN,label='NEX-GDDP (BCSD)',edgecolor='white',linewidth=1.2)
for xi,v in zip(x-w/2,cvr): ax.text(xi,v+0.012,f'{v:.3f}',ha='center',va='bottom',fontsize=7)
for xi,v in zip(x+w/2,cvn): ax.text(xi,v+0.012,f'{v:.3f}',ha='center',va='bottom',fontsize=7)
for xi,a,b in zip(x,cvr,cvn):
    ax.text(xi,max(a,b)+0.075,'\u2212%.0f%% normalised\nvariance'%(100*(1-(b/a)**2)),ha='center',va='bottom',fontsize=6.8,color=INK,linespacing=1.1)
ax.set_xticks(x); ax.set_xticklabels(['Rx1day','R95p']); ax.set_ylabel('coefficient of variation across models')
ax.set_ylim(0,0.88); ax.legend(loc='upper left'); panel(ax,'c')
fig.tight_layout(w_pad=2.2); save(fig,'Figure14_downscaling_spread')
