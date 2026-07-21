# Feature extraction

`src/extract_features.py` reads `data/seed_set.csv` and writes
`results/seed_set_features.csv` (345 rows x 136 columns: seed-set columns +
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
| divine_speech_formula | 0.00 | 0.00 | 0.12 |
| vocative_density | 0.00 | 0.00 | 0.39 |
| second_person_density | 68.42 | 20.54 | 37.47 |
| future_modal_density | 18.53 | 6.15 | 25.83 |
| imperative_density | 90.91 | 15.38 | 47.24 |
| ttr | 0.86 | 0.77 | 0.79 |

(Updated after adding the Sinai passages — see below. The Decalogue pushed
law-wisdom's `second_person_density` up further, from 54.75 to 68.42.)

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

## Angel-of-the-LORD theophanies: a within-scene validation

`docs/study-notes/angel-of-the-lord.md` documents seven scenes (Genesis 16 & 22,
Exodus 3, Judges 6 & 13) split verse-by-verse into a narrative half (angel
appears/acts) and a prophetic half (angel speaks as God in first person).
This is as close to a controlled test as the seed set has: same scene,
same characters, same book — only the speech-act changes. Result, straight
from `results/seed_set_features.csv`: in every one of the five multi-verse
episodes, the "speaks" verses score higher on `second_person_density` and
`future_modal_density` than the "appears/acts" verses from the same scene
(several narrative-half verses score exactly 0 on both). Genesis 22:16 also
fires `divine_speech_formula` — the only non-prophetic-book verse in the
seed set to do so — confirming that feature is catching the literal
formula wherever it occurs, not just tracking which book a verse is from.

## Sinai: source of the prophetic/law-wisdom overlap

`docs/study-notes/sinai.md` documents the Sinai theophany (Exodus 19-20)
split at the seam between the divine self-declaration opening the Decalogue
(Exodus 20:1-2, prophetic class) and the commandments themselves (20:3-17,
law-wisdom class). The commandments turned out to have the single highest
`second_person_density` of any passage in the seed set (several individual
commandments score 200-250 per 1000 words, vs. a 37.47 prophetic-class
average) — direct confirmation that the prophetic/law-wisdom overlap noted
above isn't a modeling artifact, it traces back to a real shared origin:
both registers descend from the same unmediated-theophany event. Also added
Micah 1:3-4, a later prophetic passage reusing Sinai's storm-theophany
imagery (third-person "the LORD cometh forth," not direct address) — a
reminder that "prophetic register" covers at least two different shapes
(direct oracle-address vs. third-person theophany-description) that this
seed set's features don't yet distinguish.

## Next up

Feature selection and the classifier itself (logistic regression / SVM per
README) — not yet built.
