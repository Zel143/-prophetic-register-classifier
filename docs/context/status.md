# Current Status

Snapshot of where the project stands. Update this as work progresses — it should always
reflect the current state, not a history (see `decisions.md` for the log of past decisions).

_Last updated: 2026-07-22_

## Summary

Stylometric classifier project: does "prophetic register" in biblical Hebrew/English text
reflect a detectable linguistic style (verb mood, address form, formulaic markers) rather
than just content, and does that style transfer to non-biblical prophetic/oracular
literature (Sibylline Oracles, 1 Enoch, Zoroastrian eschatology)? Repo scope, label scheme,
and data-sourcing plan are written up; source data for both the biblical corpus and all
three v1 transfer corpora is fetched; the hand-labeled seed set (345 verses, including
seven angel-of-the-LORD theophanies split narrative/prophetic within-scene, and the Sinai
theophany split prophetic/law-wisdom within-scene) is built and explored in a notebook; and
feature extraction (general stylometric + prophetic-specific) is done and run on the seed
set; and a classifier (logistic regression, chosen over linear SVM by CV) has been
evaluated five ways: full 129-column feature set, narrowed 24-column feature set, a further
"nostruct" 18-column feature set (narrow minus sentence/word-length columns), a "normttr"
variant (nostruct with raw ttr swapped for length-normalized Guiraud's R), and hand-picked
pericopes (all four feature sets). Best evidence so far for transfer: the specific 1 Enoch
passage Jude 1:14-15 quotes scores 64-82% prophetic across *all four* feature sets — the one
result in the project that's robust to feature-set choice. That result doesn't generalize
cleanly to Sibylline Oracles or Bahman Yasht: the length-confound test (nostruct) showed the
mislabeling wasn't about sentence length but translated-verse-form (elevated lexical
diversity, lower verb density) shared by the two verse-translated corpora but absent from
1 Enoch (prose-translated); the follow-up normttr test confirmed part of that was a fixable
ttr sample-size artifact (Sibylline Oracles's law-wisdom share dropped from 53.1% to 42.9%,
seed-set CV accuracy improved) but the freed probability mass moved to "narrative," not
"prophetic" — see `docs/classifier.md`'s "Length-normalizing ttr" section.

## In progress

- Nothing actively in flight. Next unstarted step, per `docs/classifier.md`'s updated
  conclusion: growing the seed set (345 rows is thin for 24+ features) and hand-picking
  more transfer pericopes — especially more prose-translated comparison material, to test
  whether the prose/verse split found in the nostruct/normttr tests holds beyond one corpus
  each. The verse-form confound now has one real fix applied (Guiraud's R, keep it — better
  accuracy, more defensible coefficients) and one open gap remaining (Sibylline Oracles's
  ambiguous narrative/prophetic split under normttr) that more data is better positioned to
  resolve than further feature engineering.

## Done

- Length-normalized ttr / normttr feature set (2026-07-22): added `ttr_guiraud` (Guiraud's R,
  unique words / sqrt(n)) to `src/extract_features.py` and a fourth feature set,
  `--features normttr` (nostruct with raw `ttr` swapped for `ttr_guiraud`), to
  `src/train_classifier.py`. Raw ttr is a known sample-size artifact (shorter chunks show
  higher ttr regardless of genre), and Sibylline Oracles's chunks average 18.1 words vs.
  1 Enoch's 25.3 — a plausible confound on top of the verse-form one nostruct surfaced.
  Result: partial fix. Guiraud's R pulls Sibylline Oracles's mean back inside the seed set's
  range (3.66, vs. raw ttr's 0.914 sitting above the seed set's max of 0.857); seed-set CV
  accuracy improved (0.66 vs. nostruct's 0.63); Sibylline Oracles's law-wisdom share under
  mechanical chunking dropped from 53.1% to 42.9% (no longer a majority verdict). But the
  freed-up mass went mostly to "narrative" (19.2% → 23.9% prophetic, barely moved) — so this
  fixes the false law-wisdom-majority result without manufacturing a prophetic signal that
  wasn't otherwise there. `normttr` is now the recommended feature set going forward (best
  CV accuracy among the reduced sets, most defensible coefficients, no known unfixed
  confound). Full writeup in `docs/classifier.md`.

- Length-confound test / nostruct feature set (2026-07-22): added `--features nostruct` to
  `src/train_classifier.py` (18 columns: narrow minus `avg_sent_len`/`std_sent_len`/
  `avg_word_len`/`n_words`, isolating whether sentence-length statistics specifically were
  behind the narrow model's Sibylline-Oracles-as-law-wisdom result) and extended
  `src/eval_pericopes.py` to apply all three saved models. Result: the confound did **not**
  go away (Sibylline Oracles still 53.1% law-wisdom under mechanical chunking, near-identical
  to narrow's 52.7%) — ruling out sentence length as the specific mechanism. Traced the real
  cause instead: Sibylline Oracles's `ttr` (0.914) sits above the entire seed set's range
  (max 0.857, law-wisdom), and its POS profile (verb/subordinating-conjunction density) sits
  closer to law-wisdom than prophetic — an artifact of Terry's 1890 English hexameter
  translation (short lines, high per-chunk lexical variety), not legal content. Bahman Yasht
  (also verse-translated) shows the same elevation (ttr 0.880) and the same even split;
  1 Enoch (prose-translated, Charles 1913) doesn't (ttr 0.792) and is the corpus whose
  transfer result has held up. New, better-supported reading: the confound is
  translation-*form* (verse vs. prose), not length or vocabulary era, and it isn't fixable
  by dropping more feature columns since `ttr`/POS carry the same signal `n_words` did.
  Full writeup in `docs/classifier.md`.
- Hand-picked transfer pericopes (2026-07-21): `src/transfer_pericopes.py` hand-selects 12
  coherent passages across the three transfer corpora (the seed-set editorial method,
  applied to the transfer corpora — e.g. 1 Enoch's opening theophany that Jude 1:14-15
  quotes, its "Woes for the Sinners" chapter, the Watchers' descent narrative; Sibylline
  Oracles' "Prophecy of Christ" and "Woe on Babylon"; Bahman Yasht's opening
  dream-narrative vs. Ahura Mazda's prophetic answer, and its closing resurrection oracle),
  targeting the chunking-mismatch confound named in the narrowed-feature entry below.
  First attempt applying the models to whole-pericope features (110-767 words) surfaced a
  *second* confound before it could mislead anyone: `n_words` (max 59 in the seed set) blew
  so far past the training range that every single pericope predicted "narrative"
  regardless of content. Fixed by sentence-chunking within each hand-picked pericope (160
  chunks), keeping the units length-comparable to training data while still only ever
  drawn from a deliberately chosen coherent passage. Result (`src/eval_pericopes.py`):
  under the full feature set, all three corpora scored 43-51% prophetic (up from 27-39% on
  mechanical chunking), and the Jude-quoted 1 Enoch passage specifically scored 64%
  (full model) / 82% (narrow model) prophetic — the single cleanest result in the project.
  But the narrow model doesn't replicate the broader improvement (Sibylline Oracles drops
  back to 24.3%), repeating the law-wisdom-as-default pattern from the narrowed-feature
  mechanical-chunking pass. Full numbers and interpretation in `docs/classifier.md`.
- Narrowed-feature classifier (2026-07-21): re-ran `src/train_classifier.py --features
  narrow` (24 columns: prophetic-specific features + non-lexical general-stylometric
  features, dropping the 92 `fw_*` function-word columns implicated in the earlier
  `fw_her`/`fw_she` overfitting finding). Seed-set CV accuracy barely moved (macro-F1
  0.686 → 0.691) but feature importance got much more defensible —
  `divine_speech_formula` became the single strongest prophetic-class feature. However the
  transfer result got *harder* to read, not easier: prophetic share dropped in all three
  corpora, and Sibylline Oracles got labeled law-wisdom over half the time (0.527) — traced
  to its translated-hexameter sentence length/word-length coincidentally matching the seed
  set's law-wisdom passages structurally, not genre. Net effect: narrowing fixed one
  confound (topic-leaking vocabulary) and exposed a second one underneath it
  (sentence-length statistics acting as a chunking-shape proxy rather than a genre marker).
  Neither the full nor the narrowed feature set has produced a transfer result trustworthy
  enough to call "transfers" or "doesn't transfer" — both readings are still live. Full
  writeup, including the specific numbers for both variants side by side, in
  `docs/classifier.md`.
- Classifier (2026-07-21): `src/chunk_transfer_corpora.py` sentence-chunks the three
  transfer corpora and extracts the same feature set as the seed set (4274 chunks total).
  `src/train_classifier.py` trains logistic regression vs. linear SVM (5-fold CV, macro-F1
  0.686 vs. 0.660 — logistic regression selected), evaluates on the seed set (68% CV
  accuracy; prophetic is the hardest class, confused mostly with narrative), and applies
  the fitted model to the transfer corpora. **None of the three transfer corpora came back
  majority-prophetic** (1 Enoch 39.0% prophetic, Bahman Yasht 27.2%, Sibylline Oracles
  35.8%) despite all three being sourced as heavily/near-purely oracular content — a
  real, so-far-unresolved result, not yet a clean "prophetic register does/doesn't
  transfer" answer. Also found a concrete overfitting risk in the trained model's own
  feature-importance ranking: top coefficients include `fw_her`/`fw_she`, which turn out to
  almost entirely track which narrative passages happen to be about women (Ruth, Hagar) —
  vocabulary tied to which books were picked, not narrative register generally. Full
  methodology, results, and the three candidate explanations for the weak transfer result
  (translator-era vocabulary vs. genre, chunking-method mismatch between curated seed
  verses and mechanically-chunked transfer prose, small/high-dimensional training set) are
  in `docs/classifier.md`.
- Sinai seed-set additions (2026-07-21): added the Sinai theophany (Exodus 19-20) to
  `data/seed_set.csv`, split not narrative/prophetic like the angel-of-the-LORD scenes but
  prophetic/law-wisdom — Exodus 20:1-2 (divine self-declaration) is prophetic, 20:3-17 (the
  commandments) is law-wisdom, Exodus 19:16-20 (thunder/cloud/trumpet scene-setting) is
  narrative. Also added Micah 1:3-4 (prophetic, reuses Sinai storm-theophany imagery as
  judgment poetry). This is the seed set's clearest illustration of where the
  prophetic/law-wisdom feature overlap (see feature-extraction entry below) comes from: the
  Decalogue's commandments turned out to have the single highest second-person density of
  any passage in the set. Full writeup in `docs/study-notes/sinai.md`. Seed set is now 345
  verses (127 prophetic, 130 narrative, 88 law-wisdom).
- Angel-of-the-LORD seed-set additions (2026-07-21): added seven theophany scenes
  (Genesis 16 & 22, Exodus 3, Judges 6 & 13) to `data/seed_set.csv`, each split at the
  seam between the angel's narrative appearance (narrative class) and the angel's
  first-person divine speech (prophetic class) — a direct, within-scene test of the
  README's "oracle-bearing verses excluded even within narrative books" rule. Rationale,
  per-episode table, and feature-extraction validation (the "speaks" half consistently
  scores higher on second-person/future-modal density than the "appears" half of the same
  scene) are in `docs/study-notes/angel-of-the-lord.md`. Also corrected an earlier call: Genesis 22
  ("saith the LORD" verses 16-18) was originally excluded as too hard to excise cleanly —
  turned out not to be true once specifically re-examined. Seed set is now 321 verses (123
  prophetic, 125 narrative, 73 law-wisdom).
- Feature extraction (2026-07-21): `src/extract_features.py` writes
  `results/seed_set_features.csv` (136 columns: function-word frequencies, sentence/word
  stats, TTR, POS-tag proportions, plus prophetic-specific divine-speech-formula,
  second-person, vocative, future-modal, and imperative density). Function-word list and
  general-stylometric feature shape borrowed from `../kjv-stylometry-repo` for
  cross-project comparability. Full writeup, caveats (spaCy mis-tags archaic KJV forms;
  `Mood=Imp` never fires so imperative density uses a bare-infinitive-first-word heuristic
  instead), and class-mean findings (divine-speech-formula/vocative are prophetic-exclusive
  but near-tautological; second-person/imperative density don't cleanly separate prophetic
  from law-wisdom, since legal commands use as much direct address as oracle does) are in
  `docs/features.md`.
- Seed set exploration notebook (2026-07-21): `notebooks/01_seed_set_exploration.ipynb`,
  executed. Label balance, verse-length distribution by class, sample verses, and a
  word-overlap/Jaccard check on the Jude 1:14-15 / 1 Enoch 1:9 pair (0.46 similarity,
  confirming the near-verbatim quotation from `docs/study-notes/enoch.md`).

- Seed set (2026-07-21): `src/build_seed_set.py` pulls a hand-curated reference list of
  verse ranges out of `data/Bible-kjv/` into `data/seed_set.csv` (293 verses: 107
  prophetic, 113 narrative, 73 law-wisdom). Reference list and selection rationale — what
  counts as "oracle-bearing" vs. clean narrative, why certain passages were excluded — is
  in `docs/seed-set.md`. Includes Genesis 5:21-24 (Enoch) in the narrative class and Jude
  1:14-15 in the prophetic class.
- Enoch deep dive (2026-07-21): `docs/study-notes/enoch.md` collects every canonical mention
  of Enoch (Genesis 4 vs. 5 — two different people; Luke 3; Hebrews 11; Jude 1) and traces
  the textual link this project turned up: Jude 1:14-15 is a near-verbatim quotation of
  1 Enoch 1:9, and Jude explicitly calls it "prophesied." That's a same-register anchor
  point pairing a seed-set verse with the 1 Enoch transfer corpus where the prophetic
  label isn't this project's editorial call — it's the canon's own. Both verses are now in
  `data/seed_set.csv`.
- Data pipeline (2026-07-20): `src/setup_data.py` clones `aruljohn/Bible-kjv` into
  `data/Bible-kjv/` (gitignored, same convention as `kjv-stylometry-repo`) and scrapes the
  three ready transfer corpora from sacred-texts.com into `data/transfer/*.txt` (vendored,
  committed — small public-domain texts per the README's repo-layout note). Script is
  rerunnable (`--kjv-only` / `--transfer-only` / `--corpus <name>`) and paces requests
  2s apart to stay under sacred-texts.com's Cloudflare rate limit.
  - `data/transfer/sibylline_oracles.txt` — Terry 1890 translation, Books I–XIV.
  - `data/transfer/1_enoch.txt` — Charles 1913 translation, Chapters I–CVIII.
  - `data/transfer/bahman_yasht.txt` — West 1897 translation (SBE vol. 5), Observations +
    Chapters I–III. Page range for this one required manual correction after the first
    scrape pulled the adjacent "Selections of Zâd-sparam" text instead — sacred-texts.com's
    per-work index pages don't reliably map to contiguous page-number ranges within a
    compilation volume.
- Scoping/docs: README (research question, label scheme, feature plan, repo layout),
  `docs/data-sources.md` (full sourcing research and per-corpus license status).

## Open questions / blockers

- None blocking. Known caveat: Bahman Yasht (4 pages, 3 chapters) is much shorter than the
  other two transfer corpora — worth watching for whether it gives the classifier enough
  signal to evaluate transfer meaningfully on its own.

## Next up

- Build the hand-labeled seed set (verse/pericope-level, three classes: prophetic /
  narrative / law-wisdom) per the README's label scheme — this is the next unstarted piece
  of the v1 pipeline, ahead of feature extraction and the classifier itself.
