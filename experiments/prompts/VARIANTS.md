# System-prompt variants (evaluated strings, i.e. what the model sees)

Three wording variants exist; all share the class definitions and label-only contract.
Source encodings differ (triple-quoted real newlines vs single-quoted `\n` escapes);
comparisons below are on evaluated strings (escapes decoded).

- **Variant A** (no trailing `Choose exactly one of` sentence): EXP002, EXP003, EXP004,
  EXP005, EXP006, EXP007, EXP008, EXP009 — byte-identical across all eight (verified by hash).
  Files `EXP002/003/004/005/006/007/008/009_system.txt` hold this text.
- **Variant B** (appends `Choose exactly one of: same_figure, same_paper, related_papers,
  unrelated_papers.`): EXP001, EXP010, EXP011 (dev eval, test submissions) and EXP013
  (Lightning training) — evaluated strings are identical across all four (B == D verified
  after escape decoding), so the submitted pipeline trains, validates and tests on the same
  system prompt. Files `EXP001/010/011/013_system.txt` hold this text.
- **Variant C** (EXP012 SmolVLM test submission): same wording as A plus blank-line
  whitespace differences only (verified by diff: 10 added blank lines, no word changes).
  File `EXP012_system.txt` holds this text.

Note: few-shot demos (EXP003/005/006/008) and the `Answer with one label:` user-message
closer are separate layers documented in each experiment report, not part of these files.
