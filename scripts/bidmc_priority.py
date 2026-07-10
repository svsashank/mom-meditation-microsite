import json,time,urllib.parse,urllib.request,sys
E="https://eutils.ncbi.nlm.nih.gov/entrez/eutils";H={"User-Agent":"mom/1.0"}
def get(u):
    for a in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=25) as r: return r.read().decode("utf-8","replace")
        except: time.sleep(1.2*(a+1))
    return ""
def es(t):
    d=get(E+"/esearch.fcgi?"+urllib.parse.urlencode({"db":"pubmed","term":t,"retmax":60,"retmode":"json"}))
    try: return json.loads(d)["esearchresult"].get("idlist",[])
    except: return []
pri=set()
for q in ['"Sadhguru Center"[Affiliation]','"Conscious Planet"[Affiliation]']:
    pri.update(es(q)); time.sleep(0.34)
json.dump(sorted(pri),open("/tmp/bidmc_priority.json","w"))
print("Sadhguru Center priority set:",len(pri),file=sys.stderr)
