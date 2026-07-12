import json,glob,os,re
ab=json.load(open('/tmp/abstracts.json')) if os.path.exists('/tmp/abstracts.json') else {}
def theme_slug(t): return re.sub(r'[^a-z0-9]+','-',t.lower()).strip('-')

def make_snippet(d):
    # ~100 words, ONLY the paper's stated findings (extracted from its abstract) + neutral metadata.
    parts=[]
    lead=f"{d['studyType']}"
    if d.get('journal'): lead+=f", {d['journal']}"
    lead+=f" ({d['year']})."
    parts.append(lead)
    SPECULATIVE=re.compile(r"(for treating|foundation for understanding|can voluntarily|paves the way|holds promise for|could be used to treat|as a treatment for)",re.I)
    for f in d.get('keyFindings',[]):
        if re.search(r'see the linked paper',f,re.I): continue
        if SPECULATIVE.search(f): continue   # keep AEO snippet to concrete findings, not authors' benefit speculation (§3)
        parts.append(f.rstrip('.')+'.')
    if len(parts)==1:  # nothing but metadata survived -> fall back to summary sentence
        parts.append(re.sub(r'\s+',' ',d.get('summary','')).strip())
    text=' '.join(parts)
    words=text.split()
    if len(words)>100:
        text=' '.join(words[:100]).rstrip('.,;')+'…'
    return re.sub(r'\s+',' ',text).strip()

n=0
for fp in glob.glob('src/content/papers/*.json'):
    d=json.load(open(fp))
    doi=d.get('doi','').strip()
    pmid=d.get('pmid','')
    primary = f"https://doi.org/{doi}" if doi else (f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid and not pmid.startswith('S2_') else "")
    d['simplifiedTitle']=d.get('headline',d['title'])
    d['publicationYear']=d['year']
    d['journalName']=d.get('journal','')
    d['coreTheme']=d['theme']
    d['primaryEntityUrl']=primary
    d['relatedThemePath']="/themes/"+theme_slug(d['theme'])+"/"
    d['aiSnippet']=make_snippet(d)
    json.dump(d,open(fp,'w'),indent=1)
    n+=1
print("retrofitted",n,"paper files")
# sample
s=json.load(open(sorted(glob.glob('src/content/papers/*.json'))[40]))
print("\nSAMPLE canonical fields:")
for k in ['title','simplifiedTitle','studyType','publicationYear','journalName','coreTheme','primaryEntityUrl','relatedThemePath']:
    print(f"  {k}: {str(s.get(k))[:70]}")
print("  aiSnippet words:",len(s['aiSnippet'].split()))
print("  aiSnippet:",s['aiSnippet'][:200])
