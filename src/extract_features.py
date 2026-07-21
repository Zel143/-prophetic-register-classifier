"""
Feature extraction for the hand-labeled seed set (data/seed_set.csv).

Two feature groups, per the README's "Features (planned)" section:

  general stylometric        -- function-word frequencies, sentence/word
                                 length, type-token ratio, POS distribution
  prophetic-register-specific -- divine-speech-formula density, second-person
                                 address density, vocative density, future/
                                 imperative-mood density

Function-word list and the general-stylometric feature shape (relative
freq per 1000 words, avg/std sentence length, TTR) are borrowed from
../kjv-stylometry-repo/repo/src/features.py so results stay comparable
across the two projects' pipelines.

POS-based features (POS distribution, imperative density) use spaCy's
en_core_web_sm, which is trained on modern English -- it visibly
mis-tags archaic KJV forms (e.g. "saith" as ADP, sentence-initial "Hear"
as PROPN from capitalization). Treat those columns as an approximate
signal, not ground truth; the regex-based features (function words,
divine-speech formula, second-person density, vocative density) don't
have that dependency and are the more reliable half of the feature set.

Usage:
    python src/extract_features.py
"""
import os
import re

import numpy as np
import pandas as pd
import spacy

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED_SET_PATH = os.path.join(REPO_ROOT, "data", "seed_set.csv")
RESULTS_DIR = os.path.join(REPO_ROOT, "results")
OUT_PATH = os.path.join(RESULTS_DIR, "seed_set_features.csv")

# --- General stylometric features ---

# Borrowed from kjv-stylometry-repo/repo/src/features.py::FUNCTION_WORDS.
FUNCTION_WORDS = """the and of to that in he shall for unto his i a not be
they it is with him them but as have was which all my thou me their ye you
this will from are were by we her she or when then out up upon so if at on
what there no man now also more before because into after can may might
do did done had has been am art hath thee thy your our us who whom whose
any every none both such same other another therefore wherefore yet
neither nor either while until against among through over under between""".split()

WORD_RE = re.compile(r"[a-z]+(?:'[a-z]+)?")

# --- Prophetic-register-specific features ---

DIVINE_SPEECH_RE = re.compile(
    r"thus saith the lord|saith the lord|the word of the lord came"
    r"|thus saith the lord god|saith the lord god|the lord hath said"
    r"|the lord hath spoken",
    re.IGNORECASE,
)
SECOND_PERSON_RE = re.compile(
    r"\b(thou|thee|thy|thine|ye|you|your|yours)\b", re.IGNORECASE
)
VOCATIVE_RE = re.compile(r"\bO\s+[A-Z][a-z]+")
FUTURE_MODAL_RE = re.compile(r"\b(shall|will)\b", re.IGNORECASE)


def general_features(text):
    low = text.lower()
    words = WORD_RE.findall(low)
    n = len(words) or 1
    counts = pd.Series(words).value_counts()

    feat = {f"fw_{w}": counts.get(w, 0) / n * 1000 for w in FUNCTION_WORDS}

    sents = [s for s in re.split(r"[.?!;]+", text) if s.strip()]
    slens = [len(WORD_RE.findall(s.lower())) for s in sents]
    feat["avg_sent_len"] = np.mean(slens) if slens else 0.0
    feat["std_sent_len"] = np.std(slens) if slens else 0.0
    feat["avg_word_len"] = np.mean([len(w) for w in words]) if words else 0.0
    feat["ttr"] = len(set(words)) / n
    feat["n_words"] = n
    return feat


def prophetic_features(text):
    words = WORD_RE.findall(text.lower())
    n = len(words) or 1
    return {
        "divine_speech_formula": len(DIVINE_SPEECH_RE.findall(text)),
        "second_person_density": len(SECOND_PERSON_RE.findall(text)) / n * 1000,
        "vocative_density": len(VOCATIVE_RE.findall(text)) / n * 1000,
        "future_modal_density": len(FUTURE_MODAL_RE.findall(text)) / n * 1000,
    }


def pos_features(doc):
    """Proportion of tokens per universal POS tag, plus an imperative-mood
    proxy. spaCy's English morphologizer doesn't emit Mood=Imp at all
    (imperative and bare infinitive share a form in English, and the model
    doesn't disambiguate) -- confirmed by testing "Hear, O heavens..." and
    getting VerbForm=Inf, not Mood=Imp. Proxy instead: a sentence whose
    first non-punct token is a bare-infinitive-form VERB (no subject, no
    "to" in front) is heuristically imperative. Still approximate -- see
    module docstring -- but nonzero, unlike the Mood=Imp check it replaced."""
    tags = [t.pos_ for t in doc if not t.is_punct]
    n = len(tags) or 1
    counts = pd.Series(tags).value_counts()
    universal_tags = [
        "ADJ", "ADP", "ADV", "AUX", "CCONJ", "DET", "INTJ", "NOUN",
        "NUM", "PART", "PRON", "PROPN", "SCONJ", "VERB",
    ]
    feat = {f"pos_{t.lower()}": counts.get(t, 0) / n for t in universal_tags}

    imperative_sents = 0
    for sent in doc.sents:
        toks = [t for t in sent if not t.is_punct]
        if toks and toks[0].pos_ == "VERB" and toks[0].tag_ == "VB":
            imperative_sents += 1
    n_sents = max(sum(1 for _ in doc.sents), 1)
    feat["imperative_density"] = imperative_sents / n_sents * 1000
    return feat


def build():
    df = pd.read_csv(SEED_SET_PATH)
    nlp = spacy.load("en_core_web_sm")

    general_rows = [general_features(t) for t in df["text"]]
    prophetic_rows = [prophetic_features(t) for t in df["text"]]
    pos_rows = [pos_features(doc) for doc in nlp.pipe(df["text"].tolist())]

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
