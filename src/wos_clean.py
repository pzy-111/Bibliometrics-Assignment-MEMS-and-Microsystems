import re
from collections import defaultdict

class WOSCleaner:
    def parse_wos_folder(self, folder):
        records = []
        import os
        for f in os.listdir(folder):
            if f.endswith(".txt"):
                path = os.path.join(folder, f)
                records.extend(self._parse_file(path))
        return records

    def _parse_file(self, path):
        records = []
        record = defaultdict(list)
        with open(path, encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.rstrip()
                if line.startswith("ER"):
                    records.append(dict(record))
                    record.clear()
                    continue
                m = re.match(r"^([A-Z]{2})\s+(.*)", line)
                if m:
                    field, value = m.groups()
                    record[field].append(value)
                else:
                    if record:
                        record[list(record.keys())[-1]][-1] += " " + line.strip()
        return records

    def clean_record(self, rec):
        title = " ".join(rec.get("TI", [])).strip().title()
        ab = " ".join(rec.get("AB", [])).strip()
        year = rec.get("PY", [""])[0]
        if not year.isdigit():
            year = None
        doi = " ".join(rec.get("DI", [])).lower().replace("https://doi.org/", "")
        bp = rec.get("BP", [""])[0]
        ep = rec.get("EP", [""])[0]
        pages = f"{bp}-{ep}" if bp and ep else bp

        authors = []
        for a in rec.get("AU", []):
            a = re.sub(r"[^\w\s]", "", a).strip().lower()
            parts = a.split()
            if len(parts) >= 2:
                a = f"{parts[-1]}, {' '.join(parts[:-1])}"
            authors.append(a)

        keywords = []
        for k in rec.get("DE", []) + rec.get("ID", []):
            k = k.lower().strip()
            if len(k) > 2:
                keywords.append(k)

        journal = " ".join(rec.get("SO", [])).strip().title()

        return {
            "title": title,
            "abstract": ab,
            "year": year,
            "doi": doi,
            "pages": pages,
            "authors": authors,
            "keywords": list(set(keywords)),
            "journal": journal
        }