"""
Hand-picked pericopes from the three transfer corpora, replacing (well,
complementing -- see docs/classifier.md) the mechanical sentence-chunking
in src/chunk_transfer_corpora.py.

Why: docs/classifier.md's narrowed-feature-set run traced part of the
transfer classifier's confusion to a chunking-shape confound -- mechanical
sentence-chunking produces units whose length/structure can coincidentally
match a seed-set class regardless of content (Sibylline Oracles' translated
hexameter sentence-length happened to match the seed set's law-wisdom
passages). Hand-picking pericopes -- coherent narrative or oracle units, the
same editorial method src/build_seed_set.py used for the biblical seed set
-- removes that specific confound, at the cost of coverage: 12 pericopes
here vs. 4274 mechanical chunks. This is a controlled complement to the
mechanical-chunking pass, not a full replacement -- see docs/classifier.md.

Boundaries were found by searching each corpus's raw .txt for a distinctive
start phrase and an end phrase (or, for Bahman Yasht, a fixed length -- its
scrape has heavy inline footnote-marker noise, see clean_bahman_yasht_text).

Two output files, because the whole pericopes (110-767 words) turned out to
be badly out of the seed set's training-length range (max 59 words) --
applying the trained classifier directly to whole-pericope-level features
made `n_words` alone swamp every other signal and forced every single
pericope to predict "narrative" regardless of content, confirmed by
checking the two distributions directly. Fix: sentence-chunk *within* each
hand-picked pericope (same chunker as src/chunk_transfer_corpora.py) so the
evaluation unit stays length-comparable to training data while still only
ever being drawn from a deliberately chosen coherent passage, not the whole
corpus at large.

  - results/transfer_pericopes_features.csv: one row per whole pericope
    (for reading/reference -- not used for prediction).
  - results/transfer_pericope_chunks_features.csv: sentence-level rows
    within each pericope, tagged with corpus/pericope_id/note -- this is
    what src/eval_pericopes.py actually predicts on.

Usage:
    python src/transfer_pericopes.py
"""
import os
import re

import pandas as pd
import spacy

from chunk_transfer_corpora import chunk_sentences
from extract_features import general_features, prophetic_features, pos_features

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRANSFER_DIR = os.path.join(REPO_ROOT, "data", "transfer")
RESULTS_DIR = os.path.join(REPO_ROOT, "results")
OUT_PATH = os.path.join(RESULTS_DIR, "transfer_pericopes_features.csv")
CHUNKS_OUT_PATH = os.path.join(RESULTS_DIR, "transfer_pericope_chunks_features.csv")

BRACKET_RE = re.compile(r"[⌈⌉⌊⌋⟨⟩\[\]]")
FOOTNOTE_DIGIT_RE = re.compile(r"(?<=\s)\d+(?=\s)")

# (corpus, pericope_id, start_phrase, end_phrase, note)
PERICOPES = [
    # Per the project owner's direction (2026-07-22), 1 Enoch 1:9 -- the
    # verse Jude 1:14-15 quotes -- is excluded from all analysis. The
    # pericope ends at the "9. And behold!" boundary, covering vv. 1-8 only.
    ("1_enoch", "ch1_theophany", "CHAPTER I.", "9. And behold!",
     "Enoch's opening blessing/judgment theophany, vv. 1-8 (v. 9 excluded per project owner's direction)"),
    ("1_enoch", "ch6-7_watchers", "CHAPTER VI.", "CHAPTER VIII",
     "the Watchers descend and take wives -- narrative"),
    ("1_enoch", "ch10_judgment", "CHAPTER X.", "CHAPTER XI.",
     "God's judgment commands to the archangels -- imperative-heavy oracle"),
    ("1_enoch", "ch14_throne_vision", "CHAPTER XIV.", "CHAPTER XV.",
     "Enoch's throne-vision -- apocalyptic narrative"),
    ("1_enoch", "ch94_woes", "XCIV. 6-11.", "\nXCV.",
     "'Woes for the Sinners' -- parallel structure to Isaiah 5's woe oracles"),
    ("sibylline_oracles", "book1_creation", "BEGINNING with the generation first", "60 Of the sweet",
     "creation of the world and the Fall -- narrative"),
    ("sibylline_oracles", "book1_prophecy_of_christ", "Then also shall a child of the great God", "And then shall Israel, drunken",
     "the 'Prophecy of Christ' section -- third-person future-tense messianic oracle"),
    ("sibylline_oracles", "book3_oracle_against_idolatry", "O THOU high-thundering blessed heavenly One,", "This is the God who formed four-lettered Adam",
     "the Sibyl's own first-person oracle proclamation against idolatry"),
    ("sibylline_oracles", "book3_woe_babylon", "How many lamentable sufferings", "To thee, O Egypt",
     "'Woe on Babylon' -- direct second-person judgment address"),
    ("bahman_yasht", "ch1_zoroaster_dream", "1. As", "3. Aûharmazd spoke to Zaratû",
     "Zoroaster's dream of the four-branched tree, and his report of it -- narrative"),
    ("bahman_yasht", "ch1_ahuramazda_oracle", "3. Aûharmazd spoke to Zaratû", "6. It is declared",
     "Ahura Mazda's first-person prophecy of the four ages"),
    ("bahman_yasht", "final_resurrection_oracle", "58. ‘And, afterwards, the water, fire, and vegetation", "Footnotes",
     "Ahura Mazda's first-person eschatological resurrection/renovation oracle, the book's climax"),
]


def clean_bahman_yasht_text(text):
    """Bahman Yasht's scrape has diacritic-split words (macron rendering)
    and bare footnote-reference digits inline (distinct from verse numbers,
    which are followed by a period). Collapse whitespace/newlines first,
    then strip standalone digit tokens not immediately followed by '.'."""
    text = " ".join(text.split())
    text = FOOTNOTE_DIGIT_RE.sub("", text)
    return " ".join(text.split())


def extract(text, start, end):
    start_idx = text.find(start)
    if start_idx == -1:
        raise ValueError(f"start phrase not found: {start!r}")
    end_idx = text.find(end, start_idx + len(start))
    if end_idx == -1:
        raise ValueError(f"end phrase not found after start: {end!r}")
    return text[start_idx:end_idx]


def build():
    texts_by_corpus = {}
    for corpus in ["1_enoch", "sibylline_oracles", "bahman_yasht"]:
        with open(os.path.join(TRANSFER_DIR, f"{corpus}.txt"), encoding="utf-8") as f:
            texts_by_corpus[corpus] = f.read()

    rows = []
    for corpus, pericope_id, start, end, note in PERICOPES:
        raw = extract(texts_by_corpus[corpus], start, end)
        raw = BRACKET_RE.sub(" ", raw)
        if corpus == "bahman_yasht":
            clean = clean_bahman_yasht_text(raw)
        else:
            clean = " ".join(raw.split())
        rows.append({"corpus": corpus, "pericope_id": pericope_id, "note": note, "text": clean})

    df = pd.DataFrame(rows)
    nlp = spacy.load("en_core_web_sm")

    def add_features(texts):
        general_rows = [general_features(t) for t in texts]
        prophetic_rows = [prophetic_features(t) for t in texts]
        pos_rows = [pos_features(doc) for doc in nlp.pipe(texts)]
        return pd.concat(
            [pd.DataFrame(general_rows), pd.DataFrame(prophetic_rows), pd.DataFrame(pos_rows)],
            axis=1,
        )

    texts = df["text"].tolist()
    out = pd.concat([df, add_features(texts)], axis=1)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    out.to_csv(OUT_PATH, index=False)
    print(f"wrote {len(out)} pericopes x {len(out.columns)} columns to {OUT_PATH}")
    for _, row in df.iterrows():
        print(f"[{row['corpus']}] {row['pericope_id']}: {row['note']} ({len(row['text'].split())} words)")

    chunk_rows = []
    for _, row in df.iterrows():
        for i, chunk in enumerate(chunk_sentences(row["text"])):
            chunk_rows.append({
                "corpus": row["corpus"], "pericope_id": row["pericope_id"],
                "note": row["note"], "chunk_id": i, "text": chunk,
            })
    chunks_df = pd.DataFrame(chunk_rows)
    chunks_out = pd.concat([chunks_df, add_features(chunks_df["text"].tolist())], axis=1)
    chunks_out.to_csv(CHUNKS_OUT_PATH, index=False)
    print(f"\nwrote {len(chunks_out)} pericope-chunks x {len(chunks_out.columns)} columns to {CHUNKS_OUT_PATH}")
    print(chunks_df.groupby(["corpus", "pericope_id"]).size().to_string())


if __name__ == "__main__":
    build()
