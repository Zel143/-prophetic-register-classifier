"""
Applies the two already-trained classifiers (results/classifier.joblib,
the full 129-feature model, and results/classifier_narrow.joblib, the
24-feature model -- see src/train_classifier.py) to the sentence-level
chunks within the hand-picked transfer pericopes
(results/transfer_pericope_chunks_features.csv, built by
src/transfer_pericopes.py), and reports the predicted-label mix per
pericope. (Not whole-pericope-level features -- those are 110-767 words,
badly out of the seed set's training-length range, and n_words alone
swamped every other signal when tried directly; see the module docstring
in transfer_pericopes.py.)

This is the small-N, hand-curated complement to the large-N mechanical
sentence-chunking evaluation already in results/transfer_predictions.csv
and results/transfer_predictions_narrow.csv -- see docs/classifier.md for
why both exist and what each one is (and isn't) good evidence for.

Usage:
    python src/eval_pericopes.py
"""
import os

import joblib
import pandas as pd

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(REPO_ROOT, "results")
CHUNKS_PATH = os.path.join(RESULTS_DIR, "transfer_pericope_chunks_features.csv")
OUT_PATH = os.path.join(RESULTS_DIR, "transfer_pericopes_predictions.csv")

META_COLS = ["corpus", "pericope_id", "note", "chunk_id", "text"]


def predict_with(model_path, df):
    bundle = joblib.load(model_path)
    pipe, feature_cols = bundle["pipeline"], bundle["feature_cols"]
    X = df[feature_cols].values
    preds = pipe.predict(X)
    return preds


def main():
    df = pd.read_csv(CHUNKS_PATH)
    out = df[META_COLS].copy()

    for suffix, label in [
        ("", "full"), ("_narrow", "narrow"), ("_nostruct", "nostruct"), ("_normttr", "normttr"),
    ]:
        model_path = os.path.join(RESULTS_DIR, f"classifier{suffix}.joblib")
        out[f"pred_{label}"] = predict_with(model_path, df)

    out.to_csv(OUT_PATH, index=False)
    print(f"wrote {len(out)} chunk-level rows to {OUT_PATH}\n")

    for label in ["full", "narrow", "nostruct", "normttr"]:
        print(f"--- {label} model: predicted-label mix per pericope ---")
        summary = (
            out.groupby(["corpus", "pericope_id"])[f"pred_{label}"]
            .value_counts(normalize=True)
            .unstack()
            .fillna(0)
            .round(2)
        )
        print(summary.to_string())
        print()


if __name__ == "__main__":
    main()
