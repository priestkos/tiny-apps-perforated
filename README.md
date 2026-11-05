# Tiny Apps, Perforated

A stamp album that links out to 47 small web apps on grok.me. Each stamp is a screenshot of its app. Click a stamp to open its plaque and a link to the app. Every visit pings each app and stamps a postmark on the ones that answer, showing how long each took.

The design is based on the *Stamp Gallery* page (perforated stamps, foil title, 3D plaque viewer).

## Editing

- `src/build.py` holds the sets, the order and the short "kind" line for each app.
- `src/meta.json` holds each app's own page title and meta description.
- `src/template.html` is the page.
- `shots/` holds the stamp images: 480×600 JPEGs cropped from 960×1200 captures taken on 5 November 2026.

Run `python src/build.py` to rebuild `index.html`. Don't edit `index.html` by hand.
