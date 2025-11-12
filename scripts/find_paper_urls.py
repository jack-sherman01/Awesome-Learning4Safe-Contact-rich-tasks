import csv
import sys
import argparse
import urllib.parse
import urllib.request
import json
import re
import xml.etree.ElementTree as ET
from typing import Optional, Tuple

ARXIV_API = "http://export.arxiv.org/api/query?search_query=ti:%22{title}%22&max_results=3"
CROSSREF_API = "https://api.crossref.org/works?query.title={title}&rows=5"


def normalize_title(t: str) -> str:
    t = t.strip().lower()
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"[^a-z0-9 \-:_\(\)\[\]\{\}\"]", "", t)
    return t


def arxiv_lookup(title: str) -> Optional[str]:
    try:
        q = ARXIV_API.format(title=urllib.parse.quote(title))
        with urllib.request.urlopen(q, timeout=15) as resp:
            data = resp.read()
        root = ET.fromstring(data)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        entries = root.findall("atom:entry", ns)
        norm_title = normalize_title(title)
        best_url = None
        best_score = -1
        for e in entries:
            t = e.findtext("atom:title", default="", namespaces=ns)
            link = e.findtext("atom:id", default="", namespaces=ns)
            score = 0
            nt = normalize_title(t)
            if nt == norm_title:
                score = 3
            elif norm_title in nt or nt in norm_title:
                score = 2
            else:
                # token overlap
                a = set(norm_title.split())
                b = set(nt.split())
                overlap = len(a & b)
                score = 1 if overlap >= max(3, len(a)//3) else 0
            if score > best_score:
                best_score = score
                best_url = link
        return best_url
    except Exception:
        return None


def crossref_lookup(title: str) -> Optional[str]:
    try:
        q = CROSSREF_API.format(title=urllib.parse.quote(title))
        with urllib.request.urlopen(q, timeout=15) as resp:
            data = resp.read()
        payload = json.loads(data.decode("utf-8", errors="ignore"))
        items = payload.get("message", {}).get("items", [])
        if not items:
            return None
        norm_title = normalize_title(title)
        best = None
        best_score = -1
        for it in items:
            its = it.get("title") or []
            t = its[0] if its else ""
            nt = normalize_title(t)
            score = 0
            if nt == norm_title:
                score = 3
            elif norm_title in nt or nt in norm_title:
                score = 2
            else:
                a = set(norm_title.split())
                b = set(nt.split())
                overlap = len(a & b)
                score = 1 if overlap >= max(3, len(a)//3) else 0
            if score > best_score:
                best_score = score
                best = it
        if not best:
            return None
        doi = best.get("DOI")
        url = best.get("URL")
        if doi:
            return f"https://doi.org/{doi}"
        return url
    except Exception:
        return None


def find_best_url(title: str) -> Tuple[str, Optional[str]]:
    # Try arXiv first, then Crossref
    aurl = arxiv_lookup(title)
    if aurl:
        return ("arxiv", aurl)
    curl = crossref_lookup(title)
    if curl:
        return ("crossref", curl)
    return ("none", None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Path to sim.csv")
    ap.add_argument("--range", required=True, help="Row number range like 162-171 (inclusive)")
    ap.add_argument("--output", required=True, help="Output CSV path (No.,Title,URL)")
    args = ap.parse_args()

    start, end = args.range.split("-")
    start = int(start)
    end = int(end)

    rows = []
    with open(args.input, newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for r in reader:
            if not r:
                continue
            try:
                no = int(r[0]) if r[0] else None
            except Exception:
                continue
            if no is None:
                continue
            if start <= no <= end:
                title = r[1]
                rows.append((no, title))

    out_rows = [("No.", "Title", "Source", "URL")]
    for no, title in rows:
        src, url = find_best_url(title)
        out_rows.append((str(no), title, src, url or ""))

    with open(args.output, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(out_rows)

    print(f"Wrote {len(out_rows)-1} links to {args.output}")


if __name__ == "__main__":
    main()
