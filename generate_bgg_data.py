"""Regenerate BGG.data.js from BGG.json so OurBGG.html can load data via a
<script> tag (works when opening the HTML file directly, no web server needed).

Run this again any time BGG.json is updated:
    python generate_bgg_data.py
"""
import json
import re
from pathlib import Path

SRC = Path(__file__).with_name('BGG.json')
DST = Path(__file__).with_name('BGG.data.js')


def repair_and_load(raw_text: str):
    # BGG.json is written by an appending scraper and sometimes contains multiple
    # concatenated top-level arrays (missing "," or "]" between batches).
    fixed = re.sub(r'\]\s*\[', ',', raw_text)
    fixed = re.sub(r'\}\s*\n\[\s*\n', '},\n', fixed)
    return json.loads(fixed)


def main():
    raw_text = SRC.read_text(encoding='utf-8')
    data = repair_and_load(raw_text)
    with DST.open('w', encoding='utf-8') as f:
        f.write('// Auto-generated from BGG.json. Regenerate with generate_bgg_data.py after BGG.json changes.\n')
        f.write('window.BGG_DATA = ')
        json.dump(data, f, ensure_ascii=False)
        f.write(';\n')
    print(f'Wrote {len(data)} records to {DST}')


if __name__ == '__main__':
    main()
