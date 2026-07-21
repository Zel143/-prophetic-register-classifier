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
python src/transfer_pericopes.py                    # hand-picked pericopes, see below
python src/eval_pericopes.py                        # applies both saved models to them
```

`--features narrow` drops the 92 `fw_*` function-word columns and keeps
only the prophetic-specific features plus non-lexical general-stylometric
ones (sentence/word length, TTR, POS proportions) — see "Narrowed feature
set" below for why, and what it did and didn't fix.

Outputs (each run writes its own suffixed files, so both are on disk for
comparison): `results/classifier[_narrow].joblib` (fitted pipeline),
`results/classifier_eval[_narrow].txt` (CV report + feature importance +
transfer summary), `results/transfer_predictions[_narrow].csv` (per-chunk
predictions and class probabilities for all three transfer corpora),
`results/transfer_pericope_chunks_features.csv` and
`results/transfer_pericopes_predictions.csv` (hand-picked pericopes,
sentence-chunked within each — see "Hand-picked pericopes" below for why).

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

## Hand-picked pericopes

`src/transfer_pericopes.py` hand-selects 12 coherent passages across the
three transfer corpora (4-5 per corpus — e.g. 1 Enoch's opening
theophany that Jude 1:14-15 quotes, its "Woes for the Sinners" chapter
XCIV, the Watchers' descent narrative; Sibylline Oracles' "Prophecy of
Christ" section and its "Woe on Babylon" oracle; Bahman Yasht's opening
dream-narrative split from Ahura Mazda's prophetic answer, and its closing
resurrection oracle), the same editorial method `src/build_seed_set.py`
used for the biblical seed set, targeting confound #2 above directly.
Boundaries were found the same way the Bahman Yasht page range was
originally fixed (search for a distinctive phrase, not a line-number
guess) — see the module docstring for the full list and exact anchors.
`python src/eval_pericopes.py` applies both saved models and writes
`results/transfer_pericopes_predictions.csv`.

**First attempt found a second length confound before it could mislead
anyone.** Applying the models directly to whole-pericope-level features
(110-767 words each) made every single one of the 12 pericopes predict
"narrative," regardless of content — including the ones that are about as
oracular as text gets, like the Woes chapter. Checked why: the seed set's
`n_words` tops out at 59; these pericopes start at 109. `n_words` has a
strong positive coefficient for narrative in both models (see feature
tables above), and at that much z-score distance from the training
distribution it was overwhelming every other feature. Fix: sentence-chunk
*within* each hand-picked pericope (same chunker as
`chunk_transfer_corpora.py`), so each evaluation unit is drawn only from a
deliberately chosen coherent passage (fixing confound #2) but stays
length-comparable to the training data (not reintroducing a third
confound). 160 chunks resulted; that's what's actually predicted on.

**Result: the clearest pro-transfer signal so far, but it doesn't survive
feature-set narrowing.**

| corpus | prophetic share (full model) | prophetic share (narrow model) |
|---|---|---|
| 1 Enoch | 0.509 | 0.466 |
| Bahman Yasht | 0.429 | 0.286 |
| Sibylline Oracles | 0.489 | 0.243 |

Under the full model, all three corpora land close to or above 43-51%
prophetic — a real jump from the mechanically-chunked pass (27-39%) and,
for 1 Enoch and Sibylline Oracles, close to the "should skew heavily
prophetic" result the source material would predict. The specific pericope
Jude 1:14-15 quotes (1 Enoch's opening theophany) scores especially
strongly: 64% prophetic under the full model, 82% under the narrow model —
the single cleanest result in the whole project, and notably the *one*
pericope where hand-picking and narrowing agree with each other and with
the hypothesis. Bahman Yasht's narrative/prophetic split pericopes moved in
the expected direction too: the dream-narrative half (Zoroaster's report of
his dream) scored 50/50 under the full model and 100% narrative under the
narrow model, while the oracle half (Ahura Mazda's first-person answer)
held steady at 50% prophetic under both.

But the narrow model doesn't replicate the improvement broadly — Bahman
Yasht and Sibylline Oracles both drop under narrowing (Sibylline Oracles
from 48.9% to 24.3%), the same law-wisdom-as-default pattern seen in the
mechanically-chunked narrow-model pass. So: hand-picking pericopes produced
real, checkable wins (the Jude/1-Enoch anchor pericope, the Bahman Yasht
narrative/oracle split) alongside the same structural-feature confound
narrowing already surfaced once. Sample size matters too — 12 pericopes,
160 chunks, some pericopes contributing as few as 2 chunks (Bahman Yasht's
short opening episodes) — these percentages have real sampling noise the
larger mechanical-chunking pass doesn't.

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

Confound #2 (chunking mismatch) has now been directly addressed by the
hand-picked pericopes above, with a genuinely encouraging result under the
full feature set. The honest summary after three passes (mechanical
chunking / full features, mechanical chunking / narrow features,
hand-picked pericopes / both feature sets): the strongest, most specific
piece of evidence this project has produced — the Jude-quoted 1 Enoch
passage scoring 64-82% prophetic under both models, and Bahman Yasht's
narrative/oracle split moving the expected direction — supports "prophetic
register transfers, at least somewhat, for hand-curated passages." But that
result doesn't hold up once the feature set is narrowed to the more
defensible column set, and doesn't extend cleanly to Sibylline Oracles or
to the corpora as a whole under mechanical, representative chunking. Both
"transfers" and "doesn't, or only partially" remain live readings — but the
pericope-level result narrows *where* the disagreement lives: not "is there
any prophetic-register signal at all" (there clearly is, at least in
places), but "is that signal strong and general enough to survive both
different feature sets and different sampling methods." It currently isn't,
consistently. Likely next steps, in rough order of expected payoff: growing
the seed set (345 rows is genuinely thin for 24+ features, and the
pericope-level evaluation's small N — 160 chunks across 12 pericopes — has
real sampling noise of its own); hand-picking more transfer pericopes to
shrink that noise; and only then revisiting feature selection again with
more data to check it against.
