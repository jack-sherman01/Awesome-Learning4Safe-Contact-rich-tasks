# ```python''''''
# filepath: c:\Users\hengz\Documents\phd\research\safe_learning_survey\Awesome-Learning4Safe-Contact-rich-tasks\make_ref_table.py
import re
from pathlib import Path

import bibtexparser

bib_path = Path("reference.bib")
out_path = Path("ref_title_url.tsv")

with bib_path.open(encoding="utf-8") as f:
    bib_db = bibtexparser.load(f)

def guess_url(entry):
    # 1) explicit url
    if "url" in entry:
        return entry["url"].strip()

    # 2) doi -> https://doi.org/...
    doi = entry.get("doi", "").strip()
    if doi:
        # 有些条目 doi 里已经带了完整 URL
        if doi.startswith("http://") or doi.startswith("https://"):
            return doi
        return "https://doi.org/" + doi

    # 3) arXiv: 从 journal 或 eprint 里抓 arXiv 号
    arxiv_fields = []
    for k in ("journal", "eprint", "note"):
        if k in entry:
            arxiv_fields.append(entry[k])

    text = " ".join(arxiv_fields)
    m = re.search(r"arXiv[: ](\d{4}\.\d{4,5})(v\d+)?", text)
    if m:
        return f"https://arxiv.org/abs/{m.group(1)}"

    # 没找到就空
    return ""

rows = [("key", "title", "url")]

for entry in bib_db.entries:
    key = entry.get("ID", "").strip()
    title = entry.get("title", "").replace("\n", " ").strip()
    url = guess_url(entry)
    rows.append((key, title, url))

with out_path.open("w", encoding="utf-8") as f:
    for key, title, url in rows:
        f.write(f"{key}\t{title}\t{url}\n")

print(f"Wrote {len(rows)-1} rows to {out_path}")
