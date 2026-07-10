---
name: wisdom-pairing
description: >-
  Use when selecting and placing a Sadhguru quote on any page of the Miracle of
  Mind meditation microsite — the paired quote on a paper page, the anchor quote
  on a theme hub, or entries in the "Sadhguru on Meditation" wisdom hub. Enforces
  the verbatim-only rule, the required sourcing format, the theme-matching logic,
  and the tone rules for the framing sentence. Trigger whenever a Sadhguru quote
  is added, edited, or reviewed.
version: 1.0.0
---

# wisdom-pairing

Authoritative procedure for placing Sadhguru's words on the site. Implements
BRIEF.md §3 (Sadhguru layer rules) and §8.2. This layer is the *depth* layer:
wisdom and perspective on the nature of mind, held editorially distinct from the
science. It is never evidence for a health claim.

## Non-negotiables (read first)

1. **Verbatim only.** Use the exact words. No paraphrase, no summary, no
   stitching two passages together, no "in the style of," no AI-generated
   Sadhguru-isms. If you cannot verify the exact wording against a source, do
   not use the quote.
2. **Every quote carries a source** in the required format (below). A quote
   without a verifiable source does not ship.
3. **Never presented as a scientific claim.** The quote sits beside the science,
   not inside it. It must not be placed so as to appear to validate, prove, or
   explain a study result.
4. **No hagiography.** Sadhguru is a voice on mind and meditation, not the
   subject of the page. No honorific inflation, no biography, no "the great
   master says."
5. **One quote per paper page** (template part 6). Theme hubs get one anchor
   quote. The wisdom hub may hold several per theme, each individually sourced.

## Approved sources

Draw verbatim quotes only from:

- https://isha.sadhguru.org/en/wisdom/type/quotes
- https://isha.sadhguru.org/en/wisdom/topics

Prefer quotes that carry an attributable origin (a named talk, book, or
program, with a year where available). If the source page shows only the quote
text without a talk/book origin, record the Isha wisdom URL as the source and
mark origin as "Isha wisdom archive (origin not stated)".

Do NOT source quotes from third-party quote aggregators, social media reposts,
or unverified fan sites — wording drifts on those and cannot be trusted for a
verbatim rule.

## Required sourcing format

Store and display each quote with:

```
quote_text:      "<exact verbatim text>"
speaker:         Sadhguru
origin:          <talk / book / program name>, <year if available>
source_url:      <isha.sadhguru.org URL where verified>
theme:           <one of the 7 themes>
verified_on:     <YYYY-MM-DD>
```

Display citation beneath the quote reads, e.g.: *— Sadhguru, [origin], [year]*.
Where origin is not stated, display *— Sadhguru (Isha)* and keep the URL in the
data record.

## The 7 themes (must match the site taxonomy)

Stress & Anxiety · Sleep · Focus & Attention · Emotional Wellbeing ·
Brain & Mechanisms · Clinical Research · Brief & App-Based Practice

## Theme-matching logic

1. Identify the page's primary theme (paper page inherits its top theme tag;
   theme hub is self-evident).
2. Choose a quote whose subject genuinely addresses that theme's *human
   experience* — e.g. for Sleep, a quote on rest/wakefulness/the nature of
   sleep; for Focus & Attention, a quote on the wandering vs. focused mind.
3. Match at the level of *what the mind does*, not at the level of the study's
   metric. A quote about the restless mind pairs with an attention study; it
   does not "explain" the study's reaction-time result.
4. Do not reuse the same quote on more than ~2 paper pages; rotate to keep the
   wisdom layer fresh and avoid implying a single quote is a catch-all.
5. If no genuinely fitting verified quote exists for a theme slot, leave the
   slot empty and flag it rather than forcing a weak or off-topic pairing.

## Tone rules for the framing sentence

The optional one-line framing sentence that introduces the quote must:

- Be plain and quiet. No hype, no exclamation points, no reverential adjectives.
- Introduce the *perspective*, not assert a fact. Good: "On the nature of a
  restless mind, Sadhguru offers a different vantage:" Bad: "Sadhguru reveals
  the truth science is only now catching up to."
- Never claim the quote confirms, proves, or is confirmed by the study.
- Never create a causal or evidentiary bridge between the quote and a benefit
  ("as the research below proves"). The layers stay parallel, not stacked.
- Keep Sadhguru as a voice, not a subject — avoid "the visionary mystic," etc.

## Workflow

1. Determine the page theme.
2. Search the approved Isha wisdom URLs for candidate quotes on that theme.
3. Verify wording character-for-character against the source page. Copy exactly.
4. Record the full sourcing block (format above), including verified_on date.
5. Choose placement: paper page part 6, or theme-hub anchor, or wisdom-hub entry.
6. Write the framing sentence per tone rules (or omit it).
7. Confirm editorial/visual separation from the science layer.
8. If no fitting verified quote exists, leave empty and add a line to FLAGGED.md.

## Self-check before shipping a quote

- [ ] Wording is verbatim and was verified against an approved Isha URL
- [ ] Full sourcing block recorded (origin, url, theme, verified_on)
- [ ] Displayed with a source line
- [ ] Theme genuinely matches the human experience the page is about
- [ ] Framing sentence (if any) asserts perspective, not fact; no evidentiary bridge
- [ ] Not presented as validating a study result
- [ ] No hagiography; Sadhguru is a voice, not the subject
- [ ] Visually/editorially distinct from the science layer
