# -*- coding: utf-8 -*-
import sys, io, re
sys.path.insert(0,'.')
import newblocks as NB
lines=[l for l in open('existing_manuscript_text.txt',encoding='utf8').read().split('\n') if l.strip()]
recs=[(l.split('\t',1)[0], l.split('\t',1)[1]) for l in lines if '\t' in l]
out=[]
def emit(s): out.append(s)
# --- front matter ---
emit('# '+NB.TITLE); emit('')
for k,t in recs[1:7]: emit(t)
emit('')
emit('## Abstract'); emit(''); emit(NB.ABSTRACT); emit(''); emit(NB.KEYWORDS); emit('')
emit('## Copyright statement'); emit(''); emit('[To be completed on submission.]'); emit('')
# --- walk sections ---
i=0
# find index of "1. Introduction"
while not (recs[i][0].startswith('H') and recs[i][1].startswith('1. Introduction')): i+=1
SKIP_SECTIONS = {'Highlights','Declaration of generative AI and AI-assisted technologies in the manuscript preparation process'}
REPLACE_PARA = {}   # exact-prefix -> new text
REPLACE_PARA['The analysis addresses four questions.'] = NB.INTRO_Q
cur=None
while i < len(recs):
    kind, t = recs[i]
    if kind.startswith('H'):
        cur = t
        if t in SKIP_SECTIONS:
            i+=1
            while i<len(recs) and not recs[i][0].startswith('H'): i+=1
            continue
        lvl = '#'*(1+int(kind[-1])) if kind[-1].isdigit() else '##'
        # rename Elsevier back matter to Copernicus
        ren = {'CRediT authorship contribution statement':'Author contribution',
               'Declaration of competing interest':'Competing interests',
               'Data and code availability':'Data availability',
               'Funding':'Financial support'}
        emit(''); emit(lvl+' '+ren.get(t,t)); emit('')
        # whole-section replacements
        if t.startswith('3.6 Relationship'):
            emit(NB.RESULTS_36_NEW); emit('')
            emit('### 3.7 Effect of bias-corrected downscaling on inter-model spread'); emit(''); emit(NB.RESULTS_37_NEW); emit('')
            emit('### 3.8 Thermodynamic and dynamic partition, and scaling with regional warming'); emit(''); emit(NB.RESULTS_38_NEW); emit('')
            i+=1
            while i<len(recs) and not recs[i][0].startswith('H'):
                tt=recs[i][1]
                if tt.startswith('Table 8') or tt.startswith('Table 9') or tt.startswith('Figure 9') or tt.startswith('Figure 10') or tt.startswith('Figure 11'):
                    emit('> '+tt); emit('')
                i+=1
            continue
        if t.startswith('4.4 Historical fidelity'):
            emit(NB.DISC_44_NEW); emit(''); i+=1
            while i<len(recs) and not recs[i][0].startswith('H'): i+=1
            continue
        if t.startswith('4.5 Internal variability'):
            emit(NB.DISC_45_NEW); emit(''); i+=1
            while i<len(recs) and not recs[i][0].startswith('H'): i+=1
            continue
        if t.startswith('5. Conclusions'):
            emit(NB.CONCLUSIONS_NEW); emit(''); i+=1
            while i<len(recs) and not recs[i][0].startswith('H'): i+=1
            continue
        i+=1; continue
    # paragraph
    rep=None
    for pre,newt in REPLACE_PARA.items():
        if t.startswith(pre): rep=newt; break
    if rep: emit(rep); emit('')
    else:
        emit(t); emit('')
        if cur and cur.startswith('2.2 Observations') and t.startswith('Historical monthly fields'):
            emit(NB.METHODS_22_ADD); emit('')
        if cur and cur.startswith('4.7 Limitations') and t.startswith('Operational cloud seeding'):
            emit(NB.DISC_47_ADD); emit('')
    if cur and cur.startswith('2.6 Constraint-testing') and t.startswith('Leave-one-family-out cross-validation'):
        emit(NB.METHODS_26_ADD); emit('')
    i+=1
txt='\n'.join(out)
open('Rainfall_Paper_REVISED_v15.md','w',encoding='utf8').write(txt)
print('words:',len(txt.split()))
print('sections:',sum(1 for l in out if l.startswith('#')))
