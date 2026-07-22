"""
Trains the prophetic-register classifier on the hand-labeled seed set and
evaluates whether it transfers to the three non-biblical transfer corpora.

Two stages:
  1. Cross-validated training/evaluation on results/seed_set_features.csv
     (logistic regression vs. linear SVM, per the README's "classical ML
     classifier (logistic regression / SVM)" plan). Saves the better model
     as results/classifier.joblib and prints/saves a feature-importance
     summary.
  2. Applies the trained model to results/transfer_features.csv (built by
     src/chunk_transfer_corpora.py) and reports, per corpus, what fraction
     of chunks the model calls prophetic -- the actual transfer-test result
     this project exists to produce.

--features all (default) uses the full 129-column feature set. --features
narrow drops the 92 fw_* function-word columns and keeps only the
prophetic-specific features plus non-lexical general-stylometric features
(sentence/word length, TTR, POS proportions) -- see docs/classifier.md for
why: the full feature set's top coefficients turned out to be dominated by
fw_her/fw_she, which track "is this passage about a woman" (Ruth, Hagar)
rather than narrative register generally. --features nostruct goes one
step further than narrow: it also drops the sentence/word-length columns
(avg_sent_len, std_sent_len, avg_word_len, n_words) implicated in the
narrow model's Sibylline-Oracles-as-law-wisdom result (translated-hexameter
sentence rhythm coincidentally matching the seed set's law-wisdom passages
structurally, not genre -- see docs/classifier.md). Outputs are suffixed
by mode (_narrow, _nostruct) so all runs' results stay on disk for
comparison.

--features normttr is nostruct with raw ttr swapped for Guiraud's R
(unique words / sqrt(n)), a length-normalized diversity measure -- tests
whether the nostruct confound (verse-translated corpora reading
lexically-diverse/law-wisdom-like) is a raw-ttr sample-size artifact
fixable by normalization, rather than a deeper genre-form difference.

Usage:
    python src/train_classifier.py [--features all|narrow|nostruct|normttr]
"""
import argparse
import os

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_val_predict, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(REPO_ROOT, "results")
SEED_FEATURES_PATH = os.path.join(RESULTS_DIR, "seed_set_features.csv")
TRANSFER_FEATURES_PATH = os.path.join(RESULTS_DIR, "transfer_features.csv")

SEED_META_COLS = ["book", "chapter", "verse", "ref", "label", "note", "text"]
TRANSFER_META_COLS = ["corpus", "chunk_id", "text"]

CLASSES = ["prophetic", "narrative", "law-wisdom"]

# Prophetic-specific + non-lexical general-stylometric columns (see module
# docstring). Everything else (fw_* function-word frequencies) is dropped
# in --features narrow.
NARROW_FEATURE_PREFIXES = ("pos_",)
NARROW_FEATURE_COLS = [
    "avg_sent_len", "std_sent_len", "avg_word_len", "ttr", "n_words",
    "divine_speech_formula", "second_person_density", "vocative_density",
    "future_modal_density", "imperative_density",
]

# Narrow, minus the sentence/word-length columns -- isolates whether those
# structural features (rather than genuinely content-based ones) are what's
# driving the narrow model's transfer result. Keeps ttr (lexical diversity,
# not sentence rhythm) and drops avg_sent_len/std_sent_len/avg_word_len/n_words.
NOSTRUCT_FEATURE_COLS = [
    "ttr",
    "divine_speech_formula", "second_person_density", "vocative_density",
    "future_modal_density", "imperative_density",
]

# Same as nostruct, but swaps raw ttr for Guiraud's R (unique / sqrt(n)) --
# see docs/classifier.md: raw ttr shrinks as chunk length grows, which is
# exactly the confound behind Sibylline Oracles/Bahman Yasht's elevated
# ttr (they're verse-translated with shorter chunks than 1 Enoch's prose,
# not more lexically diverse per se). Guiraud's R divides by sqrt(n)
# instead of n, the standard length-normalization for comparing TTR across
# texts of different lengths.
NORMTTR_FEATURE_COLS = [
    "ttr_guiraud",
    "divine_speech_formula", "second_person_density", "vocative_density",
    "future_modal_density", "imperative_density",
]


def load_seed_data(mode):
    df = pd.read_csv(SEED_FEATURES_PATH)
    all_feature_cols = [c for c in df.columns if c not in SEED_META_COLS]
    if mode == "narrow":
        feature_cols = [
            c for c in all_feature_cols
            if c in NARROW_FEATURE_COLS or c.startswith(NARROW_FEATURE_PREFIXES)
        ]
    elif mode == "nostruct":
        feature_cols = [
            c for c in all_feature_cols
            if c in NOSTRUCT_FEATURE_COLS or c.startswith(NARROW_FEATURE_PREFIXES)
        ]
    elif mode == "normttr":
        feature_cols = [
            c for c in all_feature_cols
            if c in NORMTTR_FEATURE_COLS or c.startswith(NARROW_FEATURE_PREFIXES)
        ]
    else:
        feature_cols = all_feature_cols
    X = df[feature_cols].values
    y = df["label"].values
    return df, X, y, feature_cols


def evaluate_models(X, y):
    """5-fold CV comparison of logistic regression vs. linear SVM."""
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    results = {}
    for name, clf in [
        ("logistic_regression", LogisticRegression(max_iter=2000)),
        ("linear_svm", LinearSVC(max_iter=5000)),
    ]:
        pipe = Pipeline([("scale", StandardScaler()), ("clf", clf)])
        scores = cross_val_score(pipe, X, y, cv=cv, scoring="f1_macro")
        results[name] = scores
        print(f"{name}: macro-F1 {scores.mean():.3f} (+/- {scores.std():.3f}) across 5 folds")
    return results


def fit_final_model(X, y, feature_cols, best_name, model_path):
    clf = LogisticRegression(max_iter=2000) if best_name == "logistic_regression" else LinearSVC(max_iter=5000)
    pipe = Pipeline([("scale", StandardScaler()), ("clf", clf)])
    pipe.fit(X, y)
    joblib.dump({"pipeline": pipe, "feature_cols": feature_cols, "classes": list(pipe.classes_)}, model_path)
    print(f"saved final model ({best_name}) to {model_path}")
    return pipe


def cv_confusion_report(X, y, best_name):
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    clf = LogisticRegression(max_iter=2000) if best_name == "logistic_regression" else LinearSVC(max_iter=5000)
    pipe = Pipeline([("scale", StandardScaler()), ("clf", clf)])
    y_pred = cross_val_predict(pipe, X, y, cv=cv)
    report = classification_report(y, y_pred, labels=CLASSES)
    cm = confusion_matrix(y, y_pred, labels=CLASSES)
    cm_df = pd.DataFrame(cm, index=[f"true_{c}" for c in CLASSES], columns=[f"pred_{c}" for c in CLASSES])
    return report, cm_df


def top_features(pipe, feature_cols, n=8):
    clf = pipe.named_steps["clf"]
    coefs = clf.coef_  # shape (n_classes, n_features) for both LogisticRegression and LinearSVC (multi-class OvR)
    lines = []
    for i, cls in enumerate(pipe.classes_):
        idx = np.argsort(np.abs(coefs[i]))[::-1][:n]
        lines.append(f"\nTop features for '{cls}':")
        for j in idx:
            lines.append(f"  {feature_cols[j]:30s} {coefs[i][j]:+.3f}")
    return "\n".join(lines)


def apply_to_transfer(pipe, feature_cols, pred_path):
    df = pd.read_csv(TRANSFER_FEATURES_PATH)
    X = df[feature_cols].values
    preds = pipe.predict(X)
    df_out = df[TRANSFER_META_COLS].copy()
    df_out["predicted_label"] = preds

    if hasattr(pipe, "predict_proba"):
        probs = pipe.predict_proba(X)
        for i, cls in enumerate(pipe.classes_):
            df_out[f"prob_{cls}"] = probs[:, i]

    df_out.to_csv(pred_path, index=False)
    print(f"wrote {len(df_out)} transfer predictions to {pred_path}")

    summary = df_out.groupby("corpus")["predicted_label"].value_counts(normalize=True).unstack().round(3)
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--features", choices=["all", "narrow", "nostruct", "normttr"], default="all")
    args = parser.parse_args()
    suffix = "" if args.features == "all" else f"_{args.features}"
    model_path = os.path.join(RESULTS_DIR, f"classifier{suffix}.joblib")
    eval_path = os.path.join(RESULTS_DIR, f"classifier_eval{suffix}.txt")
    pred_path = os.path.join(RESULTS_DIR, f"transfer_predictions{suffix}.csv")

    df, X, y, feature_cols = load_seed_data(args.features)
    print(f"feature set: {args.features} ({len(feature_cols)} columns)")
    print(f"seed set: {len(df)} rows, classes: {pd.Series(y).value_counts().to_dict()}")

    cv_results = evaluate_models(X, y)
    best_name = max(cv_results, key=lambda k: cv_results[k].mean())
    print(f"\nbest model by macro-F1: {best_name}")

    report, cm_df = cv_confusion_report(X, y, best_name)
    print("\nCross-validated classification report:")
    print(report)
    print("Confusion matrix:")
    print(cm_df)

    pipe = fit_final_model(X, y, feature_cols, best_name, model_path)

    importance = top_features(pipe, feature_cols)
    print(importance)

    with open(eval_path, "w", encoding="utf-8") as f:
        f.write(f"Feature set: {args.features} ({len(feature_cols)} columns)\n")
        f.write(f"Model: {best_name}\n\n")
        for name, scores in cv_results.items():
            f.write(f"{name}: macro-F1 {scores.mean():.3f} (+/- {scores.std():.3f})\n")
        f.write("\nCross-validated classification report:\n")
        f.write(report)
        f.write("\nConfusion matrix:\n")
        f.write(cm_df.to_string())
        f.write("\n\nFeature importance (final model, fit on all seed data):\n")
        f.write(importance)
    print(f"\nwrote eval summary to {eval_path}")

    print("\n--- Transfer-corpus predictions ---")
    summary = apply_to_transfer(pipe, feature_cols, pred_path)
    print(summary)
    with open(eval_path, "a", encoding="utf-8") as f:
        f.write("\n\nTransfer-corpus predicted-label proportions:\n")
        f.write(summary.to_string())


if __name__ == "__main__":
    main()
