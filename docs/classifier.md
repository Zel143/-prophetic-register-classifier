# Classifier

`src/train_classifier.py` trains on `results/seed_set_features.csv`,
compares logistic regression against a linear SVM by 5-fold cross-validated
macro-F1, fits the better one on the full seed set, and applies it to
`results/transfer_features.csv` (built by `src/chunk_transfer_corpora.py`,
which sentence-chunks the three transfer corpora and runs the same feature
extraction used on the seed set). Run in order:

```
python src/chunk_transfer_corpora.py
python src/train_classifier.py
```

Outputs: `results/classifier.joblib` (fitted pipeline), `results/classifier_eval.txt`
(CV report + feature importance + transfer summary), `results/transfer_predictions.csv`
(per-chunk predictions and class probabilities for all three transfer corpora).

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

## Transfer-corpus results

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
   the three would match KJV's specific idiom.
2. **Chunking method mismatch.** The seed set is curated verses (a human
   picked the boundaries to isolate clean genre signal); the transfer
   corpora are mechanically sentence-chunked continuous prose/poetry with
   no such curation — a much noisier unit that likely dilutes any signal
   present.
3. **Small, high-dimensional training set.** 345 rows and 129 features is
   thin for a model expected to generalize across three centuries of
   English and multiple literary traditions — the seed-set CV caveat above
   applies here even more.

None of this is fixed yet. It's flagged rather than resolved because
untangling it (dropping to a narrower, more deliberately register-specific
feature set; growing the seed set; or trying per-translator baseline
normalization) is real follow-on work, not a small tweak — and reporting an
inconclusive transfer result honestly is more useful than quietly picking
whichever reading flatters the hypothesis.
