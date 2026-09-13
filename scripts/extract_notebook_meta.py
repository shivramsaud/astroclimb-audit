"""Dump cell counts, execution counts, MODEL_IDs and metric snippets for every notebook."""
import json, pathlib, re
root = pathlib.Path(__file__).resolve().parents[1]
for nb in sorted(list((root/"notebooks/valid").glob("*.ipynb"))+list((root/"notebooks/excluded").glob("*.ipynb"))):
    data = json.loads(nb.read_text(encoding="utf-8"))
    cells = data.get("cells", [])
    code = [c for c in cells if c.get("cell_type")=="code"]
    ex = sum(1 for c in code if c.get("execution_count"))
    src = "\n".join("".join(c.get("source",[])) for c in code)
    mids = sorted(set(m.group(0).strip()[:120] for m in re.finditer(r'MODEL_ID\s*=\s*[^\n]+', src)))
    print(f"{nb.relative_to(root)}: cells={len(cells)} code={len(code)} executed={ex}")
    for m in mids[:4]:
        print(f"    {m}")
