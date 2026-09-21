# -*- coding: utf-8 -*-
import csv, math
from collections import defaultdict
rows=list(csv.DictReader(open('seasons_all.csv')))
fam={r['model']:r['family'] for r in csv.DictReader(open('wetseason_matrix_n33.csv'))}
D=defaultdict(list)
for r in rows:
    for idx in ('rx1day','r95p'):
        D[(r['model'],r['region'],r['period'],idx)].append((int(r['season']),float(r[idx])))
def mean(a): return sum(a)/len(a)
def var(a): m=mean(a); return sum((x-m)**2 for x in a)/(len(a)-1)
def cov(x,y):
    mx,my=mean(x),mean(y); return sum((a-mx)*(b-my) for a,b in zip(x,y))/(len(x)-1)
def pear(x,y): return cov(x,y)/math.sqrt(var(x)*var(y)) if var(x)*var(y)>0 else 0
def ser(m,reg,per,idx):
    v=D.get((m,reg,per,idx)); return [x for _,x in sorted(v)] if v else None
print('Split-half behaviour of the HISTORICAL record, across 33 models')
print('%-7s %-5s | %8s %8s %8s | %8s %8s | %8s'%('idx','reg','r(Ho,He)','sd(Ho)','sd(Hfull)','r(Ho,F)','r(He,F)','r(H,F)'))
for idx in ('rx1day','r95p'):
    for reg in ('uae','east'):
        H=[];F=[];Ho=[];He=[]
        for m in sorted(fam):
            h=ser(m,reg,'hist',idx); f=ser(m,reg,'fut',idx)
            if not h or not f: continue
            H.append(mean(h)); F.append(mean(f)); Ho.append(mean(h[0::2])); He.append(mean(h[1::2]))
        print('%-7s %-5s | %+8.3f %8.3f %8.3f | %+8.3f %+8.3f | %+8.3f'%(idx,reg,pear(Ho,He),math.sqrt(var(Ho)),math.sqrt(var(H)),pear(Ho,F),pear(He,F),pear(H,F)))
print()
print('If the two disjoint halves of the same record were independent estimates of the')
print('same model-specific level, r(Ho,He) would be POSITIVE and sd(Ho) only slightly')
print('above sd(Hfull). A strong NEGATIVE r(Ho,He) with sd(Ho) ~ 2x sd(Hfull) indicates')
print('the halves are mechanically constrained by a quantity fixed over the full record.')
print()
# random split control for r95p uae: 200 random half/half splits
import random
random.seed(20260918)
idx,reg='r95p','uae'
series={}
for m in sorted(fam):
    h=ser(m,reg,'hist',idx)
    if h: series[m]=h
rs=[]
for _ in range(200):
    order=list(range(25)); random.shuffle(order); A=order[:13]; B=order[13:]
    a=[mean([series[m][i] for i in A]) for m in series]; b=[mean([series[m][i] for i in B]) for m in series]
    rs.append(pear(a,b))
rs.sort()
print('r95p uae: 200 RANDOM disjoint half-splits -> r(halfA,halfB) median %.3f, 5-95%% [%.3f, %.3f]'%(rs[100],rs[10],rs[190]))
