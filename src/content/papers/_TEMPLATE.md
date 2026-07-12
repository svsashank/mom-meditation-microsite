# Research page frontmatter template (site-wide standard)

Every `/research/[slug]/` page is generated from one JSON file in
`src/content/papers/`. Each file MUST carry the canonical fields below. This is
the JSON equivalent of the YAML frontmatter blueprint; the field order here is
the standard. Claims discipline (BRIEF §3) applies to every value — nothing may
be stronger than the source paper supports.

## Canonical fields (blueprint)

```yaml
title:              # exact published paper title
simplified_title:   # plain-language headline (no hype); JSON key: simplifiedTitle
study_type:         # Meta-analysis / Systematic review | RCT | Cohort / Longitudinal | Cross-sectional / Mechanistic ; JSON: studyType
publication_year:   # integer ; JSON: publicationYear
journal_name:       # peer-reviewed journal ; JSON: journalName
core_theme:         # one of the 7 themes ; JSON: coreTheme
primary_entity_url: # canonical source: DOI (https://doi.org/…) or PubMed URL ; JSON: primaryEntityUrl
related_theme_path: # internal link to the theme hub, e.g. /themes/stress-anxiety/ ; JSON: relatedThemePath
```

## Rules

- **No `app_deep_link` field.** A study's findings are NOT executed or embodied
  by the Miracle of Mind app. Pages link to the general practice page
  (`/practice/`) only, never to an app deep link tied to a specific study result.
- `ai_snippet` (JSON: `aiSnippet`) is a ≤100-word AEO summary built ONLY from the
  paper's own stated findings — no added claims, no cross-study synthesis.
- `primary_entity_url` prefers the DOI; falls back to the PubMed record.
- All existing fields (summary, keyFindings, methodology, limitations, quoteKey,
  bidmc, nullOrCritical, editorialReview, etc.) remain required by the schema.
