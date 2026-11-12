import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build(edit_meta=None):
    """Run src/build.py on a temp copy of src/ and return the index.html it writes."""
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copytree(ROOT / 'src', Path(tmp) / 'src')
        if edit_meta:
            meta_path = Path(tmp) / 'src/meta.json'
            meta = json.loads(meta_path.read_text(encoding='utf8'))
            edit_meta(meta)
            meta_path.write_text(json.dumps(meta), encoding='utf8')
        subprocess.run([sys.executable, '-I', str(Path(tmp) / 'src/build.py')],
                       check=True, capture_output=True)
        return (Path(tmp) / 'index.html').read_text(encoding='utf8')


class BuildTest(unittest.TestCase):
    def test_index_matches_build(self):
        self.assertTrue(build() == (ROOT / 'index.html').read_text(encoding='utf8'),
                        'index.html was hand-edited or not rebuilt: run python src/build.py')

    def test_every_meta_slug_has_shot_and_vice_versa(self):
        slugs = {m['slug'] for m in json.loads((ROOT / 'src/meta.json').read_text(encoding='utf8'))}
        shots = {p.stem for p in (ROOT / 'shots').glob('*.jpg')}
        self.assertEqual(slugs, shots)

    def test_readme_count_matches_total(self):
        total = len(json.loads((ROOT / 'src/meta.json').read_text(encoding='utf8')))
        self.assertIn(f'links out to {total} small web apps', (ROOT / 'README.md').read_text(encoding='utf8'))


if __name__ == '__main__':
    unittest.main()
