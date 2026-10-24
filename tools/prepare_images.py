"""Convert generated editorial assets to bounded WebP covers and thumbnails.

The original PNGs remain untouched in /workspace/generated_images. This is an
export/format conversion step; it does not alter the depicted content.
"""
import io
import json
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT/'site/images'
SOURCES = {
    'networking':'/workspace/generated_images/exec-a7e857ab-865b-401c-b879-925d873c1677.png',
    'water-flosser':'/workspace/generated_images/exec-935b2028-192d-4e03-bd63-cc98e4b6b561.png',
    'hammer':'/workspace/generated_images/exec-9b518707-1433-4316-9392-e703ff9226ea.png',
    'governance':'/workspace/generated_images/exec-3952fb7d-70d9-45ab-bcd0-82f2fd47fcf6.png',
    'operating-model':'/workspace/generated_images/exec-85a0c2db-cbab-4c2d-9d95-5ce727ed2057.png',
    'risk-assessment':'/workspace/generated_images/exec-b932d0fe-c087-450b-aa2d-235bd7b92062.png',
    'space':'/workspace/generated_images/exec-406f5e76-0118-488e-87d3-22271855b6f7.png',
    'travel':'/workspace/generated_images/exec-2d25b4e1-5f38-4c58-99b0-6791fa1e34fb.png',
    'business':'/workspace/generated_images/exec-6a01ea00-7752-4626-bde4-ca46267991d9.png',
    'wellness':'/workspace/generated_images/exec-34ebab3b-5e91-46c1-9f94-4977e0ab72ee.png',
    'data':'/workspace/generated_images/exec-8b4375e3-1e48-4c1c-afb3-f0655ad54361.png',
    'brand-data':'/workspace/generated_images/exec-c2ed2f60-f8ab-4a20-b74d-fd6f597feb8d.png',
}
ALT = {
    'networking':'AI-generated illustration of professionals talking in small groups at a bright networking reception',
    'water-flosser':'Conceptual white cordless water flosser with a pale-blue reservoir on a bathroom counter; not the actual CVS product',
    'hammer':'A navy laptop showing conceptual AI chat bubbles and a luminous model cube beside a teal notebook',
    'ai':'A robotic hand reaching toward a glowing orb in a calm architectural space',
    'governance':'Business colleagues reviewing an abstract network model around a boardroom table',
    'operating-model':'A hand arranging connected glass and metal structures on a blue tabletop',
    'risk-assessment':'Hands examining a transparent layered cube with illuminated checkpoints',
    'space':'A sunlit room with an arched opening, natural furniture and a blue chair',
    'travel':'An alpine lake, a winding walking path and a distant mountain village',
    'business':'A notebook, calculator, blue tray and coins arranged on a light wooden desk',
    'wellness':'A quiet garden bench beside a shaded path with a blue notebook',
    'data':'Irregular translucent pieces becoming a precisely ordered grid of glass cubes',
    'brand-data':'Luminous blue and teal identity paths converging into one glass prism',
}


def export(source, destination, width, budget):
    picture = Image.open(source).convert('RGB')
    picture.thumbnail((width, width*2), Image.Resampling.LANCZOS)
    payload = b''
    for quality in [82,78,74,70,66,62]:
        stream = io.BytesIO()
        picture.save(stream, format='WEBP', quality=quality, method=6)
        payload = stream.getvalue()
        if len(payload) <= budget:
            break
    while len(payload) > budget and picture.width > 320:
        picture = picture.resize((int(picture.width*.9),int(picture.height*.9)),Image.Resampling.LANCZOS)
        stream = io.BytesIO()
        picture.save(stream,format='WEBP',quality=68,method=6)
        payload = stream.getvalue()
    destination.write_bytes(payload)
    return {'width':picture.width,'height':picture.height,'bytes':len(payload)}


manifest_path = IMAGES/'editorial-manifest.json'
manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
selected = sys.argv[1:] or list(SOURCES)
for name in selected:
    if name == 'ai':
        continue
    source = SOURCES[name]
    cover = export(source, IMAGES/f'{name}.webp', 1200, 100_000)
    card = export(source, IMAGES/f'{name}-card.webp', 600, 35_000)
    manifest[name] = {'cover':f'{name}.webp','thumbnail':f'{name}-card.webp','alt':ALT[name],'generated':True,**cover,'thumbnail_bytes':card['bytes']}
if not sys.argv[1:] or 'ai' in selected:
    source = IMAGES/'ai.webp'
    card = export(source, IMAGES/'ai-card.webp', 600, 35_000)
    with Image.open(source) as picture:
        manifest['ai'] = {'cover':'ai.webp','thumbnail':'ai-card.webp','alt':ALT['ai'],'generated':True,'width':picture.width,'height':picture.height,'bytes':source.stat().st_size,'thumbnail_bytes':card['bytes']}
if 'hammer' in selected:
    export('/workspace/generated_images/exec-bd413f80-b3da-4e08-9a8a-9db5a0861b17.png', IMAGES/'hammer-local-cloud.webp',1200,80_000)
manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
print(f'Prepared {len(manifest)} article covers and lightweight thumbnails; originals preserved.')
