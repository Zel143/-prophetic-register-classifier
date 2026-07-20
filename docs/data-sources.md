# Data sourcing notes

Research conducted 2026-07-20. Re-verify licensing before any bulk
redistribution — status below reflects what was found at that time.

## Biblical text

- **KJV** — public domain (English). Reuse `aruljohn/Bible-kjv` JSON, same
  source as `kjv-stylometry-repo/data/Bible-kjv` (gitignored, cloned via
  setup script, not vendored — see that repo's `.gitignore` convention).

## Comparison / transfer-test corpora

### Sibylline Oracles — READY
- Translation: Milton S. Terry, 1890. Public domain.
- Source: https://sacred-texts.com/cla/sib/index.htm (HTML) and
  https://sacred-texts.com/cla/sib/sib.pdf
- Mirror: https://archive.org/stream/sibyllineoracle00terrgoog/sibyllineoracle00terrgoog_djvu.txt
- Format: clean HTML / plain-text djvu, easy to scrape.
- Content: almost entirely oracular/eschatological verse — ideal
  high-signal transfer set, minimal pre-filtering needed.

### 1 Enoch — READY
- Translation: R.H. Charles, 1913 (Oxford). Public domain.
- Source: https://sacred-texts.com/bib/boe/index.htm and
  https://en.wikisource.org/wiki/The_Book_of_Enoch_(Charles)
- Format: clean HTML / wikitext.
- Content: heavily apocalyptic/prophetic throughout.

### Testaments of the Twelve Patriarchs — READY (mixed genre)
- Translation: R.H. Charles. Public domain.
- Source: https://sacred-texts.com/bib/fbe/fbe266.htm and
  https://www.earlychristianwritings.com/text/patriarchs-charles.html
- Content: mixes ethical-narrative framing with embedded oracular
  predictions per testament — needs pre-filtering to isolate the
  oracular sections if used.

### 4 Ezra / 2 Baruch — PARTIAL, not used in v1
- No complete freely-licensed English edition readily available; 2 Baruch
  survives only in Syriac and most accessible translations are modern and
  copyrighted. Revisit later if needed.

### Bahman Yasht (Zoroastrian eschatology) — READY
- Translation: E.W. West, 1897, *Sacred Books of the East* vol. 5 (Oxford).
  Public domain.
- Source: https://sacred-texts.com/zor/sbe05/sbe0506.htm ff., mirrored at
  http://www.avesta.org/mp/vohuman.html
- Format: clean HTML.
- Content: explicitly framed as prophecy (Ahura Mazda foretelling the
  future to Zoroaster) — near-pure signal.

### Sefaria (Talmud / Midrash messianic material) — USABLE, license-gated
- Source: https://github.com/Sefaria/Sefaria-Export (also public GCS
  bucket) and REST API at https://developers.sefaria.org/
- Format: structured JSON, machine-ready.
- **License is per-document, not blanket.** Many translations are CC-BY or
  CC0 (including Sefaria's own Talmud translation); some included modern
  translations (certain JPS or named-scholar editions) retain traditional
  copyright. Must check the license field per text before use — see
  https://help.sefaria.org/hc/en-us/articles/18490043237148
- Target passage: Sanhedrin 90a-99a (messianic age discussions).

### Dead Sea Scrolls — BLOCKED for v1
- All major quality English translations (Vermes; Wise/Abegg/Cook) are
  actively copyrighted. No public-domain full translation exists — the
  scrolls weren't discovered until 1947, so no pre-1928 translation exists
  either. Pirated scans exist on Internet Archive but are not license-clear
  for redistribution in a public repo.
- Options if needed later: license a translation for private local eval
  only (not committed to the repo), or drop this corpus.

### Delphic Oracle / Oracle of the Potter — WEAK, stretch goal
- No consolidated free English translation found. Delphic responses are
  scattered across copyrighted secondary scholarship (Fontenrose's
  catalogue). Oracle of the Potter has no complete freely-licensed edition.
- Feasible fallback: hand-assemble short oracle-response fragments quoted
  within Herodotus / Plutarch (both public domain, on Perseus /
  sacred-texts.com) — labor-intensive, not planned for v1.

## Existing labeled genre datasets

None found. No HuggingFace or Kaggle dataset tags biblical/religious text
by genre (prophecy/narrative/law/wisdom/etc). Existing Bible NLP datasets
(bible-nlp/biblenlp-corpus, Helsinki-NLP/bible_para) are parallel-translation
corpora, not genre-labeled. Genre labeling for this project is original
work — see the seed-set scheme in the main README.
