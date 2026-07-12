import json,glob,csv,re,os
# Build the claims register from the generated paper JSON (the source of the draft pages).
papers=[]
for fp in sorted(glob.glob('src/content/papers/*.json')):
    papers.append((os.path.basename(fp)[:-5], json.load(open(fp))))

base_url="/mom-meditation-microsite/research/"
rows=[]
for slug,d in papers:
    # Each key finding that asserts a benefit-relevant statement becomes a registered claim.
    for f in d["keyFindings"]:
        # skip non-claims (pointers)
        if re.search(r'see the linked paper',f,re.I): 
            continue
        rows.append({
          "page": base_url+slug+"/",
          "claim_text": re.sub(r'\s+',' ',f).strip()[:400],
          "claim_strength": d["claimStrength"],
          "study_type": d["studyType"],
          "source_doi": d["doi"],
          "practice_studied": d["practiceStudied"],
          "is_MoM": d["isMoM"],
          "theme": d["theme"],
          "null_or_critical": d.get("nullOrCritical",""),
          "bidmc": "Y" if d.get("bidmc") else "N",
          "reviewer_signoff": "",
        })
    # Mechanistic-transfer bridge claim ("Why this matters for the 7-minute practice")
    if d.get("whyItMatters"):
        rows.append({
          "page": base_url+slug+"/",
          "claim_text": d["whyItMatters"],
          "claim_strength": "Mechanistic-transfer inference (hedged; MoM not studied directly)",
          "study_type": d["studyType"],
          "source_doi": d["doi"],
          "practice_studied": d["practiceStudied"],
          "is_MoM": d["isMoM"],
          "theme": d["theme"],
          "null_or_critical": "mechanistic-transfer bridge ("+d.get("mechanismOverlap","")+")",
          "bidmc": "Y" if d.get("bidmc") else "N",
          "reviewer_signoff": "",
        })

# Write machine-readable CSV companion + human-readable markdown
with open('data/claims-register.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

# Markdown
by_theme={}
for r in rows: by_theme.setdefault(r["theme"],[]).append(r)
THEME_ORDER=['Stress & Anxiety','Sleep','Focus & Attention','Emotional Wellbeing','Brain & Mechanisms','Clinical Research','Brief & App-Based Practice']

lines=[]
lines.append("# CLAIMS-REGISTER.md\n")
lines.append("> **This register must be read in full, not skimmed (BRIEF §10).** Every health- or benefit-related statement that appears on a research page is logged here with the strength of evidence behind it, the exact source, the practice actually studied, and whether that practice is the Miracle of Mind practice. A qualified medical/scientific reviewer must co-sign each row (fill `reviewer_signoff`) before any production launch (BRIEF §11).\n")
lines.append("\n**Status:** DRAFT — generated from auto-drafted page content. No rows are signed off yet. Claims are drawn verbatim from each study's own abstract conclusions and phrased with claim-strength language; they have not yet been checked against full text or human-edited.\n")
lines.append(f"\n**Totals:** {len(rows)} registered claims across {len(papers)} papers. ")
nmom=sum(1 for r in rows if r['is_MoM']=='N'); adj=sum(1 for r in rows if r['is_MoM']=='adjacent')
lines.append(f"{adj} claims come from MoM-adjacent (breath-and-attention) practices; {nmom} from practices that are **not** the MoM practice (transfer gap noted on-page). \n")
lines.append("\n**Includes a distinct claim class:** *mechanistic-transfer inference* rows — the \"Why this matters for the 7-minute practice\" bridges. Each states MoM shares a specific mechanism (breath regulation and/or directed attention) with the studied practice and that a benefit *may* extend to MoM, always ending \"…though MoM hasn't been studied directly for this outcome.\" 72 papers carry one; 28 do not (no specific shared mechanism — see FLAGGED F24). These inferences need reviewer scrutiny of the *inference itself*, not just the source finding.\n")
lines.append("\nMachine-readable copy: `data/claims-register.csv`.\n")
lines.append("\n## How to read a row\n")
lines.append("- **Claim** — the statement as it appears (or is derived) on the page.\n- **Strength** — evidence tier framing (meta-analytic / randomized-trial / longitudinal / mechanistic). Claims must never be phrased more strongly than this.\n- **Practice / MoM?** — the practice actually studied, and whether it is the Miracle of Mind practice (Y), MoM-adjacent breath-and-attention (adjacent), or unrelated (N).\n- **Source** — DOI of the single paper on the same page supporting the claim.\n- **Sign-off** — blank until a qualified reviewer approves the claim and its phrasing.\n")

idx=1
for th in THEME_ORDER:
    rs=by_theme.get(th,[])
    if not rs: continue
    lines.append(f"\n---\n\n## {th}  ({len(rs)} claims)\n")
    for r in rs:
        doi = f"https://doi.org/{r['source_doi']}" if r['source_doi'] else "(no DOI)"
        mom = {"Y":"MoM practice","adjacent":"MoM-adjacent (breath/attention)","N":"NOT MoM — transfer gap"}[r['is_MoM']]
        flag = f" · _{r['null_or_critical']}_" if r['null_or_critical'] else ""
        bid = " · BIDMC Sadhguru Center" if r['bidmc']=='Y' else ""
        lines.append(f"\n**{idx}.** {r['claim_text']}{flag}{bid}  ")
        lines.append(f"\n&nbsp;&nbsp;• _Strength:_ {r['claim_strength']} ({r['study_type']}) &nbsp; • _Practice:_ {r['practice_studied']} — **{mom}** &nbsp; • _Source:_ {doi} &nbsp; • _Sign-off:_ ☐\n")
        idx+=1

open('CLAIMS-REGISTER.md','w').write("".join(lines))
print("registered claims:",len(rows))
print("papers covered:",len(papers))
print("claims by theme:",{t:len(by_theme.get(t,[])) for t in THEME_ORDER})
