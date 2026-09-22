# -*- coding: utf-8 -*-
"""Figure: pre-specified constraint battery. Diverging colour for signed correlation,
neutral grey midpoint; survivors marked by outline + asterisk (never colour alone)."""
import csv, os, numpy as np
from figstyle import *
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
SRC=os.path.expanduser('~/mnt/RAINFALL PAPER B/reanalysis_2026-09-18/multiscenario/battery_results.csv')
R=list(csv.DictReader(open(SRC)))
SC=['ssp126','ssp245','ssp370','ssp585']
SCL=['SSP1-2.6','SSP2-4.5','SSP3-7.0','SSP5-8.5']
ORDERP=[('A','PFS'),
        ('B','Rx1day climatology'),('B','R95p climatology'),('B','R99p climatology'),
        ('B','tail concentration R95p/PRCPTOT'),('B','event duration Rx5day/Rx1day'),('B','wet-day frequency'),
        ('C','interannual variability Rx1day'),('C','interannual variability R95p'),
        ('C','historical trend Rx1day'),('C','historical trend R95p')]
LAB={'PFS':'Process Fidelity Score','Rx1day climatology':'Rx1day climatology','R95p climatology':'R95p climatology',
 'R99p climatology':'R99p climatology','tail concentration R95p/PRCPTOT':'Tail concentration  R95p/PRCPTOT',
 'event duration Rx5day/Rx1day':'Event duration  Rx5day/Rx1day','wet-day frequency':'Wet-day frequency',
 'interannual variability Rx1day':'Interannual variability, Rx1day','interannual variability R95p':'Interannual variability, R95p',
 'historical trend Rx1day':'Historical trend, Rx1day','historical trend R95p':'Historical trend, R95p'}
# diverging: blue (negative) - neutral grey - vermillion (positive); no hue at the midpoint
cmap=LinearSegmentedColormap.from_list('div',[BLUE,'#EDEDED',VERM])
norm=TwoSlopeNorm(vmin=-1,vcenter=0,vmax=1)
D={(d['region'],d['predictor'],d['index'],d['scenario']):d for d in R}
def gate(d): return float(d['q_BH'])<0.05 and float(d['LOFO'])>0 and float(d['sign_stability'])>0.9
panels=[('uae','rx1day','UAE  ·  Rx1day'),('uae','r95p','UAE  ·  R95p'),
        ('east','rx1day','Eastern  ·  Rx1day'),('east','r95p','Eastern  ·  R95p')]
fig,axes=plt.subplots(1,4,figsize=(10.4,4.5),sharey=True)
for ax,(reg,idx,title),L in zip(axes,panels,'abcd'):
    M=np.full((len(ORDERP),4),np.nan)
    for i,(g,p) in enumerate(ORDERP):
        for j,s in enumerate(SC):
            d=D.get((reg,p,idx,s))
            if d: M[i,j]=float(d['r'])
    ax.imshow(M,cmap=cmap,norm=norm,aspect='auto',interpolation='nearest')
    ax.set_xticks(range(4)); ax.set_xticklabels(SCL,rotation=45,ha='right')
    ax.set_yticks(range(len(ORDERP)))
    ax.grid(False); ax.tick_params(axis='y',length=0)
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.set_xticks(np.arange(-.5,4,1),minor=True); ax.set_yticks(np.arange(-.5,len(ORDERP),1),minor=True)
    ax.grid(which='minor',color='white',linewidth=1.6); ax.tick_params(which='minor',length=0)
    for i,(g,p) in enumerate(ORDERP):
        for j,s in enumerate(SC):
            d=D.get((reg,p,idx,s))
            if not d: continue
            r=float(d['r'])
            ax.text(j,i,('%+.2f'%r).replace('0.','.'),ha='center',va='center',fontsize=6.2,
                    color='white' if abs(r)>0.55 else INK)
            if gate(d):
                ax.add_patch(plt.Rectangle((j-.5,i-.5),1,1,fill=False,edgecolor=INK,linewidth=1.5,zorder=5))
                ax.text(j+.34,i-.30,'*',ha='center',va='center',fontsize=9,color=INK,fontweight='bold',zorder=6)
    ax.set_title(title,pad=6); panel(ax,L)
axes[0].set_yticklabels([LAB[p] for g,p in ORDERP])
# family brackets
for y0,y1,lab in [(-0.5,0.5,'A'),(0.5,6.5,'B'),(6.5,10.5,'C')]:
    axes[0].plot([-3.15,-3.15],[y0,y1],color=MUTED,lw=1.1,clip_on=False)
    axes[0].text(-3.35,(y0+y1)/2,lab,ha='center',va='center',fontsize=8,fontweight='bold',color=MUTED,clip_on=False)
cb=fig.colorbar(plt.cm.ScalarMappable(norm=norm,cmap=cmap),ax=axes,fraction=0.018,pad=0.015)
cb.set_label('Correlation with projected absolute change',fontsize=7.5)
cb.outline.set_visible(False); cb.ax.tick_params(labelsize=7)
fig.text(0.5,-0.06,'Bold outline and asterisk: satisfies all pre-specified criteria '
 '(q < 0.05, leave-one-family-out skill > 0, sign stability > 0.9). '
 'Families: A process fidelity, B present-day extreme state, C variability and historical change.',
 ha='center',fontsize=7,color=MUTED)
save(fig,'Figure17_constraint_battery')
