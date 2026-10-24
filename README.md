# DailyVertex

An English-language responsive multi-niche editorial website for Cloudflare Pages. Navy, sky blue and teal visual identity, locally served Outfit/Manrope fonts, SVG icons, motion with reduced-motion support and thirteen topic-specific AI-generated article covers. No third-party runtime dependencies.

## Run locally

```sh
cd /workspace/blogging-site-project
python3 tools/build.py
python3 -m http.server 3000 --bind 0.0.0.0 --directory site
```

## Features

- Thirteen separate, crawlable article pages across technology, lifestyle, business, travel and wellness. Includes a source-based Hammer AI desktop guide, a three-guide AI governance cluster, an original branded normalization field guide and a separate numerical/text normalization guide.
- Working client-side search, category filters, empty states, saved reading list, persistent dark/light theme, reading progress and native sharing/copy link.
- Saves and theme use this browser's localStorage; no accounts or cloud sync.
- Mobile layouts, keyboard focus, skip link, reduced motion support, local images, lazy loading below the fold.
- Unique titles/descriptions, article-specific social images, Article/BreadcrumbList/FAQPage JSON-LD, an AI governance collection hub, clean canonical URLs, sitemap, robots.txt, favicon, privacy/about and custom 404.
- Run tools/build.py to generate pages. The current design templates live in tools/modern.py; current styles and behavior are site/modern.css and site/modern.js. Legacy styles.css/app.js remain for preservation but are not loaded by current pages. Image originals stay in site/images.
- Article fragments are maintained in content/. The original normalization research is documented in research/content-research.md. The new governance research, two live competitor reviews, primary sources and access limitations are recorded separately in research/ai-governance-research.md. No Google PAA panel, Reddit thread or Quora answer was retrieved; FAQ provenance is disclosed.
- All thirteen articles have descriptive image alt text and visible AI illustration captions. Covers are at most 100 KB, with card thumbnails at most 35 KB. The Hammer AI guide also includes a 28 KB explanatory local/cloud illustration. WebP files and their manifest are retained in site/images; original generated PNGs are preserved outside the checkout in /workspace/generated_images. Regenerating exports requires those originals and Pillow; routine builds use the retained WebPs. `python3 tools/prepare_images.py hammer` refreshes only the Hammer AI images and preserves other exports.
- Two working calculators distinguish brand mention/recommendation rates from numerical feature scaling, including invalid-input handling.
- The Hammer AI research map is research/hammer-ai-research.md. Publisher-linked release assets, Jan's directory, and primary Ollama/Jan documentation were reviewed. Current product pricing, privacy policy and exact hardware requirements were not retrieved; the guide discloses this and makes no hands-on benchmark claim. Natural long-tail coverage includes downloads, offline use, privacy, model requirements, troubleshooting and alternatives. Eight visible FAQs match FAQPage schema.
- Run python3 tools/export_preview.py to produce /workspace/dailyvertex-preview.html, /workspace/dailyvertex-article.html and /workspace/dailyvertex-hammer-ai.html. Fonts, images, CSS and JavaScript are embedded; all articles open in accessible dialogs. The last file opens the Hammer AI article immediately.
- Browser verification: node tools/check_site.cjs (requires the environment's Playwright and /usr/bin/chromium). It checks user-facing behavior, production pages, offline preview, images, schema, calculators and five viewport sizes.

## SEO and domain

Alternative text sitemap: `/sitemap.txt`, with the same sixteen canonical URLs as the XML file, one URL per UTF-8 line. Both versions are declared in robots.txt. Google's official sitemap documentation supports this format. It is a diagnostic alternative for the user's unresolved GSC fetch error; it is not evidence of a successful Google fetch. The local Pages runtime returns HTTP 200 and `text/plain; charset=utf-8`.

Sitemap path casing: `site/_redirects` permanently redirects `/Sitemap.txt` and `/Sitemap.xml` to their lowercase canonical files. The user's detail screenshot appears to show the capitalized text path, which previously returned a local 404. Keep `_redirects` in the distribution and retain lowercase URLs in robots.txt. A subsequent Google fetch must confirm the external outcome.

A readable sitemap is available at `/sitemap`: an English directory grouping all eleven articles by topic and linking to the main publication pages. The XML at `/sitemap.xml` also has a lightweight native CSS browser view (`site/sitemap.css`); no XSLT or script is required. The XML still contains standard sitemap elements. It includes sixteen indexable URLs, with the directory itself included. The directory's own fifteen destination links exclude itself. Browser checks passed at mobile and desktop widths; this visual change does not claim to fix the separate GSC fetch status.

After you know the exact HTTPS production origin, rebuild with:

```sh
SITE_URL=https://YOUR-ACTUAL-DOMAIN python3 tools/build.py
```

Use the actual origin without a trailing path. This generates absolute clean canonical URLs and sitemap.xml and registers the sitemap in robots.txt. Production origin is https://dailyvertex.pages.dev. Cloudflare Pages redirects .html requests to clean URLs; production internal links match that behavior. Each article uses its own fingerprinted cover in Open Graph, Twitter and Article schema. Search rankings, rich results and AI citations are not guaranteed. Continue reviewing the introductory launch stories and editorial sourcing as the publication grows.

Both user-supplied Google Search Console HTML verification meta tags are retained in `head()` in `tools/modern.py` and are present in generated HTML, including the homepage. Preserve them in future builds. Each token occurs once per page. This does not itself confirm Google ownership verification or sitemap submission. Use the **HTML tag** verification method for these tokens; the user's latest screenshot shows a failure under the separate **HTML file** method. The intended URL-prefix property is `https://dailyvertex.pages.dev/` and its sitemap is `https://dailyvertex.pages.dev/sitemap.xml`; see `research/search-console-setup.md` for the remaining Google-account steps.

## Cloudflare Pages

Framework preset: None. The recommended output directory is `dist`, using the optimized build below. Set SITE_URL to the real production origin. For Direct Upload, upload the contents of dist or the refreshed /workspace/dailyvertex-cloudflare.zip. _headers applies security policies on Cloudflare Pages.

### Optimized production upload

The production directory is now `dist/`: only deployed pages/assets, WOFF2 font subsets, minified CSS/JavaScript, fingerprinted URLs, font licenses and one-year immutable caching for fingerprinted assets. Source TTFs and legacy assets remain in `site/` for preservation and are excluded from deployment. WOFF2 subsets cover the English content and punctuation; regenerate them before publishing another script or alphabet.

```sh
SITE_URL=https://dailyvertex.pages.dev python3 tools/build.py
npm exec --yes --package=esbuild@0.28.2 -- python3 tools/prepare_dist.py
python3 tools/export_preview.py
python3 tools/audit_seo.py
```

For Git-integrated Pages builds, use the build commands above and output directory `dist`. For Direct Upload or Wrangler, upload `dist`, not the large standalone preview. The standalone preview now embeds fonts in WOFF2 and stores each repeated image only once.

`tools/audit_seo.py` checks all 18 indexable pages, canonical/sitemap agreement, unique metadata, image URLs, internal links and visible FAQ/schema consistency. `PAGES_TEST_ORIGIN=http://127.0.0.1:3001 node tools/check_site.cjs` also checks a local Wrangler Pages runtime when running on that port, in addition to the source server on port 3000. Loopback URLs are for internal checks only.

Deployment tool installed outside the checkout: `/workspace/.tools/dailyvertex-cli/node_modules/.bin/wrangler` (4.151.3). The user completed Cloudflare OAuth device authorization with account read, user read and Pages write scopes. Use Wrangler's normal credential storage without reading or copying its contents; no manually pasted API token is required. For this environment set `XDG_CONFIG_HOME=/workspace/.config`, `XDG_CACHE_HOME=/workspace/.cache`, and `WRANGLER_SEND_METRICS=false` when invoking the CLI.

### Current production deployment

Production website: https://dailyvertex.pages.dev/

Cloudflare Pages project: `dailyvertex`, production branch: `main`.

Deployment ID: `5bcceaba` (latest full identifier in `research/deployment.json`).

Immutable deployment URL: https://5bcceaba.dailyvertex.pages.dev/

Updated October 21, 2026 (Asia/Karachi) with exact sitemap-case redirects. The user's latest detail screenshot appears to show /Sitemap.txt, which reproduced a 404 locally while lowercase /sitemap.txt returned 200. Both capitalized text and XML paths now redirect permanently to their canonical lowercase files. A fresh Pages runtime confirmed 301 then 200, correct content types and the exact sixteen-URL bodies for ordinary and Googlebot User-Agent requests. Cloudflare confirmed Production/main and uploaded _redirects. Distribution: 54 generated files, 1,776,287 bytes; Wrangler uploaded one asset and reused 52, then uploaded both header and redirect configuration. Google has not yet confirmed a successful next fetch. Both Google meta tags and the readable, XML and text sitemap versions are preserved.

For future updates, build with `SITE_URL=https://dailyvertex.pages.dev`, prepare `dist/`, then run:

```sh
WRANGLER_SEND_METRICS=false XDG_CONFIG_HOME=/workspace/.config XDG_CACHE_HOME=/workspace/.cache /workspace/.tools/dailyvertex-cli/node_modules/.bin/wrangler pages deploy /workspace/blogging-site-project/dist --project-name dailyvertex --branch main --commit-dirty=true
```

## Deliberate boundaries

No CMS, admin login, comments database, newsletter service, live AI integration, analytics, or contact submission backend is configured. No fake subscriptions or generated usage statistics are shown. API-backed features need separate service configuration and credentials. Content is in English; status updates can be in Urdu. Source code, article content, optimized images, and build scripts are versioned in this repository. Cloudflare deployment remains a separate step; connecting a repository alone does not enable automatic deployment.

The CVS Health cordless water flosser guide adds ten H2 sections and eight original FAQs. Product-specific specifications could not be verified; see `research/cvs-water-flosser-editorial.md` for the disclosure and validation record.

The networking-events guide was updated after reading five Columbia CCE sources and is ready for production. See `research/networking-events-research.md` for exact evidence and remaining Google/Reddit/Quora/Pinterest limitations. The earlier separate preview copy remains noindex.
