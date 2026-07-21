# Current Status

Snapshot of where the project stands. Update this as work progresses — it should always
reflect the current state, not a history (see `decisions.md` for the log of past decisions).

_Last updated: 2026-07-21_

## Summary

Stylometric classifier project: does "prophetic register" in biblical Hebrew/English text
reflect a detectable linguistic style (verb mood, address form, formulaic markers) rather
than just content, and does that style transfer to non-biblical prophetic/oracular
literature (Sibylline Oracles, 1 Enoch, Zoroastrian eschatology)? Repo scope, label scheme,
and data-sourcing plan are written up; source data for both the biblical corpus and all
three v1 transfer corpora is fetched; the hand-labeled seed set (293 verses) is built and
explored in a notebook; and feature extraction (general stylometric + prophetic-specific)
is done and run on the seed set. The classifier itself is not yet built.

## In progress

- Nothing actively in flight. Next unstarted step is the classifier (logistic
  regression / SVM per README).

## Done

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
  confirming the near-verbatim quotation from `docs/enoch-deep-dive.md`).

- Seed set (2026-07-21): `src/build_seed_set.py` pulls a hand-curated reference list of
  verse ranges out of `data/Bible-kjv/` into `data/seed_set.csv` (293 verses: 107
  prophetic, 113 narrative, 73 law-wisdom). Reference list and selection rationale — what
  counts as "oracle-bearing" vs. clean narrative, why certain passages were excluded — is
  in `docs/seed-set.md`. Includes Genesis 5:21-24 (Enoch) in the narrative class and Jude
  1:14-15 in the prophetic class.
- Enoch deep dive (2026-07-21): `docs/enoch-deep-dive.md` collects every canonical mention
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
