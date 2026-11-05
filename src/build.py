"""Assemble index.html from src/template.html + src/meta.json + the set list below.

Run from anywhere:  python src/build.py
meta.json holds each site's own <title> and meta description, fetched from the live page.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
meta = {m['slug']: m for m in json.loads((ROOT / 'src/meta.json').read_text(encoding='utf8'))}

# Name overrides (the page title is longer than the stamp can carry) and missing descriptions.
NAMES = {
    'bay-umbra-bamboo-qr': 'Pressmark',
    'orchid-sapphire-swift-bloom': 'Halo One',
    'opal-flame-timber-clover': 'Lantern Yard',
}
DESC = {
    'palm-finance': 'A monthly budget book: income, spending by category, an emergency-fund goal and a dated list of transactions.',
}

SETS = [
    ('playable', 'Playable', 'Six small games: a causeway to hold, cliffs to run, two mazes, a mountain range to fly and a field of stars.', [
        ('palm-vivid-cap-horizon', 'Tower defence'),
        ('prism-hazel-crisp-iris', 'Cliff platformer'),
        ('ever-topaz-bamboo-bold', 'Brick maze'),
        ('juniper-brush-jolly-flora', 'Hedge maze'),
        ('glow-honey-sail-craft', 'Low-poly flight'),
        ('royal-baker-turbo-jolly', 'Warp starfield'),
    ]),
    ('instruments', 'Instruments', 'Things that make sound, and two that listen to it.', [
        ('honey-pilot-fleet-brook', 'Desk synthesizer'),
        ('mint-dune-king-drum', 'Drum machine'),
        ('lotus-gold-drum-terra', 'Chord practice'),
        ('slate-topaz-beam-dove', 'Music visualizer'),
        ('tulip-xenon-fair-cabin', 'Music visualizer'),
    ]),
    ('physics', 'Physics & flocks', 'Planets, boxes, birds, branches and water, left to their own rules.', [
        ('bolt-swift-earth-grove', 'Orbit sandbox'),
        ('royal-star-yonder-willow', 'Solar system model'),
        ('maple-ivory-orbit-umbra', 'Physics stacking'),
        ('cosmic-gem-rapid-pixel', 'Boid murmuration'),
        ('beacon-sky-glow', 'Particle vortex'),
        ('solar-cap-berry-rapid', 'Fractal tree'),
        ('timber-civic-pilot-flora', 'Viscous wave surface'),
        ('dawn-grove-bloom-flora', 'Fluid surface'),
        ('pilot-wolf-branch-fluid', 'Tunable fluid surface'),
    ]),
    ('mathematics', 'Mathematics', 'Fractals, functions, primes and probability you can poke at.', [
        ('arch-mandelbrot', 'Fractal explorer'),
        ('moss-moss-wind-berry', 'Function plotter'),
        ('beam-cabin-harbor-vector', 'Vector field'),
        ('leaf-wood-arrow-earth', 'Fourier drawing'),
        ('bamboo-topaz-conway-life', 'Game of Life'),
        ('sunny-tulip', 'Prime sieve'),
        ('able-toss', 'Probability lab'),
    ]),
    ('atlases', 'Charts & atlases', 'Maps, networks and one revenue dashboard.', [
        ('falcon-hill-able-light', 'Choropleth atlas'),
        ('vivid-wind-crane-thunder', 'Night globe'),
        ('king-lagoon-zinc-valley', 'Force-directed atlas'),
        ('crystal-ocean-juniper-blaze', 'Hydrographic network'),
        ('scarlet-wave-glow-ever', 'Revenue dashboard'),
    ]),
    ('desk', 'Desk tools', 'Budgets, notes, timers, polls and colour: quiet helpers for the working day.', [
        ('palm-finance', 'Monthly budget'),
        ('lark-lagoon-king-blaze', 'Markdown notebook'),
        ('able-cherry-lagoon-sky', 'Kanban board'),
        ('civic-dove-blade-cactus', 'Pomodoro timer'),
        ('cabin-grove-garden-kind', 'Habit daybook'),
        ('lion-bolt-mist-quorum', 'Live poll'),
        ('bay-umbra-bamboo-qr', 'QR code generator'),
        ('reef-plum-harbor-tulip', 'Palette instrument'),
    ]),
    ('draw', 'Draw & pose', 'Two pixel desks, a kaleidoscope and two photo booths that want your camera.', [
        ('giant-swift-fleet-swift', 'Pixel desk'),
        ('bamboo-xenon-fjord-shale', 'Retro pixel desk'),
        ('honey-bamboo-kaleidoscope-plaza', 'Camera kaleidoscope'),
        ('clear-earth-wood-grove', 'Carnival photo booth'),
        ('birch-palm-pilot-breeze', 'Pocket photo booth'),
    ]),
    ('showcases', 'Showcases', 'A speaker to orbit and finish, and one night under paper lanterns.', [
        ('orchid-sapphire-swift-bloom', 'AUREL speaker'),
        ('opal-flame-timber-clover', '12 December, Kowdiar'),
    ]),
]

out = []
seen = set()
for sid, sname, blurb, items in SETS:
    rows = []
    for slug, kind in items:
        assert slug in meta, slug
        assert slug not in seen, slug
        seen.add(slug)
        m = meta[slug]
        rows.append({'s': slug, 't': NAMES.get(slug, m['title']), 'k': kind, 'd': DESC.get(slug, m['desc'])})
    out.append({'id': sid, 'n': sname, 'b': blurb, 'items': rows})
missing = set(meta) - seen
assert not missing, missing
total = sum(len(s['items']) for s in out)

tpl = (ROOT / 'src/template.html').read_text(encoding='utf8')
assert '/*DATA*/' in tpl and '{{TOTAL}}' in tpl
html = tpl.replace('/*DATA*/', 'const SETS=' + json.dumps(out, ensure_ascii=False) + ';').replace('{{TOTAL}}', str(total))
(ROOT / 'index.html').write_text(html, encoding='utf8', newline='\n')
print(f'index.html: {total} stamps in {len(out)} sets')
