# -*- coding: utf-8 -*-
"""
Replace citation keys only inside the subsubsection titled exactly:
  \subsubsection{{safe execution (after contact)}}

For each cited key k_old in that section:
  1) Find entry with key k_old in reference.bib.bak and read its title.
  2) Find entry in reference.bib with the same (normalized) title; get key k_new.
  3) If k_new != k_old, replace k_old with k_new in that section only.

Creates a backup main_new.tex.bak. No other sections are modified.
"""
import re
import sys
from pathlib import Path
from difflib import SequenceMatcher

def norm_title(s: str) -> str:
    """Normalize a title for robust matching (lowercase, collapse spaces/punctuation)."""
    if not s:
        return ""
    s = s.strip().lower()
    s = re.sub(r'[\s\-_]+', ' ', s)
    s = re.sub(r'[^a-z0-9\s:]+', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s

ENTRY_HEAD_RE = re.compile(r'(@[a-zA-Z]+)\s*\{\s*([^,]+)\s*,', re.M)
TITLE_BLOCK_RE = re.compile(r'title\s*=\s*({.*?}|\".*?\")', re.I | re.S)

def parse_bib_entries(text: str):
    """Parse .bib into entries: {type,key,title}."""
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

def find_section_span(tex: str):
    """
    Locate the exact subsubsection start/end:
      start at literal '\\subsubsection{{safe execution (after contact)}}'
      end at next \\subsubsection or \\section or EOF.
    """
    marker = r'\subsubsection{{safe execution (after contact)}}'
    idx = tex.find(marker)
    if idx < 0:
        return None, None
    # Section body starts right after the marker linebreak (include the marker in section slice)
    start = idx
    tail = tex[idx + len(marker):]
    m2 = re.search(r'\n\\(subsubsection|section)\{', tail)
    end = idx + len(marker) + (m2.start() if m2 else len(tail))
    return start, end

def collect_cite_keys(s: str):
    """Collect citation keys inside \cite{...} and \citep{...} (supports comma-separated keys)."""
    keys = set()
    for m in re.finditer(r'\\cite[p]?\{([^}]*)\}', s):
        inside = m.group(1)
        for k in inside.split(','):
            k = k.strip()
            if k:
                keys.add(k)
    return keys

def main():
    root = Path('.').resolve()
    tex_path = root / 'main_new.tex'
    bib_path = root / 'reference.bib'
    bib_bak_path = root / 'reference.bib.bak'

    if not tex_path.exists() or not bib_path.exists() or not bib_bak_path.exists():
        print('[ERR] main_new.tex or reference.bib(.bak) not found.')
        sys.exit(1)

    tex = tex_path.read_text(encoding='utf-8')
    s0, s1 = find_section_span(tex)
    if s0 is None:
        print('[ERR] Target subsubsection not found: \\subsubsection{{safe execution (after contact)}}')
        sys.exit(1)

    prefix, sect, suffix = tex[:s0], tex[s0:s1], tex[s1:]

    # Load bib files
    bib_new = bib_path.read_text(encoding='utf-8', errors='ignore')
    bib_old = bib_bak_path.read_text(encoding='utf-8', errors='ignore')
    entries_new = parse_bib_entries(bib_new)
    entries_old = parse_bib_entries(bib_old)

    # Build maps
    old_key2title = {e['key']: (e.get('title') or '') for e in entries_old}

    # Build normalized title -> list of new keys
    title2keys_new = {}
    for e in entries_new:
        nt = norm_title(e.get('title') or '')
        if not nt:
            continue
        title2keys_new.setdefault(nt, []).append(e['key'])

    # Collect keys in the section
    keys = sorted(collect_cite_keys(sect))

    replacements = 0
    report = []
    for k_old in keys:
        title = old_key2title.get(k_old)
        if not title:
            report.append(f'- {k_old}: not in reference.bib.bak (skip)')
            continue
        nt = norm_title(title)

        # Exact normalized title match
        cand = title2keys_new.get(nt, [])
        if cand:
            # Prefer numeric keys if present
            numeric = [k for k in cand if re.fullmatch(r'\d+', k)]
            k_new = numeric[0] if numeric else cand[0]
        else:
            # Fuzzy match over new entries
            best_k, best_s = None, 0.0
            for e in entries_new:
                s = SequenceMatcher(None, nt, norm_title(e.get('title') or '')).ratio()
                if s > best_s:
                    best_s, best_k = s, e['key']
            k_new = best_k if best_s >= 0.95 else None

        if not k_new:
            report.append(f'- {k_old}: no match by title in reference.bib (skip)')
            continue
        if k_new == k_old:
            report.append(f'- {k_old}: already up-to-date')
            continue

        # Replace inside this section only, for \cite{...} and \citep{...}
        pattern = re.compile(r'(\\cite[p]?\{[^}]*?)\b' + re.escape(k_old) + r'\b')
        # FIX: use a lambda to avoid "\1" + digits being parsed as group-12 etc.
        sect_new = pattern.sub(lambda m: m.group(1) + k_new, sect)
        if sect_new != sect:
            sect = sect_new
            replacements += 1
            report.append(f'- {k_old} → {k_new}')
        else:
            report.append(f'- {k_old}: referenced pattern not found (skip)')

    if replacements > 0:
        bak = tex_path.with_suffix('.tex.bak')
        bak.write_text(tex, encoding='utf-8')
        tex_path.write_text(prefix + sect + suffix, encoding='utf-8')
        print(f'[OK] Replaced {replacements} citation keys in the target subsubsection. Backup: {bak.name}')
    else:
        print('[INFO] No changes made.')

    print('-- Report --')
    for line in report:
        print(line)

if __name__ == '__main__':
    main()