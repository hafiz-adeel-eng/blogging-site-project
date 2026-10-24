"""DailyVertex's editorial design and accessible static page templates."""

import html
import json
import os
import re
from pathlib import Path
from urllib.parse import urlsplit
from math import ceil
from xml.etree import ElementTree as ET

E = html.escape
ROOT = Path(__file__).resolve().parents[1]
KEYWORD = 'brandrank-ai-normalization-transformation-rules'
TITLE = 'BrandRank.ai Normalization Transformation Rules: Practical Guide'
DESCRIPTION = 'A practical guide to BrandRank.ai normalization transformation rules: brand aliases, verified facts, AI mentions, recommendation metrics, and audit-ready records.'
GOVERNANCE = 'ai-transformation-is-a-problem-of-governance'
GOVERNANCE_TITLE = 'AI Transformation Is a Problem of Governance: A Practical Guide'
GOVERNANCE_DESCRIPTION = 'Why AI transformation is a problem of governance: decision rights, accountable owners, risk-based release gates, human oversight, and a practical 90-day plan.'
HAMMER = 'hammer-ai'
HAMMER_TITLE = 'Hammer AI: Downloads, Local Chat, Privacy & Setup Guide'
HAMMER_DESCRIPTION = 'Explore Hammer AI downloads, local versus cloud chat, privacy checks, model requirements, troubleshooting, and alternatives in this source-based desktop guide.'
NETWORKING = 'tips-for-networking-events'
NETWORKING_TITLE = 'Tips for Networking Events: A Practical Before-and-After Plan'
NETWORKING_DESCRIPTION = 'Practical tips for networking events: introductions, conversation starters, joining groups, polite exits, and follow-up templates for beginners and professionals.'
NETWORKING_POST = (NETWORKING, 'Business', NETWORKING_TITLE, NETWORKING_DESCRIPTION, 'networking', '12', '', [])
FLOSSER = 'cvs-health-cordless-water-flosser'
FLOSSER_TITLE = 'CVS Health Cordless Water Flosser'
FLOSSER_DESCRIPTION = 'A CVS Health cordless water flosser buying and care guide: model checks, general use, cleaning, troubleshooting, replacement tips, and common questions.'
FLOSSER_POST = (FLOSSER, 'Wellness', FLOSSER_TITLE, FLOSSER_DESCRIPTION, 'water-flosser', '8', '', [])
HAMMER_POST = (HAMMER, 'AI & Technology', HAMMER_TITLE, HAMMER_DESCRIPTION, 'hammer', '12', '', [])
CLUSTER = [
    (GOVERNANCE, 'AI & Technology', GOVERNANCE_TITLE, GOVERNANCE_DESCRIPTION, 'governance', '11', '', []),
    ('ai-governance-operating-model', 'AI & Technology', 'AI Governance Operating Model: Roles, Decisions, and Release Gates', 'Build a practical AI governance operating model with named owners, a use-case register, permissions, release evidence, and change review.', 'operating-model', '6', '', []),
    ('ai-use-case-risk-assessment', 'AI & Technology', 'AI Use-Case Risk Assessment: A Practical Intake and Review Guide', 'Assess an AI use case through people, data, authority, evidence, residual risk, and operational controls, with a worked support-assistant example.', 'risk-assessment', '6', '', []),
]
RICH_ARTICLES = {NETWORKING, FLOSSER, HAMMER, GOVERNANCE, 'ai-governance-operating-model', 'ai-use-case-risk-assessment', KEYWORD, 'normalization-transformation-rules'}
SEO_TITLES = {
    NETWORKING: 'Tips for Networking Events: Conversations & Follow-Up',
    FLOSSER: 'CVS Health Cordless Water Flosser: Use & Care Guide',
    HAMMER: 'Hammer AI Guide: Downloads, Local Chat & Privacy',
    GOVERNANCE: 'AI Transformation Is a Problem of Governance',
    'ai-governance-operating-model': 'AI Governance Operating Model: Practical Guide',
    'ai-use-case-risk-assessment': 'AI Use-Case Risk Assessment: Practical Guide',
    KEYWORD: 'BrandRank.ai Normalization Transformation Rules',
    'ai-workflow': 'A Practical AI Workflow: Keep Human Judgment',
}
SEO_DESCRIPTIONS = {
    'ai-workflow':'Build a thoughtful AI workflow: choose a useful task, verify generated answers, protect sensitive information, and compare results with your current process.',
    'intentional-spaces':'Create a calmer everyday space with small changes: clear one area, arrange essentials around your routine, and adjust the layout as your habits change.',
    'slow-travel':'Plan a slower trip with fewer destinations, local context and time to explore. Review transport, entry requirements and practical travel essentials.',
    'money-basics':'Start a practical personal budget by reviewing actual income and spending, planning for irregular bills, and choosing a sustainable next step.',
    'better-breaks':'Make breaks part of your day: notice your attention, change activity when comfortable, and keep realistic expectations about rest and screen time.',
    'normalization-transformation-rules':'Learn normalization transformation rules with Unicode examples, numeric scaling, validation contracts, versioned pipelines, and an interactive calculator.',
}
IMAGE_METADATA = {}
TOPICS = [('AI & Technology', 'spark', 'violet'), ('Lifestyle', 'sun', 'rose'),
          ('Business', 'chart', 'amber'), ('Travel', 'compass', 'blue'), ('Wellness', 'leaf', 'mint')]
PATHS = {
    'arrow': '<path d="M5 19 19 5M5 5h14v14"/>',
    'right': '<path d="M4 12h16m-6-6 6 6-6 6"/>',
    'search': '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 4.5 4.5"/>',
    'bookmark': '<path d="M6 4h12v17l-6-4-6 4z"/>',
    'moon': '<path d="M20 14A8 8 0 0 1 10 4 8.5 8.5 0 1 0 20 14Z"/>',
    'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5"/>',
    'spark': '<path d="m12 3 2.5 6.5L21 12l-6.5 2.5L12 21l-2.5-6.5L3 12l6.5-2.5Z"/>',
    'chart': '<path d="M4 20V9m7 11V4m7 16v-8M2 20h20"/>',
    'compass': '<circle cx="12" cy="12" r="9"/><path d="m16 8-2 6-6 2 2-6Z"/>',
    'leaf': '<path d="M20 3C4 2 2 10 6 16s15 1 14-13ZM5 20 16 8"/>',
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    'check': '<path d="m5 12 4 4L19 6"/>',
    'menu': '<path d="M4 6h16M4 12h16M4 18h16"/>',
    'close': '<path d="m6 6 12 12M6 18 18 6"/>',
    'share': '<path d="M12 16V3M7 8l5-5 5 5M5 13v8h14v-8"/>',
}


def icon(name, extra=''):
    return f'<svg class="icon {extra}" viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round">{PATHS[name]}</svg>'


def logo():
    return '<span class="brand-mark" aria-hidden="true"><svg viewBox="0 0 32 32"><path d="M4 5h10l6 11-6 11H4l6-11Z" fill="currentColor"/><path d="m19 5 9 11-9 11 5-11Z" fill="currentColor" opacity=".5"/></svg></span><span>dailyvertex<span class="brand-period">.</span></span>'


def header(prefix=''):
    return f'''<div class="announcement"><div class="wrap"><span><span class="status-dot"></span> A fresh perspective starts here</span><a href="{prefix}articles/{HAMMER}.html">New guide: Hammer AI, local chat and privacy {icon('right')}</a></div></div>
<header class="wrap site-header"><a class="logo" href="{prefix}index.html" aria-label="DailyVertex home">{logo()}</a>
<nav id="main-nav" aria-label="Main navigation"><a href="{prefix}index.html#latest">Discover</a><a href="{prefix}index.html?category=AI%20%26%20Technology#latest">Technology</a><a href="{prefix}index.html?category=Lifestyle#latest">Lifestyle</a><a href="{prefix}ai-governance.html">AI governance</a></nav>
<div class="header-actions"><button class="icon-button" id="theme" aria-label="Use dark theme">{icon('moon')}</button><a class="saved-link icon-button" href="{prefix}index.html?saved=1#latest" aria-label="Open saved articles">{icon('bookmark')}<span class="saved-count">0</span></a><a class="btn header-btn" href="{prefix}index.html#latest">Explore the edit {icon('arrow')}</a><button class="icon-button menu-button" aria-label="Toggle navigation" aria-controls="main-nav" aria-expanded="false">{icon('menu')}</button></div></header>'''


def footer(prefix=''):
    return f'''<footer><div class="wrap footer-top"><div><a class="logo" href="{prefix}index.html">{logo()}</a><p>A little discovery.<br>A whole new perspective.</p><span class="footer-badge">INDEPENDENT MINDS. OPEN POSSIBILITIES.</span></div><div><h3>Your next discovery</h3><a href="{prefix}index.html#latest">The latest edit</a><a href="{prefix}index.html?saved=1#latest">Your reading list</a><a href="{prefix}articles/{KEYWORD}.html">Data field guide</a></div><div><h3>Around here</h3><a href="{prefix}about.html">Our story</a><a href="{prefix}privacy.html">Privacy & storage</a></div><div class="footer-statement">Good ideas.<br><span>Great rabbit holes.</span>{icon('spark')}</div></div><div class="wrap footer-bottom"><span>© 2026 DailyVertex</span><span>Built for your wonderfully curious mind.</span><a href="#">Back to top ↑</a></div></footer><div id="toast" role="status" aria-live="polite"></div></body></html>'''


def head(title, desc, prefix='', schema=None, noindex=False):
    data = f'<script type="application/ld+json">{json.dumps(schema).replace("<", chr(92)+"u003c")}</script>' if schema else ''
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="theme-color" content="#1465db">
<meta name="google-site-verification" content="UpYL4fiFN0CwTYaH04DkzRC9XkPhGdKv6uJwptCc8yY">
<meta name="google-site-verification" content="m7TtPBMnF5VicM4Tw33S0PAz9phVYjJKGIoBrt_d2n8">
<meta property="og:site_name" content="DailyVertex"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:type" content="{'article' if schema and schema.get('@type')=='Article' else 'website'}"><meta name="twitter:card" content="summary_large_image">
{'<meta name="robots" content="noindex,follow">' if noindex else ''}<link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml"><link rel="preload" href="{prefix}fonts/outfit-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{prefix}modern.css"><script src="{prefix}modern.js" defer></script>{data}</head><body><a class="skip" href="#main">Skip to content</a><div id="progress"></div>'''


def image(img, prefix='', thumbnail=False):
    metadata = IMAGE_METADATA.get(img)
    if metadata:
        return prefix+'images/'+metadata['thumbnail' if thumbnail else 'cover']
    return f'{prefix}images/{img}.webp' if img == 'ai' else f'{prefix}images/{img}.svg'


def image_alt(img):
    return IMAGE_METADATA.get(img, {}).get('alt', 'Editorial illustration')


def structured_script(data):
    return '<script type="application/ld+json">'+json.dumps(data).replace('<', '\\u003c')+'</script>'


def related_links(slug, posts):
    relationships = {
        NETWORKING:['money-basics','better-breaks','ai-workflow'],
        FLOSSER:['intentional-spaces','money-basics'],
        HAMMER:['ai-workflow','ai-use-case-risk-assessment',GOVERNANCE],
        GOVERNANCE:['ai-governance-operating-model','ai-use-case-risk-assessment','ai-workflow'],
        'ai-governance-operating-model':[GOVERNANCE,'ai-use-case-risk-assessment'],
        'ai-use-case-risk-assessment':[GOVERNANCE,'ai-governance-operating-model','normalization-transformation-rules',HAMMER],
        'ai-workflow':[HAMMER,GOVERNANCE,'ai-use-case-risk-assessment'],
        'normalization-transformation-rules':['ai-use-case-risk-assessment',KEYWORD],
        KEYWORD:[GOVERNANCE,'normalization-transformation-rules'],
        'intentional-spaces':['better-breaks','slow-travel'],
        'better-breaks':['intentional-spaces','slow-travel'],
        'slow-travel':['intentional-spaces','money-basics'],
        'money-basics':['slow-travel','intentional-spaces',FLOSSER,NETWORKING],
    }
    by_slug = {post[0]:post for post in posts}
    return ''.join(f'<a href="{E(target)}.html">{E(by_slug[target][2])} {icon("right")}</a>' for target in relationships.get(slug,[]) if target in by_slug)


def card(p, i):
    slug, cat, title, desc, img, mins, _, _ = p
    topic = next(t for t in TOPICS if t[0] == cat)
    badge = f'{icon("spark")} FIELD GUIDE' if slug == KEYWORD else f'{icon(topic[1])} {E(cat.upper())}'
    return f'''<article class="story {topic[2]}" data-category="{E(cat)}" data-slug="{slug}" data-search="{E((title+' '+desc+' '+cat).lower())}"><div class="story-image"><a href="articles/{slug}.html" tabindex="-1" aria-hidden="true"><img src="{image(img,thumbnail=True)}" width="600" height="400" alt="{E(image_alt(img))}" loading="lazy" decoding="async"></a><span class="image-label">{badge}</span><button class="bookmark" data-save="{slug}" aria-label="Save article: {E(title)}" aria-pressed="false">{icon('bookmark')}</button></div><div class="story-meta"><span>{E(cat)}</span><span>{icon('clock')} {mins} min read</span></div><h3><a href="articles/{slug}.html">{E(title)}</a></h3><p>{E(desc)}</p><div class="story-bottom"><span><span class="tiny-avatar">dv</span> DailyVertex Editorial</span><a href="articles/{slug}.html" class="round-link" aria-label="Read: {E(title)}">{icon('arrow')}</a></div></article>'''


def build(posts, out):
    global IMAGE_METADATA
    manifest = out/'images/editorial-manifest.json'
    IMAGE_METADATA = json.loads(manifest.read_text()) if manifest.exists() else {}
    posts = list(posts)
    old = next(p for p in posts if p[0] == 'normalization-transformation-rules')
    posts = [(KEYWORD, old[1], 'BrandRank.ai normalization rules: turn scattered mentions into meaningful signals.', DESCRIPTION, 'brand-data', '11', old[6], old[7])] + posts
    posts = [NETWORKING_POST, FLOSSER_POST, HAMMER_POST] + CLUSTER + posts
    for i, post in enumerate(posts):
        words = ''
        if post[0] in RICH_ARTICLES:
            words = re.sub('<[^>]+>', ' ', (ROOT/'content'/f'{post[0]}.html').read_text())
        else:
            words = ' '.join(h+' '+b for h,b in post[7])
        minutes = str(max(1,ceil(len(words.split())/210)))
        posts[i] = (*post[:5],minutes,*post[6:])
    content = head('DailyVertex — Stay Curious. Discover More.', 'Fresh ideas in technology, lifestyle, business, travel and wellness. Explore practical field guides and stories for a more curious everyday.') + header()
    content += f'''<main id="main"><section class="hero wrap"><div class="hero-heading"><div><p class="eyebrow"><span class="mini-spark">{icon('spark')}</span> A LITTLE CURIOSITY CHANGES EVERYTHING</p><h1>Life moves fast.<br><span class="gradient-text">Stay wonderfully curious.</span><span class="headline-star" aria-hidden="true">✳</span></h1></div><div class="hero-intro"><p>Your next big idea. Your new favorite thing.<br>A fresh take on the world, <em>every day.</em></p><a class="text-link" href="#latest">Find your next discovery {icon('right')}</a></div></div>
<div class="hero-grid"><a class="cover" href="articles/ai-workflow.html"><img src="images/ai.webp" width="1200" height="800" alt="AI-generated robotic hand reaching toward a glowing orb" fetchpriority="high"><div class="cover-shade"></div><div class="cover-top"><span class="glass-badge">{icon('spark')} THE NEXT CHAPTER</span><span class="cover-arrow">{icon('arrow')}</span></div><div class="floating-note"><span class="note-dot"></span> HUMAN IDEAS. NEW POSSIBILITIES.</div><div class="cover-copy"><span class="cover-category">AI & TECHNOLOGY <span>·</span> 6 MIN READ</span><h2>The future has<br>a human side.</h2><p>AI is changing the way we work.<br>Here's how to keep your perspective.</p><div class="author"><span class="avatar">dv</span><span>DailyVertex Editorial<small>Thoughtful takes. Practical ideas.</small></span><span class="read-pill">Read the story {icon('right')}</span></div></div></a>
<aside class="hero-side"><a class="data-feature" href="articles/{KEYWORD}.html"><div class="data-feature-top"><span class="badge">{icon('check')} THE PRACTICAL GUIDE</span>{icon('arrow')}</div><div class="data-art" aria-hidden="true"><span class="data-wire"></span><span class="data-node">Aa</span><span class="data-node">01</span><span class="data-node">{icon('check')}</span></div><span class="eyebrow">DATA, WITHOUT THE GUESSWORK</span><h2>Messy inputs.<br><span>Clearer outcomes.</span></h2><p>Normalization transformation rules, explained with examples you can actually use.</p><div class="data-feature-bottom"><span>12 min read</span><span>Open the field guide {icon('right')}</span></div></a><a class="mini-feature" href="articles/intentional-spaces.html"><img src="images/space.svg" width="300" height="220" alt="Sunlit arch and plant illustration"><div><span class="eyebrow">THE GOOD EVERYDAY</span><h3>Less noise.<br>More living.</h3><span class="text-link">Make a little space {icon('arrow')}</span></div></a></aside></div>
<div class="topic-strip"><span>YOUR WORLD,<br><b>WIDER.</b></span>'''
    for cat, name, color in TOPICS:
        from urllib.parse import quote
        content += f'<a class="topic-link {color}" href="index.html?category={quote(cat)}#latest"><span class="topic-icon">{icon(name)}</span><span>{E(cat)}<small>{ {"AI & Technology":"What comes next", "Lifestyle":"A better everyday", "Business":"Ideas that move", "Travel":"Beyond the familiar", "Wellness":"Room to recharge"}[cat]}</small></span>{icon("arrow")}</a>'
    content += '</div></section><section class="wrap latest" id="latest"><div class="section-heading"><div><p class="eyebrow"><span class="status-dot"></span> THE DAILY EDIT</p><h2>Find your next <span>“oh, interesting.”</span></h2></div><p>A little of everything.<br>Something just for you.</p></div><div class="discovery"><div class="filters" role="group" aria-label="Filter stories by topic">'
    for i, cat in enumerate(['All stories'] + [t[0] for t in TOPICS] + ['saved']):
        label = f'{icon("bookmark")} Saved' if cat == 'saved' else E(cat)
        content += f'<button class="filter {"active" if not i else ""}" data-filter="{E(cat)}" aria-pressed="{str(not i).lower()}">{label}</button>'
    content += f'''</div><label class="search">{icon('search')}<input id="search" type="search" placeholder="Search your curiosity…" aria-label="Search stories"></label></div><p id="results" class="sr-only" aria-live="polite"></p><div class="stories">{''.join(card(p,i) for i,p in enumerate(posts))}</div><div id="empty" hidden><span>{icon('search')}</span><h3>A new discovery is one search away.</h3><p>Try another topic or save a story for later.</p><button class="btn" id="reset">Explore all stories {icon('right')}</button></div></section>
<section class="wrap manifesto"><div class="manifesto-orb" aria-hidden="true">{icon('spark')}</div><div><p class="eyebrow">ONE PUBLICATION. A WORLD OF POSSIBILITIES.</p><h2>Follow the unexpected.<br><span>It might lead somewhere good.</span></h2><p>For the tech-curious, the slow travelers, the big thinkers.<br>And every interesting version of you in between.</p></div><a class="btn" href="about.html">This is DailyVertex {icon('arrow')}</a></section></main>'''
    content = content.replace('<span class="headline-star" aria-hidden="true">✳</span>', '<span class="headline-star" aria-hidden="true">'+icon('spark')+'</span>')
    content = content.replace('Normalization transformation rules, explained with examples you can actually use.', 'Brand identity, AI mentions, and recommendations. Make every signal mean something.')
    content = content.replace('<span>12 min read</span>', '<span>11 min read</span>')
    content = content.replace('href="articles/ai-workflow.html"', f'href="articles/{GOVERNANCE}.html"', 1)
    content = content.replace('src="images/ai.webp"', f'src="{image("governance")}"', 1)
    content = content.replace('alt="AI-generated robotic hand reaching toward a glowing orb"', f'alt="{E(image_alt("governance"))}"', 1)
    content = content.replace('The future has<br>a human side.', 'AI transformation.<br>Governance first.')
    content = content.replace("AI is changing the way we work.<br>Here's how to keep your perspective.", 'Clear decisions. Named owners.<br>A practical guide to responsible AI.')
    content = content.replace('6 MIN READ', next(post[5] for post in posts if post[0]==GOVERNANCE)+' MIN READ', 1)
    content = content.replace('src="images/space.svg"', f'src="{image("space",thumbnail=True)}"')
    content = content.replace('The field guide: better data, clearer decisions', 'New field guide: AI transformation and governance')
    content = content.replace(f'href="articles/{KEYWORD}.html">New field guide:', f'href="articles/{GOVERNANCE}.html">New field guide:', 1)
    (out/'index.html').write_text(content + footer())

    for p in posts:
        slug, cat, title, desc, img, mins, subtitle, sections = p
        desc = SEO_DESCRIPTIONS.get(slug,desc)
        keyword = slug == KEYWORD
        title = TITLE if keyword else title
        schema = {'@context':'https://schema.org','@type':'Article','headline':title,'description':desc,'author':{'@type':'Organization','name':'DailyVertex Editorial'},'publisher':{'@type':'Organization','name':'DailyVertex'},'articleSection':cat,'inLanguage':'en'}
        schema['timeRequired'] = f'PT{mins}M'
        if slug in {post[0] for post in CLUSTER}:
            schema.update({'datePublished':'2026-10-20','dateModified':'2026-10-20','about':{'@type':'Thing','name':'AI governance'}})
        if slug in RICH_ARTICLES:
            schema['dateModified'] = '2026-10-20'
            body = (ROOT/'content'/f'{slug}.html').read_text()
            toc = re.findall(r'<h2 id="([^"]+)">([^<]+)</h2>',body)
        else:
            body = f'<p class="article-intro">{E(subtitle)}.</p>'
            for i,(h,b) in enumerate(sections):
                body += f'<section><h2 id="section-{i}">{E(h)}</h2><p>{E(b)}</p></section>'
            toc = [(f'section-{i}',h) for i,(h,_) in enumerate(sections)]
        if slug == HAMMER:
            schema.update({'datePublished':'2026-10-21','dateModified':'2026-10-21','about':{'@type':'SoftwareApplication','name':'Hammer AI','url':'https://www.hammerai.com/desktop'},'citation':['https://github.com/hammer-ai/hammerai/releases/tag/v1.0.78','https://github.com/janhq/awesome-local-ai','https://github.com/ollama/ollama/blob/main/docs/faq.mdx']})
        if slug == NETWORKING:
            schema.update({'datePublished':'2026-10-21','dateModified':'2026-10-21','about':[{'@type':'Thing','name':name} for name in ['Professional networking','Networking events','Business communication','Career development']],'citation':['https://www.careereducation.columbia.edu/resources/'+path for path in ['making-most-networking-event','3-tips-attending-networking-events-confidence','career-fairs-how-prepare-and-engage-employers','what-not-do-avoid-these-7-common-networking-mistakes','follow-letters-extra-touch']]})
        if slug == FLOSSER:
            schema.update({'datePublished':'2026-10-21','dateModified':'2026-10-21','about':{'@type':'Thing','name':'Cordless water flossers'}})
        s = head(SEO_TITLES.get(slug,title)+' | DailyVertex',desc,'../',schema) + header('../')
        s += f'''<main id="main" class="wrap article-layout"><article><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a><span>/</span><a href="../index.html#latest">The edit</a><span>/</span>{E(cat)}</nav><span class="article-badge">{icon('spark')} {'AI GOVERNANCE FIELD GUIDE' if slug==GOVERNANCE else 'DATA FIELD GUIDE' if keyword else E(cat.upper())}</span><h1>{E(title)}</h1><p class="article-deck">{E(desc)}</p><div class="article-tools"><span class="avatar">dv</span><span>DailyVertex Editorial<small>{'Reviewed October 20, 2026 · ' if slug in RICH_ARTICLES else ''}{mins} min read</small></span><button class="bookmark inline" data-save="{slug}" aria-label="Save article" aria-pressed="false">{icon('bookmark')} Save</button><button class="share">{icon('share')} Share</button></div><figure class="article-figure"><img class="article-cover" src="{image(img,'../')}" width="1200" height="800" alt="{E(image_alt(img))}" fetchpriority="high"><figcaption>AI-generated editorial illustration.</figcaption></figure><div class="article-body">{body}</div><div class="related"><p class="eyebrow">CONTINUE EXPLORING</p>{related_links(slug,posts)}</div></article><aside class="toc"><p class="eyebrow">ON THIS PAGE</p>{''.join(f'<a href="#{ident}">{E(h)}</a>' for ident,h in toc)}<a class="text-link" href="../index.html#latest">Back to the edit {icon('arrow')}</a></aside></main>'''
        if slug in {HAMMER, FLOSSER, NETWORKING}:
            s = s.replace('Reviewed October 20, 2026', 'Reviewed October 21, 2026')
        if slug == NETWORKING:
            s = s.replace('AI-generated editorial illustration.', 'AI-generated illustration of a fictional professional networking event.')
        if slug == FLOSSER:
            s = s.replace('AI-generated editorial illustration.', 'AI-generated conceptual illustration; not a photograph of the CVS Health product.')
        if slug in {entry[0] for entry in CLUSTER}:
            s = s.replace('<a href="../index.html#latest">The edit</a><span>/</span>'+E(cat), '<a href="../ai-governance.html">AI governance</a><span>/</span><span aria-current="page">'+E(title)+'</span>')
        else:
            s = s.replace('<a href="../index.html#latest">The edit</a><span>/</span>'+E(cat), '<a href="../index.html#latest">The edit</a><span>/</span><span aria-current="page">'+E(title)+'</span>')
        (out/'articles'/f'{slug}.html').write_text(s+footer('../'))

    hub_schema = {'@context':'https://schema.org','@type':'CollectionPage','name':'AI Governance: Practical Guides for Responsible Transformation','description':'Explore connected AI governance guides covering transformation, decision rights, operating models, use-case risk assessment, release gates and monitoring.'}
    hub = head('AI Governance Guides & Practical Tools | DailyVertex',hub_schema['description'],schema=hub_schema)+header()
    hub += '<main id="main" class="wrap governance-hub"><p class="eyebrow">THE AI GOVERNANCE COLLECTION</p><h1>Better AI starts<br>with better decisions.</h1><p class="hub-intro">A practical path from the transformation argument to the people, evidence, and controls that make it operational.</p><div class="hub-sequence">'
    for i,post in enumerate(CLUSTER):
        slug,_,title,desc,img,*_ = post
        hub += f'<article><span class="hub-number">0{i+1}</span><a href="articles/{slug}.html"><img src="{image(img,thumbnail=True)}" width="600" height="400" alt="{E(image_alt(img))}" loading="lazy"><h2>{E(title)}</h2><p>{E(desc)}</p><span class="text-link">Read the guide {icon("arrow")}</span></a></article>'
    hub += f'</div><section class="hub-context"><h2>Three guides. One connected workflow.</h2><p>Start with <a href="articles/{GOVERNANCE}.html">the governance pillar</a> to define the decision problem. Use the operating-model guide to assign responsibilities and release gates. Then apply the risk-assessment guide to one real workflow. These articles provide practical starting points; publishing a cluster is not a certification or a guarantee of search authority.</p><h2>Related foundations</h2><p>Explore <a href="articles/ai-workflow.html">a thoughtful AI workflow</a>, <a href="articles/normalization-transformation-rules.html">data normalization and validation</a>, and <a href="articles/{KEYWORD}.html">auditable AI brand-monitoring records</a> where those topics support the actual use case.</p></section></main>'
    hub = hub.replace('</section></main>', f'<p>When evaluating a desktop chat tool, the <a href="articles/{HAMMER}.html">Hammer AI guide</a> separates local inference from application privacy and shows how to record a practical model evaluation.</p></section></main>')
    (out/'ai-governance.html').write_text(hub+footer())

    directory_title = 'DailyVertex Sitemap: Browse All Pages & Articles'
    directory_desc = 'Find every DailyVertex article and guide in one clear directory. Browse AI and technology, lifestyle, business, travel, wellness, and publication pages.'
    directory = head(directory_title,directory_desc,schema={'@context':'https://schema.org','@type':'CollectionPage','name':'DailyVertex Sitemap','description':directory_desc})
    directory = directory.replace('</head>','<link rel="stylesheet" href="directory.css"></head>')+header()
    directory += f'<main id="main" class="wrap directory"><p class="eyebrow">YOUR NEXT DISCOVERY, ONE CLICK AWAY</p><h1>Every good idea.<br><span class="gradient-text">One easy way in.</span></h1><p class="hub-intro">A little less searching. A little more discovering. Find your way through every corner of DailyVertex.</p><div class="directory-counts"><span>{len(posts)} articles</span><span>{len(TOPICS)} topics</span><span>All in one place</span></div><section class="directory-section"><h2>Start here</h2><div class="directory-grid">'
    for label,url,detail,symbol in [('Home','index.html','The latest stories and fresh perspectives','spark'),('AI governance','ai-governance.html','Explore the connected field-guide collection','chart'),('Our story','about.html','Get to know DailyVertex','sun'),('Privacy & storage','privacy.html','Your browser preferences and privacy','bookmark')]:
        directory += f'<a class="directory-card" href="{url}"><span class="topic-icon">{icon(symbol)}</span><span><strong>{E(label)}</strong><small>{E(detail)}</small></span>{icon("arrow")}</a>'
    directory += '</div></section>'
    for category,symbol,_ in TOPICS:
        directory += f'<section class="directory-section"><h2>{E(category)}</h2><div class="directory-grid">'
        for post in posts:
            if post[1] == category:
                directory += f'<a class="directory-card" href="articles/{post[0]}.html"><span class="topic-icon">{icon(symbol)}</span><span><strong>{E(TITLE if post[0]==KEYWORD else post[2])}</strong><small>{post[5]} min read · DailyVertex Editorial</small></span>{icon("arrow")}</a>'
        directory += '</div></section>'
    directory += '<p class="directory-footnote"><a href="/sitemap.xml">Open the XML version</a> · <a href="/sitemap.txt">Open the plain-text version</a></p></main>'
    (out/'sitemap.html').write_text(directory+footer())

    for slug,title,body in [
        ('about','For every curious version of you.','DailyVertex is an independent, English-language publication exploring technology, lifestyle, business, travel, and wellness. We publish approachable guides and thoughtful starting points for your next discovery. Our data field guide includes primary-source references and working examples; other launch stories are introductory editorial pieces. We do not present AI-generated artwork as documentary photography. Our articles are edited as static pages, with no member accounts or paid subscriptions.'),
        ('privacy','Your curiosity. Your privacy.','DailyVertex does not currently collect newsletter subscriptions or use analytics and advertising trackers. Your saved articles and theme preference stay in this browser using localStorage. They are not sent to an account or synced across devices. Clear them below or through your browser settings. The hosting provider may process technical request information to deliver and secure the website. This policy must be reviewed before adding analytics, accounts, forms, or other services.')]:
        description = {'about':'Meet DailyVertex, an English-language publication covering technology, lifestyle, business, travel and wellness. Learn about our editorial approach.', 'privacy':'How DailyVertex handles saved articles, theme preferences, browser storage and hosting requests. Learn what is stored and how to clear your preferences.'}[slug]
        s = head(('About DailyVertex' if slug=='about' else 'Privacy & Browser Storage')+' | DailyVertex',description)+header()+f'<main id="main" class="wrap info-page"><p class="eyebrow">DAILYVERTEX / {slug.upper()}</p><h1>{title}</h1><p>{body}</p>'
        if slug == 'privacy':
            s += '<button class="btn" id="clear-data">Clear saved articles & theme</button>'
        s += f'<a class="text-link" href="index.html#latest">Find your next discovery {icon("arrow")}</a></main>'
        (out/f'{slug}.html').write_text(s+footer())
    (out/'404.html').write_text(head('Page not found | DailyVertex','Let’s find your next discovery.',noindex=True)+header()+'<main id="main" class="wrap info-page"><p class="eyebrow">404 / A LITTLE DETOUR</p><h1>Good discoveries<br>are still out there.</h1><p>This page could not be found.</p><a class="btn" href="index.html">Back to DailyVertex</a></main>'+footer())
    (out/'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="18" fill="#1465db"/><path d="M14 13h13l10 19-10 19H14l10-19Zm24 0 14 19-14 19 8-19Z" fill="white"/></svg>')
    (out/'robots.txt').write_text('User-agent: *\nAllow: /\n')
    origin = os.environ.get('SITE_URL','').rstrip('/')
    if origin:
        parsed = urlsplit(origin)
        if parsed.scheme != 'https' or not parsed.netloc or parsed.path or parsed.query or parsed.fragment or parsed.username:
            raise ValueError('SITE_URL must be the real HTTPS production origin without a path or credentials')
        urls = {}
        for f in out.rglob('*.html'):
            if f.name == '404.html':
                continue
            path = f.relative_to(out).as_posix()
            url = origin+'/' + ('' if path=='index.html' else path.removesuffix('.html'))
            urls[url] = None
            page = f.read_text()
            post = next((post for post in posts if post[0]==f.stem), None)
            meta_image = origin+'/'+image(post[4] if post else 'governance')
            page = page.replace('</head>', f'<link rel="canonical" href="{E(url)}"><meta property="og:url" content="{E(url)}"><meta property="og:image" content="{E(meta_image)}"><meta property="og:image:alt" content="{E(image_alt(post[4] if post else "governance"))}"><meta name="twitter:image" content="{E(meta_image)}"></head>')
            if 'Article' in page:
                def enrich(match):
                    data = json.loads(match.group(1))
                    if data.get('@type') == 'Article':
                        data.update({'url':url,'mainEntityOfPage':{'@type':'WebPage','@id':url},'image':meta_image})
                        data['publisher'].update({'@id':origin+'/#organization','url':origin+'/'})
                    return '<script type="application/ld+json">'+json.dumps(data).replace('<','\\u003c')+'</script>'
                page = re.sub(r'<script type="application/ld\+json">(.*?)</script>',enrich,page)
            supplemental = []
            if post:
                supplemental.append({'@type':'BreadcrumbList','itemListElement':[
                    {'@type':'ListItem','position':1,'name':'Home','item':origin+'/'},
                    {'@type':'ListItem','position':2,'name':'AI governance' if post[0] in {entry[0] for entry in CLUSTER} else 'The edit','item':origin+'/ai-governance' if post[0] in {entry[0] for entry in CLUSTER} else origin+'/#latest'},
                    {'@type':'ListItem','position':3,'name':TITLE if post[0]==KEYWORD else post[2],'item':url},
                ]})
                pairs = re.findall(r'<details><summary>(.*?)</summary>(.*?)</details>',page,re.S)
                def plain(value):
                    return html.unescape(re.sub('<[^>]+>', ' ', value)).strip()
                if pairs:
                    supplemental.append({'@type':'FAQPage','@id':url+'#faq','mainEntity':[
                        {'@type':'Question','name':plain(question),'acceptedAnswer':{'@type':'Answer','text':plain(answer)}} for question,answer in pairs
                    ]})
            elif f.name == 'index.html':
                supplemental.extend([
                    {'@type':'WebSite','@id':origin+'/#website','url':origin+'/','name':'DailyVertex','inLanguage':'en'},
                    {'@type':'Organization','@id':origin+'/#organization','name':'DailyVertex','url':origin+'/'},
                ])
            elif f.name == 'ai-governance.html':
                supplemental.append({'@type':'ItemList','name':'AI governance reading path','numberOfItems':len(CLUSTER),'itemListElement':[
                    {'@type':'ListItem','position':i+1,'name':post[2],'url':origin+'/articles/'+post[0]} for i,post in enumerate(CLUSTER)
                ]})
            if supplemental:
                page = page.replace('</head>',structured_script({'@context':'https://schema.org','@graph':supplemental})+'</head>')
            for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>',page,re.S):
                data = json.loads(raw)
                if data.get('@type') == 'Article':
                    # Keep content review dates; a rebuild is not a content update.
                    urls[url] = data.get('dateModified')
            f.write_text(page)
        sitemap = ET.Element('urlset',xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
        ordered_urls = sorted(urls,key=lambda value:(value != origin+'/',value))
        for url in ordered_urls:
            entry = ET.SubElement(sitemap,'url')
            ET.SubElement(entry,'loc').text = url
            if urls[url]:
                ET.SubElement(entry,'lastmod').text = urls[url]
        ET.indent(sitemap,space='  ')
        # A CSS stylesheet gives browsers a readable view while keeping standard XML.
        xml_header = b'<?xml version="1.0" encoding="utf-8"?>\n<?xml-stylesheet type="text/css" href="/sitemap.css"?>\n'
        (out/'sitemap.xml').write_bytes(xml_header+ET.tostring(sitemap,encoding='utf-8')+b'\n')
        (out/'sitemap.txt').write_text('\n'.join(ordered_urls)+'\n',encoding='utf-8')
        (out/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+origin+'/sitemap.xml\nSitemap: '+origin+'/sitemap.txt\n')
    else:
        # A build without a domain must not retain a previous domain's sitemaps.
        for name in ['sitemap.xml','sitemap.txt']:
            if (out/name).exists():
                (out/name).unlink()
    print('Modern DailyVertex pages built. '+('Production SEO URLs generated.' if origin else 'Canonical URLs await the real production origin.'))
