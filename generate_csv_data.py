"""Regenerate csv_data.js from the source CSV files so index.html can load
data via a <script> tag as a fallback when opened directly from disk
(file:// URLs), where fetch() of local files is blocked by the browser.

Run this again any time collection.csv, boardgames_ranks.csv,
collectiondetails2026.csv, or More data/boardgame.csv are updated:
    python generate_csv_data.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
DST = ROOT / 'csv_data.js'
FILES = ['collection.csv', 'boardgames_ranks.csv', 'collectiondetails2026.csv', 'More data/boardgame.csv']


def main():
    with DST.open('w', encoding='utf-8') as f:
        f.write('// Auto-generated from CSV files so index.html can load data via <script> tag\n')
        f.write('// when opened directly from disk (fetch() of local files is blocked by browsers).\n')
        f.write('// Regenerate with: python generate_csv_data.py\n')
        f.write('window.CSV_DATA = window.CSV_DATA || {};\n')
        for filename in FILES:
            text = (ROOT / filename).read_text(encoding='utf-8')
            f.write('window.CSV_DATA[' + json.dumps(filename) + '] = ' + json.dumps(text) + ';\n')
    print(f'Wrote {DST}')


if __name__ == '__main__':
    main()
