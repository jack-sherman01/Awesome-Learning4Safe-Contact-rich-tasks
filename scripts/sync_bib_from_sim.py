# -*- coding: utf-8 -*-
import csv
import re
import sys
import json
import time
import argparse
import textwrap
from pathlib import Path
from difflib import SequenceMatcher
from urllib.parse import quote
import xml.etree.ElementTree as ET

import urllib.request

def http_get(url, headers=None, timeout=15):
    """Simple HTTP GET helper."""
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def norm_title(s: str) -> str:
    """Normalize a title for robust matching (lowercase, collapse spaces/punctuation)."""
    if not s:
        return ""
    s = s.strip().lower()
    s = re.sub(r'[\s\-_]+', ' ', s)
    s = re.sub(r'[^a-z0-9\s:]+', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s

def load_sim_batch(sim_csv: Path, start_no: int, count: int):
    """Read sim.csv and return a list of (no, title) for the requested range."""
    want = set(range(start_no, start_no + count))
    out = []
    with sim_csv.open('r', encoding='utf-8-sig', newline='') as f:
        rdr = csv.DictReader(f)
        headers = [h.strip().lower() for h in (rdr.fieldnames or [])]
        idx_no = headers.index('no.') if 'no.' in headers else headers.index('no')
        idx_title = headers.index('title')
        f.seek(0); rr = csv.reader(f)
        _ = next(rr)  # skip header
        for row in rr:
            if not row:
                continue
            try:
                no = int(str(row[idx_no]).strip())
            except:
                continue
            if no in want:
                title = (row[idx_title] or '').strip()
                if title:
                    out.append((no, title))
    return out

# Entry header pattern: @type{key,
ENTRY_HEAD_RE = re.compile(r'(@[a-zA-Z]+)\s*\{\s*([^,]+)\s*,', re.M)
# Capture title across lines: title = {...} or "..."
TITLE_BLOCK_RE = re.compile(r'title\s*=\s*({.*?}|\".*?\")', re.I | re.S)

def parse_bib_entries(text: str):
    """Parse .bib into a list of entries with fields: type, key, body, start, end, title."""
    entries = []
    for m in ENTRY_HEAD_RE.finditer(text):
        etype = m.group(1)
        key   = m.group(2)
        start = m.start()
        next_m = ENTRY_HEAD_RE.search(text, m.end())
        end = next_m.start() if next_m else len(text)
        body = text[m.end():end]
        mt = TITLE_BLOCK_RE.search(body)
        title = None
        if mt:
            raw = mt.group(1).strip()
            if raw.startswith('{') and raw.endswith('}'):
                raw = raw[1:-1]
            if raw.startswith('"') and raw.endswith('"'):
                raw = raw[1:-1]
            title = raw
        entries.append({'type': etype, 'key': key, 'body': body, 'start': start, 'end': end, 'title': title})
    return entries

def bib_has_title(entries, sim_title, cutoff=0.92):
    """Check if a similar title already exists in .bib; return (exists, entry, best_score)."""
    nt = norm_title(sim_title)
    best = 0.0
    for e in entries:
        et = e.get('title') or ""
        s = SequenceMatcher(None, nt, norm_title(et)).ratio()
        best = max(best, s)
        if s >= cutoff:
            return True, e, s
    return False, None, best

def fetch_arxiv_bibtex_by_title(title: str):
    """Try to fetch BibTeX from arXiv via Atom API using the title."""
    q = f'http://export.arxiv.org/api/query?search_query=ti:"{quote(title)}"&max_results=1'
    try:
        data = http_get(q)
    except Exception:
        return None
    try:
        root = ET.fromstring(data)
        # Find first entry
        ns = {'a': 'http://www.w3.org/2005/Atom'}
        entry = root.find('a:entry', ns)
        if entry is None:
            return None
        eid = entry.find('a:id', ns).text  # e.g., http://arxiv.org/abs/1903.08542v1
        arx_id = eid.split('/')[-1]
        # Get BibTeX from arXiv export
        bib = http_get(f'https://arxiv.org/bibtex/{arx_id}').decode('utf-8', errors='ignore')
        return bib.strip()
    except Exception:
        return None

def fetch_crossref_json_by_title(title: str):
    """Fetch Crossref JSON search results for a title."""
    url = f'https://api.crossref.org/works?query.bibliographic={quote(title)}&rows=3'
    try:
        data = http_get(url, headers={'User-Agent': 'safe-learning-bib/1.0'})
        obj = json.loads(data.decode('utf-8', errors='ignore'))
        return obj
    except Exception:
        return None

def crossref_bibtex_from_doi(doi: str):
    """Use DOI content negotiation to get publisher BibTeX."""
    url = f'https://dx.doi.org/{quote(doi)}'
    try:
        data = http_get(url, headers={'Accept': 'application/x-bibtex; charset=utf-8'})
        return data.decode('utf-8', errors='ignore').strip()
    except Exception:
        return None

def render_bibtex_from_crossref(item: dict):
    """Fallback: render a minimal BibTeX from Crossref JSON if publisher BibTeX is unavailable."""
    typ = item.get('type', 'article-journal')
    bibtype = {
        'journal-article': 'article',
        'proceedings-article': 'inproceedings',
        'posted-content': 'article',
        'report': 'techreport',
        'book-chapter': 'incollection',
        'monograph': 'book',
    }.get(typ, 'article')
    title = (item.get('title') or [''])[0]
    authors = item.get('author') or []
    author_str = ' and '.join(['{}, {}'.format(a.get("family",""), a.get("given","")).strip(', ') for a in authors if (a.get('family') or a.get('given'))])
    year = ''
    if item.get('issued') and item['issued'].get('date-parts'):
        year = str(item['issued']['date-parts'][0][0])
    container = (item.get('container-title') or [''])[0]
    vol = item.get('volume') or ''
    num = item.get('issue') or ''
    pages = item.get('page') or ''
    doi = item.get('DOI') or ''
    fields = []
    fields.append(f'  title={{${{}}}}'.replace('${}', title))
    if author_str:
        fields.append(f'  author={{{author}}}'.replace('{author}', author_str))
    if container:
        if bibtype == 'article':
            fields.append(f'  journal={{{journal}}}'.replace('{journal}', container))
        elif bibtype == 'inproceedings':
            fields.append(f'  booktitle={{{book}}}'.replace('{book}', container))
    if vol: fields.append(f'  volume={{{vol}}}'.replace('{vol}', vol))
    if num: fields.append(f'  number={{{num}}}'.replace('{num}', num))
    if pages: fields.append(f'  pages={{{pages}}}'.replace('{pages}', pages))
    if year: fields.append(f'  year={{{year}}}'.replace('{year}', year))
    if doi: fields.append(f'  doi={{{doi}}}'.replace('{doi}', doi))
    return '@{typ}{{KEY,\n{body}\n}}'.format(typ=bibtype, body=',\n'.join(fields))

def choose_best_crossref_item(items, title):
    """Choose the most similar Crossref item by title similarity."""
    nt = norm_title(title)
    best = None
    best_s = 0.0
    for it in items:
        t = (it.get('title') or [''])[0]
        s = SequenceMatcher(None, nt, norm_title(t)).ratio()
        if s > best_s:
            best_s = s
            best = it
    return best, best_s

def ensure_key(bibtex: str, key: str):
    """Ensure the BibTeX key is set to the provided key (right after @type{)."""
    return re.sub(r'^(@[a-zA-Z]+)\s*\{\s*[^,]+', r'\g<1>{' + key, bibtex, count=1, flags=re.M)

def main():
    ap = argparse.ArgumentParser(description='Sync reference.bib from sim.csv by fetching missing BibTeX (arXiv/Crossref).')
    ap.add_argument('--sim', default='sim.csv')
    ap.add_argument('--bib', default='reference.bib')
    ap.add_argument('--start', type=int, default=1)
    ap.add_argument('--count', type=int, default=100)
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--sleep', type=float, default=0.8, help='Sleep seconds between web requests')
    args = ap.parse_args()

    sim_csv = Path(args.sim)
    bib_file = Path(args.bib)
    if not sim_csv.exists() or not bib_file.exists():
        print('[ERR] sim.csv or reference.bib not found'); sys.exit(1)

    batch = load_sim_batch(sim_csv, args.start, args.count)
    text = bib_file.read_text(encoding='utf-8')
    entries = parse_bib_entries(text)

    added = 0
    report = []

    for no, title in batch:
        # If an entry already uses this numeric key, skip.
        has_key = any(e['key'] == str(no) for e in entries)
        if has_key:
            report.append(f'No.{no}: key {no} already exists (skip)')
            continue
        # If a similar title exists, just rename that entry's key.
        exists, entry, score = bib_has_title(entries, title, cutoff=0.92)
        if exists:
            old_key = entry['key']
            pattern = r'(@[a-zA-Z]+\s*\{)\s*' + re.escape(old_key) + r'\s*(,)'
            new_text = re.sub(pattern, r'\g<1>' + str(no) + r'\2', text, count=1, flags=re.M)
            if new_text != text:
                text = new_text
                entries = parse_bib_entries(text)
                report.append(f'No.{no}: matched existing title (sim={score:.2f}), renamed {old_key} -> {no}')
            else:
                report.append(f'No.{no}: matched title but rename failed (head not found)')
            continue

        # Remote fetch: try arXiv first, then Crossref.
        bibtex = None
        source = 'arXiv'
        bibtex = fetch_arxiv_bibtex_by_title(title)
        if not bibtex:
            cj = fetch_crossref_json_by_title(title)
            if cj and cj.get('message', {}).get('items'):
                item, sim = choose_best_crossref_item(cj['message']['items'], title)
                if item and sim >= 0.9:
                    doi = item.get('DOI')
                    if doi:
                        bt = crossref_bibtex_from_doi(doi)
                        if bt:
                            bibtex = bt
                            source = 'Crossref(BibTeX)'
                    if not bibtex:
                        bibtex = render_bibtex_from_crossref(item)
                        source = 'Crossref(render)'
        if not bibtex:
            report.append(f'No.{no}: not found online (manual add required) — {title}')
            continue

        # Force the BibTeX key to be the numeric No.
        bibtex = ensure_key(bibtex, str(no))
        # Ensure title is present (some publisher bibtex may omit it)
        if 'title=' not in bibtex.lower():
            bibtex = re.sub(r'\}\s*$', f',\n  title={{ {title} }}\n}}', bibtex.rstrip())

        # Append to the end of .bib
        snippet = '\n\n' + bibtex.strip() + '\n'
        if not args.dry:
            text += snippet
            entries = parse_bib_entries(text)
            added += 1
            report.append(f'No.{no}: appended ({source})')
        else:
            report.append(f'No.{no}: [dry-run] would append ({source})')

        time.sleep(args.sleep)

    if not args.dry and added > 0:
        bak = bib_file.with_suffix('.bib.bak')
        bak.write_text(bib_file.read_text(encoding='utf-8'), encoding='utf-8')
        bib_file.write_text(text, encoding='utf-8')
        print(f'[OK] appended {added} entries; backup saved to {bak.name}')
    else:
        print('[INFO] no write (dry-run or no additions)')

    print('-- Report --')
    for line in report:
        print(line)

if __name__ == '__main__':
    main()