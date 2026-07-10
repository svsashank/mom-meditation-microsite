import json,time,urllib.parse,urllib.request,sys
EUTILS="https://eutils.ncbi.nlm.nih.gov/entrez/eutils"; HDRS={"User-Agent":"mom-microsite-harvester/1.0"}
def get(url):
    for a in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers=HDRS),timeout=25) as r:
                return r.read().decode("utf-8","replace")
        except Exception: time.sleep(1.2*(a+1))
    return ""
def esearch(term,retmax=60):
    d=get(EUTILS+"/esearch.fcgi?"+urllib.parse.urlencode({"db":"pubmed","term":term,"retmax":retmax,"retmode":"json"}))
    try: return json.loads(d)["esearchresult"].get("idlist",[])
    except: return []
# Sadhguru Center for a Conscious Planet @ BIDMC + Isha-practice studies
queries=[
 '"Sadhguru Center"[Affiliation]',
 '"Conscious Planet"[Affiliation]',
 '("Beth Israel Deaconess"[Affiliation]) AND ("meditation"[tiab] OR "yoga"[tiab] OR "Isha"[tiab] OR "Shoonya"[tiab])',
 '("Isha"[tiab] OR "Shoonya"[tiab] OR "Samyama"[tiab] OR "Inner Engineering"[tiab] OR "Shambhavi"[tiab]) AND ("meditation"[tiab] OR "yoga"[tiab] OR "meditators"[tiab])',
]
found={}
for q in queries:
    ids=esearch(q); found[q]=ids
    sys.stderr.write(f"{q[:45]:45s} -> {len(ids)}\n"); time.sleep(0.34)
bidmc=set()
for ids in found.values(): bidmc.update(ids)
json.dump(sorted(bidmc),open("/tmp/bidmc.json","w"))
sys.stderr.write(f"BIDMC/Isha-affiliated or Isha-practice unique: {len(bidmc)}\n")
# merge into main pool
col=json.load(open("/tmp/pmids.json"))
new=0
for p in bidmc:
    if p not in col:
        col[p]={"themes":["bidmc_isha"],"tiers":["cross_mech"],"yogic":True}; new+=1
    else:
        if "bidmc_isha" not in col[p]["themes"]: col[p]["themes"].append("bidmc_isha")
        col[p]["yogic"]=True
json.dump(col,open("/tmp/pmids.json","w"))
sys.stderr.write(f"newly added to pool: {new}; pool now {len(col)}\n")
