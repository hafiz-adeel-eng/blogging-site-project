"""Audit the built Pages directory for crawlable URLs and consistent metadata."""

import json
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT/'dist'
ORIGIN = 'https://dailyvertex.pages.dev'


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

    def values(self, tag, key, **where):
        return [attrs[key] for name, attrs in self.tags if name == tag and key in attrs and all(attrs.get(k) == v for k, v in where.items())]


class PageText(HTMLParser):
    def __init__(self, markup):
        super().__init__(convert_charrefs=True)
        self.text = ''
        self.feed(markup)

    def handle_data(self, data):
        self.text += ' '+data


def target(url):
    path = unquote(urlsplit(url).path)
    file = DIST/path.lstrip('/') if path != '/' else DIST/'index.html'
    if not file.suffix:
        file = file.with_suffix('.html')
    assert file.is_relative_to(DIST), url
    return file


def flatten(data):
    return data.get('@graph', [data])


canonicals, titles, descriptions = set(), set(), set()
content_dates = {}
articles = 0
for file in sorted(DIST.rglob('*.html')):
    text = file.read_text()
    page = Page(text)
    assert len(re.findall(r'<h1\b', text)) == 1, file
    if file.name == '404.html':
        assert page.values('meta', 'content', name='robots') == ['noindex,follow']
        continue
    title = re.search(r'<title>(.*?)</title>', text).group(1)
    desc, = page.values('meta', 'content', name='description')
    canonical, = page.values('link', 'href', rel='canonical')
    expected = ORIGIN+'/'+('' if file.name == 'index.html' else file.relative_to(DIST).as_posix().removesuffix('.html'))
    assert canonical == expected, file
    assert title not in titles and desc not in descriptions
    assert 25 <= len(title) <= 75, (file, len(title))
    assert 70 <= len(desc) <= 180, (file, len(desc))
    titles.add(title)
    descriptions.add(desc)
    canonicals.add(canonical)
    assert page.values('meta', 'content', property='og:url') == [canonical]
    og, = page.values('meta', 'content', property='og:image')
    assert target(og).is_file(), (file, og)
    assert page.values('meta', 'content', name='twitter:image') == [og]
    for tag, attrs in page.tags:
        if tag == 'img':
            assert attrs.get('alt') and attrs.get('width') and attrs.get('height'), file
            assert target(attrs['src']).is_file(), (file, attrs['src'])
        if tag == 'a' and attrs.get('href'):
            url = urlsplit(attrs['href'])
            if url.scheme or url.netloc or not url.path:
                continue
            assert url.path.startswith('/') and not url.path.endswith('.html'), (file, url.path)
            assert target(attrs['href']).is_file(), (file, attrs['href'])
    entities = [entity for blob in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S) for entity in flatten(json.loads(blob))]
    article = next((item for item in entities if item.get('@type') == 'Article'), None)
    if article:
        articles += 1
        assert article['url'] == canonical
        assert article['image'] == og
        if article.get('dateModified'):
            content_dates[canonical] = article['dateModified']
        assert any(item.get('@type') == 'BreadcrumbList' for item in entities)
        pairs = re.findall(r'<details><summary>(.*?)</summary>(.*?)</details>', text, re.S)
        faq = next((item for item in entities if item.get('@type') == 'FAQPage'), None)
        if pairs:
            assert faq and len(faq['mainEntity']) == len(pairs)
            for (question, answer), entity in zip(pairs, faq['mainEntity']):
                assert ' '.join(PageText(question).text.split()) == ' '.join(entity['name'].split())
                assert ' '.join(PageText(answer).text.split()) == ' '.join(entity['acceptedAnswer']['text'].split())


namespace = {'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
sitemap = ET.parse(DIST/'sitemap.xml')
listed = [element.text for element in sitemap.findall('s:url/s:loc', namespace)]
assert len(listed) == len(set(listed)) and set(listed) == canonicals
assert (DIST/'sitemap.txt').read_text(encoding='utf-8').splitlines() == listed
for entry in sitemap.findall('s:url',namespace):
    url = entry.findtext('s:loc',namespaces=namespace)
    assert entry.findtext('s:lastmod',namespaces=namespace) == content_dates.get(url), url
assert 'Sitemap: '+ORIGIN+'/sitemap.xml' in (DIST/'robots.txt').read_text()
assert 'Sitemap: '+ORIGIN+'/sitemap.txt' in (DIST/'robots.txt').read_text()
assert articles == 13
homepage = (DIST/'index.html').read_text()
for article in (DIST/'articles').glob('*.html'):
    assert f'href="/articles/{article.stem}"' in homepage
images = json.loads((ROOT/'site/images/editorial-manifest.json').read_text())
assert len(images) == articles
assert all(item['bytes'] <= 100000 and item['thumbnail_bytes'] <= 35000 for item in images.values())
print(f'PASS: {len(canonicals)} indexable pages; {articles} articles with optimized covers/thumbnails; unique metadata; clean canonical URLs; matching sitemap, social images, schema, FAQs and internal links.')
