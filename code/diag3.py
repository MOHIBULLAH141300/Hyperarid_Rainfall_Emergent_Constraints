# -*- coding: utf-8 -*-
import csv, math, random
from collections import defaultdict
random.seed(20260918)
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
def pear(x,y):
    v=var(x)*var(y); return cov(x,y)/math.sqrt(v) if v>0 else 0.0
def ser(m,reg,per,idx):
    v=D.get((m,reg,per,idx)); return [x for _,x in sorted(v)] if v else None

print("="*78)
print("COMPLETED DIAGNOSIS OF THE 'SURVIVING' R95p CONSTRAINT")
print("="*78)
for idx in ('r95p','rx1day'):
  for reg in ('uae','east'):
    H=[];F=[];Ho=[];He=[];S=[]
    for m in sorted(fam):
        h=ser(m,reg,'hist',idx); f=ser(m,reg,'fut',idx)
        if not h or not f: continue
        H.append(mean(h)); F.append(mean(f)); Ho.append(mean(h[0::2])); He.append(mean(h[1::2])); S.append(h)
    n=len(H); d=[F[i]-He[i] for i in range(n)]
    r_obs=pear(Ho,d)
    # surrogate 1: permute F across models -> destroys any real hist->fut link,
    # keeps the mechanical Ho/He anticorrelation intact
    null=[]
    for _ in range(5000):
        Fp=F[:]; random.shuffle(Fp)
        null.append(pear(Ho,[Fp[i]-He[i] for i in range(n)]))
    null.sort()
    p_sur=sum(1 for v in null if v>=r_obs)/len(null)
    # surrogate 2: 500 RANDOM disjoint splits instead of odd/even
    rr=[]
    for _ in range(500):
        o=list(range(len(S[0]))); random.shuffle(o); A=o[:len(o)//2]; B=o[len(o)//2:]
        a=[mean([S[i][j] for j in A]) for i in range(n)]
        b=[mean([S[i][j] for j in B]) for i in range(n)]
        rr.append(pear(a,[F[i]-b[i] for i in range(n)]))
    rr.sort()
    print("\n%s / %s   (n=%d)"%(idx.upper(),reg,n))
    print("  r(H_full , F)                       = %+0.3f   <- does historical level predict future level?"%pear(H,F))
    print("  r(H_odd  , H_even)                  = %+0.3f   <- should be POSITIVE if halves are independent"%pear(Ho,He))
    print("  r(H_odd  , F)                       = %+0.3f"%pear(Ho,F))
    print("  r(H_even , F)                       = %+0.3f   <- opposite sign to r(H_odd,F) => split artifact"%pear(He,F))
    print("  r(H_odd  , F - H_even)  [PUBLISHED] = %+0.3f"%r_obs)
    print("  null from permuting F  : median %+0.3f, 95%% CI [%+0.3f, %+0.3f], p = %.3f"%(null[2500],null[125],null[4875],p_sur))
    print("  500 random half-splits : median %+0.3f, 95%% CI [%+0.3f, %+0.3f]"%(rr[250],rr[12],rr[487]))
