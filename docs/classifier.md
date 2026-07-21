# Classifier

`src/train_classifier.py` trains on `results/seed_set_features.csv`,
compares logistic regression against a linear SVM by 5-fold cross-validated
macro-F1, fits the better one on the full seed set, and applies it to
`results/transfer_features.csv` (built by `src/chunk_transfer_corpora.py`,
which sentence-chunks the three transfer corpora and runs the same feature
extraction used on the seed set). Run in order:

```
python src/chunk_transfer_corpora.py
python src/train_classifier.py --features all      # results/classifier*.joblib etc.
python src/train_classifier.py --features narrow   # results/classifier_narrow* etc.
```

`--features narrow` drops the 92 `fw_*` function-word columns and keeps
only the prophetic-specific features plus non-lexical general-stylometric
ones (sentence/word length, TTR, POS proportions) — see "Narrowed feature
set" below for why, and what it did and didn't fix.

Outputs (each run writes its own suffixed files, so both are on disk for
comparison): `results/classifier[_narrow].joblib` (fitted pipeline),
`results/classifier_eval[_narrow].txt` (CV report + feature importance +
transfer summary), `results/transfer_predictions[_narrow].csv` (per-chunk
predictions and class probabilities for all three transfer corpora).

## Seed-set cross-validation result

Logistic regression beat linear SVM (macro-F1 0.686 vs. 0.660, 5-fold CV) and
was selected as the final model.

|            | precision | recall | f1   |
|---|---|---|---|
| prophetic  | 0.61 | 0.60 | 0.61 |
| narrative  | 0.69 | 0.75 | 0.72 |
| law-wisdom | 0.78 | 0.70 | 0.74 |

Overall accuracy 0.68 on 345 seed-set rows (5-fold CV). Prophetic is the
hardest class to separate — most of its confusion is with narrative (38 of
127 true-prophetic rows predicted narrative), which tracks with the project's
own thesis: the boundary is supposed to be genuinely blurry in places (that's
exactly what the angel-of-the-LORD and Sinai case studies in
`docs/study-notes/` were built to probe).

## A real caveat: feature importance looks partly like an artifact of which books were picked, not genre

The top logistic-regression coefficients for "narrative" and "prophetic"
are dominated by literal function-word frequencies — `fw_her`, `fw_she`,
`fw_so`, `fw_if`. Checked where `fw_her`/`fw_she` actually concentrate in
the seed set:

| book | fw_her | fw_she |
|---|---|---|
| Ruth | 32.5 | 19.6 |
| Genesis | 12.6 | 14.4 |
| 1 Kings | 16.0 | 13.5 |
| Judges, Exodus, 2 Chronicles | 0.0 | 0.0 |

"She"/"her" frequency is almost entirely a function of which narrative
passages happen to be about women (Ruth, Hagar in Genesis, the woman
brought before Solomon) — not a property of narrative register in general.
With 345 rows and 129 features, the model has ample room to key on
incidental vocabulary from the specific passages chosen rather than a
genuinely transferable stylistic signal. This is the same risk flagged
speculatively in `docs/study-notes/enoch.md`'s Jude/1-Enoch word-overlap
case study ("if they don't [score close], that's a signal the feature set
is picking up on something other than register") — except here it shows up
directly in the trained model's own coefficients, not just as a
hypothetical. Worth treating class-level accuracy numbers as provisional
until the seed set is either larger or the feature set is narrowed to
fewer, more deliberately register-specific columns (the `divine_speech_formula`,
`second_person_density`, `future_modal_density` set, rather than the full
92-column function-word table).

## Narrowed feature set

Dropped the 92 `fw_*` function-word columns and kept 24: the five
prophetic-specific features plus non-lexical general-stylometric ones
(`avg_sent_len`, `std_sent_len`, `avg_word_len`, `ttr`, `n_words`, and the
14 `pos_*` proportions). Two things came out of this, one encouraging, one
not.

**Encouraging: seed-set CV accuracy barely moved (macro-F1 0.686 → 0.691),
but feature importance got much more defensible.** `fw_her`/`fw_she` are
gone by construction, and the new top coefficients are things the project's
own hypothesis would predict: `divine_speech_formula` is now the single
strongest prophetic-class feature (+0.675, previously 6th out of 8),
`future_modal_density` and `imperative_density` show up meaningfully for
law-wisdom and narrative. Losing 105 columns for essentially no accuracy
cost is itself informative — most of the full model's apparent skill wasn't
coming from the function-word table.

**Not encouraging: the transfer result got harder to read, not easier.**

| corpus | prophetic (full) | prophetic (narrow) | law-wisdom (narrow) |
|---|---|---|---|
| 1 Enoch | 0.390 | 0.352 | 0.283 |
| Bahman Yasht | 0.272 | 0.177 | 0.345 |
| Sibylline Oracles | 0.358 | 0.242 | 0.527 |

Prophetic share *dropped* in all three corpora under the narrowed model,
and Sibylline Oracles — poetry with no legal content whatsoever — got
labeled law-wisdom over half the time. Checked why: Sibylline Oracles
chunks average 18.1 words/sentence and 4.36 letters/word, which lines up
almost exactly with the seed set's law-wisdom passages (17.8 words, 4.24
letters/word) — a coincidence of English-hexameter sentence structure, not
genre. With the topic-leaking `fw_*` columns gone, `n_words` and
`avg_word_len` (structural, not lexical, but still not really "law-wisdom"
markers) became the dominant law-wisdom signal, and they happen to fire on
translated-verse sentence rhythm as readily as on legal-code prose. In
other words: narrowing the feature set fixed one confound (topic-leaking
vocabulary) and exposed a second one underneath it (sentence-length
statistics acting as an accidental proxy for "translated verse" rather than
for law-wisdom specifically).

## Transfer-corpus results (full feature set)

Fraction of chunks per corpus the model predicted for each class:

| corpus | prophetic | narrative | law-wisdom |
|---|---|---|---|
| 1 Enoch | 0.390 | 0.423 | 0.187 |
| Bahman Yasht | 0.272 | 0.464 | 0.264 |
| Sibylline Oracles | 0.358 | 0.241 | 0.401 |

**None of the three transfer corpora came back majority-prophetic.** Given
`docs/data-sources.md` describes all three as "almost entirely
oracular/eschatological" (Sibylline Oracles), "heavily apocalyptic/prophetic
throughout" (1 Enoch), and "near-pure signal" (Bahman Yasht) in content, a
clean transfer result would have looked like all three skewing heavily
prophetic. That didn't happen. Before reading this as "prophetic register
doesn't transfer" (a real, informative possible answer per the README's own
framing), rule out three more mundane explanations first:

1. **Translator-era vocabulary, not genre.** These are three different
   translators (Terry 1890, Charles 1913, West 1897) writing archaic-register
   English deliberately styled after the KJV, but not the KJV's actual
   1611 vocabulary. If the model is substantially keyed on incidental
   function-word frequency (see caveat above), it may be detecting
   "which translator/era wrote this," not "is this prophetic," and none of
   the three would match KJV's specific idiom. **Tested this directly**
   (see "Narrowed feature set" below) by dropping the function-word table
   entirely — the transfer numbers didn't improve, they got worse in all
   three corpora. So this confound was real (the narrowed model's feature
   importances are much more defensible), but removing it wasn't
   sufficient on its own to produce a clean transfer signal, which means
   it isn't the whole story.
2. **Chunking method mismatch.** The seed set is curated verses (a human
   picked the boundaries to isolate clean genre signal); the transfer
   corpora are mechanically sentence-chunked continuous prose/poetry with
   no such curation — a much noisier unit that likely dilutes any signal
   present. **Gained direct evidence for this one**: with the function-word
   table gone, sentence-length statistics (`n_words`, `avg_word_len`) took
   over as the dominant law-wisdom signal, and Sibylline Oracles's
   translated-hexameter sentence rhythm happens to match the seed set's
   law-wisdom passages structurally (see "Narrowed feature set"). That's
   chunking-shape leaking into the prediction, not genre.
3. **Small, high-dimensional training set.** 345 rows and 129 (or 24,
   narrowed) features is thin for a model expected to generalize across
   three centuries of English and multiple literary traditions — the
   seed-set CV caveat above applies here even more.

Still not fixed. Narrowing the feature set was informative — it confirmed
confound #1 was real and, in the same pass, surfaced #2 more concretely —
but the net transfer result is, if anything, less clean than before
narrowing, not more. The honest summary after two feature-set variants:
this project has not yet produced a transfer result that's trustworthy
enough to read as either "prophetic register transfers" or "it doesn't."
Both readings are still live. Likely next steps, in rough order of
expected payoff: growing the seed set (345 rows is genuinely thin for 24+
features); replacing mechanical sentence-chunking of the transfer corpora
with hand-picked pericopes the way the seed set itself was built, so the
transfer evaluation isn't fighting a unit-of-analysis mismatch on top of
everything else; and only then revisiting feature selection.
