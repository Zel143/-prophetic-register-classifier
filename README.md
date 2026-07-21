# Prophetic Register Classifier

A stylometric study of "prophetic register" in biblical Hebrew/English text,
and whether that register transfers to prophetic/oracular literature outside
the biblical canon.

## Research question

Prophetic writing (oracles, judgment speech, apocalyptic vision) reads
differently from narrative, law, or wisdom text — but is that difference a
matter of *content* (what's being said) or *register* (a detectable
linguistic style: verb mood, address form, formulaic markers, structure)?

This project trains a classical ML classifier (logistic regression / SVM) on
hand-labeled biblical text to detect prophetic register from stylometric
features alone, then tests whether the classifier transfers to non-biblical
prophetic/oracular literature (Sibylline Oracles, 1 Enoch, Zoroastrian
eschatological texts). If it transfers, that's evidence "prophetic register"
is a cross-cultural genre signal, not an artifact specific to biblical
Hebrew/English. If it doesn't, that's informative too.

This is a computational-linguistics / stylometry project. It does not
attempt to evaluate, prove, or adjudicate any prophecy's fulfillment or any
tradition's theological claims — it measures textual style.

## Status

Data, seed set, feature extraction, and a classifier (evaluated three ways
— full feature set, narrowed feature set, and hand-picked pericopes) are
all in place — see `docs/context/status.md` for the current snapshot and
`docs/classifier.md` for the full methodology and results. Best result so
far: the specific 1 Enoch passage Jude 1:14-15 quotes scores 64-82%
prophetic under both models — the strongest evidence yet for transfer —
but that doesn't hold up consistently across the rest of either transfer
corpus or across feature sets, so the overall transfer question is still
open. See `docs/classifier.md` for the full accounting.

## Project scope (v1)

- **Language**: English only (KJV). Hebrew morphological features (e.g.
  parallelism detection via MACULA) are a planned v2 extension, not in v1.
- **Labeling unit**: verse/pericope level, not chapter/book level — genre
  shifts within chapters (a narrative chapter can contain an embedded
  oracle), so labels need to be fine-grained enough to not conflate the two.

## Label scheme

Three classes, hand-curated seed set (not derived from any existing
copyrighted genre outline — see [docs/data-sources.md](docs/data-sources.md)):

- **Prophetic** — oracle/judgment-speech passages: divine-speech-formula
  passages ("thus saith the LORD", "the word of the LORD came unto...") from
  Isaiah, Jeremiah, Ezekiel, and the Minor Prophets, plus the classic
  messianic prophecy set (Isaiah 53, Micah 5:2, Psalm 22, Zechariah 9:9,
  Daniel 9:24-27, etc.).
- **Narrative** — prose narrative with no embedded oracle: Ruth, Esther,
  patriarchal narrative in Genesis, historical narrative in Kings/Chronicles
  (oracle-bearing verses excluded even within narrative books).
- **Law/wisdom** — Leviticus, Proverbs. A third bucket so the classifier
  learns "prophetic vs. everything else," not just "prophecy vs. story."

## Features (planned)

**General stylometric** (reusing the approach from
[kjv-stylometry-repo](../kjv-stylometry-repo)):
- Function-word frequency ratios
- Sentence/clause length distribution
- POS n-gram frequencies
- Type-token ratio / lexical diversity

**Prophetic-register-specific** (new to this project):
- Divine-speech-formula density
- Imperative / future-tense verb density
- Second-person direct-address density
- Vocative / apostrophe frequency ("O Israel", "O daughter of Zion")
- Poetic parallelism markers (v2, Hebrew-dependent — see MACULA note above)

## Comparison / transfer-test corpora

See [docs/data-sources.md](docs/data-sources.md) for the full sourcing
research, license status, and URLs. Summary:

| Corpus | Status | Source |
|---|---|---|
| Sibylline Oracles (Terry, 1890) | Ready — public domain | sacred-texts.com |
| 1 Enoch (Charles, 1913) | Ready — public domain | sacred-texts.com / Wikisource |
| Bahman Yasht (West, 1897) | Ready — public domain | sacred-texts.com |
| Sefaria (Talmud/Midrash) | Usable, per-document license check required | Sefaria-Export (GitHub) |
| Dead Sea Scrolls | Blocked — all quality translations copyrighted | n/a |
| Delphic Oracle / Oracle of the Potter | Weak — no consolidated source, would require hand-assembly from Herodotus/Plutarch | stretch goal |

## Repo layout

```
data/           raw text (gitignored where third-party/large; small public-domain
                comparison texts may be vendored directly)
src/            feature extraction, labeling, classifier, transfer-eval scripts
notebooks/      exploratory analysis
results/        classifier metrics, figures
docs/           data-sourcing notes, seed-set definitions
```

## Related repos

- [kjv-stylometry-repo](../kjv-stylometry-repo) — NT authorship stylometry
  pipeline this project borrows conventions from (function-word list,
  chunking, PCA/permutation-test utilities).
- [macula-hebrew](../macula-hebrew) — Hebrew morphological data, planned
  source for v2 parallelism features.

## License

MIT (this repo's code). Source texts retain their own public-domain status
per translator/date — see docs/data-sources.md for per-corpus notes.
