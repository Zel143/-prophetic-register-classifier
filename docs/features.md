# Feature extraction

`src/extract_features.py` reads `data/seed_set.csv` and writes
`results/seed_set_features.csv` (293 rows x 136 columns: seed-set columns +
features). Requires the spaCy English model:
`python -m spacy download en_core_web_sm`. Run: `python src/extract_features.py`.

## Feature groups

**General stylometric** (borrowed shape from
`../kjv-stylometry-repo/repo/src/features.py` — same function-word list,
same relative-frequency-per-1000-words convention, so results are
comparable across the two projects):
- `fw_*` — 92 function-word relative frequencies
- `avg_sent_len`, `std_sent_len` — clause length (split on `.?!;`)
- `avg_word_len`, `ttr` (type-token ratio), `n_words`
- `pos_*` — POS-tag proportions (spaCy `en_core_web_sm`, 14 universal tags)

**Prophetic-register-specific** (regex-based unless noted):
- `divine_speech_formula` — count of "thus saith the LORD" / "the word of
  the LORD came" / similar formulas
- `second_person_density` — thou/thee/thy/thine/ye/you/your/yours per 1000
  words
- `vocative_density` — `O <Capitalized word>` pattern per 1000 words
- `future_modal_density` — shall/will per 1000 words
- `imperative_density` — spaCy-based, see caveat below

## Known caveat: spaCy on archaic English

`en_core_web_sm` is trained on modern English and visibly mis-tags KJV
forms — e.g. "saith" tags as `ADP` not `VERB`, sentence-initial "Hear" tags
as `PROPN` from capitalization alone. Treat `pos_*` and `imperative_density`
as an approximate signal, not ground truth. The regex-based features
(function words, divine-speech formula, second-person density, vocative
density) don't depend on the tagger and are the more reliable half of the
set.

One specific fix already made: spaCy's English morphologizer never emits
`Mood=Imp` at all — imperative and bare infinitive share a surface form in
English and the model doesn't disambiguate them (verified directly: "Hear,
O heavens" tags as `VerbForm=Inf`, never `Mood=Imp`). `imperative_density`
uses a heuristic instead — a sentence whose first non-punct token is a
bare-infinitive-form verb — which is nonzero and behaves sensibly (see
below), but is still an approximation, not a mood the tagger actually
detects.

## What the seed set shows so far (class means)

| feature | law-wisdom | narrative | prophetic |
|---|---|---|---|
| divine_speech_formula | 0.00 | 0.00 | 0.13 |
| vocative_density | 0.00 | 0.00 | 0.47 |
| second_person_density | 54.75 | 21.90 | 33.61 |
| future_modal_density | 21.83 | 6.61 | 25.67 |
| imperative_density | 82.19 | 17.70 | 56.07 |
| ttr | 0.86 | 0.78 | 0.79 |

Two things worth flagging before feature selection / modeling:

- **Divine-speech formula and vocative density are prophetic-exclusive in
  this seed set** (zero elsewhere) — strong, clean signal, but also nearly
  tautological (they're close to how "prophetic" was defined when picking
  passages). Don't expect them alone to prove much; they're closer to a
  sanity check than a discovery.
- **Second-person density does *not* cleanly separate prophetic from
  law-wisdom** — Leviticus's legal commands ("Ye shall not steal...") use
  about as much direct address as prophetic oracle does, sometimes more.
  Imperative density shows the same pattern (law-wisdom highest, from
  legal commands like "Speak unto the children of Israel..."). This is
  informative, not a bug: it means "prophetic vs. law" will lean more on
  the divine-speech-formula and future-tense features than on
  second-person/imperative address, which those two classes actually
  share stylistically (both are commanding-voice registers — one legal,
  one oracular).

## Next up

Feature selection and the classifier itself (logistic regression / SVM per
README) — not yet built.
