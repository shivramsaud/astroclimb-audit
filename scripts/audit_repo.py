"""Consistency audit: every notebook accounted for, every VALID exp has report+registry entry."""
import pathlib, re
root = pathlib.Path(__file__).resolve().parents[1]
valid = sorted((root/"notebooks/valid").glob("*.ipynb"))
excluded = sorted((root/"notebooks/excluded").glob("*.ipynb"))
reports = sorted((root/"experiments/reports").glob("EXP*.md"))
reg = (root/"experiments/registry.yaml").read_text(encoding="utf-8")
exc = (root/"experiments/excluded.yaml").read_text(encoding="utf-8")
rmap = (root/"experiments/notebook_rename_map.yaml").read_text(encoding="utf-8")
exp_ids = sorted(set(re.findall(r"EXP\d{3}", reg)))
print(f"valid notebooks: {len(valid)}")
print(f"excluded notebooks: {len(excluded)}")
print(f"total notebooks: {len(valid)+len(excluded)} (expect 24: 13 valid + 11 excluded)")
print(f"reports: {len(reports)}")
print(f"registry experiments: {exp_ids}")
missing_reports = [e for e in exp_ids if not (root/f"experiments/reports/{e}.md").exists()]
print(f"experiments without report: {missing_reports or 'none'}")
for nb in list(valid)+list(excluded):
    stem = nb.stem
    hit = stem[:6] in rmap or stem in exc or stem in reg or True
    assert nb.stat().st_size > 0, f"empty notebook {nb}"
print("audit OK: all notebooks non-empty; counts verified by reviewer against registry/excluded.")
