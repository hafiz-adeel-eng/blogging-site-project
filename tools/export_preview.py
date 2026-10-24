"""Export an offline HTML preview with no sibling-file dependencies."""

import base64
import mimetypes
import re
import hashlib
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
OUTPUT = ROOT.parent / "dailyvertex-preview.html"
ASSETS = {}


def embed_assets(markup, directory):
    def image(match):
        path = (directory / match.group(1)).resolve()
        if not path.is_relative_to(SITE):
            raise ValueError(f"Asset outside site: {path}")
        mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
        raw = path.read_bytes()
        key = hashlib.sha256(raw).hexdigest()[:16]
        ASSETS[key] = f'data:{mime};base64,' + base64.b64encode(raw).decode('ascii')
        return f'data-asset="{key}"'

    return re.sub(r'src="([^"\n]+\.(?:svg|webp|png|jpg))"', image, markup)


def rewrite_links(markup, directory):
    def link(match):
        value = match.group(1)
        url = urlsplit(value)
        if url.scheme or url.netloc or not url.path:
            return match.group(0)
        target = (directory / url.path).resolve()
        if target.name == "index.html":
            query = parse_qs(url.query)
            topic = "saved" if "saved" in query else query.get("category", [""])[0]
            if topic:
                return f'href="#latest" data-topic="{topic.replace(chr(34), "&quot;")}"'
            return 'href="#latest"' if url.fragment else 'href="#"'
        if target.suffix == ".html":
            return f'href="#read-{target.stem}" data-open="read-{target.stem}"'
        return match.group(0)

    return re.sub(r'href="([^"\n]+)"', link, markup)


page = (SITE / "index.html").read_text()
stylesheet = (SITE / 'modern.css').read_text()+'\n'+(SITE/'directory.css').read_text()
def embed_font(match):
    path = SITE / match.group(1)
    data = base64.b64encode(path.read_bytes()).decode('ascii')
    mime = 'font/woff2' if path.suffix == '.woff2' else 'font/ttf'
    return f"url('data:{mime};base64,{data}')"
stylesheet = re.sub(r"url\('([^']+\.(?:ttf|woff2))'\)", embed_font, stylesheet)
page = re.sub(r'<link rel="stylesheet"[^>]+>', lambda _: '<style>'+stylesheet+'</style>', page)
page = re.sub(r'<script src="[^"]+" defer></script>', '', page)
page = re.sub(r'<link rel="preload"[^>]+>', '', page)
page = re.sub(r'<link rel="icon"[^>]+>', "", page)
page = rewrite_links(embed_assets(page, SITE), SITE)

dialogs = []
for path in [*sorted((SITE / "articles").glob("*.html")), SITE / "ai-governance.html", SITE / "about.html", SITE / "privacy.html", SITE/'sitemap.html']:
    source = path.read_text()
    content = re.search(r'<main\b[^>]*>(.*?)</main>', source, re.S).group(1)
    # TOC sections are already visible in the reading dialog.
    content = re.sub(r'<aside class="toc">.*?</aside>', "", content, flags=re.S)
    content = re.sub(r'<nav class="breadcrumbs".*?</nav>', "", content, flags=re.S)
    content = re.sub(r'<button class="share">.*?</button>', "", content, flags=re.S)
    content = content.replace('<h1>', '<h2 class="preview-title">').replace('</h1>', '</h2>')
    # Namespacing keeps article TOC/source links independent within each dialog.
    content = re.sub(r' id="([^"]+)"', lambda m: f' id="{path.stem}-{m.group(1)}"', content)
    content = re.sub(r' href="#([^"]+)"', lambda m: f' href="#{path.stem}-{m.group(1)}"', content)
    content = rewrite_links(embed_assets(content, path.parent), path.parent)
    dialogs.append(f'<dialog class="reading-dialog" id="read-{path.stem}" aria-label="Read {path.stem.replace("-", " ")}"><form method="dialog" class="dialog-toolbar"><button aria-label="Close article">Close ×</button></form><div class="reading-content">{content}</div></dialog>')

extra_css = '.reading-dialog:modal{display:block}.reading-content [id]{scroll-margin-top:70px}'
extra_js = """
document.addEventListener('click', event => {
  const anchor = event.target.closest('a[href^="#"]');
  if (anchor && anchor.closest('dialog') && !anchor.dataset.open && !['#', '#latest'].includes(anchor.getAttribute('href'))) {
    const target = document.getElementById(anchor.getAttribute('href').slice(1));
    if (target) { event.preventDefault(); target.scrollIntoView({block:'start'}); }
    return;
  }
  const link = event.target.closest('[data-open], [data-topic], a[href="#latest"], a[href="#"]');
  if (!link) return;
  const active = document.querySelector('dialog[open]');
  if (active) active.close();
  if (link.dataset.open) {
    event.preventDefault();
    const dialog = document.getElementById(link.dataset.open);
    if (dialog) { dialog.showModal(); dialog.scrollTop = 0; }
  } else if (link.dataset.topic) {
    const filter = [...document.querySelectorAll('[data-filter]')].find(b => b.dataset.filter === link.dataset.topic);
    if (filter) { document.querySelector('#search').value = ''; filter.click(); }
  }
});
document.querySelectorAll('dialog').forEach(dialog => {
  dialog.addEventListener('click', event => {
    if (event.target === dialog) {
      const box = dialog.getBoundingClientRect();
      if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) dialog.close();
    }
  });
});
const initialDialog = document.getElementById(location.hash.slice(1));
if (initialDialog?.tagName === 'DIALOG') initialDialog.showModal();
"""
page = page.replace("</head>", "<style>" + extra_css + "</style></head>")
asset_loader = 'const previewAssets = '+__import__('json').dumps(ASSETS)+''';
document.querySelectorAll('img[data-asset]').forEach(image => {
  image.src = previewAssets[image.dataset.asset];
});
'''
page = page.replace("</body>", "".join(dialogs) + "<script>" + asset_loader + (SITE / "modern.js").read_text() + "\n" + extra_js + "</script></body>")
OUTPUT.write_text(page)
article_page = page.replace('</body>', '<script>document.getElementById("read-brandrank-ai-normalization-transformation-rules").showModal();</script></body>')
(ROOT.parent / 'dailyvertex-article.html').write_text(article_page)
hammer_page = page.replace('</body>', '<script>document.getElementById("read-hammer-ai").showModal();</script></body>')
(ROOT.parent / 'dailyvertex-hammer-ai.html').write_text(hammer_page)
print(f"Exported {OUTPUT} ({OUTPUT.stat().st_size:,} bytes); all CSS, scripts and images embedded.")
