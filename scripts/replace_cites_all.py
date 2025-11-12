# -*- coding: utf-8 -*-
"""
Replace citation keys across the entire LaTeX file by mapping old keys (from reference.bib.bak) to
current keys (from reference.bib) via title matching.

Process:
- Parse reference.bib.bak: build old_key -> title.
- Parse reference.bib: build normalized_title -> [new_keys].
- Scan main_new.tex for \cite* commands (with optional [] args) and replace keys using the mapping.
- Write a backup main_new.tex.bak before saving.

Supports commands like: \cite{...}, \citep{...}, \citet{...}, \citealt{...}, etc.
Supports optional arguments: \citep[pre][post]{a,b}

Usage:
  python tools\replace_cites_all.py --tex main_new.tex --bib reference.bib --bib-old reference.bib.bak
  python tools\replace_cites_all.py --dry   # preview only
"""
import re
import sys
import argparse
from pathlib import Path
from difflib import SequenceMatcher

ENTRY_HEAD_RE = re.compile(r'(@[a-zA-Z]+)\s*\{\s*([^,]+)\s*,', re.M)
TITLE_BLOCK_RE = re.compile(r'title\s*=\s*({.*?}|\".*?\")', re.I | re.S)

def norm_title(s: str) -> str:
    if not s:
        return ""
    s = s.strip().lower()
    s = re.sub(r'[\s\-_]+', ' ', s)
    s = re.sub(r'[^a-z0-9\s:]+', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s

def parse_bib_entries(text: str):
    """Return list of entries: {type, key, title}."""
    entries = []
    for m in ENTRY_HEAD_RE.finditer(text):
        etype = m.group(1)
        key   = m.group(2)
        start = m.end()
        next_m = ENTRY_HEAD_RE.search(text, start)
        end = next_m.start() if next_m else len(text)
        body = text[start:end]
        mt = TITLE_BLOCK_RE.search(body)
        title = None
        if mt:
            raw = mt.group(1).strip()
            if raw.startswith('{') and raw.endswith('}'):
                raw = raw[1:-1]
            if raw.startswith('"') and raw.endswith('"'):
                raw = raw[1:-1]
            title = raw
        entries.append({'type': etype, 'key': key, 'title': title})
    return entries

def build_mapping(bib_old_text: str, bib_new_text: str, fuzzy_cutoff=0.95):
    """Build mapping old_key -> new_key using title matching."""
    old_entries = parse_bib_entries(bib_old_text)
    new_entries = parse_bib_entries(bib_new_text)

    # title -> [keys] for new
    title2keys_new = {}
    for e in new_entries:
        nt = norm_title(e.get('title') or '')
        if nt:
            title2keys_new.setdefault(nt, []).append(e['key'])

    mapping = {}
    report = []

    for e in old_entries:
        k_old = e['key']
        title = e.get('title') or ''
        if not title:
            report.append(f'- {k_old}: no title in reference.bib.bak (skip)')
            continue
        nt = norm_title(title)
        # exact normalized title match
        cands = title2keys_new.get(nt, [])
        if cands:
            numeric = [k for k in cands if re.fullmatch(r'\d+', k)]
            k_new = numeric[0] if numeric else cands[0]
            mapping[k_old] = k_new
            if k_new == k_old:
                report.append(f'- {k_old}: already up-to-date')
            else:
                report.append(f'- {k_old} -> {k_new} (exact title)')
            continue
        # fuzzy fallback
        best_k, best_s = None, 0.0
        for ne in new_entries:
            s = SequenceMatcher(None, nt, norm_title(ne.get('title') or '')).ratio()
            if s > best_s:
                best_s, best_k = s, ne['key']
        if best_k and best_s >= fuzzy_cutoff:
            mapping[k_old] = best_k
            if best_k == k_old:
                report.append(f'- {k_old}: already up-to-date (fuzzy {best_s:.2f})')
            else:
                report.append(f'- {k_old} -> {best_k} (fuzzy {best_s:.2f})')
        else:
            report.append(f'- {k_old}: no match in reference.bib (skip)')
    return mapping, report

def replace_cite_keys_in_text(tex: str, key_map: dict):
    """
    Replace keys inside \cite-like commands across the entire file.
    Matches:
      \cite{a,b}  \citep{a}  \citet[pre][post]{a,b}  etc.
    Pattern: \cite\w* (optional [..] any number) then {keys}
    """
    # Compile once; optional args allowed 0 or more times.
    cite_pat = re.compile(r'(\\cite\w*(?:\s*\[[^\]]*\])*)\{([^}]*)\}', re.M)

    def repl(m):
        head = m.group(1)  # command + any optional args
        inside = m.group(2)  # keys content
        # split keys by comma (ignore whitespace)
        parts = [p.strip() for p in re.split(r'\s*,\s*', inside.strip()) if p.strip()]
        changed = False
        new_parts = []
        for k in parts:
            k_new = key_map.get(k, k)
            if k_new != k:
                changed = True
            new_parts.append(k_new)
        if not changed:
            return m.group(0)
        return f'{head}' + '{' + ', '.join(new_parts) + '}'

    new_tex, n = cite_pat.subn(repl, tex)
    return new_tex, n

def main():
    ap = argparse.ArgumentParser(description='Replace citation keys across a LaTeX file using bib.bak->bib title mapping.')
    ap.add_argument('--tex', default='main_new.tex', help='Path to the LaTeX file')
    ap.add_argument('--bib', default='reference.bib', help='Path to the current .bib')
    ap.add_argument('--bib-old', default='reference.bib.bak', help='Path to the previous .bib (for old keys)')
    ap.add_argument('--dry', action='store_true', help='Dry run (no write)')
    args = ap.parse_args()

    tex_path = Path(args.tex)
    bib_path = Path(args.bib)
    bib_old_path = Path(args.bib_old)
    if not tex_path.exists() or not bib_path.exists() or not bib_old_path.exists():
        print('[ERR] Required files not found.')
        sys.exit(1)

    tex = tex_path.read_text(encoding='utf-8')
    bib_new = bib_path.read_text(encoding='utf-8', errors='ignore')
    bib_old = bib_old_path.read_text(encoding='utf-8', errors='ignore')

    key_map, map_report = build_mapping(bib_old, bib_new)
    new_tex, num_edits = replace_cite_keys_in_text(tex, key_map)

    print('-- Mapping report --')
    for line in map_report:
        print(line)
    print(f'-- Edits in {args.tex}: {num_edits} cite blocks processed')

    if not args.dry and new_tex != tex:
        bak = tex_path.with_suffix('.tex.bak')
        bak.write_text(tex, encoding='utf-8')
        tex_path.write_text(new_tex, encoding='utf-8')
        print(f'[OK] Wrote changes. Backup: {bak.name}')
    else:
        print('[INFO] No write (dry-run or no changes)')

if __name__ == '__main__':
    main()