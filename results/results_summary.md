# Results summary (local evidence only; official scores pending user confirmation)

| ID | Split | n | Macro-F1 | Accuracy | Note |
|----|---|---|---|---|---|
| EXP001 | NEW val 1800 | 1800/1800 | 0.6170 | 0.6239 | finetuned adapter; best local |
| EXP002 | OLD bal 1800 | 1800/1800 | 0.4408 | 0.5206 | zero-shot baseline (different rows) |
| EXP003 | NEW-ish 1800 | 1800/1800 | 0.3925 | 0.5050 | few-shot thinking; dataset grouping ambiguous |
| EXP004 | OLD bal 1800 | 1800/1800 | 0.1068 | 0.2461 | degenerate (unrelated collapse) |
| EXP005 | NEW subset | 397/1800 | 0.2497 | 0.3300 | truncated by 6.5h guard |
| EXP006 | NEW 1800 | 1800/1800 | 0.1000 | 0.2500 | all-OOM degenerate |
| EXP007 | OLD bal 1800 | 1800/1800 | 0.1723 | 0.2511 | 500M fallback |
| EXP008 | NEW subset | 445/1800 | 0.4200 | 0.5236 | truncated by 6.5h guard |
| EXP009 | OLD subset | 610/1800 | 0.1020 | 0.2557 | truncated + degenerate |
| EXP010 | test 10k | 10000/10000 | n/a | n/a | submission completed |
| EXP011 | test 10k | 10000/10000 | n/a | n/a | submission completed |
| EXP012 | test 10k | 10000/10000 | n/a | n/a | submission completed, anomalous (0 unrelated) |

Traceability: README -> experiments/registry.yaml -> experiments/reports/EXP*.md -> notebooks/valid/*.ipynb outputs.
