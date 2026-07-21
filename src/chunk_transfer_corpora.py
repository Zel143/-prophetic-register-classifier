"""
Splits the three transfer-test corpora (data/transfer/*.txt) into
sentence-level chunks and extracts the same feature set used for the
biblical seed set, so the trained classifier can be applied to them.

Sentence-level chunking (not the ~1500-word chunks kjv-stylometry-repo uses
for author-attribution) because this project's labeling unit is
verse/pericope-level -- sentence length in these translations (median ~14
words) is comparable to KJV verse length, so it's the closer match.

Usage:
    python src/chunk_transfer_corpora.py
"""
import os
import re

import pandas as pd

from extract_features import general_features, prophetic_features, pos_features, WORD_RE

import spacy

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRANSFER_DIR = os.path.join(REPO_ROOT, "data", "transfer")
RESULTS_DIR = os.path.join(REPO_ROOT, "results")
OUT_PATH = os.path.join(RESULTS_DIR, "transfer_features.csv")

CORPORA = ["sibylline_oracles", "1_enoch", "bahman_yasht"]

MIN_WORDS = 5
MAX_WORDS = 60


def chunk_sentences(text):
    sents = [s.strip() for s in re.split(r"[.?!;]+", text) if s.strip()]
    chunks = []
    for s in sents:
        s = " ".join(s.split())  # collapse embedded newlines/whitespace
        n = len(WORD_RE.findall(s.lower()))
        if MIN_WORDS <= n <= MAX_WORDS:
            chunks.append(s)
    return chunks


def build():
    nlp = spacy.load("en_core_web_sm")
    rows = []
    texts = []
    for corpus in CORPORA:
        path = os.path.join(TRANSFER_DIR, f"{corpus}.txt")
        with open(path, encoding="utf-8") as f:
            text = f.read()
        chunks = chunk_sentences(text)
        print(f"[{corpus}] {len(chunks)} chunks")
        for i, chunk in enumerate(chunks):
            rows.append({"corpus": corpus, "chunk_id": i, "text": chunk})
            texts.append(chunk)

    df = pd.DataFrame(rows)
    general_rows = [general_features(t) for t in texts]
    prophetic_rows = [prophetic_features(t) for t in texts]
    pos_rows = [pos_features(doc) for doc in nlp.pipe(texts)]
    features = pd.concat(
        [pd.DataFrame(general_rows), pd.DataFrame(prophetic_rows), pd.DataFrame(pos_rows)],
        axis=1,
    )
    out = pd.concat([df, features], axis=1)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    out.to_csv(OUT_PATH, index=False)
    print(f"wrote {len(out)} rows x {len(out.columns)} columns to {OUT_PATH}")


if __name__ == "__main__":
    build()
