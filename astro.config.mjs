import { defineConfig } from 'astro/config';

// Staging config. No production/custom-domain deploy without sign-off (BRIEF §7).
// For GitHub Pages, set `site` + `base` to the repo path at deploy time.
export default defineConfig({
  site: 'https://svsashank.github.io',
  base: '/mom-meditation-microsite',
  build: { format: 'directory' },
});
