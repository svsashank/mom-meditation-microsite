import json,glob,re,os,csv
ab=json.load(open('/tmp/abstracts.json')) if os.path.exists('/tmp/abstracts.json') else {}

# MoM mechanisms: (1) breath regulation (guided breath-based process),
# (2) directed attention, (3) brief guided daily format (~7 min).
RE_BREATH=re.compile(r'\b(breath|breathing|pranayam|respirat|sudarshan|bhastrika|bhramari|exhalation|inhalation|diaphragm|paced breathing|slow breathing|breathwork|nadi shodhana|kriya)\b',re.I)
RE_ATTN=re.compile(r'\b(focused[- ]attention|attention[- ]?monitoring|directed attention|sustained attention|attention to|mindful|mindfulness|concentrat|dharana|awareness of breath|breath[- ]?focused|open[- ]monitoring|meditat)\b',re.I)
RE_BRIEF=re.compile(r'\b(brief|short|daily|per day|minutes|min\b|single[- ]session|one session|app|smartphone|mobile|online|web[- ]based|internet[- ]based|self[- ]guided|guided (audio|meditation))\b',re.I)

# Practices that do NOT, on their own, share MoM's breath+attention core:
RE_TM=re.compile(r'transcendental meditation|\bTM\b|mantra',re.I)
RE_BODYSCAN_ONLY=re.compile(r'body[- ]scan',re.I)
RE_MOVEMENT=re.compile(r'\b(asana|posture|physical exercise|physical activity|aerobic|walking|movement|tai chi|qigong|hatha)\b',re.I)
RE_PMR=re.compile(r'progressive muscle relaxation|muscle relaxation',re.I)
RE_LOVINGKIND=re.compile(r'loving[- ]kindness|compassion meditation|metta',re.I)
RE_ISHA=re.compile(r'\bisha\b|isha kriya|inner engineering|shoonya|shambhavi|samyama|upa yoga',re.I)

rows=[]
for fp in sorted(glob.glob('src/content/papers/*.json')):
    d=json.load(open(fp))
    pmid=d['pmid']; abst=ab.get(pmid,{}).get('abstract','')
    hay=' '.join([d['title'],d.get('practiceStudied',''),abst])
    breath=bool(RE_BREATH.search(hay))
    attn=bool(RE_ATTN.search(hay))
    brief=bool(RE_BRIEF.search(hay))
    isha=bool(RE_ISHA.search(hay))
    # explicit weak-only signals
    tm=bool(RE_TM.search(hay)); pmr=bool(RE_PMR.search(hay)); lk=bool(RE_LOVINGKIND.search(hay))
    movement=bool(RE_MOVEMENT.search(hay)); bodyscan=bool(RE_BODYSCAN_ONLY.search(hay))
    prac=d.get('practiceStudied','')

    # Decide overlap
    overlaps=[]
    if breath: overlaps.append('breath')
    if attn: overlaps.append('attention')
    # brief only counts as an overlap ANCHOR if paired with breath/attention (delivery alone isn't a mechanism)
    decision='INCLUDE'; note=''
    mech=None

    if isha:
        mech="its breath-and-attention structure and brief, guided daily format"
        note="Isha practice — same family as MoM"
    elif breath and attn:
        mech="breath regulation and directed attention"
    elif breath:
        if re.search(r'sudarshan|pranayam|bhastrika|bhramari|yogic breath',hay,re.I):
            mech="yogic breath regulation"
        elif re.search(r'slow breathing|paced breathing|extended|exhalation',hay,re.I):
            mech="slow, paced breath regulation"
        else:
            mech="breath regulation"
    elif attn:
        # attention-only: acceptable if it's focused/mindful attention (MoM has directed attention)
        mech="directed attention (the focused-attention component)"
    else:
        decision='OMIT'; note='No breath or directed-attention component identifiable'

    # brief-daily refinement to the phrase (delivery format, only as add-on)
    if mech and brief and not isha and 'brief' not in mech:
        mech=mech+", delivered as a brief guided practice"

    # Borderline / weak-practice guards -> flag (may still include if breath/attn present)
    flags=[]
    if tm and not breath:
        decision='OMIT'; note='Transcendental Meditation (mantra-based, effortless) — not MoM\'s focused-attention/breath mechanism'
    if (pmr and not breath and not attn):
        decision='OMIT'; note='Progressive muscle relaxation — no breath/attention overlap'
    if bodyscan and not breath and not (attn and not bodyscan):
        # body scan alone
        decision='BORDERLINE'; note='Body-scan-based attention differs from MoM breath/attention focus'
    if lk and not breath:
        decision='BORDERLINE'; note='Loving-kindness/compassion focus; attention style differs from MoM'
    if movement and not breath and not attn:
        decision='OMIT'; note='Movement/exercise-led practice without breath or attention component'
    # generic multi-intervention reviews: practice vague
    if prac in ('mindfulness / meditation',) and not breath and re.search(r'(various|multiple|range of|different) (interventions|practices|techniques)',hay,re.I):
        decision='BORDERLINE'; note='Broad/mixed-intervention review; specific shared mechanism unclear'

    rows.append({'slug':os.path.basename(fp)[:-5],'pmid':pmid,'theme':d['theme'],'practice':prac,
      'breath':breath,'attn':attn,'brief':brief,'isha':isha,'decision':decision,'mechanism':mech or '',
      'note':note,'title':d['title'][:60]})

# report
from collections import Counter
print("decisions:",dict(Counter(r['decision'] for r in rows)))
print()
print("=== OMIT (no section; flag) ===")
for r in rows:
    if r['decision']=='OMIT': print(f"  [{r['theme'][:14]:14s}] {r['practice'][:28]:28s} | {r['note']} | {r['title']}")
print()
print("=== BORDERLINE (flag; decide) ===")
for r in rows:
    if r['decision']=='BORDERLINE': print(f"  [{r['theme'][:14]:14s}] {r['practice'][:28]:28s} | {r['note']} | {r['title']}")
json.dump(rows,open('/tmp/mech.json','w'),indent=1)
print("\nsaved /tmp/mech.json")
