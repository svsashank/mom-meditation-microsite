import { defineCollection, z } from 'astro:content';

const THEMES = [
  'Stress & Anxiety','Sleep','Focus & Attention','Emotional Wellbeing',
  'Brain & Mechanisms','Clinical Research','Brief & App-Based Practice',
] as const;

const papers = defineCollection({
  type: 'data',
  schema: z.object({
    pmid: z.string(),
    doi: z.string().optional().default(''),
    title: z.string(),
    year: z.number(),
    journal: z.string().optional().default(''),
    authors: z.array(z.string()).optional().default([]),
    theme: z.enum(THEMES),
    allThemes: z.array(z.string()).optional().default([]),
    studyType: z.string(),
    claimStrength: z.string(),          // permitted stem family
    alignment: z.string(),              // yogic/breath-attention vs general
    practiceStudied: z.string(),
    isMoM: z.string(),                  // Y / N / adjacent
    citationCount: z.number().optional().default(0),
    rcr: z.string().optional().default(''),
    headline: z.string(),
    summary: z.string(),
    keyFindings: z.array(z.string()),
    methodology: z.object({
      studyType: z.string(), sampleSize: z.string(), duration: z.string(),
      practice: z.string(), comparator: z.string(),
    }),
    limitations: z.array(z.string()),
    nullOrCritical: z.string().optional().default(''),
    bidmc: z.boolean().optional().default(false),
    quoteKey: z.string().optional().default(''),   // -> quotes collection
    editorialReview: z.boolean().optional().default(true),
  }),
});

const quotes = defineCollection({
  type: 'data',
  schema: z.object({
    theme: z.string(),
    verified: z.boolean(),
    quoteText: z.string().optional().default(''),
    origin: z.string().optional().default(''),
    sourceUrl: z.string().optional().default(''),
    verifiedOn: z.string().optional().default(''),
    note: z.string().optional().default(''),
  }),
});

export const collections = { papers, quotes };
