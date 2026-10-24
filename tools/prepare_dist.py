"""Build a lean Cloudflare upload directory without changing source assets.

Requires esbuild 0.28.2 (set ESBUILD_BIN or put esbuild on PATH).
WOFF2 font subsets are retained in site/fonts and need no build-time converter.
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
DESTINATION = ROOT / 'dist'
ESBUILD = os.environ.get('ESBUILD_BIN') or shutil.which('esbuild')
if not ESBUILD:
    raise SystemExit('esbuild is required: npm exec --yes --package=esbuild@0.28.2 -- python3 tools/prepare_dist.py')


def fingerprint(name, data):
    path = Path(name)
    digest = hashlib.sha256(data).hexdigest()[:12]
    return f'assets/{path.stem}.{digest}{path.suffix}'


def minify(text, loader):
    result = subprocess.run([ESBUILD, '--minify', '--legal-comments=none', f'--loader={loader}', '--target=es2020'], input=text, text=True, capture_output=True, check=True)
    return result.stdout.encode()


with tempfile.TemporaryDirectory(prefix='.dailyvertex-dist-', dir=ROOT) as directory:
    stage = Path(directory) / 'dist'
    (stage/'assets').mkdir(parents=True)
    replacements = {}
    references = '\n'.join(path.read_text() for path in SITE.rglob('*.html'))+'\n'+(SITE/'modern.css').read_text()
    # TTF originals, old design files, and launch-only helper files stay outside deployment.
    for path in [*sorted((SITE/'images').glob('*')), *sorted((SITE/'fonts').glob('*.woff2')), *sorted((SITE/'fonts').glob('*LICENSE.txt')), SITE/'favicon.svg']:
        if not path.is_file() or path.name == 'ai.svg':
            continue
        if path.parent == SITE/'images' and 'images/'+path.name not in references:
            continue
        data = path.read_bytes()
        name = fingerprint(path.name, data)
        (stage/name).write_bytes(data)
        replacements[path.resolve()] = '/'+name

    css = (SITE/'modern.css').read_text()
    def css_asset(match):
        path = (SITE/match.group(1)).resolve()
        return "url('"+replacements[path]+"')"
    css = re.sub(r"url\('([^']+\.woff2)'\)", css_asset, css)
    for path, content, loader in [(SITE/'modern.css', css, 'css'), (SITE/'directory.css', (SITE/'directory.css').read_text(), 'css'), (SITE/'modern.js', (SITE/'modern.js').read_text(), 'js')]:
        data = minify(content, loader)
        name = fingerprint(path.name, data)
        (stage/name).write_bytes(data)
        replacements[path.resolve()] = '/'+name

    for path in sorted(SITE.rglob('*.html')):
        text = path.read_text()
        def html_asset(match):
            attribute, quote, value = match.groups()
            parsed = urlsplit(value)
            if parsed.scheme or parsed.netloc or not parsed.path:
                return match.group(0)
            resolved = (path.parent/unquote(parsed.path)).resolve()
            replacement = replacements.get(resolved)
            if replacement:
                return attribute+'='+quote+replacement+quote
            if attribute == 'href' and resolved.suffix == '.html' and resolved.is_file() and resolved.is_relative_to(SITE):
                relative = resolved.relative_to(SITE).as_posix()
                clean = '/' if relative == 'index.html' else '/'+relative.removesuffix('.html')
                if parsed.query:
                    clean += '?'+parsed.query
                if parsed.fragment:
                    clean += '#'+parsed.fragment
                return attribute+'='+quote+clean+quote
            return match.group(0)
        text = re.sub(r'\b(src|href)=([\'"])(.*?)\2', html_asset, text)
        # Only collapse inter-tag whitespace; preserve code blocks and inline text.
        text = re.sub(r'>\s+<', '><', text)
        target = stage/path.relative_to(SITE)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
    for name in ['robots.txt', 'sitemap.xml', 'sitemap.txt', 'sitemap.css', '_redirects']:
        if (SITE/name).exists():
            shutil.copy2(SITE/name, stage/name)
    for path in stage.rglob('*.html'):
        text = path.read_text()
        for original, replacement in replacements.items():
            # Metadata and JSON-LD use absolute image URLs rather than src/href.
            if original.is_relative_to((SITE/'images').resolve()):
                relative = original.relative_to(SITE.resolve()).as_posix()
                text = re.sub(r'(https://[^/"<>\s]+)/'+re.escape(relative)+r'(?=["<>\s])', lambda m: m.group(1)+replacement, text)
        path.write_text(text)
    headers = (SITE/'_headers').read_text() + '\n/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n'
    (stage/'_headers').write_text(headers)
    files = {str(p.relative_to(stage)):p.stat().st_size for p in stage.rglob('*') if p.is_file()}
    if DESTINATION.exists():
        # Remove only obsolete generated distribution assets, never source or user files.
        old_manifest = DESTINATION/'.generated-files.json'
        if not old_manifest.exists():
            raise SystemExit('dist exists without a generated-file manifest; preserve it and choose a different output path')
        for name in json.loads(old_manifest.read_text()):
            old_path = (DESTINATION/name).resolve()
            if not old_path.is_relative_to(DESTINATION.resolve()):
                raise ValueError('Invalid path in previous distribution manifest')
            if old_path.is_file():
                old_path.unlink()
    DESTINATION.mkdir(exist_ok=True)
    shutil.copytree(stage, DESTINATION, dirs_exist_ok=True)
    (DESTINATION/'.generated-files.json').write_text(json.dumps(sorted(files)))
    print(f'Optimized upload: {len(files)} files, {sum(files.values()):,} bytes. Assets have content hashes and immutable caching.')
