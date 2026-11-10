import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUGS = {
    'spark-flame-zinc-beam', 'daisy-pilot-horizon-bay', 'lotus-comet-cap-fair',
    'quiet-quartz-amber-willow', 'earth-cherry-sage-reef', 'blend-spark-prism-stone',
    'clear-zenith-leaf-quiet', 'gold-charm-wolf-sapphire', 'eagle-zenith-sand-ruby',
    'otter-green-daisy-arrow', 'raven-fleet-hazel-eagle', 'storm-gold-trail-winter',
}


class NewStampsTest(unittest.TestCase):
    def test_built_album_includes_each_new_app_and_its_image(self):
        html = (ROOT / 'index.html').read_text(encoding='utf8')
        match = re.search(r'const SETS=(.*?);\n', html)
        self.assertIsNotNone(match)
        sets = json.loads(match.group(1))
        items = [item for group in sets for item in group['items']]
        for slug in SLUGS:
            self.assertEqual(sum(item['s'] == slug for item in items), 1, slug)
            self.assertTrue((ROOT / 'shots' / f'{slug}.jpg').is_file(), slug)
        self.assertIn(f'{len(items)} small web apps', html)


if __name__ == '__main__':
    unittest.main()
