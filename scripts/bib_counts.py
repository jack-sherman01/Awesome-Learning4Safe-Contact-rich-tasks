import os
import re
import csv
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(__file__))
BIB_PATH = os.path.join(ROOT, "reference.bib")
OUT_DIR = os.path.join(ROOT, "data")
OUT_CSV = os.path.join(OUT_DIR, "publication_counts.csv")

YEARS = list(range(2018, 2026))

SAFETY_PAT = re.compile(r"\b(safe|safety|barrier|cbf|shield|shielding|reachab|risk|constrain)\b", re.I)
RL_PAT = re.compile(r"(reinforcement learning|\bRL\b|actor-critic|policy gradient|q-?learning|model[- ]based reinforcement|distributional reinforcement|safe reinforcement)", re.I)
YEAR_IN_KEY = re.compile(r"(19|20)\d{2}")

def parse_bib_entries(text: str):
    entries = []
    i = 0
    n = len(text)
    while i < n:
        m = re.search(r"@(\w+)\s*\{\s*([^,]+)\s*,", text[i:], re.S)
        if not m:
            break
        typ, key = m.group(1), m.group(2)
        start = i + m.end()
        # find matching closing brace for this entry
        depth = 1
        j = start
        while j < n and depth > 0:
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
            j += 1
        body = text[start:j-1]
        entries.append((typ, key, body))
        i = j
    return entries

FIELD_RE = re.compile(r"(\w+)\s*=\s*(\{|\")(.+?)(\}|\")\s*,?", re.S)

def fields_from_body(body: str):
    fields = {}
    for fm in FIELD_RE.finditer(body):
        k = fm.group(1).strip().lower()
        v = re.sub(r"\s+", " ", fm.group(3).strip())
        fields[k] = v
    return fields

def infer_year(key: str, fields: dict):
    # 1) explicit year field
    y = fields.get("year") or fields.get("date")
    if y:
        m = re.search(r"(19|20)\d{2}", y)
        if m:
            return int(m.group(0))
    # 2) from key like zhang2025towards
    m = YEAR_IN_KEY.search(key)
    if m:
        return int(m.group(0))
    return None

def is_safety(title: str, key: str, fields: dict):
    corpus = " ".join([title or "", key or "", fields.get("keywords","")])
    return bool(SAFETY_PAT.search(corpus))

def is_rl(title: str, key: str, fields: dict):
    corpus = " ".join([title or "", key or "", fields.get("keywords",""), fields.get("booktitle",""), fields.get("journal","")])
    return bool(RL_PAT.search(corpus))

def main():
    if not os.path.isfile(BIB_PATH):
        raise SystemExit(f"Not found: {BIB_PATH}")

    with open(BIB_PATH, "r", encoding="utf-8") as f:
        text = f.read()

    totals = defaultdict(int)
    safety = defaultdict(int)
    rl = defaultdict(int)

    for typ, key, body in parse_bib_entries(text):
        fields = fields_from_body(body)
        title = fields.get("title", "")
        year = infer_year(key, fields)
        if year is None:
            continue
        totals[year] += 1
        if is_safety(title, key, fields):
            safety[year] += 1
        if is_rl(title, key, fields):
            rl[year] += 1

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["year", "total_bib", "safety_bib", "rl_bib"])
        for y in YEARS:
            w.writerow([y, totals.get(y, 0), safety.get(y, 0), rl.get(y, 0)])

    print(f"Wrote {OUT_CSV}")

if __name__ == "__main__":
    main()