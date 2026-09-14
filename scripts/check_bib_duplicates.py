#!/usr/bin/env python3
r"""
Systematic duplicate check for reference.bib  (Reviewer 1 Comment 1,
Reviewer 2 Comment 1: "the bibliography should be checked systematically for
duplicate titles/DOIs").

Usage
-----
    # 1. report only
    python3 check_bib_duplicates.py reference.bib

    # 2. report + rewrite the manuscript so every duplicate group uses one
    #    canonical key, and write a cleaned .bib with the redundant entries
    #    commented out
    python3 check_bib_duplicates.py reference.bib --fix npjRobotics_V3.tex

What it does
------------
* groups entries by normalised title (lower-cased, punctuation/whitespace and
  common arXiv/preprint suffixes stripped) and, separately, by DOI;
* also reports "near-duplicate" titles (>=0.93 similarity) so that
  arXiv-vs-journal versions of the same paper are caught even when the titles
  differ slightly -- this is the case for the entries the reviewer named
  (Shao et al. RTS, Sootla et al. Saute RL, Liu et al. CBF-guided MPC);
* picks a canonical key per group, preferring the entry with a DOI, then the
  one with the most fields, then the peer-reviewed (non-arXiv) one;
* with --fix, rewrites \cite/\citep/\citet keys in the given .tex file(s) and
  writes reference_dedup.bib.

No third-party packages required.
"""

import re
import sys
import os
from collections import defaultdict
from difflib import SequenceMatcher

ENTRY_RE = re.compile(r'@(\w+)\s*\{\s*([^,\s]+)\s*,', re.IGNORECASE)


def split_entries(text):
    """Return [(entry_type, key, raw_text), ...] by brace matching."""
    entries = []
    for m in ENTRY_RE.finditer(text):
        etype, key = m.group(1).lower(), m.group(2)
        if etype in ('comment', 'preamble', 'string'):
            continue
        i = text.index('{', m.start())
        depth, j = 0, i
        while j < len(text):
            if text[j] == '{':
                depth += 1
            elif text[j] == '}':
                depth -= 1
                if depth == 0:
                    break
            j += 1
        entries.append((etype, key, text[m.start():j + 1]))
    return entries


def field(raw, name):
    m = re.search(r'\b' + name + r'\s*=\s*', raw, re.IGNORECASE)
    if not m:
        return ''
    i = m.end()
    if text_at(raw, i) in '{"':
        opener = raw[i]
        closer = '}' if opener == '{' else '"'
        depth, j, out = 0, i, []
        while j < len(raw):
            c = raw[j]
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
            if (opener == '{' and depth == 0 and j > i) or \
               (opener == '"' and c == closer and j > i and depth == 0):
                break
            out.append(c)
            j += 1
        return ''.join(out[1:]).strip()
    return raw[i:].split(',')[0].strip()


def text_at(s, i):
    return s[i] if i < len(s) else ''


def norm_title(s):
    s = re.sub(r'\{|\}|\\[a-zA-Z]+', '', s)
    s = s.lower()
    s = re.sub(r'\b(arxiv preprint|preprint|extended version|supplementary)\b', '', s)
    s = re.sub(r'[^a-z0-9]+', ' ', s)
    return ' '.join(s.split())


def norm_doi(s):
    s = s.strip().lower()
    s = re.sub(r'^https?://(dx\.)?doi\.org/', '', s)
    return s


def score(e):
    """Higher = better canonical candidate."""
    _, key, raw = e
    s = 0
    if field(raw, 'doi'):
        s += 10
    j = (field(raw, 'journal') + field(raw, 'booktitle')).lower()
    if j and 'arxiv' not in j:
        s += 5
    if field(raw, 'pages'):
        s += 2
    if field(raw, 'volume'):
        s += 1
    s += raw.count('=') * 0.1
    # tie-break only: prefer a readable mnemonic key over a bare numeric one
    if not key.isdigit():
        s += 0.05
    return s


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    bibpath = sys.argv[1]
    fix_files = sys.argv[sys.argv.index('--fix') + 1:] if '--fix' in sys.argv else []

    text = open(bibpath, encoding='utf-8', errors='replace').read()
    entries = split_entries(text)
    print(f'Parsed {len(entries)} entries from {bibpath}\n')

    by_title = defaultdict(list)
    by_doi = defaultdict(list)
    for e in entries:
        t = norm_title(field(e[2], 'title'))
        if t:
            by_title[t].append(e)
        d = norm_doi(field(e[2], 'doi'))
        if d:
            by_doi[d].append(e)

    groups = []
    seen = set()

    def add_group(g, why):
        keys = tuple(sorted(x[1] for x in g))
        if len(g) > 1 and keys not in seen:
            seen.add(keys)
            groups.append((why, g))

    for t, g in by_title.items():
        add_group(g, 'identical title')
    for d, g in by_doi.items():
        add_group(g, 'identical DOI')

    # near-duplicate titles (arXiv vs journal version)
    titles = sorted(by_title.items())
    for i in range(len(titles)):
        for j in range(i + 1, len(titles)):
            a, b = titles[i][0], titles[j][0]
            if abs(len(a) - len(b)) > 25:
                continue
            if SequenceMatcher(None, a, b).ratio() >= 0.93:
                add_group(titles[i][1] + titles[j][1], 'near-identical title')

    if not groups:
        print('No duplicate or near-duplicate entries found.')
    remap = {}
    for why, g in groups:
        canon = max(g, key=score)
        print(f'--- {why} ---')
        print(f'  title : {field(canon[2], "title")[:95]}')
        print(f'  keep  : {canon[1]}')
        for e in g:
            if e[1] != canon[1]:
                print(f'  drop  : {e[1]}')
                remap[e[1]] = canon[1]
        print()

    if not fix_files:
        print(f'{len(groups)} duplicate group(s); {len(remap)} key(s) would be remapped.')
        print('Re-run with  --fix <manuscript.tex>  to apply.')
        return

    # ---- rewrite citations in the manuscript ----
    cite_re = re.compile(r'(\\cite[tp]?\*?(?:\[[^\]]*\])*\{)([^}]*)(\})')
    for f in fix_files:
        src = open(f, encoding='utf-8').read()

        def sub(m):
            keys = [k.strip() for k in m.group(2).split(',')]
            new, out = [], []
            for k in keys:
                nk = remap.get(k, k)
                if nk not in out:
                    out.append(nk)
            return m.group(1) + ', '.join(out) + m.group(3)

        new = cite_re.sub(sub, src)
        open(f, 'w', encoding='utf-8').write(new)
        print(f'rewrote citation keys in {f}')

    # ---- write cleaned bib ----
    # NOTE: '%' is NOT a comment character in BibTeX -- BibTeX scans for '@' and
    # would still parse a '%'-prefixed entry, reintroducing the duplicate. The
    # redundant entries are therefore DELETED, leaving a marker line with no '@'.
    out = text
    for k in remap:
        for e in entries:
            if e[1] == k:
                out = out.replace(
                    e[2],
                    '[removed duplicate: key "' + k + '" merged into "'
                    + remap[k] + '"]')
    dest = os.path.join(os.path.dirname(bibpath) or '.', 'reference_dedup.bib')
    open(dest, 'w', encoding='utf-8').write(out)
    print(f'wrote {dest}  ({len(remap)} duplicate entries removed)')


if __name__ == '__main__':
    main()
