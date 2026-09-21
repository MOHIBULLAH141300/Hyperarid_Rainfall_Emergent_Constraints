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
def pear(x,y): return cov(x,y)/math.sqrt(var(x)*var(y))
def ser(m,reg,per,idx):
    v=D.get((m,reg,per,idx)); return [x for _,x in sorted(v)] if v else None
idx,reg='r95p','uae'
H=[];F=[];Ho=[];He=[];M=[];nh=[];nf=[]
for m in sorted(fam):
    h=ser(m,reg,'hist',idx); f=ser(m,reg,'fut',idx)
    if not h or not f: continue
    M.append(m); H.append(mean(h)); F.append(mean(f)); Ho.append(mean(h[0::2])); He.append(mean(h[1::2]))
    nh.append(len(h)); nf.append(len(f))
print('n models',len(M),'hist seasons',sorted(set(nh)),'fut seasons',sorted(set(nf)))
print('sd(H)=%.3f sd(F)=%.3f sd(Ho)=%.3f sd(He)=%.3f'%(math.sqrt(var(H)),math.sqrt(var(F)),math.sqrt(var(Ho)),math.sqrt(var(He))))
print('r(H,F)=%.3f  r(Ho,He)=%.3f  r(Ho,F)=%.3f  r(He,F)=%.3f'%(pear(H,F),pear(Ho,He),pear(Ho,F),pear(He,F)))
print('cov(H,F)=%.3f  var(H)=%.3f'%(cov(H,F),var(H)))
print('cov(Ho,F)-cov(Ho,He) = %.3f - %.3f = %.3f'%(cov(Ho,F),cov(Ho,He),cov(Ho,F)-cov(Ho,He)))
d=[F[i]-He[i] for i in range(len(M))]
print('r(Ho, F-He) = %.3f'%pear(Ho,d))
# influence: drop each model
base=pear(Ho,d)
infl=sorted(((abs(base-pear([Ho[j] for j in range(len(M)) if j!=i],[d[j] for j in range(len(M)) if j!=i])),M[i],Ho[i],F[i]) for i in range(len(M))),reverse=True)
print('\nmost influential models on r(Ho,F-He):')
for a,m,ho,f in infl[:5]: print('   %-18s dr=%.3f  Ho=%7.2f F=%7.2f'%(m,a,ho,f))
print('\nlargest Ho:',sorted(zip(Ho,M),reverse=True)[:4])
print('largest F :',sorted(zip(F,M),reverse=True)[:4])
