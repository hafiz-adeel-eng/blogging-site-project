# DailyVertex: Google Search Console submission

Prepared October 21, 2026 (Asia/Karachi).

- Production URL-prefix property: `https://dailyvertex.pages.dev/`
- Sitemap URL: `https://dailyvertex.pages.dev/sitemap.xml`
- Alternative plain-text sitemap: `https://dailyvertex.pages.dev/sitemap.txt`. It contains the same sixteen canonical URLs, one per line, UTF-8, without dates, markup, or comments. Both versions are declared in robots.txt.
- Expected sitemap inventory: 16 unique canonical HTTPS URLs, including `/articles/hammer-ai` and the human-readable `/sitemap` directory.
- Browser view: `/sitemap.xml` loads a same-origin CSS stylesheet so it displays a readable list. `/sitemap` is a clickable HTML directory with grouped article links. Styling does not establish or repair a Google fetch; the previously reported GSC error remains unconfirmed.
- Sitemap entries are sorted with the homepage first. Six articles include `lastmod` from their recorded Article `dateModified`; entries without a known content date omit it. Build/deployment time is not substituted for content dates.
- Source and production-build robots.txt both allow crawling and declare the sitemap.
- The existing SEO audit passed. This is a local artifact check, not confirmation that Google fetched the live website.

## Current state

The user reports the GSC fetch failure persists after the case redirect deployment; a Google-side root cause has not been established. Stop treating the local case-path correction or a format change as proof of a resolved GSC error.

Live-check blocker confirmed October 21: the running environment reports current enforced policy without `dailyvertex.pages.dev`, while the newer saved/published configuration includes it. The running instance's source configuration version differs from the configuration draft's base version. A turn-scoped network-permission grant was obtained, then ordinary proxy requests to `/`, `/robots.txt`, `/sitemap.xml`, and `/sitemap.txt` all failed at CONNECT with proxy HTTP 403, before contacting the site. The general permission grant did not update the environment's destination allowlist. No Google password or API token is needed to unblock public HTTP checks. Apply the preserved network rules to the running environment through environment settings, or reconnect it using the current published configuration, then recheck actual public responses. Saving a draft is not proof this runtime policy changed. No further sitemap format changes should be presented as a verified solution before that evidence or an authenticated GSC diagnostic is available.

Latest diagnostic: the user's detail screenshot appears to show `/Sitemap.txt` with an uppercase S. In the local Pages runtime, `/Sitemap.txt` and `/Sitemap.xml` returned HTTP 404 while lowercase `/sitemap.txt` and `/sitemap.xml` returned HTTP 200. This is a concrete case-sensitive path defect, though Google's next fetch is still needed to confirm it explains the reported failure. Two exact 301 rules in `site/_redirects` map those capitalized paths to the canonical lowercase files; the production preparer now retains that config. Do not broaden the rules to unrelated site paths or claim Google accepted the sitemap before a successful result.

The user supplied two Google HTML verification meta tags at different stages. Both are retained in the shared `head()` template in `tools/modern.py`, so they survive rebuilds and existing verification is preserved. The new token supplied on October 21 ends in `Brt_d2n8`. Each token occurs exactly once inside the head of all 17 source and production HTML pages, including the homepage; the existing SEO audit passed.

The latest screenshot explicitly reports **Verification method: HTML file** and a missing verification file. A meta tag is verified using **Other verification methods → HTML tag**, not the HTML file upload method. The screenshot's background property is not clearly DailyVertex, so confirm the intended URL-prefix property is exactly `https://dailyvertex.pages.dev/`. The phone also displays **No internet connection**; the user needs connectivity when pressing Verify. Google ownership success has not been confirmed.

No Google Search Console connector, Google outbound identity, or relevant injected credential is available. Cloudflare deployment authorization does not provide access to the user's Google account. The user's screenshot now shows access to the property's Sitemaps screen and a submitted entry dated October 21, 2026 with status **Couldn't fetch**, type **Unknown**, and zero discovered pages. The submitted URL is hidden by the table's horizontal scroll position. Its exact URL and detailed error have been requested; a successful Google fetch is not confirmed. Do not request another verification tag based on this screenshot.

Cloudflare confirmed the refreshed sitemap deployment `50e74fdf-adf7-4c6c-b125-1d193f005ed1` as **Production**, branch **main**. The exact sitemap artifact serves locally through Wrangler Pages with HTTP 200 and an XML MIME type for both an ordinary request and a Googlebot User-Agent. That User-Agent check does not reproduce Google's actual crawl. Direct public sitemap retrieval was denied by the environment proxy during CONNECT (403), before reaching the website; this is not evidence that the live site returns 403 to Google.

The screenshot's new-sitemap field already contains the `https://dailyvertex.pages.dev/` prefix. Enter `sitemap.xml` in the remaining input. Do not infer that the existing failed submission used the wrong path until its full URL is visible. If the exact correct URL still fails, inspect the detailed GSC error and actual public response before changing server settings or assuming a timing issue.

## Required ownership step

1. Open https://search.google.com/search-console/welcome in the intended Google account.
2. Add a **URL prefix** property for `https://dailyvertex.pages.dev/`. Do not choose a Domain property for `pages.dev`, which is Cloudflare's parent domain.
3. If ownership is not already verified, choose **HTML tag** and copy Google's exact `google-site-verification` meta tag. It is a public verification tag, not a password or API key.
4. The supplied tag has been added to the generated `<head>` in a way that survives subsequent builds. The exact tag was checked in the production artifact. Keep the tag after verification, and check the deployment record before requesting Google's ownership check.
5. The user clicks **Verify** in Search Console unless authenticated tool access becomes available. Do not describe ownership as verified without a successful result.

## Submit the sitemap after verification

The user reports the XML fetch issue still persists. An alternative text sitemap was added as a supported-format diagnostic, not as a claimed repair of an identified server problem. Google's official documentation was retrieved and read on October 21, 2026: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap#text. It explicitly supports a `.txt` file containing only one absolute URL per line. The local Cloudflare runtime serves the text file with HTTP 200 and `text/plain; charset=utf-8`; its body matches the production artifact. Successful Google fetch and the exact original GSC failure remain unconfirmed. If the text sitemap also fails, changing XML presentation is not a demonstrated remedy; the actual GSC fetch detail and public HTTP response are still needed.

For the alternative test, submit `sitemap.txt` in the existing property's new-sitemap input. The property origin is already prefixed in the user's UI. Do not submit the human-facing `/sitemap` HTML page, and do not claim the alternative has been accepted before a real GSC result.

Open the verified property, select **Sitemaps**, and submit `sitemap.xml` (the full URL is above). Check the actual result. A successful sitemap submission does not mean all URLs have been indexed.

Direct property link: https://search.google.com/search-console/sitemaps?resource_id=https%3A%2F%2Fdailyvertex.pages.dev%2F

Use URL Inspection for the homepage and priority article URLs if desired. Request indexing only through the available Search Console flow; do not use Google's restricted Indexing API for these ordinary editorial articles or the retired sitemap-ping endpoint.
