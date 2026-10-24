const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');

(async () => {
  const browser = await chromium.launch({ executablePath: '/usr/bin/chromium', headless: true, args: ['--no-sandbox'] });
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1100 }, reducedMotion: 'reduce' });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto('http://127.0.0.1:3000/', { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    assert.equal(await page.locator('.story:visible').count(), 13);
    assert.equal(await page.locator('.site-header').evaluate(el => getComputedStyle(el).display), 'flex');
    assert(await page.evaluate(() => document.fonts.check('500 16px Outfit')));
    await page.locator('[data-filter="Travel"]').click();
    assert.equal(await page.locator('.story:visible').count(), 1);
    await page.locator('[data-filter="All stories"]').click();
    await page.locator('#search').fill('hammer ai');
    assert.equal(await page.locator('.story:visible').count(), 1);
    assert.equal(await page.locator('.story:visible').getAttribute('data-slug'), 'hammer-ai');
    await page.locator('#search').fill('brandrank');
    assert.equal(await page.locator('.story:visible').count(), 1);
    await page.locator('#search').fill('unfindable query zxqw');
    assert(await page.locator('#empty').isVisible());
    await page.locator('#reset').click();
    await page.locator('.story [data-save]').first().click();
    assert.equal(await page.locator('.saved-count').textContent(), '1');
    await page.locator('[data-filter="saved"]').click();
    assert.equal(await page.locator('.story:visible').count(), 1);
    await page.reload();
    assert.equal(await page.locator('.saved-count').textContent(), '1');
    await page.locator('#theme').click();
    assert(await page.locator('body').evaluate(el => el.classList.contains('dark')));
    await page.reload();
    assert(await page.locator('body').evaluate(el => el.classList.contains('dark')));
    await page.locator('#theme').click();

    const slug = 'brandrank-ai-normalization-transformation-rules';
    await page.goto(`http://127.0.0.1:3000/articles/${slug}.html`);
    assert.equal(await page.locator('h1').count(), 1);
    assert((await page.locator('h1').textContent()).includes('BrandRank.ai'));
    const schema = JSON.parse(await page.locator('script[type="application/ld+json"]').first().textContent());
    assert.equal(schema['@type'], 'Article');
    assert.equal(schema.headline, await page.locator('h1').textContent());
    const visibility = page.locator('[data-visibility-calculator]');
    assert.equal(await visibility.locator('output').textContent(), '60% / 25%');
    await visibility.locator('[name="recommendations"]').fill('25');
    assert.equal(await visibility.locator('output').textContent(), 'Check the inputs');
    await visibility.locator('[name="recommendations"]').fill('10');
    await visibility.locator('[name="responses"]').fill('0');
    assert.equal(await visibility.locator('output').textContent(), 'Check the inputs');
    await visibility.locator('[name="responses"]').fill('40');
    assert.equal(await visibility.locator('output').textContent(), '60% / 25%');
    await page.locator('.faq summary').first().click();
    assert(await page.locator('.faq details').first().evaluate(el => el.open));
    await page.screenshot({ path: '/workspace/dailyvertex-final-article.png', fullPage: false });

    await page.goto('http://127.0.0.1:3000/articles/normalization-transformation-rules.html');
    const numeric = page.locator('[data-calculator]');
    assert.equal(await numeric.locator('output').textContent(), '0.25');
    await numeric.locator('[name="observation"]').fill('70');
    assert.equal(await numeric.locator('output').textContent(), '1.25');
    await numeric.locator('[name="maximum"]').fill('20');
    assert.equal(await numeric.locator('output').textContent(), 'Check the inputs');
    await numeric.locator('[name="minimum"]').fill('');
    assert.equal(await numeric.locator('output').textContent(), 'Check the inputs');

    for (const width of [360, 390, 768, 1024, 1440]) {
      await page.setViewportSize({ width, height: 1100 });
      await page.goto('http://127.0.0.1:3000/', { waitUntil: 'networkidle' });
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false, `home overflow at ${width}`);
      assert(await page.locator('img').evaluateAll(async images => {
        images.forEach(image => { image.loading = 'eager'; });
        await Promise.all(images.map(image => image.decode()));
        return images.every(image => image.complete && image.naturalWidth > 0);
      }));
      if (width === 390) {
        await page.locator('.menu-button').click();
        assert.equal(await page.locator('.menu-button').getAttribute('aria-expanded'), 'true');
        await page.keyboard.press('Escape');
        assert.equal(await page.locator('.menu-button').getAttribute('aria-expanded'), 'false');
        await page.screenshot({ path: '/workspace/dailyvertex-final-mobile.png', fullPage: true });
      }
      if (width === 1440) await page.screenshot({ path: '/workspace/dailyvertex-final-design.png', fullPage: false });
      await page.goto(`http://127.0.0.1:3000/articles/${slug}.html`);
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false, `article overflow at ${width}`);
    }

    const context = await browser.newContext({ offline: true, viewport: { width: 1000, height: 900 }, reducedMotion: 'reduce' });
    const offline = await context.newPage();
    const requests = [];
    offline.on('pageerror', error => errors.push(error.message));
    offline.on('request', request => { if (!request.url().startsWith('data:')) requests.push(request.url()); });
    await offline.setContent(fs.readFileSync('/workspace/dailyvertex-preview.html', 'utf8'), { waitUntil: 'load' });
    await offline.evaluate(() => document.fonts.ready);
    assert.equal(await offline.locator('.story:visible').count(), 13);
    assert(await offline.evaluate(() => document.fonts.check('500 16px Outfit')));
    assert(await offline.locator('img').evaluateAll(async images => {
      images.forEach(image => { image.loading = 'eager'; });
      await Promise.all(images.map(image => image.decode()));
      return images.every(image => image.complete && image.naturalWidth > 0);
    }));
    await offline.locator('.data-feature').click();
    assert(await offline.locator(`#read-${slug}`).isVisible());
    assert.equal(await offline.locator(`#read-${slug} output`).textContent(), '60% / 25%');
    await offline.locator(`#read-${slug} a[href="#${slug}-sources"]`).first().click();
    assert(await offline.locator(`#${slug}-sources`).isVisible());
    await offline.keyboard.press('Escape');
    await offline.locator('.story [data-save]').first().click();
    await offline.locator('.saved-link').click();
    assert.equal(await offline.locator('.story:visible').count(), 1);
    await offline.locator('[data-filter="All stories"]').click();
    await offline.locator('#search').fill('brandrank');
    assert.equal(await offline.locator('.story:visible').count(), 1);
    await offline.locator('#search').fill('hammer ai');
    await offline.locator('.story:visible h3 a').click();
    assert(await offline.locator('#read-hammer-ai').isVisible());
    assert.equal(await offline.locator('#read-hammer-ai img').count(), 2);
    await offline.keyboard.press('Escape');
    assert.deepEqual(requests, []);
    assert.deepEqual(errors, []);
    await page.goto('http://127.0.0.1:3000/articles/ai-transformation-is-a-problem-of-governance.html');
    assert((await page.locator('h1').textContent()).includes('AI Transformation Is a Problem of Governance'));
    const structured = await page.locator('script[type="application/ld+json"]').allTextContents();
    const entities = structured.flatMap(text => { const value=JSON.parse(text); return value['@graph'] || [value]; });
    assert(entities.some(value => value['@type']==='Article'));
    assert(entities.some(value => value['@type']==='BreadcrumbList'));
    const faq = entities.find(value => value['@type']==='FAQPage');
    assert.equal(faq.mainEntity.length, await page.locator('.faq details').count());
    const cover = await page.locator('.article-cover').getAttribute('src');
    assert(cover.includes('governance.webp'));
    await page.goto('http://127.0.0.1:3000/ai-governance.html');
    assert.equal(await page.locator('.hub-sequence article').count(), 3);
    await page.goto('http://127.0.0.1:3000/articles/hammer-ai.html');
    const hammerEntities = (await page.locator('script[type="application/ld+json"]').allTextContents()).flatMap(text => {
      const value = JSON.parse(text); return value['@graph'] || [value];
    });
    const hammerArticle = hammerEntities.find(value => value['@type']==='Article');
    assert.equal(hammerArticle.datePublished, '2026-10-21');
    assert.equal(hammerArticle.headline, await page.locator('h1').textContent());
    assert.equal(hammerEntities.find(value => value['@type']==='FAQPage').mainEntity.length, 8);
    assert.equal(await page.locator('article img').count(), 2);
    assert((await page.locator('.editorial-note').first().textContent()).includes('not a hands-on'));
    await page.locator('.faq summary').first().click();
    assert(await page.locator('.faq details').first().evaluate(element => element.open));
    if (process.env.PAGES_TEST_ORIGIN) {
      const origin = process.env.PAGES_TEST_ORIGIN;
      const sitemap = await (await page.request.get(`${origin}/sitemap.xml`)).text();
      const paths = [...sitemap.matchAll(/<loc>https:\/\/dailyvertex.pages.dev([^<]*)<\/loc>/g)].map(match => match[1]);
      for (const path of paths) {
        const response = await page.request.get(origin+path, { maxRedirects: 0 });
        assert.equal(response.status(), 200, `production route ${path}`);
      }
      const redirect = await page.request.get(`${origin}/articles/ai-transformation-is-a-problem-of-governance.html`, { maxRedirects: 0 });
      assert.equal(redirect.status(), 308);
      assert.equal(redirect.headers().location, '/articles/ai-transformation-is-a-problem-of-governance');
      for (const width of [390, 1440]) {
        await page.setViewportSize({ width, height: 1000 });
        for (const path of ['/', '/ai-governance', '/articles/ai-transformation-is-a-problem-of-governance', '/articles/hammer-ai']) {
          await page.goto(origin+path, { waitUntil: 'networkidle' });
          assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false, `${path} overflow at ${width}`);
          assert(await page.locator('img').evaluateAll(async images => {
            images.forEach(image => { image.loading = 'eager'; });
            await Promise.all(images.map(image => image.decode()));
            return images.every(image => image.complete && image.naturalWidth > 0);
          }));
          if (path === '/' || path.startsWith('/articles/')) {
            const name = path === '/' ? 'home' : path.endsWith('hammer-ai') ? 'hammer' : 'governance';
            await page.screenshot({ path: `/workspace/dailyvertex-seo-${name}-${width}.png`, fullPage: false });
          }
        }
      }
      assert.deepEqual(errors, []);
      console.log(`PASS: ${paths.length} Cloudflare runtime routes, clean URL redirect, production images, mobile/desktop layouts and no JavaScript errors.`);
    }
    console.log('PASS: thirteen stories; Hammer AI search, two images, eight FAQs and schema; filters/empty state; saved articles and theme persistence; both calculators; mobile menu; five viewport sizes; three-guide governance hub; standalone HTML with embedded images/fonts and zero external requests; no JavaScript errors.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
