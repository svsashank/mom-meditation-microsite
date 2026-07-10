# DECISIONS.md

Running log of non-obvious judgment calls made under the standing authority of
BRIEF.md §9. Each entry: the call, the reasoning, and the brief clause it traces
to. Lowest-confidence calls are additionally surfaced in `FLAGGED.md`.

Scope of this log so far: **Phase 1** — authoring the two skills (§8) and
building the paper longlist (§5). Content production, per-paper pages, and the
CLAIMS-REGISTER are downstream.

---

## A. Skills (§8)

**A1. Two skills authored as Claude/Cowork skills with YAML frontmatter + SKILL.md.**
`research-summary` and `wisdom-pairing` live under `skills/`. Each encodes the
brief's rules as an executable procedure with a self-check list, so downstream
content work is constrained by §3 automatically rather than by memory.

**A2. `research-summary` treats the claim-strength vocabulary as a hard mapping,
not guidance.** Each evidence tier has permitted sentence stems and an explicit
"never say" column (§3 claims discipline). Cross-sectional/mechanistic evidence
is barred from causal verbs. Rationale: the brief calls claims discipline
"non-negotiable," so the skill enforces downgrade-by-default.

**A3. Banned-phrases list is a superset of the brief's explicit bans.** The brief
names "cures/treats/heals" and "no medical advice." I extended this to the
wellness-cliché register the brief's voice section rejects (boosts, rewires,
detoxes, clinically proven, exclamation points, second-person health promises).
Rationale: §3 voice rules + claims discipline read together. Flagged as a
judgment call (F1) because the exact boundary is editorial.

**A4. `wisdom-pairing` enforces verbatim-only with a "cannot verify → do not use"
stop.** No paraphrase, no synthesis, no third-party quote aggregators — only the
two Isha URLs in §8/§13. Each quote requires a full sourcing block incl.
`verified_on`. Rationale: §3 Sadhguru-layer rules are strict; the skill fails
closed.

**A5. Theme-matching rule: pair on "what the mind does," never on the study
metric.** The framing sentence may not assert the quote confirms or is confirmed
by the research. Rationale: §3 requires the two layers stay editorially distinct;
this prevents an implicit evidentiary bridge from wisdom to health claim.

---

## B. Longlist sources & method (§5)

**B1. Primary source = PubMed E-utilities; citation signal = NIH iCite.**
Semantic Scholar's API returned empty responses in this environment, so it was
not usable. PubMed (esearch/esummary) supplied search + metadata; NIH iCite
supplied citation_count and the Relative Citation Ratio (RCR). Traces to §5
("Semantic Scholar + PubMed APIs"). Flagged (F2): Semantic Scholar coverage is
therefore absent from this pass.

**B2. "Citation count normalized by publication year" implemented via iCite RCR
where available, citations-per-year as fallback.** RCR is field- and
time-normalized (1.0 = NIH average), which matches the brief's intent better
than raw counts and prevents older papers from dominating purely on age. Recent
papers without an RCR yet use a capped citations-per-year proxy. Traces to §5
"impact signal."

**B3. Evidence hierarchy encoded as a tier score.** meta-analysis/systematic
review (5) > RCT (4) > cohort/longitudinal (3) > cross-sectional/mechanistic
(2). Tier is taken as the *best* tier a paper qualifies for, upgraded using
PubMed publication types when present (e.g. an item tagged "Meta-Analysis"[pt] is
scored as meta regardless of which query surfaced it). Traces to §5 evidence
hierarchy.

**B4. Yogic/breath-attention practices weighted UP (not at parity).** Two
mechanisms: (a) every theme×tier query was run twice — once against a yogic/
breath-practice term set (yoga, pranayama, Sudarshan Kriya, Isha, Shoonya, Kriya,
Bhastrika, bhramari, OM chanting), once against a general meditation/mindfulness
set; (b) a +2.0 score bonus for any paper matching the yogic set. Result: 151 of
292 longlist papers (52%) are yogic-weighted. Traces to §4 resolved weighting
rule.

**B5. BIDMC Sadhguru Center prioritized via dedicated affiliation search + force-
include.** Ran `"Sadhguru Center"[Affiliation]` and `"Conscious Planet"[Affiliation]`
(23 unique hits), plus broader BIDMC+meditation and Isha-practice queries. Papers
in the Sadhguru Center affiliation set get a +2.5 score bonus and are force-
included in the longlist ahead of the per-theme quota. Traces to §5 BIDMC
prioritization.

**B6. Affiliation-only papers must pass a meditation-relevance gate.** The
Sadhguru Center is housed in BIDMC's anesthesiology research group, so the raw
affiliation search returned that group's unrelated clinical work (perioperative
pharmacology, postoperative delirium, ventilation, a journal "In Response"
letter). 20 such affiliation-only, non-meditation items were dropped; 13
genuinely meditation/Isha Sadhguru Center papers were retained and prioritized.
Rationale: §4 alignment definition governs — prioritization applies to the
Center's *meditation* research, not everything its members co-author. Flagged
(F3) as the highest-judgment call in this pass.

**B7. Longlist depth ≈ 2.85× each theme's final-100 target, capped near 300.**
Per-theme depth is proportional to the §5 final distribution (stress 20, brain 20,
attention 15, emotional 15, sleep 10, clinical 10, app 10), so the curation to
100 can be done within-theme. Final longlist = 292 papers. Traces to §5 longlist
target (250–300) and distribution.

**B8. Null / mixed-result and critical-review inclusion is built in, not left to
chance.** A dedicated query set targeted "no significant difference / null / no
effect / failed to" and, separately, meta-analyses/reviews on "risk of bias /
publication bias / methodological quality / overstated." 34 longlist papers carry
the null-or-critical flag. Traces to §5 balance requirement.

**B9. Quality-floor filtering.** Excluded PubMed publication types that are not
primary research or reviews (Retracted Publication, Retraction, Erratum, Comment,
Editorial, News, Biography, Interview). Deduplicated by DOI, then by normalized
title where DOI was absent. Result: 0 duplicate PMIDs, 292/292 unique DOIs.
Traces to §5 quality floor + §4 exclusion of retracted papers.

**B10. Deferred to the final-100 gate, not decided here.** (a) Balancing the
brain/mechanisms theme toward neuroimaging/mechanistic studies — the longlist is
currently meta-analysis-heavy (159/292) because the scorer rewards the top
evidence tier; the "mechanisms" theme is scored separately per §5 and will be
rebalanced during curation. (b) Final selection of the single "major critical
review of meditation-research quality." Both are longlist-appropriate to defer.

---

## C. Repository & process

**C1. Artifacts committed to the repo root and `skills/`; raw pool kept for
transparency.** `LONGLIST.csv` (292 rows, ranked, scored) at root; full scored
pool of 494 candidates at `data/scored_pool.csv`; harvest/scoring scripts under
`scripts/` so the selection is reproducible. Traces to §9 logging + §10 review
artifacts (PAPERS-100.csv is the later, curated deliverable; this is its
longlist precursor).
