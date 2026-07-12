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

---

## Phase 2 — Semantic Scholar merge, neuroimaging supplement, curation to 100

**D1. Semantic Scholar recovered via the bulk endpoint (resolves F2).** The
keyless `/paper/search` endpoint returns HTTP 429 (shared-pool rate limit), but
`/paper/search/bulk` responds without a key. Ran 8 bulk queries (7 themes +
a dedicated yogic/breath neuroimaging query), 6,169 unique S2 papers. Deduped
against the existing pool by PMID, DOI, and normalized title.

**D2. S2 merge is quality-gated, not bulk-dumped.** Of 6,081 genuinely new S2
papers, I folded in only those that were (a) meditation-relevant by title,
(b) ≥100 citations (landmark threshold — if PubMed's structured queries missed a
100+ citation meditation paper, it is worth catching), (c) had a DOI, and
(d) were not preprints. Result: 152 added (125 PubMed-indexed, enriched via iCite
for scoring consistency; 27 outside PubMed, scored on S2 citation count
normalized by year). Rationale: honor the brief's Semantic Scholar source
without importing thousands of low-quality/preprint hits. Notable catches:
Sudarshan Kriya Yogic Breathing (Brown & Gerbarg), meditation-induced
white-matter change (Tang), voxel-based morphometry of meditators.

**D3. Dedicated neuroimaging supplement (resolves F5/F6 for the brain theme).**
Ran a PubMed search crossing yogic/breath-attention practices with imaging
methods (fMRI, EEG, MEG, VBM, cortical thickness, functional connectivity, DMN,
ERP, gamma/alpha). 101 hits, 77 new to the pool. The brain & mechanisms theme
now has 139 primary-neuroimaging/mechanistic candidates to draw its 20 from.

**D4. Final-100 curation rules (§5).** (a) Theme quotas filled exactly to the §5
distribution (20/10/15/15/20/10/10). (b) Brain theme carries a floor of 10
primary neuroimaging/mechanistic studies before meta-analyses top it up. (c) A
per-theme soft cap of ~60% on meta-analyses so landmark primary RCTs and
mechanistic studies are represented — this moved the tier mix from 72%
meta-analysis (longlist) to 45 meta / 47 RCT / 8 mechanistic in the final 100.
(d) Balance guarantee: ≥3 null/mixed-or-field-critical papers and ≥1 dedicated
critical/safety review of meditation research (§5 balance requirement).
(e) ≥4 Sadhguru Center @ BIDMC papers retained. Scarce themes are assigned first
so multi-theme papers land where slots are tightest.

**D5. Title-level alignment gate for the final 100 (directly resolves F6).** An
early cut of the 100 contained ~40 broad "exercise / physical-activity /
non-pharmacological intervention" reviews where meditation was only one arm
(e.g. neck-disorder exercises, migraine prevention, physician burnout). I
required the paper's TITLE to name a meditation/mind-body practice
(meditation, mindfulness, yoga, pranayama, breath, tai chi/qigong, MBSR/MBCT,
etc.), excluding exercise-only reviews, and exempting the pre-vetted Sadhguru
Center papers. This removed all 40 off-topic titles and refilled with genuinely
meditation-centered studies. The final 100 has zero non-core, non-BIDMC titles.

**D6. `PAPERS-100.csv` schema.** rank, pmid/id, DOI, title, year, journal, theme,
study type, alignment (yogic-weighted vs general), citation count, citations/yr,
RCR, yogic flag, BIDMC flag, null/critical flag, selection score, inclusion
reason, last author. `LONGLIST.csv` regenerated over the expanded 723-candidate
pool (296 rows). Full pool retained at `data/scored_pool.csv`.

---

## Phase 2b — F13 (critical review) and F12 (null-result verification)

**D7. Critical-review slot upgraded to field-level methodology critiques (resolves
F13).** Replaced the fibromyalgia-specific safety review with the two canonical
critiques of meditation-research quality: Van Dam et al. 2018, "Mind the Hype: A
Critical Evaluation and Prescriptive Agenda for Research on Mindfulness and
Meditation" (Perspectives on Psychological Science; 538 citations, RCR 36.3) and
Davidson & Kaszniak 2015, "Conceptual and methodological issues in research on
mindfulness and meditation" (American Psychologist; 308 citations, RCR 15.5).
Both clear the quality floor comfortably and directly address effect sizes,
active-control problems, publication bias, and measurement/definitional issues.
The critical-review detector was tightened to match genuine research-quality
critiques so a safety review no longer fills this slot.

**D8. All 7→8 null-flagged papers verified against their abstracts (resolves
F12).** Read each abstract's results/conclusions rather than trusting keyword
flags. 4 held up as genuine null/mixed and are now labelled "null/mixed
(F12-verified)": Goyal 2014 (no benefit over active controls), the workplace-
mindfulness MA (burnout ambivalent, depression confounded by publication bias),
the acceptance/mindfulness-for-anxiety MA (no significant difference vs TAU/CBT
at 6–12 mo; placebo-exceeding effects unclear), and the prenatal-mindfulness RCT
(null on mother–infant bonding). 4 were abstract-keyword false positives and had
the flag removed (they remain in the 100 as valid positive studies): a yoga/
stress-physiology MA (positive; "however… heterogeneous"), the Calm-app RCT
(positive), an MBTI-vs-MBSR insomnia RCT (positive), and a mindfulness+PMR
sarcopenia RCT where "no significant differences" referred to *baseline*
equivalence, not outcomes. Net balance section: 4 verified null/mixed + 2
methodology critiques. Full-text verification of the 4 remains a content-
production step.

---

## Phase 3 — Astro staging site and per-paper pages

**D9. Framework and structure per §7.** Astro static site. Papers stored as
structured JSON, one file per paper (`src/content/papers/*.json`), in a typed
content collection — matching §7's "structured MDX/JSON, one file per paper."
Site map follows §6: home, 7 theme hubs, filterable research library, 100 paper
pages, "Sadhguru on Meditation" wisdom hub, "The Practice" single-CTA page, and
an About/Methodology transparency page.

**D10. Per-paper page prose is generated from the study abstract, not invented.**
The 8-part template (research-summary skill) is populated by extracting the
study's own conclusion sentences and parsing sample size / duration / comparator
from the abstract. No effect sizes or findings are fabricated; where the abstract
does not state a value, the field reads "see paper." Every page carries the
claim-strength badge, a mandatory non-empty Limitations section (with the
transfer-gap note when the practice studied is not MoM), the standing medical
disclaimer, and a visible "draft — pending editorial and medical review" flag per
§11. A banned-phrase scan across all 112 built pages found no generated
cure/treat/heal claims (only benign matches: the methodology page's own
description of the rule, the disclaimer, verbatim paper titles, and a genomics
abstract's "detoxification").

**D11. Sadhguru quotes: 4 verified verbatim, 3 pending (wisdom-pairing rule).**
Four themes carry genuine verbatim quotes sourced and verified against
isha.sadhguru.org on 2026-07-10 (Stress & Anxiety, Emotional Wellbeing, Focus &
Attention, Brain & Mechanisms), each stored with its source URL and shown on both
the theme hub and that theme's paper pages. The remaining three (Sleep, Clinical
Research, Brief & App-Based Practice) are left as clearly-marked "pending verified
quote" slots rather than paraphrased or force-fitted — exactly as the
wisdom-pairing skill requires (leave empty and flag). See F14.

**D12. Staging deploy via GitHub Pages workflow (§7).** Added
`.github/workflows/deploy-staging.yml`. `astro.config.mjs` sets `site`/`base` for
the project-pages path. No production or custom-domain deploy is configured —
that awaits sign-off per §7/§11. `node_modules/` and `dist/` are git-ignored;
the site is reproducible via `npm ci && npx astro build`.

---

## Phase 3b — Claims register, draft banner, staging deploy

**D13. CLAIMS-REGISTER.md generated from the draft pages (§10).** 209 benefit-
relevant claims across the 100 papers, one row each, grouped by theme. Every row
records the claim text, evidence-strength framing, the practice studied and
whether it is the MoM practice (30 MoM-adjacent, 179 not-MoM with on-page
transfer-gap notes), the source DOI, and a blank reviewer sign-off. No rows are
signed off — the register is explicitly DRAFT pending a qualified medical/
scientific co-signer (§11). Machine-readable copy at `data/claims-register.csv`.

**D14. Site-wide unreviewed-draft banner added (in addition to per-paper flags).**
A sticky banner renders on all 112 pages via the base layout: "Unreviewed working
draft. Medical & research claims here are auto-drafted and pending expert
medical/scientific review. Not for public distribution."

**D15. Deployed to GitHub Pages staging (§7).** Pages enabled with the Actions
build type; the deploy-staging workflow built and published the site. Live at
https://svsashank.github.io/mom-meditation-microsite/ . This is staging only — no
production or custom-domain deploy, consistent with §7/§11.

---

## Phase 3d — Site-wide architecture improvements

**D16. Canonical research-page frontmatter template + retrofit.** Documented the
standard in `src/content/papers/_TEMPLATE.md` and added the canonical fields
(`simplifiedTitle`, `publicationYear`, `journalName`, `coreTheme`,
`primaryEntityUrl`, `relatedThemePath`, `aiSnippet`) to the schema and to all 100
paper files. `primaryEntityUrl` = DOI (fallback PubMed). No `app_deep_link` field:
per instruction, pages link only to the general `/practice/` page — a study's
findings are not executed or embodied by the app. Each page now renders a
semantic `<section id="ai-snippet">` ≤100-word summary built only from the paper's
own findings (see F21).

**D17. Global sticky mobile app bar (<768px), OS-aware, non-obstructing.** Bottom
bar "Practice the science in 7 mins" + Open App; routes to the iOS App Store on
iOS, Google Play on Android, else the practice page. It hides whenever the medical
disclaimer, limitations section, draft-review flag, or footer is near the viewport
bottom, and reveals only after scrolling down past the hero — so those elements
are never covered (see F23). Desktop unaffected.

**D18. Homepage schema: Organization + WebSite (not medical).** Added JSON-LD for
`Organization` and `WebSite` (with `WebSite.hasPart` referencing all 7 theme
hubs). Deliberately NOT MedicalOrganization/MedicalBusiness — we are not a medical
provider. `knowsAbout`/`about` link only Meditation, Mindfulness, and Sadhguru
(Wikipedia); no neuro-mechanism entities were added (F18/F20).

**D19. Theme cards rewritten with exact tallies.** The 7 homepage cards now carry
specific 15–20 word keyword-rich snippets and descriptive anchor text
("Explore N {theme} studies →"). Every number is inserted from the live
PAPERS-100 tally — verified equal to the dataset per theme (e.g. Stress & Anxiety
20 total / 12 RCTs / 5 reviews; Brain & Mechanisms 20 total / 4 mechanistic /
9 RCTs / 7 reviews). No rounding.
