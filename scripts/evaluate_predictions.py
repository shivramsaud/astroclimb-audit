"""Recompute macro-F1/accuracy from a preds npy + true labels (same convention as notebooks).

Usage: python evaluate_predictions.py preds.npy labels.npy [--labels same_figure,same_paper,related_papers,unrelated_papers]
Labels files are expected as integer arrays aligned to LABEL_COLS order.
"""
import argparse, numpy as np
from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix
LABEL_COLS = ["same_figure", "same_paper", "related_papers", "unrelated_papers"]
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("preds"); ap.add_argument("labels")
    a = ap.parse_args()
    preds = np.load(a.preds); true = np.load(a.labels)
    n = min(len(preds), len(true))
    if len(preds) != len(true):
        print(f"Warning: preds {len(preds)} != true {len(true)} -> truncating to {n}")
    preds, true = preds[:n], true[:n]
    print(classification_report(true, preds, labels=list(range(4)), target_names=LABEL_COLS))
    print("macro-F1:", f1_score(true, preds, average="macro"))
    print("accuracy:", accuracy_score(true, preds))
    print(confusion_matrix(true, preds, labels=list(range(4))))
if __name__ == "__main__":
    main()
