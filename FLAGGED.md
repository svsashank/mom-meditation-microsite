# FLAGGED.md

The ~10 lowest-confidence judgment calls from Phase 1 (skills + longlist).
These are where a reasonable reviewer might overrule me. Ordered roughly by
risk. Cross-references are to `DECISIONS.md`.

---

**F1 — Extent of the banned-phrases list (→ A3).** *Editorial.* I extended the
brief's explicit bans ("cures/treats/heals") to a wider wellness-cliché register
(boosts, rewires, detoxes, "clinically proven," exclamation points, second-person
health promises). This reflects §3's voice rules, but the exact line between
"banned" and "discouraged" is a call the content owner should confirm. Low harm
risk; easy to relax.

**F2 — Semantic Scholar not used this pass (→ B1).** *Coverage.* The brief names
Semantic Scholar + PubMed. Semantic Scholar's API returned empty responses in
this environment, so the longlist is PubMed-derived only. PubMed's coverage of
peer-reviewed biomedical meditation research is strong, but preprints and some
psychology/CS-venue app studies indexed by Semantic Scholar may be missing. Rerun
with a working Semantic Scholar key before the final 100 to close gaps.

**F3 — Meditation-relevance gate on BIDMC affiliation results (→ B6).** *Highest-
judgment call.* The Sadhguru Center sits inside BIDMC anesthesiology, so its
members co-author perioperative/critical-care papers unrelated to meditation. I
dropped 20 such affiliation-only items and kept 13 meditation/Isha ones. If the
intent was to showcase the Center's full output (not just its meditation work),
this is wrong and should be reversed. My read of §4 is that alignment governs, so
I filtered — but this is the call most worth a human eye.

**F4 — RCR as the "normalized citation" metric (→ B2).** *Methodological.* I used
iCite's Relative Citation Ratio as the impact signal. RCR is field- and
time-normalized, which I judged closer to the brief's intent than raw counts, but
it is an NIH-specific metric with known limitations for very new or
non-biomedical papers. A reviewer may prefer a simpler citations-per-year or a
percentile approach.

**F5 — Longlist is meta-analysis-heavy: 159/292 (→ B3, B10).** *Balance.* The
tier score rewards the top of the evidence hierarchy, so systematic reviews and
meta-analyses dominate. That is defensible for a longlist, but the final 100 —
especially the 20-slot "brain & mechanisms" theme, which §5 says is scored
separately — needs deliberate inclusion of primary neuroimaging/mechanistic
studies. Not yet done.

**F6 — Some top-ranked papers study yoga/mindfulness as one arm of a broader
review (→ B4).** *Alignment strength.* Highly-cited overviews (e.g. non-invasive
low-back-pain treatments, physician-burnout interventions) rank high because they
are meta-analyses that include a yoga/mindfulness component, not because they
study a MoM-adjacent practice directly. They pass the alignment test loosely.
Curation to 100 should prefer studies whose primary intervention is the
meditation/breath practice.

**F7 — Yogic-weighting magnitude (+2.0 bonus + dedicated queries) (→ B4).**
*Calibration.* The brief says weight yogic research UP but doesn't specify how
much. 52% of the longlist is now yogic-weighted. If that over-represents yogic
practice relative to the evidence base the reviewer wants surfaced, the bonus can
be reduced. The direction is per §4; the size is my calibration.

**F8 — Theme assignment is single-primary (→ B7).** *Taxonomy.* Many papers span
themes (e.g. an HRV study of a stress intervention is both "stress" and "brain").
I assigned one primary theme by priority order for the distribution math; the
`all_themes` column preserves the rest. Papers may therefore sit under a theme a
reviewer would file differently.

**F9 — Null/critical detection is keyword-based (→ B8).** *Recall risk.* I flagged
null/mixed and critical-methodology papers via title/abstract keywords
("no significant," "risk of bias," etc.). This will miss null results that are
phrased less explicitly, and the count (34) is a floor, not a census. The single
"major critical review" the brief requires is not yet individually chosen.

**F10 — Recency cutoff / 2026 papers with thin citation data (→ B2).** *Data
maturity.* The pool includes 2025–2026 papers that have little or no citation
history, so their impact score rests on the fallback proxy or is near zero. A few
may be ranked lower than their eventual importance warrants (or included on
recency alone). Worth a second look at the newest entries during curation.

---

## Phase 2 additions / updates

**F2 — RESOLVED.** Semantic Scholar recovered via the bulk endpoint; 152 quality-
gated new papers merged (see DECISIONS D1–D2). No key was needed.

**F5 — LARGELY RESOLVED.** Meta-analysis share cut from 72% to 45% via a per-theme
soft cap; final tier mix is 45 meta / 47 RCT / 8 mechanistic. Residual note: only
8 cross-sectional/mechanistic papers overall — reviewers wanting a more
mechanism-heavy brain theme could raise the neuroimaging floor above 10.

**F6 — RESOLVED via title-alignment gate (D5).** All broad exercise/
non-pharmacological reviews where meditation was one arm were removed. Residual
judgment: "mind-body exercise" reviews (tai chi/yoga) are kept as MoM-adjacent;
a stricter reviewer might want only breath-and-attention practices.

**F11 (new) — 27 outside-PubMed S2 papers scored on a different basis.** Papers
not indexed in PubMed lack an iCite RCR, so they are scored on S2 citation count
normalized by year rather than the field-normalized RCR used elsewhere. None
reached the final 100, but they sit in the longlist/pool on a slightly different
metric. Re-verify their metadata before promoting any into the 100.

**F12 (new) — "null result" detection is abstract-keyword based.** The 7
null/mixed papers in the final 100 were flagged from abstract-level language in
the harvest, not from reading results tables. Titles rarely announce a null, so
a reviewer should confirm each genuinely reports a null/mixed primary outcome
before it is presented as the brief's required null-result representation.

**F13 (new) — single critical review may be thin.** The final 100 contains one
dedicated critical/safety review (meditative-movement therapy safety in
fibromyalgia). The brief asks for "at least one major critical review of
meditation-research quality"; this qualifies, but a stronger choice would be a
general methodological critique (e.g. a risk-of-bias/repro review of the whole
field). Worth swapping in during content production.

---

## Phase 2b updates

**F13 — RESOLVED.** Two field-methodology critiques added (Van Dam "Mind the Hype"
2018; Davidson & Kaszniak 2015). See DECISIONS D7.

**F12 — RESOLVED at abstract level.** 4 of 8 keyword-flagged null papers verified
genuine; 4 false positives corrected. See DECISIONS D8. Residual: verification
used abstracts (results + conclusions sections), not full-text results tables —
confirm the 4 verified nulls against full text during content production before
presenting them as null-result representation.

---

## Phase 3 additions

**F14 (new) — 3 of 7 theme wisdom slots are empty pending verified quotes.**
Sleep, Clinical Research, and Brief & App-Based Practice have no paired Sadhguru
quote yet. Per the wisdom-pairing rule I left them empty and flagged rather than
paraphrasing. Source verbatim quotes for these three themes from
isha.sadhguru.org (topic pages for Sleep, Breath, etc.) before launch.

**F15 (new) — per-paper prose is auto-drafted from abstracts and needs editorial
+ medical review.** Summaries, key findings, and limitations are extracted from
abstract text. They are faithful to the abstract but have not been read against
full text, and phrasing has not been human-edited for the claim-strength
vocabulary case by case. Every page is flagged "draft." A qualified medical/
scientific reviewer must co-sign the CLAIMS-REGISTER before any production launch
(§11). The CLAIMS-REGISTER itself is not yet generated — it is the next step.

**F16 (new) — methodology parsing is heuristic.** Sample size, duration, and
comparator are regex-extracted from abstracts; some read "see paper" where the
abstract was not explicit. These should be confirmed against full text during
content production.

---

## Phase 3c — /practice/ SEO/AEO/ASO pass

**F17 (new) — og:image is a placeholder.** The practice page ships with
`og:image` = `REPLACE_WITH_OG_IMAGE_URL` pending the supplied asset. Social/link
previews will not render an image until this is replaced. Not a claims issue; a
launch checklist item.

**F18 (new) — removed an unsourced timeline claim.** Earlier draft copy on the
practice page stated the research studies effects "over four to eight weeks of
regular practice." I could not source a specific efficacy-timeline finding to
PAPERS-100.csv without approximating across heterogeneous study durations, so I
removed the specific week-count and reframed the guidance around consistency
(one session a day) rather than a promised timeframe. If a defensible timeline is
wanted, it should be derived from named studies during content review.

**F19 (new) — store-badge images are hotlinked from Apple/Google.** The App Store
and Google Play badges load from Apple's and Google's official asset URLs. These
are the real badges but depend on those URLs staying live; consider self-hosting
the official badge assets before production.

---

## Phase 3d — site-wide architecture (frontmatter, app bar, homepage schema, theme cards)

**F20 (new) — entity links use Wikipedia URLs, not Wikidata QIDs.** The homepage
`knowsAbout`/`about` schema links Meditation, Mindfulness, and Sadhguru to their
English Wikipedia pages. I did not add Wikidata Q-identifiers because I could not
verify the exact QIDs from our own data without guessing; Wikipedia URLs are
verifiable and sufficient. Add verified Wikidata QIDs later if desired. Per the
instruction, no entity associations were added for EEG, alpha waves, or other
neuro-mechanism terms (mirrors F18).

**F21 (new) — AEO snippets exclude authors' speculative benefit sentences.** The
`ai_snippet` on each research page is built only from the paper's stated findings.
Because a snippet can be surfaced standalone by an answer engine (without the
page's disclaimer and transfer-gap note), I additionally drop authors'
interpretive "…for treating various conditions / foundation for / holds promise"
sentences and keep the concrete empirical results. This is a claims-discipline
call (§3): the omitted text is the paper's own, but it over-reaches when quoted
out of context. Reviewers may restore fuller author conclusions on-page if paired
with the caveats.

**F22 (note) — "detoxification" appears in one AEO snippet.** The BIDMC genomic
study's own results name "oxidative stress, detoxification, and cell cycle
regulation pathways." This is scientific pathway terminology, verbatim from the
paper — not a wellness "detox" claim — and was retained as the paper's stated
finding. Flagging only because the word appears on the banned-phrase list in a
different (wellness) sense.

**F23 (new) — sticky app bar suppression is viewport-heuristic.** The mobile app
bar hides whenever the disclaimer, limitations, review-flag, or footer is within
~96px of the viewport bottom (IntersectionObserver + scroll handler), so it never
covers those elements. On very short viewports where a protected element is
always in view, the bar stays hidden by design. Verify on-device across a few
screen sizes before launch.

---

## Phase 3e — "Why this matters" mechanistic-transfer bridge

**F24 — 28 papers omitted from the practice-bridge (no specific breath/attention mechanism).** Per rule 2, the bridge was left off these pages (a plain gap note is shown instead) because the paper's own practice description does not share a concrete breath-regulation or directed-attention mechanism with MoM. Grouped reasons below. None were forced.

_No breath or directed-attention component identifiable_ (21):
- [Focus & Attention] A randomized controlled trial of Kundalini yoga in mild cogn (PMID 28088925)
- [Brain & Mechanisms] Acceptance and Commitment Therapy and yoga for drug-refracto (PMID 18343200)
- [Brain & Mechanisms] Changes in Neural Connectivity and Memory Following a Yoga I (PMID 27060939)
- [Focus & Attention] Cognitive and immunological effects of yoga compared to memo (PMID 38355715)
- [Brain & Mechanisms] Effects of yoga in men with prostate cancer on quality of li (PMID 34815548)
- [Brain & Mechanisms] Effects of yoga on the autonomic nervous system, gamma-amino (PMID 22365651)
- [Stress & Anxiety] Physical and psychosocial benefits of yoga in cancer patient (PMID 23181734)
- [Clinical Research] Randomised controlled trial of yoga and bio-feedback in mana (PMID 49737)
- [Sleep] The effect of yoga on sleep quality and insomnia in women wi (PMID 32357858)
- [Brain & Mechanisms] The Meditative Mind: A Comprehensive Meta-Analysis of MRI St (PMID 26146618)
- [Focus & Attention] Yoga and Cognition: A Meta-Analysis of Chronic and Acute Eff (PMID 26186435)
- [Brain & Mechanisms] Yoga and heart rate variability: A comprehensive review of t (PMID 27512317)
- [Emotional Wellbeing] Yoga as a therapeutic approach to mental health in universit (PMID 38903593)
- [Clinical Research] Yoga as an adjunctive treatment for posttraumatic stress dis (PMID 25004196)
- [Sleep] Yoga-based intervention for carpal tunnel syndrome: a random (PMID 9820263)
- [Clinical Research] Yoga for anxiety: A systematic review and meta-analysis of r (PMID 29697885)
- [Stress & Anxiety] Yoga for breast cancer patients and survivors: a systematic  (PMID 22988934)
- [Clinical Research] Yoga for treating low back pain: a systematic review and met (PMID 34326296)
- [Brain & Mechanisms] Yoga Nidra for hypertension: A systematic review and meta-an (PMID 38484438)
- [Clinical Research] Yoga, Physical Therapy, or Education for Chronic Low Back Pa (PMID 28631003)
- [Clinical Research] Yoga research review (PMID 27502816)

_Transcendental Meditation (mantra-based, effortless) — not MoM's focused-attention/breath mechanism_ (1):
- [Brief & App-Based Practice] EEG based interpretation of human brain activity during yoga (PMID 33618287)

_Movement/exercise-led practice without breath or attention component_ (6):
- [Brain & Mechanisms] Effects of yoga versus walking on mood, anxiety, and brain G (PMID 20722471)
- [Stress & Anxiety] Meditation and Yoga for Irritable Bowel Syndrome: A Randomiz (PMID 36422517)
- [Sleep] The effects of yoga compared to active and inactive controls (PMID 30953508)
- [Emotional Wellbeing] The Practice of Hatha Yoga for the Treatment of Pain Associa (PMID 27869485)
- [Emotional Wellbeing] Yoga for chronic non-specific low back pain (PMID 36398843)
- [Clinical Research] Yoga for depression: a systematic review and meta-analysis (PMID 23922209)

**F25 — attention-only bridges rest on the directed-attention component.** Where a paper's practice is mindfulness/focused-attention meditation without an explicit breath component, the bridge anchors to "directed attention (the focused-attention component)" only. This is a real, specific mechanism MoM shares, but a stricter reviewer may want the anchor narrowed to studies that explicitly train breath-focused attention. Applies to the attention-only subset of the 72 bridges.

**F26 — the bridge was NOT folded into the ≤100-word AEO key-finding snippet.** Rule 4 asks to apply the logic to AEO snippets. To avoid the standalone snippet degrading into a bare outcome claim (and to preserve the findings-only integrity of `aiSnippet` per F21), the mechanistic-transfer sentence is exposed as its own crawlable `<section id="why-mom">` — mechanism-anchored, with the final clause intact — rather than merged into the key-finding summary. If reviewers prefer it inside the snippet, it can be appended there verbatim (never truncating the final clause).

**F27 — the bridge is a hedged inference, now a registered claim type.** Each of the 72 bridges is an explicit mechanistic-transfer inference ("may extend to MoM… though MoM hasn't been studied directly"). These are logged in CLAIMS-REGISTER.md as their own claim class so a reviewer evaluates the inference itself, not just the underlying finding.

---

## Phase 3f — crawler indexing prep

**F28 — NO noindex directive existed when this task began (important).** The task
said to preserve "the current noindex directive," but there was none: `robots.txt`
was `Allow: /` and no page carried a robots meta tag — the staging site was fully
indexable. Because the requested robots.txt AI-crawler *allow* rules are only
"harmless" if a noindex is active, I added a site-wide `<meta name="robots"
content="noindex, follow">` in the base layout (all 113 built pages incl. 404).
This is the single tag to remove at go-live. If you believed indexing was already
blocked by another mechanism (repo privacy, host config), please confirm — as far
as this repo shows, nothing was suppressing indexing until now.

**F29 — AI-crawler token nuances (kept all 7 as requested; flagging scope).**
- `anthropic-ai` — a legacy Anthropic token; current Anthropic crawlers are
  `ClaudeBot` (already included) and `Claude-User`/`Claude-SearchBot`. `anthropic-ai`
  may be deprecated/ignored by newer infrastructure. Kept per request; consider
  adding `Claude-User` and `Claude-SearchBot` at go-live.
- `ChatGPT-User` — OpenAI's user-triggered fetch agent (fires when a user asks
  ChatGPT to open a link), not the training crawler (`GPTBot`) nor the search
  crawler (`OAI-SearchBot`). Included as requested; `OAI-SearchBot` could be added
  for AI-search indexing.
- `Google-Extended` — not a fetching user-agent; it is a robots.txt token that
  controls use of already-crawled content for Google's Gemini/Vertex AI. The allow
  rule is valid, but it governs training-use permission, not crawl behavior.
- `GPTBot`, `ClaudeBot`, `PerplexityBot`, `CCBot` — current and correct as of the
  last known guidance; verify against each operator's published list at go-live,
  since these strings change.
- Reminder: robots.txt is advisory and only honored by compliant bots; the
  `noindex` meta tag is what actually keeps pages out of indexes.

---

## Phase 3g — bridge/limitations coherence audit (all 72 bridge pages)

**F30 — audited all 72 bridge pages for the Limitations-vs-"Why this matters" contradiction.** 65 pages had a flat "findings do not transfer directly to MoM" limitation sitting immediately before a bridge that argues the benefit may extend — a genuine incoherence. On those, the limitation was rewritten to acknowledge the shared mechanism and point to the bridge ("…so its findings don't transfer directly — though the shared [mechanism] component may make some transfer plausible (see 'Why this matters…' below)"). Both sections retained. 7 bridge pages had no transfer-gap limitation (it was truncated earlier by the 4-item limitations cap), so no contradiction existed; the bridge's own "…hasn't been studied directly" hedge stands. Full per-page audit: `data/bridge-transfer-audit.csv`.

Per-page audit (slug · overlap · reconciled):
- a-randomised-active-controlled-trial-to-examine-the-effects-of-an-onli · attention · reconciled
- a-randomised-controlled-trial-of-a-brief-online-mindfulness-based-inte · attention · reconciled
- a-randomized-controlled-trial-of-mindfulness-meditation-for-chronic-in · attention · reconciled
- a-structured-literature-review-on-the-role-of-mindfulness-mindful-eati · attention · reconciled
- a-systematic-review-and-meta-analysis-of-acceptance-and-mindfulness-ba · attention · no-transfer-lim (no conflict)
- a-systematic-review-and-meta-analysis-of-workplace-mindfulness-trainin · attention · reconciled
- a-systematic-review-of-the-neurophysiology-of-mindfulness-on-eeg-oscil · attention · reconciled
- benefits-of-preparing-for-childbirth-with-mindfulness-training-a-rando · attention · reconciled
- brief-daily-meditation-enhances-attention-memory-mood-and-emotional-re · attention · reconciled
- brief-mindfulness-based-training-and-mindfulness-trait-attenuate-psych · attention · reconciled
- brief-mindfulness-training-for-negative-affectivity-a-systematic-revie · attention · reconciled
- conceptual-and-methodological-issues-in-research-on-mindfulness-and-me · attention · reconciled
- cultivating-mindfulness-effects-on-well-being · attention · reconciled
- does-mindfulness-based-stress-reduction-training-have-an-impact-on-the · attention · reconciled
- effect-of-mindfulness-yoga-on-anxiety-and-depression-in-early-breast-c · attention · reconciled
- effectiveness-of-online-mindfulness-interventions-on-medical-students- · attention · reconciled
- effects-of-a-prenatal-mindfulness-program-on-longitudinal-changes-in-s · attention · reconciled
- effects-of-mind-body-exercise-on-perimenopausal-and-postmenopausal-wom · attention · reconciled
- effects-of-mindfulness-training-and-exercise-on-cognitive-function-in- · attention · reconciled
- effects-of-mindfulness-yoga-vs-stretching-and-resistance-training-exer · attention · reconciled
- effects-of-mobile-mindfulness-meditation-on-the-mental-health-of-unive · attention · no-transfer-lim (no conflict)
- efficacy-of-the-mindfulness-meditation-mobile-app-calm-to-reduce-stres · attention · reconciled
- guided-self-help-works-randomized-waitlist-controlled-trial-of-pacific · attention · reconciled
- health-care-workers-need-for-headspace-findings-from-a-multisite-defin · attention · reconciled
- holistic-nursing-in-practice-mindfulness-based-yoga-as-an-intervention · attention · reconciled
- impact-of-mindfulness-based-stress-reduction-training-on-intrinsic-bra · attention · reconciled
- impact-of-short-and-long-term-mindfulness-meditation-training-on-amygd · attention · no-transfer-lim (no conflict)
- improving-stress-management-anxiety-and-mental-well-being-in-medical-s · attention · reconciled
- investigation-of-mindfulness-meditation-practitioners-with-voxel-based · attention · reconciled
- meditation-programs-for-psychological-stress-and-well-being-a-systemat · attention · reconciled
- meta-analytic-evidence-that-mindfulness-training-alters-resting-state- · attention · reconciled
- mind-the-hype-a-critical-evaluation-and-prescriptive-agenda-for-resear · attention · reconciled
- mindfulness-based-interventions-for-psychiatric-disorders-a-systematic · attention · reconciled
- mindfulness-based-stress-reduction-for-healthy-individuals-a-meta-anal · attention · reconciled
- mindfulness-based-stress-reduction-for-stress-management-in-healthy-pe · attention · reconciled
- mindfulness-based-stress-reduction-in-post-treatment-breast-cancer-pat · attention · reconciled
- mindfulness-based-therapy-a-comprehensive-meta-analysis · attention · reconciled
- mindfulness-for-smoking-cessation · attention · reconciled
- mindfulness-interventions · attention · reconciled
- mindfulness-meditation-and-network-neuroscience-review-synthesis-and-f · attention · reconciled
- mindfulness-meditation-and-the-immune-system-a-systematic-review-of-ra · attention · no-transfer-lim (no conflict)
- mindfulness-meditation-improves-emotion-regulation-and-reduces-drug-ab · attention · reconciled
- mindfulness-meditation-training-alters-stress-related-amygdala-resting · attention · reconciled
- mindfulness-training-improves-working-memory-capacity-and-gre-performa · attention · reconciled
- neurobiological-changes-induced-by-mindfulness-and-meditation-a-system · attention · reconciled
- psychological-and-mind-body-interventions-for-endometriosis-a-systemat · attention · reconciled
- reducing-stress-with-yoga-a-systematic-review-based-on-multimodal-bios · attention · reconciled
- research-review-the-effects-of-mindfulness-based-interventions-on-cogn · attention · reconciled
- review-of-the-neural-oscillations-underlying-meditation · attention · reconciled
- the-clinical-efficacy-of-mindfulness-based-treatments-for-alcohol-and- · attention · reconciled
- the-effect-of-mindfulness-based-programs-on-cognitive-function-in-adul · attention · reconciled
- the-effectiveness-of-mindfulness-based-programs-in-reducing-stress-exp · attention · reconciled
- the-effects-of-mindfulness-meditation-on-nursing-students-stress-and-a · attention · reconciled
- the-impact-of-mindfulness-meditation-on-the-wandering-mind-a-systemati · attention · no-transfer-lim (no conflict)
- the-influence-of-mindfulness-meditation-combined-with-progressive-musc · attention · reconciled
- the-potential-effects-of-meditation-on-age-related-cognitive-decline-a · attention · reconciled
- yoga-mindfulness-based-stress-reduction-and-stress-related-physiologic · attention · reconciled
- breathing-practices-for-stress-and-anxiety-reduction-conceptual-framew · breath · reconciled
- effect-of-a-single-session-of-yoga-and-meditation-on-stress-reactivity · breath · reconciled
- effectiveness-of-yoga-in-modulating-markers-of-immunity-and-inflammati · breath · reconciled
- effects-of-breathing-exercises-in-patients-with-chronic-obstructive-pu · breath · reconciled
- efficacy-of-mhealth-aided-12-week-meditation-and-breath-intervention-o · breath · reconciled
- how-breath-control-can-change-your-life-a-systematic-review-on-psycho- · breath · reconciled
- physiology-of-long-pranayamic-breathing-neural-respiratory-elements-ma · breath · reconciled
- slow-breathing-for-reducing-stress-the-effect-of-extending-exhale · breath · reconciled
- yoga-for-improving-health-related-quality-of-life-mental-health-and-ca · breath · no-transfer-lim (no conflict)
- mechanisms-of-mindfulness-emotion-regulation-following-a-focused-breat · breath+attention · reconciled
- mindful-attention-to-breath-regulates-emotions-via-increased-amygdala- · breath+attention · reconciled
- isha-yoga-practices-vegan-diet-and-participation-in-samyama-meditation · isha · no-transfer-lim (no conflict)
- large-scale-genomic-study-reveals-robust-activation-of-the-immune-syst · isha · reconciled
- online-guided-meditation-training-isha-kriya-improves-self-reported-sy · isha · reconciled
- online-isha-upa-yoga-for-student-mental-health-and-well-being-during-c · isha · reconciled

**F31 — 28 bridges rest on a broad mindfulness/meditation review via attention-only overlap (the F25 case for reviewers).** These are the weakest-anchored bridges: the shared mechanism is only "directed attention," and the source is a broad systematic review/meta-analysis (often pooling many mindfulness or yoga programs) rather than a study of a specific breath-and-attention practice. The mechanistic-transfer inference is most debatable here and should be the priority for reviewer sign-off — reviewers may choose to soften or drop the bridge on these:
- [A systematic review and meta-analysis of acceptanc] · Mindfulness-Based Stress Reduction (MBSR) · Meta-analysis / Systematic review
- [A systematic review and meta-analysis of workplace] · mindfulness / meditation · Meta-analysis / Systematic review
- [A systematic review of the neurophysiology of mind] · mindfulness / meditation · Meta-analysis / Systematic review
- [Brief mindfulness training for negative affectivit] · mindfulness / meditation · Meta-analysis / Systematic review
- [Conceptual and methodological issues in research o] · mindfulness / meditation · Meta-analysis / Systematic review
- [Effectiveness of online mindfulness interventions ] · mindfulness / meditation · Meta-analysis / Systematic review
- [Effects of Mobile Mindfulness Meditation on the Me] · mindfulness / meditation · Meta-analysis / Systematic review
- [Effects of mind-body exercise on perimenopausal an] · Tai Chi · Meta-analysis / Systematic review
- [Meditation programs for psychological stress and w] · mindfulness / meditation · Meta-analysis / Systematic review
- [Meta-analytic evidence that mindfulness training a] · mindfulness / meditation · Meta-analysis / Systematic review
- [Mind the Hype: A Critical Evaluation and Prescript] · mindfulness / meditation · Meta-analysis / Systematic review
- [Mindfulness for smoking cessation] · yoga · Meta-analysis / Systematic review
- [Mindfulness meditation and the immune system: a sy] · mindfulness / meditation · Meta-analysis / Systematic review
- [Mindfulness-based interventions for psychiatric di] · mindfulness / meditation · Meta-analysis / Systematic review
- [Mindfulness-based stress reduction for healthy ind] · Mindfulness-Based Stress Reduction (MBSR) · Meta-analysis / Systematic review
- [Mindfulness-based stress reduction for stress mana] · Mindfulness-Based Stress Reduction (MBSR) · Meta-analysis / Systematic review
- [Mindfulness-based therapy: a comprehensive meta-an] · mindfulness / meditation · Meta-analysis / Systematic review
- [Neurobiological Changes Induced by Mindfulness and] · mindfulness / meditation · Meta-analysis / Systematic review
- [Psychological and mind-body interventions for endo] · yoga · Meta-analysis / Systematic review
- [Reducing Stress with Yoga: A Systematic Review Bas] · yoga · Meta-analysis / Systematic review
- [Research Review: The effects of mindfulness-based ] · mindfulness / meditation · Meta-analysis / Systematic review
- [Review of the Neural Oscillations Underlying Medit] · mindfulness / meditation · Meta-analysis / Systematic review
- [The Clinical Efficacy of Mindfulness-Based Treatme] · mindfulness / meditation · Meta-analysis / Systematic review
- [The Effect of Mindfulness-based Programs on Cognit] · mindfulness / meditation · Meta-analysis / Systematic review
- [The Impact of Mindfulness Meditation on the Wander] · mindfulness / meditation · Meta-analysis / Systematic review
- [The effectiveness of mindfulness based programs in] · Mindfulness-Based Stress Reduction (MBSR) · Meta-analysis / Systematic review
- [The potential effects of meditation on age-related] · mindfulness / meditation · Meta-analysis / Systematic review
- [Yoga, mindfulness-based stress reduction and stres] · yoga · Meta-analysis / Systematic review
