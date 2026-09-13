# Results summary (local evidence + user-confirmed official scores)

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
| EXP010 | test 10k | 10000/10000 | n/a | n/a | submission completed | official 0.64282 |
| EXP011 | test 10k | 10000/10000 | n/a | n/a | submission completed | official 0.39754 |
| EXP012 | test 10k | 10000/10000 | n/a | n/a | submission completed, anomalous (0 unrelated) | official 0.23675 |
| EXP013 | train-val (loss) | 8200/1800 | best eval_loss 0.3464 @step-1000 | n/a | training only; adapter behind official 0.64282 |

## Official test scores (user-confirmed, leaderboard Image 1; Score column, presumed macro-F1)

| Score | Experiment | User mapping |
|---|---|---|
| 0.64282 | EXP010 (v2-fresh adapter, from EXP013) | 3.5ep e4b gemma, Lightning-trained, Kaggle test run (highest, selected) |
| 0.40088 | EXP001 lineage (v1 ~1.8ep adapter, merged_best) | same model 1.8ep (second; no completed local run preserved) |
| 0.39754 | EXP011 (BASE zero-shot) | same-model baseline on official test (third) |
| 0.23675 | EXP012 (SmolVLM LoRA) | smolvlm500 finetuned (lowest) |

Traceability: README -> experiments/registry.yaml -> experiments/reports/EXP*.md -> notebooks/valid/*.ipynb outputs.
