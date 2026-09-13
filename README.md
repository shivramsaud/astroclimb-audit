# AstroCLIMB Experiments — Forensic Audit of Kaggle Output Notebooks

## Overview

This repository is a forensic reconstruction of AstroCLIMB modeling work. The `wasp/` parent folder held
source notebooks that were uploaded to Kaggle; this directory (`OUTPUT NOTEBOOKS`, the audit root) holds the
24 notebooks downloaded back from Kaggle/Lightning after execution (23 in the first audit + 1 Lightning training notebook added by the user afterwards). Filenames, notebook titles and markdown claims from
those downloads were **untrusted**: several filenames contradict their own code (e.g. `baseline-qwen (1).ipynb`
actually runs Gemma4-E4B; `loading-encoded-astroclimb-images (*).ipynb` hides 8 different models).

Every notebook was inspected (code + executed outputs). Notebooks were renamed to reflect their **actual
implementation**, assigned stable IDs (EXP001–EXP013), and split into `notebooks/valid/` (13 completed
experiments) vs `notebooks/excluded/` (11 duplicates / failed / metric-less runs, all preserved with reasons
in `experiments/excluded.yaml`). Only runs with trustworthy **local** evaluation evidence (or completed
test-submission inference) are listed as valid. No official score is claimed without user confirmation.

## Competition

https://www.kaggle.com/competitions/astroclimb

## Shared Task

https://ui.adsabs.harvard.edu/WIESP/2026/shared_task

## Dataset

https://huggingface.co/datasets/adsabs/AstroCLIMB

Two data formats appear in this directory (do not mix them):

| Format | Path on Kaggle | Columns | Images | Used by |
|---|---|---|---|---|
| NEW 23-col sampled | `/kaggle/input/datasets/jcxiv42/astroclimb/astroclimb_4class(sampled).csv` + `object_images_sampled/{uuid}.png` | 23 cols incl. `object_*_uuid`, `object_*_content`, `label` (0=same_paper,1=related_papers,2=same_figure,3=unrelated_papers), `label_name` | local PNG by UUID (3090 files) | EXP001, EXP003, EXP005, EXP006, EXP008 |
| OLD 7-col | `/kaggle/input/competitions/astroclimb/train.csv` (`obj_1/obj_2` base64-or-text) + `test.csv` (10k, `obj_1/obj_2` only) | 7 cols, base64 images inline | base64 decode | EXP002, EXP004, EXP007, EXP009, EXP010, EXP011, EXP012 |

## Task Definition

4-class classification of an (Object A, Object B) pair — each object a figure image or a caption text —
into exactly one of `same_figure` (caption directly describes the figure), `same_paper` (same DOI, different
figures), `related_papers` (one DOI cites the other), `unrelated_papers` (none of the above). Test data has
ONLY `obj_1/obj_2` (no DOI/metadata), so prompts must classify from visual/textual content alone.
Submission column order: `same_figure, same_paper, related_papers, unrelated_papers` (one-hot).

## Evaluation Metric

Macro-F1 (unweighted mean of the 4 per-class F1 scores) via sklearn `classification_report`, plus accuracy,
per-class F1, confusion matrix and per-pair-type F1. **Local** metrics (computed in-notebook) are never mixed
with **official** Kaggle/shared-task scores (all pending user confirmation).

## Repository Structure

```text
.
├── README.md
├── .gitignore
├── notebooks/
│   ├── valid/                  # 12 renamed completed experiments (EXP001-EXP012)
│   └── excluded/               # 11 preserved failures/duplicates/superseded (see excluded.yaml)
├── experiments/
│   ├── registry.yaml           # machine-readable record of all 12 valid experiments
│   ├── excluded.yaml           # every excluded notebook + reason + alternatives searched
│   ├── notebook_rename_map.yaml# original -> corrected filename + reason
│   ├── reports/                # EXP001.md ... EXP012.md (full per-experiment dossiers)
│   └── prompts/                # EXP*_system.txt (exact system prompts + few-shot notes)
├── configs/                    # EXP001.yaml ... EXP012.yaml (reproducibility snapshots)
├── scripts/                    # evaluate_predictions.py, audit_repo.py, extract_notebook_meta.py
├── results/                    # results_summary.md (metric table)
├── artifacts/                  # reserved for small committed artifacts (currently empty)
└── archive/                    # reserved for raw historical copies (currently empty)
```

## Experiment Inventory

| ID | Model | Data | Method | Prompting | Eval | Local Macro-F1 | Official | Confirm |
|----|---|---|---|---|---|---|---|---|
| EXP001 | Gemma4-E4B + v1 QLoRA adapter_best (~1.8ep) → merged_best | NEW 1800 full | finetuned eval | zero-shot, greedy 32 | val 1800 | **0.6170** (acc 0.6239) | **0.40088** | confirmed by user |
| EXP002 | Gemma4-E4B (bf16) | OLD 1800 full | zero-shot | zero-shot, greedy 32 | bal 1800 | 0.4408 (acc 0.5206) | — | pending |
| EXP003 | Gemma4-E4B thinking | NEW 1800 full* | few-shot eval | 4-shot + think | 1800 | 0.3925 (acc 0.5050) | — | pending (*dataset grouping ambiguous, see report) |
| EXP004 | Qwen3-VL-8B-Thinking | OLD 1800 full | zero-shot | zero-shot + think | bal 1800 | 0.1068 (degenerate) | — | pending |
| EXP005 | Qwen3-VL-4B-Thinking | NEW 397 subset | few-shot | 4-shot + think, 512 tok | trunc 397 | 0.2497 (subset) | — | pending |
| EXP006 | Kimi-VL-A3B-Thinking | NEW 1800 full | few-shot | 4-shot + think (all OOM) | 1800 | 0.1000 (degenerate) | — | pending |
| EXP007 | SmolVLM-500M-Instruct (fallback) | OLD 1800 full | zero-shot | zero-shot, greedy 32 | bal 1800 | 0.1723 | — | pending |
| EXP008 | GLM-4.1V-9B-Thinking-bnb-4bit | NEW 445 subset | few-shot | 4-shot + think | trunc 445 | 0.4200 (subset) | — | pending |
| EXP009 | GLM-4.6V-Flash (bf16) | OLD 610 subset | zero-shot | zero-shot | trunc 610 | 0.1020 (degenerate) | — | pending |
| EXP010 | Gemma4-E4B + v2-fresh adapter (~3.1–3.5ep, EXP013) | test 10k | submission | greedy 32 | test (no labels) | n/a (10000/10000 scored) | **0.64282** | confirmed by user |
| EXP011 | Gemma4-E4B BASE | test 10k | submission | greedy 32 | test (no labels) | n/a (10000/10000 scored) | **0.39754** | confirmed by user |
| EXP012 | SmolVLM-500M + LoRA adapter | test 10k | submission | greedy 32 | test (no labels) | n/a (10000/10000, 0 unrelated!) | **0.23675** | confirmed by user |
| EXP013 | Gemma4-E4B QLoRA finetune (Lightning A100) | OLD 8200/1800 | training (SFT) | answer-only | train-val (loss) | best eval_loss 0.3464 @step-1000 | n/a (training) | confirmed (provenance) |

## Results

Ranked full-1800 local macro-F1 (subset/truncated runs excluded from ranking):

1. **EXP001 — 0.6170** (finetuned Gemma4-E4B, NEW)
2. EXP002 — 0.4408 (zero-shot Gemma4-E4B, OLD; different rows, not strictly comparable)
3. EXP003 — 0.3925 (few-shot thinking Gemma4-E4B, NEW)
4. EXP007 — 0.1723 (SmolVLM-500M, OLD)
5. EXP004 — 0.1068 (Qwen3-8B thinking, OLD, degenerate)
6. EXP006 — 0.1000 (Kimi-A3B, NEW, all-OOM degenerate)

Truncated (not rankable): EXP008 0.4200 (445), EXP005 0.2497 (397), EXP009 0.1020 (610).
Test submissions (no local metric): EXP010, EXP011, EXP012 — all 10000/10000 scored; EXP012's
distribution (0/10000 unrelated_papers) is anomalous and flagged.

## Training Configuration Summary

| Run | Train? | Method | Rank/targets | Quant | Precision | Batch | Seq | Steps/loss |
|---|---|---|---|---|---|---|---|---|
| EXP001 (eval) | adapter external (v1, ~1.8ep) | QLoRA eval+merge | unknown | NF4 4-bit, double_quant, bf16 compute | bf16 | unknown | unknown | 900 steps, best val_loss 0.3489 | official test 0.40088 (user-confirmed) |
| EXP013 (train) | yes, Lightning A100-80GB | QLoRA SFT r64/a128 | r64, 7 targets | NF4 4-bit | bf16 | 2×8 eff 16 | 1536 | ~1600 steps (~3.1ep), best loss 0.3464 @step-1000; downstream official 0.64282 |
| EXP012 (infer) / excluded train | yes (excluded nb) | LoRA SmolVLM | r32, q/k/v/o/gate/up/down | none | fp16 | 1×16 eff 16 | 2048 | ckpt 400/800, best 0.3029 |
| excluded GLM train | yes (no eval) | QLoRA DDP 2×T4 | r16 | pre-quant bnb-4bit | bf16 | 1 | 2048 | unknown |
| all others | no | zero/few-shot | — | NF4 or bf16 fallback (see reports) | bf16/fp16 | infer 1 | — | — |

Common inference: greedy (`do_sample=False`, temperature 0), `max_new_tokens=32` (512 for Qwen-4B thinking),
`thumbnail(448,448)`, captions `[:2000]`, `device_map="auto"`, Kaggle GPU T4 x2, 6.5h guard.

## Prompting Strategies

One shared descriptive SYSTEM_PROMPT (exact text in `experiments/prompts/EXP*_system.txt`): expert persona,
4 class definitions with visual/textual alignment cues, content-only instruction, lowercase-label-only output.
Variants: **zero-shot** (EXP001/002/004/007/009/010/011/012) vs **few-shot 4 demos** (1/class, seed 42,
prefer FIG-CAP/CAP-FIG; EXP003/005/006/008); **thinking** on/off per model (native `<think>`/`<|think|>`,
single generation, no self-consistency/voting); image-before-text ordering; OOM/parse fallback →
`unrelated_papers`. Test submissions reuse the same contract with one-hot mapping.

## Evaluation Methodology

Predictions → normalized lowercase → mapped to 4 labels → sklearn `classification_report`
(`labels=label_cols`) on the scored split; OOM fallbacks counted; truncation warnings emitted when
`preds != true` (subset metrics flagged non-comparable); trailing-plot crashes (EXP004/009) occur after
metrics and don't affect them. Local ≠ official: no leaderboard score is inferred from any local number.

## Excluded / Failed Experiments

See `experiments/excluded.yaml`. Summary: 2 failed submissions (v2-fresh 4021-unscored — recovered by EXP010;
merged_best 3136-unscored ×2 copies — unrecovered, no completed merged run exists here); InternVL3_5-8B
OOM + ValueError (no metric); Gemma smoke test (10 samples, by design no metric); GLM DDP train-only ×2
(no eval); SmolVLM LoRA train-only ×2 (training OK incl. adapter_best, eval SyntaxError — adapter reused by
EXP012 for test, but test is unlabeled so no metric was recoverable); 1 superseded Qwen twin; 2 byte-exact
duplicates.

## Version Reconstruction

No VALID_RECONSTRUCTED experiments: every valid result comes from a single completed notebook. Two near-miss
candidates were deliberately NOT merged: (a) SmolVLM train-only + EXP012 test submission — different splits
(train vs unlabeled test), no shared evaluated artifact with a metric; (b) GLM train-only + EXP008 few-shot
eval — different methods (finetune vs no-finetune), no shared adapter evaluation. Both documented in
`experiments/excluded.yaml`.

## Official Test Results and Submission Confirmation

User-confirmed via leaderboard screenshot (Image 1, four `submission.zip` by Shivram Saud) + text mapping.
Scores are the leaderboard Score column (presumed macro-F1 per task metric, not independently verified).
Shared-task scores: unknown. No submission/run IDs were provided.

| Official rank | Score | User mapping | Repository experiment | Status |
|---|---|---|---|---|
| 1st (selected) | **0.64282** (6d ago) | 3.5ep e4b gemma trained on Lightning, test run on Kaggle | EXP010 (v2-fresh adapter; adapter from EXP013) | confirmed by user |
| 2nd | **0.40088** (7d ago) | same model, 1.8ep trained | EXP001 lineage (v1 ~900-step ≈1.76ep adapter → merged_best) | confirmed by user (no completed local submission run preserved; in-dir twins failed) |
| 3rd | **0.39754** (6d ago) | same model, baseline on official test | EXP011 (BASE zero-shot) | confirmed by user |
| 4th | **0.23675** (6d ago) | smolvlm500 finetuned | EXP012 (SmolVLM LoRA) | confirmed by user |

Local vs official (kept separate, never overwritten): EXP001 lineage local NEW-val 0.6170 vs official 0.40088
(-0.216 gap — sampled-val/test distribution shift). EXP010/011/012 have no local metric (test unlabeled).

Known reporting conflicts (preserved, not harmonized): (a) winning-model epochs — EXP010 notebook says
adapter_best "best at 3.1ep", Lightning session log (EXP013) shows best eval_loss at step-1000 (~1.95ep inferred)
with the run continuing to ~step-1600 (~3.1ep inferred), user states "3.5ep" — treated as one run with approximate
epoch reporting; HF adapter_best is mutable and may postdate the session. (b) The completed 0.40088 submission
session has no preserved notebook (the two in-directory merged_best attempts failed with 3136 unscored);
attribution to the v1 adapter lineage rests on converging evidence + user confirmation.

## Reproducibility

Kaggle GPU T4 x2, Internet ON, `HF_TOKEN` in Kaggle Secrets for gated models/HF pushes; `transformers>=5.15.1`
for Gemma4 (notebooks self-upgrade); data paths as in Dataset table. Per-experiment snapshots in `configs/`,
metric recomputation in `scripts/evaluate_predictions.py`, repo audit in `scripts/audit_repo.py`.
Large artifacts (model weights, datasets, `*.npy` predictions, `submission.csv` files) live on Kaggle/HF, not
in git — see `.gitignore`.
