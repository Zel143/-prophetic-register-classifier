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

Usage:
    python src/train_classifier.py
"""
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
MODEL_PATH = os.path.join(RESULTS_DIR, "classifier.joblib")
EVAL_PATH = os.path.join(RESULTS_DIR, "classifier_eval.txt")
TRANSFER_PRED_PATH = os.path.join(RESULTS_DIR, "transfer_predictions.csv")

SEED_META_COLS = ["book", "chapter", "verse", "ref", "label", "note", "text"]
TRANSFER_META_COLS = ["corpus", "chunk_id", "text"]

CLASSES = ["prophetic", "narrative", "law-wisdom"]


def load_seed_data():
    df = pd.read_csv(SEED_FEATURES_PATH)
    feature_cols = [c for c in df.columns if c not in SEED_META_COLS]
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


def fit_final_model(X, y, feature_cols, best_name):
    clf = LogisticRegression(max_iter=2000) if best_name == "logistic_regression" else LinearSVC(max_iter=5000)
    pipe = Pipeline([("scale", StandardScaler()), ("clf", clf)])
    pipe.fit(X, y)
    joblib.dump({"pipeline": pipe, "feature_cols": feature_cols, "classes": list(pipe.classes_)}, MODEL_PATH)
    print(f"saved final model ({best_name}) to {MODEL_PATH}")
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


def apply_to_transfer(pipe, feature_cols):
    df = pd.read_csv(TRANSFER_FEATURES_PATH)
    X = df[feature_cols].values
    preds = pipe.predict(X)
    df_out = df[TRANSFER_META_COLS].copy()
    df_out["predicted_label"] = preds

    if hasattr(pipe, "predict_proba"):
        probs = pipe.predict_proba(X)
        for i, cls in enumerate(pipe.classes_):
            df_out[f"prob_{cls}"] = probs[:, i]

    df_out.to_csv(TRANSFER_PRED_PATH, index=False)
    print(f"wrote {len(df_out)} transfer predictions to {TRANSFER_PRED_PATH}")

    summary = df_out.groupby("corpus")["predicted_label"].value_counts(normalize=True).unstack().round(3)
    return summary


def main():
    df, X, y, feature_cols = load_seed_data()
    print(f"seed set: {len(df)} rows, {len(feature_cols)} features, classes: {pd.Series(y).value_counts().to_dict()}")

    cv_results = evaluate_models(X, y)
    best_name = max(cv_results, key=lambda k: cv_results[k].mean())
    print(f"\nbest model by macro-F1: {best_name}")

    report, cm_df = cv_confusion_report(X, y, best_name)
    print("\nCross-validated classification report:")
    print(report)
    print("Confusion matrix:")
    print(cm_df)

    pipe = fit_final_model(X, y, feature_cols, best_name)

    importance = ""
    if best_name == "logistic_regression":
        importance = top_features(pipe, feature_cols)
        print(importance)
    else:
        importance = top_features(pipe, feature_cols)
        print(importance)

    with open(EVAL_PATH, "w", encoding="utf-8") as f:
        f.write(f"Model: {best_name}\n\n")
        for name, scores in cv_results.items():
            f.write(f"{name}: macro-F1 {scores.mean():.3f} (+/- {scores.std():.3f})\n")
        f.write("\nCross-validated classification report:\n")
        f.write(report)
        f.write("\nConfusion matrix:\n")
        f.write(cm_df.to_string())
        f.write("\n\nFeature importance (final model, fit on all seed data):\n")
        f.write(importance)
    print(f"\nwrote eval summary to {EVAL_PATH}")

    print("\n--- Transfer-corpus predictions ---")
    summary = apply_to_transfer(pipe, feature_cols)
    print(summary)
    with open(EVAL_PATH, "a", encoding="utf-8") as f:
        f.write("\n\nTransfer-corpus predicted-label proportions:\n")
        f.write(summary.to_string())


if __name__ == "__main__":
    main()
