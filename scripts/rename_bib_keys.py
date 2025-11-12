# -*- coding: utf-8 -*-
import csv
import re
import argparse
from pathlib import Path
from difflib import SequenceMatcher

def norm_title(s: str) -> str:
    """Normalize titles for robust matching (lowercase, collapse spaces/punctuation)."""
    if not s:
        return ""
    s = s.strip().lower()
    s = re.sub(r'[\s\-_]+', ' ', s)
    s = re.sub(r'[^a-z0-9\s:]+', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s

def load_sim_titles(sim_csv: Path, start_no: int, count: int):
    """Read sim.csv and return {no: title} for the given range [start_no, start_no+count)."""
    want = set(range(start_no, start_no + count))
    mapping = {}
    with sim_csv.open('r', encoding='utf-8-sig', newline='') as f:
        rdr = csv.DictReader(f)
        headers = [h.strip().lower() for h in (rdr.fieldnames or [])]
        # Support "No." or "No"
        idx_no = headers.index('no.') if 'no.' in headers else headers.index('no')
        idx_title = headers.index('title')
        # Re-iterate with csv.reader to avoid DictReader consumption side effects
        f.seek(0)
        rr = csv.reader(f)
        _ = next(rr)  # skip header
        for row in rr:
            if not row:
                continue
            try:
                no = int(str(row[idx_no]).strip())
            except Exception:
                continue
            if no in want:
                title = (row[idx_title] or '').strip()
                if title:
                    mapping[no] = title
    return mapping

# Entry header pattern: @type{key,
ENTRY_RE = re.compile(r'(@[a-zA-Z]+)\s*\{\s*([^,]+)\s*,', re.M)
# Capture title across lines: title = {...} or "..."
TITLE_BLOCK_RE = re.compile(r'title\s*=\s*({.*?}|\".*?\")', re.I | re.S)

def parse_bib_entries(text: str):
    """Parse .bib text into a list of entries with fields: type, key, body, start, end, title."""
    entries = []
    for m in ENTRY_RE.finditer(text):
        etype = m.group(1)
        key   = m.group(2)
        start = m.start()
        next_m = ENTRY_RE.search(text, m.end())
        end = next_m.start() if next_m else len(text)
        body = text[m.end():end]
        title = None
        mt = TITLE_BLOCK_RE.search(body)
        if mt:
            raw = mt.group(1).strip()
            if raw.startswith('{') and raw.endswith('}'):
                raw = raw[1:-1]
            if raw.startswith('"') and raw.endswith('"'):
                raw = raw[1:-1]
            title = raw
        entries.append({'type': etype, 'key': key, 'body': body, 'start': start, 'end': end, 'title': title})
    return entries

def build_title_index(entries):
    """Build an index from normalized title to entry indices."""
    idx = {}
    for i, e in enumerate(entries):
        nt = norm_title(e.get('title') or "")
        if nt:
            idx.setdefault(nt, []).append(i)
    return idx

def best_match_entry(sim_title: str, entries, title_idx, used_indices, cutoff_exact=0.98, cutoff_fuzzy=0.84):
    """Find the best matching entry by title: try exact normalized match, then fuzzy."""
    nt = norm_title(sim_title)
    # Exact (normalized) match
    if nt in title_idx:
        for i in title_idx[nt]:
            if i not in used_indices:
                return i, 1.0, 'exact'
    # Fuzzy match
    best_i, best_s = None, 0.0
    for i, e in enumerate(entries):
        if i in used_indices:
            continue
        et = e.get('title') or ""
        s = SequenceMatcher(None, nt, norm_title(et)).ratio()
        if s > best_s:
            best_s, best_i = s, i
    if best_i is not None and best_s >= cutoff_fuzzy:
        return best_i, best_s, 'fuzzy'
    return None, 0.0, 'none'

def rename_key(text: str, old_key: str, new_key: str):
    """
    Replace a single BibTeX key in the full .bib text.
    Turns: @article{old_key,  into  @article{new_key,
    Uses a regex on the entry head so that offsets do not break after replacements.
    """
    pattern = r'(@[a-zA-Z]+\s*\{)\s*' + re.escape(old_key) + r'\s*(,)'
    return re.sub(pattern, r'\g<1>' + new_key + r'\2', text, count=1, flags=re.M)

def main():
    ap = argparse.ArgumentParser(description='Rename BibTeX keys to sim.csv No. (batch-wise).')
    ap.add_argument('--sim', default='sim.csv', help='Path to sim.csv')
    ap.add_argument('--bib', default='reference.bib', help='Path to reference.bib')
    ap.add_argument('--start', type=int, required=True, help='Start No. (1-based) of the batch')
    ap.add_argument('--count', type=int, default=10, help='Batch size (default 10)')
    ap.add_argument('--dry', action='store_true', help='Dry run (no file write)')
    args = ap.parse_args()

    sim_csv = Path(args.sim).resolve()
    bib_file = Path(args.bib).resolve()
    if not sim_csv.exists():
        print(f'[ERR] sim.csv not found: {sim_csv}')
        return
    if not bib_file.exists():
        print(f'[ERR] reference.bib not found: {bib_file}')
        return

    sim_batch = load_sim_titles(sim_csv, args.start, args.count)
    if not sim_batch:
        print(f'[WARN] No titles found in range [{args.start}..{args.start+args.count-1}] in {sim_csv.name}')
        return

    text = bib_file.read_text(encoding='utf-8')
    entries = parse_bib_entries(text)
    title_idx = build_title_index(entries)
    used = set()

    existing_keys = set(e['key'] for e in entries)
    report = []
    changed = 0

    for no in sorted(sim_batch.keys()):
        stitle = sim_batch[no]
        i, score, how = best_match_entry(stitle, entries, title_idx, used)
        if i is None:
            report.append(f'No.{no}: not found in .bib — {stitle}')
            continue
        e = entries[i]
        old_key = e['key']
        new_key = str(no)

        # Key conflict: number already used by another entry
        if new_key in existing_keys and old_key != new_key:
            report.append(f'No.{no}: conflict (key {new_key} already exists); skip: {e["title"]}')
            used.add(i)
            continue
        if old_key == new_key:
            report.append(f'No.{no}: already numbered as {new_key} ({how}, {score:.2f})')
            used.add(i)
            continue

        new_text = rename_key(text, old_key, new_key)
        if new_text == text:
            report.append(f'No.{no}: replace failed (entry head not found for key {old_key}); skip')
            used.add(i)
            continue

        text = new_text
        existing_keys.add(new_key)
        existing_keys.discard(old_key)
        e['key'] = new_key
        used.add(i)
        changed += 1
        report.append(f'No.{no}: {how} match ({score:.2f}) → renamed to {new_key}')

    # Write file with backup
    if not args.dry and changed > 0:
        bak = bib_file.with_suffix('.bib.bak')
        bak.write_text(Path(bib_file).read_text(encoding='utf-8'), encoding='utf-8')
        bib_file.write_text(text, encoding='utf-8')
        print(f'[OK] updated {changed} entries, backup: {bak.name}')
    else:
        print('[INFO] no write (dry-run or no changes)')

    print('— Report —')
    for line in report:
        print(line)

if __name__ == '__main__':
    main()