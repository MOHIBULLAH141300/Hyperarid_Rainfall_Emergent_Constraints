# -*- coding: utf-8 -*-
"""Clean emergent-constraint formulation: predict FUTURE LEVEL from HISTORICAL LEVEL.
No sampling error is shared between predictor and predictand."""
import csv, math, random
from collections import defaultdict

rows=list(csv.DictReader(open('seasons_all.csv')))
fam={}
for r in csv.DictReader(open('wetseason_matrix_n33.csv')): fam[r['model']]=r['family']

D=defaultdict(list)   # (model,region,period,index) -> [season values]
for r in rows:
    for idx in ('rx1day','r95p'):
        D[(r['model'],r['region'],r['period'],idx)].append((int(r['season']),float(r[idx])))
models=sorted({r['model'] for r in rows})
models=[m for m in models if m in fam]
print('models with family:',len(models))

def mean(a): return sum(a)/len(a)
def sd(a):
    m=mean(a); return math.sqrt(sum((x-m)**2 for x in a)/(len(a)-1))
def pear(x,y):
    mx,my=mean(x),mean(y)
    num=sum((a-mx)*(b-my) for a,b in zip(x,y))
    den=math.sqrt(sum((a-mx)**2 for a in x)*sum((b-my)**2 for b in y))
    return num/den if den else 0.0
def pval(r,n):
    if abs(r)>=1: return 0.0
    t=abs(r)*math.sqrt((n-2)/(1-r*r))
    # two-sided t approx via normal for n>=30
    z=t*(1-1/(4*(n-2)))/math.sqrt(1+t*t/(2*(n-2)))
    return math.erfc(z/math.sqrt(2))

def series(m,reg,per,idx):
    v=D.get((m,reg,per,idx))
    return [x for _,x in sorted(v)] if v else None

def ols(x,y):
    mx,my=mean(x),mean(y)
    b=sum((a-mx)*(c-my) for a,c in zip(x,y))/sum((a-mx)**2 for a in x)
    return my-b*mx, b

def skill(pred,obs,trainmean):
    ss=sum((o-p)**2 for p,o in zip(pred,obs)); s0=sum((o-trainmean)**2 for o in obs)
    return 1-ss/s0 if s0 else float('nan')

print('\n%-8s %-6s | %7s %7s %8s | %7s %7s | %s'%('index','region','r','p','n','LOO','LOFO','note'))
OUT={}
for idx in ('rx1day','r95p'):
    for reg in ('uae','east'):
        X=[];Y=[];M=[]
        for m in models:
            h=series(m,reg,'hist',idx); f=series(m,reg,'fut',idx)
            if not h or not f: continue
            X.append(mean(h)); Y.append(mean(f)); M.append(m)
        n=len(X); r=pear(X,Y); p=pval(r,n)
        # leave-one-out
        pr=[]
        for i in range(n):
            xs=[X[j] for j in range(n) if j!=i]; ys=[Y[j] for j in range(n) if j!=i]
            a,b=ols(xs,ys); pr.append(a+b*X[i])
        loo=skill(pr,Y,mean(Y))
        # leave-one-family-out
        fams=sorted({fam[m] for m in M}); pr2=[];ob2=[]
        for fm in fams:
            tr=[j for j in range(n) if fam[M[j]]!=fm]; te=[j for j in range(n) if fam[M[j]]==fm]
            a,b=ols([X[j] for j in tr],[Y[j] for j in tr])
            for j in te: pr2.append(a+b*X[j]); ob2.append(Y[j])
        lofo=skill(pr2,ob2,mean(Y))
        OUT[(idx,reg)]=dict(X=X,Y=Y,M=M,r=r,p=p,n=n,loo=loo,lofo=lofo,nfam=len(fams))
        print('%-8s %-6s | %+7.3f %7.4f %8d | %+7.3f %+7.3f | %d families'%(idx,reg,r,p,n,loo,lofo,len(fams)))

import json
json.dump({f'{k[0]}_{k[1]}':{kk:vv for kk,vv in v.items()} for k,v in OUT.items()},open('ec_futlevel.json','w'))
print('\nsaved ec_futlevel.json')
