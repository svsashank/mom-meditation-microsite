# Project Brief: Meditation Research Microsite (Miracle of Mind)

**Status:** v2 — approved. This document is the standing authority for all autonomous work. Every downstream decision traces back to a line in this brief.

---

## 1. Purpose

Build an exhaustive, publicly accessible microsite on meditation under the Miracle of Mind (MoM) umbrella. The site contains Sadhguru's wisdom on meditation as well as plain-language summaries of the 100 most significant research papers on meditation that align with MoM.

**Strategic function:** This is a *doorway* asset, not a devotee asset. It engages with consciousness and mental-wellbeing content through a research lens. Science is the lead framing; Sadhguru's wisdom is the depth layer; MoM (the 7-minute practice) is the action layer.

**Primary conversion goal:** MoM app installs / practice initiation.
**Secondary goals:** Organic search *and answer-engine authority* on meditation-research queries; a citable reference asset for PR, media, and AI crawlers.

## 2. Audience

- Primary: 25–45, globally distributed, mental-wellbeing-curious, research-respecting, not self-identifying as spiritual seekers. Arrives via search, social shares, AI suggestions, or media citation.
- Explicitly NOT designed for: existing Isha meditators (they don't need convincing).

## 3. Positioning boundaries — what we say and never say

**Voice:** Calm, precise, evidence-respecting. Reads like a well-edited science publication with a contemplative sensibility. No hype, no wellness-industry clichés, no exclamation points.

**Claims discipline (non-negotiable):**
- Every health/benefit claim must cite a specific paper on the same page and use claim-strength language matched to the evidence: "an RCT found," "a meta-analysis suggests," "preliminary evidence indicates."
- Never: "meditation cures/treats/heals [condition]." Never medical advice. Never imply MoM substitutes for medical care.
- MoM-specific claims are limited to what MoM's own published data or clearly attributable research supports. Where a paper studied a different practice, say so plainly.
- Sadhguru's words are presented as wisdom/perspective, never as scientific claims. The two layers are visually and editorially distinct on every page.
- Standard disclaimer on all research pages: informational, not medical advice.

**Sadhguru layer rules:**
- Verbatim quotes only. No paraphrase, no synthesis "in the style of." Every quote carries a source (talk/book/program, year where available).
- No hagiography. Sadhguru appears as a voice on the nature of mind and meditation, not as the subject of the site.

## 4. Definition of "aligned with Miracle of Mind"

A paper qualifies if it studies one or more of:
1. Brief daily meditation practices (≤20 min/day) and their outcomes.
2. Core outcome domains MoM addresses: stress, anxiety, sleep quality, attention/focus, emotional regulation, general wellbeing.
3. Mechanisms: neuroplasticity, default mode network, HRV, cortisol, interoception, breath-attention interaction.
4. App-delivered or self-guided meditation efficacy.
5. Meditation traditions mechanistically adjacent to the MoM practice (breath-and-attention-based), including yogic practices where studied scientifically.

**Weighting rule (resolved):** Yogic-practice research is explicitly weighted UP in ranking — not merely included at parity with generic mindfulness studies. All else equal, a study of a yogic/breath-attention practice outranks a generic mindfulness study for the same theme slot.

Excluded: papers solely on practices with no mechanistic relation to MoM, retracted papers, predatory journals, papers with undisclosed conflicts that undermine credibility.

## 5. Paper selection criteria (the 100)

- **Sources:** Semantic Scholar + PubMed APIs, plus (resolved) prioritized search of publications from the **Sadhguru Center for a Conscious Planet at Beth Israel Deaconess Medical Center** (Harvard-affiliated, est. 2020) — an active, high-credibility source studying Sadhguru's own practices specifically. Longlist target: 250–300.
- **Quality floor:** Peer-reviewed, indexed journals.
- **Evidence hierarchy for ranking:** meta-analyses & systematic reviews > RCTs > longitudinal cohort > cross-sectional > mechanistic/neuroimaging (scored separately for "mechanisms" theme).
- **Impact signal:** citation count normalized by publication year; landmark older papers qualify despite age.
- **Balance requirement:** the 100 must include papers reporting null or mixed results and at least one major critical review of meditation-research quality.
- **Distribution target across themes (approved as-is):** stress & anxiety 20, sleep 10, attention & cognition 15, emotional regulation & wellbeing 15, brain & mechanisms 20, clinical applications 10, app-based/brief-practice efficacy 10.

**Framing note on BIDMC sourcing:** the Sadhguru Center discloses that Sadhguru and Isha Foundation play no role in its funding. Any page citing BIDMC Sadhguru Center research must state this independence plainly and must not imply institutional endorsement beyond what is factual.

## 6. Content taxonomy & site structure

```
Home
├── Theme hubs (7): Stress & Anxiety / Sleep / Focus & Attention /
│   Emotional Wellbeing / Brain & Mechanisms / Clinical Research /
│   Brief & App-Based Practice
├── Research library: 100 paper pages (filterable by theme, study type, year)
├── Sadhguru on Meditation: wisdom hub organized by the same 7 themes
├── The Practice: what MoM is, the 7-minute structure, how to start (single CTA page)
└── About / Methodology: how papers were selected — full transparency page
```

**Per-paper page template:**
1. Plain-language headline (finding, not hype)
2. One-paragraph summary
3. Methodology snapshot: study type, sample size, duration, practice studied
4. Key findings (bulleted, claim-strength language)
5. Limitations (always present)
6. "Sadhguru's perspective" — one paired verbatim quote on the theme
7. Citation (full, linked to DOI) + theme tags
8. MoM CTA

**Theme hub template:** editorial overview of the evidence landscape (what's strong, emerging, contested) + Sadhguru anchor quote + linked paper cards + CTA.

## 7. Technical decisions (standing authority granted)

- Static site: **Astro**. Content stored as structured MDX/JSON — one file per paper.
- Deploy to **Netlify staging** or **GitHub Pages** for review. No production/custom-domain deployment without explicit sign-off.
- Design: within Isha/MoM aesthetic language — restrained, spacious, contemplative; typography-led; no stock-photo wellness imagery.
- Full SEO structure: semantic markup, per-page meta, schema.org ScholarlyArticle markup, programmatic theme×outcome landing pages only where content genuinely supports them.
- Accessibility: WCAG AA.
- Analytics: placeholder slot only.

## 8. Skills to be authored before content production

1. `research-summary` — paper-page template, claim-strength vocabulary, banned phrases list, limitations-section requirement.
2. `wisdom-pairing` — verbatim-only rule, sourcing format (drawing from https://isha.sadhguru.org/en/wisdom/type/quotes and /topics), theme-matching logic, tone rules for framing sentences.

## 9. Autonomous authority & logging

Standing authority to: select the 100 papers per §5, write all copy per §3, make all design/technical calls per §7, and deploy to staging — without asking.

Every non-obvious judgment call is logged in `DECISIONS.md`. Lowest-confidence calls go to `FLAGGED.md`.

## 10. Review artifacts delivered with the staging site

1. **DECISIONS.md**
2. **CLAIMS-REGISTER.md** — must be genuinely read, not skimmed.
3. **FLAGGED.md** — ~10 lowest-confidence judgment calls.
4. **PAPERS-100.csv** — final list with selection scores.

## 11. Review gates

- **Gate 1 (this document):** Approved.
- **Gate 2 (final):** Staging site + four review artifacts. Claims register read in full; a qualified medical/scientific reviewer should co-sign it before any production launch.

## 12. Ongoing operation (post-launch)

Monthly agent run: scan new publications against §5, draft candidate additions with the same artifacts. No auto-publish.

## 13. Open items — RESOLVED

1. **Alignment definition (§4):** Yogic-practice research weighted UP. ✅ folded into §4/§5.
2. **Theme distribution (§5):** Approved as originally drafted. ✅
3. **Sadhguru wisdom source:** No internal Drive archive — source verbatim quotes from https://isha.sadhguru.org/en/wisdom/type/quotes and https://isha.sadhguru.org/en/wisdom/topics. ✅ folded into §8.
4. **Domain/subdomain intent:** Deferred — does not block staging build.
5. **Research partnerships/in-house data:** Sadhguru Center for a Conscious Planet at BIDMC (Harvard-affiliated). ✅ folded into §5, with independence-framing note.

---

*This is the final brief. Commit as `BRIEF.md` in the project repo. It supersedes all conversational instructions.*
