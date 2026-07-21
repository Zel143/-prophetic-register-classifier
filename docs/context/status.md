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
three v1 transfer corpora is fetched, and the hand-labeled seed set (291 verses across the
three label classes) is built. Feature extraction and the classifier itself are not yet
built.

## In progress

- Nothing actively in flight. Next unstarted step is feature extraction.

## Done

- Seed set (2026-07-21): `src/build_seed_set.py` pulls a hand-curated reference list of
  verse ranges out of `data/Bible-kjv/` into `data/seed_set.csv` (291 verses: 105
  prophetic, 113 narrative, 73 law-wisdom). Reference list and selection rationale — what
  counts as "oracle-bearing" vs. clean narrative, why certain passages were excluded — is
  in `docs/seed-set.md`. Includes Genesis 5:21-24 (Enoch) in the narrative class; that doc
  also notes the thematic link between the four-verse canonical Enoch and the 1 Enoch
  transfer corpus.
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
