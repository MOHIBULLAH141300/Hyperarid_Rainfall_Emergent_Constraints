# -*- coding: utf-8 -*-
import csv, math
from collections import defaultdict
rows=list(csv.DictReader(open('seasons_all.csv')))
fam={r['model']:r['family'] for r in csv.DictReader(open('wetseason_matrix_n33.csv'))}
D=defaultdict(list)
for r in rows:
    for idx in ('rx1day','r95p'):
        D[(r['model'],r['region'],r['period'],idx)].append((int(r['season']),float(r[idx])))
models=sorted(fam)
def mean(a): return sum(a)/len(a)
def pear(x,y):
    mx,my=mean(x),mean(y)
    num=sum((a-mx)*(b-my) for a,b in zip(x,y)); den=math.sqrt(sum((a-mx)**2 for a in x)*sum((b-my)**2 for b in y))
    return num/den if den else 0.0
def ser(m,reg,per,idx):
    v=D.get((m,reg,per,idx));  return [x for _,x in sorted(v)] if v else None
def oddeven(h):
    return mean(h[0::2]), mean(h[1::2])
print('%-7s %-5s | %-28s %-28s %-28s %-28s'%('idx','reg','r(Hfull, fut-Hfull) abs','r(Hodd, fut-Heven) abs','r(Hfull, pct) ','r(Hodd, pct vs Heven)'))
for idx in ('rx1day','r95p'):
    for reg in ('uae','east'):
        a1=[];b1=[];a2=[];b2=[];a3=[];b3=[];a4=[];b4=[]
        for m in models:
            h=ser(m,reg,'hist',idx); f=ser(m,reg,'fut',idx)
            if not h or not f: continue
            H=mean(h); F=mean(f); Ho,He=oddeven(h)
            a1.append(H); b1.append(F-H)
            a2.append(Ho); b2.append(F-He)
            a3.append(H); b3.append(100*(F-H)/H)
            a4.append(Ho); b4.append(100*(F-He)/He)
        print('%-7s %-5s | %+28.3f %+28.3f %+28.3f %+28.3f'%(idx,reg,pear(a1,b1),pear(a2,b2),pear(a3,b3),pear(a4,b4)))
