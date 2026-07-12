import json,glob,os
mech={r['pmid']:r for r in json.load(open('/tmp/mech.json'))}
FINAL_CLAUSE=" — though MoM hasn't been studied directly for this outcome."

def clean_mech(m):
    # natural phrasing for the [mechanism] slot
    m=m.replace(", delivered as a brief guided practice"," in a brief, guided format")
    return m

n_inc=n_omit=0
for fp in glob.glob('src/content/papers/*.json'):
    d=json.load(open(fp))
    r=mech.get(d['pmid'])
    if not r:  # safety
        d['whyItMatters']=''; d['mechanismOverlap']=''; d['mechanismGap']=''
        json.dump(d,open(fp,'w'),indent=1); continue
    if r['decision']=='INCLUDE':
        mm=clean_mech(r['mechanism'])
        d['whyItMatters']=(f"MoM shares {mm} with the practice studied here. "
          "Because the benefit is linked to that mechanism rather than to any one method, "
          "it's reasonable to expect it may extend to MoM as well" + FINAL_CLAUSE)
        d['mechanismOverlap']=('isha' if r['isha'] else ('breath+attention' if (r['breath'] and r['attn']) else ('breath' if r['breath'] else 'attention')))
        d['mechanismGap']=''
        n_inc+=1
    else:
        d['whyItMatters']=''
        d['mechanismOverlap']='none'
        d['mechanismGap']=("The practice in this study does not share a specific breath-regulation or "
          "directed-attention mechanism with the Miracle of Mind practice, so no practice bridge is drawn here.")
        n_omit+=1
    json.dump(d,open(fp,'w'),indent=1)
print(f"applied: {n_inc} bridges, {n_omit} gap-notes")
# sanity: final clause never dropped
bad=[fp for fp in glob.glob('src/content/papers/*.json')
     if (json.load(open(fp)).get('whyItMatters') and not json.load(open(fp))['whyItMatters'].endswith("this outcome."))]
print("bridges missing final clause:",len(bad))
