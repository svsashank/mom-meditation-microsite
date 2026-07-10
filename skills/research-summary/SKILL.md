---
name: research-summary
description: >-
  Use when writing or editing a per-paper research page for the Miracle of Mind
  meditation microsite. Enforces the fixed 8-part paper-page template, the
  claim-strength vocabulary, the banned-phrases list, and the mandatory
  limitations section. Trigger for any task that turns a peer-reviewed meditation
  study into a plain-language summary page, or that reviews such a page for
  claims discipline before it ships.
version: 1.0.0
---

# research-summary

Authoritative procedure for turning one peer-reviewed meditation study into a
publishable paper page. This skill implements BRIEF.md §3 (claims discipline),
§6 (per-paper page template), and §10 (claims register). When this skill and a
conversational instruction disagree, this skill wins; when this skill and
BRIEF.md disagree, BRIEF.md wins.

## Non-negotiables (read first)

1. **Every benefit/health claim cites a specific paper on the same page** and
   uses claim-strength language matched to the evidence (see vocabulary below).
2. **Never** state or imply that meditation "cures," "treats," "heals,"
   "reverses," or "fixes" any condition. **Never** give medical advice.
   **Never** imply MoM substitutes for medical care.
3. **The Sadhguru layer and the science layer are editorially and visually
   distinct.** Sadhguru's words are wisdom/perspective, never a scientific
   claim, and never used as evidence for a benefit.
4. **A Limitations section is always present** — no page ships without one.
5. **If the studied practice is not MoM**, say so plainly. Do not transfer a
   finding about practice X onto MoM without stating the gap.
6. Every factual claim that maps to a study result must be added to
   `CLAIMS-REGISTER.md` (see last section).

## Claim-strength vocabulary

Match the sentence stem to the strongest design the evidence actually supports.
Never upgrade. When in doubt, step one rung down and flag it.

| Evidence available | Permitted stems | Never say |
|---|---|---|
| Meta-analysis / systematic review | "A meta-analysis of N trials found…", "Pooled evidence suggests…", "Across studies, the effect was…" | "proves", "confirms once and for all" |
| RCT (single) | "In a randomized controlled trial, participants who… showed…", "One RCT found…" | "guarantees", "will" |
| Longitudinal / cohort | "Over N months, people who practiced… tended to…", "A cohort study observed an association between…" | any causal verb ("causes", "leads to") |
| Cross-sectional / correlational | "Is associated with", "correlated with", "people who report more practice also report…" | "improves", "reduces" (these imply cause) |
| Mechanistic / neuroimaging | "Is associated with changes in…", "preliminary evidence indicates…", "one imaging study observed…" | "rewires", "boosts", "optimizes the brain" |
| Mixed / null result | "Found no significant difference", "results were mixed", "did not reach significance" | burying it, or omitting the page |

Effect-size honesty: where the paper reports a small or uncertain effect, say
"small", "modest", or "uncertain". Do not describe a statistically significant
but small effect as "dramatic" or "powerful".

## Banned phrases (hard block)

Reject the page if any of these (or close paraphrases) appear in the science
layer:

- "cure", "cures", "cured", "treats", "treatment for", "heals", "healing"
  (as a claimed outcome), "reverses", "fixes"
- "miracle" as a benefit descriptor (note: "Miracle of Mind" as the product
  name is fine; "meditation is a miracle cure" is not)
- "clinically proven", "scientifically proven", "proven to", "guaranteed"
- "boosts", "supercharges", "rewires your brain", "unlocks", "detoxes"
- "eliminates stress/anxiety", "eliminates disease"
- "natural alternative to medication", "instead of medication", "no need for"
- exclamation points anywhere in the science layer
- second-person promises about the reader's health ("you will sleep better")
- superlatives about the research ("the definitive study", "the best evidence
  ever")

## Per-paper page template (fixed 8 parts — all required, in order)

```
1. HEADLINE
   Plain-language statement of the finding, not hype. Names the outcome and the
   claim strength implicitly. Max ~12 words.
   e.g. "An 8-week trial linked daily breath meditation to lower self-reported stress"

2. ONE-PARAGRAPH SUMMARY (60–110 words)
   What was studied, in whom, what was found, and how confident we can be.
   Written for a curious non-scientist. No jargon without a gloss.

3. METHODOLOGY SNAPSHOT (structured)
   - Study type: (meta-analysis | systematic review | RCT | cohort |
     cross-sectional | mechanistic/neuroimaging)
   - Sample size: N (and population)
   - Duration: intervention length + follow-up
   - Practice studied: name it exactly (e.g. "Isha Shoonya", "MBSR",
     "focused-attention breath meditation"). State whether it is MoM,
     MoM-adjacent (breath-and-attention based), or unrelated.
   - Comparator: (waitlist | active control | none)

4. KEY FINDINGS (bulleted, claim-strength language)
   Each bullet uses a permitted stem from the vocabulary table. Include the
   direction and, where reported, the magnitude. Cite the same paper.

5. LIMITATIONS (always present — never empty)
   Sample size/representativeness, self-report vs objective measures, blinding,
   active-control absence, short follow-up, funding/conflict, generalizability.
   If the practice studied is not MoM, the transfer gap is stated here.

6. SADHGURU'S PERSPECTIVE (one paired verbatim quote)
   Exactly one verbatim quote on this theme, produced via the wisdom-pairing
   skill. Visually and editorially separated. Framed as perspective on the
   nature of mind — never as support for the study's benefit claim.

7. CITATION + THEME TAGS
   Full citation, linked to DOI. Theme tag(s) from the 7-theme taxonomy.
   If BIDMC Sadhguru Center research: include the standing independence note
   (Sadhguru and Isha Foundation play no role in the Center's funding; no
   institutional endorsement is implied).

8. MoM CTA
   Single, calm call to action toward the 7-minute practice. No health promise
   in the CTA.
```

Also required on every research page: the standing disclaimer — *"This page is
informational and is not medical advice. It does not replace care from a
qualified professional."*

## Workflow

1. Read the source paper (or its abstract + methods). Identify study type,
   population, practice, comparator, primary outcome, effect direction and size,
   and stated limitations.
2. Classify the practice: MoM / MoM-adjacent / unrelated. Set the transfer-gap
   note accordingly.
3. Draft parts 1–5 using only claim-strength stems the design supports.
4. Run the banned-phrases check. Remove or downgrade any violation.
5. Request the Sadhguru quote via the wisdom-pairing skill for this theme.
   Place it in part 6, visually separated.
6. Add citation, DOI link, tags, disclaimer, CTA.
7. Register every benefit claim in `CLAIMS-REGISTER.md`.

## CLAIMS-REGISTER.md row format

One row per benefit claim that appears on any page:

```
| page_slug | claim_text (as shown) | claim_strength | source_paper_DOI | practice_studied | is_MoM (Y/N/adjacent) | reviewer_signoff |
```

Leave `reviewer_signoff` blank; a qualified medical/scientific reviewer
co-signs at Gate 2 (BRIEF.md §11). The register must be readable end-to-end,
not skimmed.

## Self-check before shipping a page

- [ ] All 8 template parts present and in order
- [ ] Limitations section non-empty
- [ ] Every benefit claim cites a paper on the same page
- [ ] Claim strength matches design; nothing upgraded
- [ ] Zero banned phrases in the science layer
- [ ] Practice correctly labelled; transfer gap stated if not MoM
- [ ] Exactly one verbatim Sadhguru quote, sourced, editorially separated
- [ ] Disclaimer present
- [ ] Claims added to CLAIMS-REGISTER.md
