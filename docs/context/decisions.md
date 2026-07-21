# Decision Log

Running log of notable decisions made on this project — what was decided, why, and what
alternatives were considered. Newest entries at the top.

---

## 2026-07-21 — Classifier: reported an inconclusive transfer result honestly rather than reframing it

**Decision:** `src/train_classifier.py` trains logistic regression (selected over linear
SVM by 5-fold CV macro-F1) on the full 129-column feature set and applies it as-is to the
transfer corpora, rather than narrowing to a smaller register-specific feature subset
before reporting results. The transfer result — none of the three transfer corpora came
back majority-prophetic, contrary to how heavily oracular their source material is
described as being in `docs/data-sources.md` — is written up in `docs/classifier.md` as
inconclusive, with three named candidate explanations (translator-era vocabulary vs. genre,
seed-vs-transfer chunking mismatch, small/high-dimensional training set), rather than
picked apart until it produces a cleaner-looking number.

**Why:** The README frames both outcomes as informative ("If it transfers... If it
doesn't... that's informative too") specifically to avoid pressure toward one answer. The
model's own feature importances handed over more direct evidence than expected for one of
the three candidate confounds: top coefficients for narrative include `fw_her`/`fw_she`,
which checking against the seed set showed are concentrated almost entirely in Ruth and the
Hagar passages — i.e. "is this passage about a woman," not "is this narrative register."
With 345 seed rows and 129 features that's a real overfitting risk, not a hypothetical, and
reporting the transfer numbers without that caveat attached would have been misleading
regardless of which way the numbers came out.

**Alternatives considered:** Narrowing to a smaller, more deliberately register-specific
feature subset (just `divine_speech_formula`, `second_person_density`, `future_modal_density`,
etc.) before running the transfer evaluation, to get a cleaner signal (deferred, not
rejected — flagged as the most likely next step in `docs/classifier.md`, but doing it now
would have meant retroactively picking the feature set to fit a hoped-for transfer result
rather than reporting what the originally-planned full feature set actually produced first).
Suppressing or downplaying the `fw_her`/`fw_she` finding since it complicates the narrative
(rejected outright — it's exactly the kind of caveat the project's own scope-boundary
principle, see `docs/study-notes/README.md`, exists to keep visible).

---

## 2026-07-21 — Added Sinai theophany, split prophetic/law-wisdom within-scene (not narrative/prophetic)

**Decision:** Added Exodus 19:16-20 (narrative), Exodus 20:1-2 (prophetic), Exodus 20:3-17
(law-wisdom), and Micah 1:3-4 (prophetic) to `src/build_seed_set.py`'s reference list. Wrote
up the episode in `docs/study-notes/sinai.md`.

**Why:** The angel-of-the-LORD scenes added earlier the same day all split narrative from
prophetic. Sinai is a different, arguably more useful case: it's the seed set's only
unmediated theophany (no angel — "God spake all these words" directly), and its content
splits cleanly across the *other* boundary this project's own feature-extraction findings
flagged as blurry — prophetic vs. law-wisdom, since both use commanding-voice address. That
made Sinai worth deliberately hunting for as a targeted test, not just another
narrative/prophetic pair. Result confirmed the hypothesis: re-ran feature extraction and the
Decalogue's commandments (20:3-17) turned out to have the single highest
`second_person_density` of any passage in the whole seed set (up to 250 per 1000 words on
"Thou shalt not..." verses) — direct evidence that the earlier-noted prophetic/law-wisdom
overlap traces back to a real shared origin, not a modeling artifact. Micah 1:3-4 was added
alongside as a second data point: prophetic material that reuses Sinai's storm-theophany
imagery in the third person ("the LORD cometh forth") rather than direct second-person
address, which is a different shape of "prophetic register" than most of the seed set's
other entries and worth remembering once feature weighting starts.

**Alternatives considered:** Treating the Decalogue as a single prophetic-class block since
it's introduced by divine speech (rejected — the content shift at 20:3 from
self-declaration to commandment is exactly the kind of verse-level genre seam the README's
labeling unit exists to catch; lumping it as one block would have hidden the finding rather
than revealing it). Adding more of the Sinai-echo passages found in research (Habakkuk 3,
Judges 5:4-5, Psalm 68:7-8) directly to the seed set (deferred — kept as background in
`docs/study-notes/sinai.md` instead, to avoid scope creep on a single case study; can be
added later if the prophetic class needs more third-person-theophany examples).

---

## 2026-07-21 — Added angel-of-the-LORD theophanies, split narrative/prophetic within-scene; reversed the Genesis 22 exclusion

**Decision:** Added seven angel-of-the-LORD scenes to `src/build_seed_set.py`'s reference
list (Genesis 16 & 22, Exodus 3, Judges 6 & 13), each split into a narrative-class range
(the angel appearing/acting) and a prophetic-class range (the angel's first-person divine
speech) from the same passage. This reverses part of the 2026-07-20 Genesis-22 call:
`docs/seed-set.md` originally excluded Genesis 22 (the Akedah) entirely, reasoning the
divine-oath verses were "hard to excise cleanly from the narrative frame" — but verses
16-18 ("By myself have I sworn, saith the LORD...") turned out to excise cleanly once
specifically targeted for this purpose.

**Why:** These theophany scenes are a natural, textually-motivated test of the README's
core labeling-unit rule (verse-level granularity because narrative chapters can contain
embedded oracles) — same scene, same characters, only the speech-act changes between
narrative and prophetic halves. Ran feature extraction on the split and it validated the
approach: in every multi-verse episode, the "speaks" half scores higher on
`second_person_density` and `future_modal_density` than the "appears/acts" half of the same
scene, and Genesis 22:16 fires `divine_speech_formula` — the only non-prophetic-book verse
in the set to do so. Full detail in `docs/study-notes/angel-of-the-lord.md`.

**Alternatives considered:** Leaving Genesis 22 excluded per the original call (rejected —
the new evidence directly contradicts the original reasoning for verses 16-18 specifically,
even though verses 12-14 are correctly still excluded). Including all 52 angel-of-the-LORD
verses found across the OT (rejected — seven episodes were enough to make the
narrative/prophetic-split point without ballooning the seed set; the other 45 largely
repeat the same pattern, e.g. Numbers 22's Balaam's-ass episode, and can be added later if
the seed set needs more prophetic volume).

---

## 2026-07-21 — Feature extraction: regex features over spaCy where the tagger disagrees with itself

**Decision:** `src/extract_features.py`'s prophetic-specific features (divine-speech
formula, second-person density, vocative density, future-modal density) are all
regex-based, not POS/dependency-based, even though a POS tagger (spaCy `en_core_web_sm`)
is used elsewhere in the same script for the general-stylometric POS-distribution
features. `imperative_density` uses a POS-based heuristic (bare-infinitive-form verb as
the first token of a sentence) instead of checking for `Mood=Imp` directly.

**Why:** Tested spaCy directly on KJV text ("Hear, O heavens, and give ear, O earth.") and
found `en_core_web_sm` never emits `Mood=Imp` for English at all — imperative and bare
infinitive share a surface form and the model doesn't disambiguate them, so a
`Mood=Imp`-based feature would be silently zero for every row (confirmed: it was, before
the heuristic replaced it). Separately, the tagger visibly mis-tags archaic KJV
constructions even on non-imperative text (e.g. "saith" as `ADP`), which pushed the
prophetic-specific features toward regex where a clean literal pattern was available
("thus saith the LORD", thou/thee/thy/ye/you, "O <Name>", shall/will) rather than trusting
the tagger's judgment calls.

**Alternatives considered:** A better-suited tagger/model for Early Modern English
(rejected for now — added complexity not justified before the classifier itself exists;
worth revisiting if POS features turn out to matter once the classifier is trained).
Dropping `imperative_density` entirely rather than using a heuristic (rejected — the
heuristic produces a feature that behaves sensibly against the seed set's three classes,
see `docs/features.md`, so it's more useful kept-and-flagged-as-approximate than dropped).

---

## 2026-07-21 — Added Jude 1:14-15 to the prophetic seed class after finding it quotes 1 Enoch 1:9

**Decision:** Added `Jude 1:14-15` to the prophetic class in `src/build_seed_set.py`'s
reference list, and wrote up the full canonical Enoch record in
`docs/study-notes/enoch.md`.

**Why:** While researching every canonical mention of Enoch (Genesis 5, Luke 3, Hebrews
11, Jude 1) for `docs/seed-set.md`'s Enoch note, found that Jude 1:14-15 is a near-verbatim
quotation of 1 Enoch 1:9 (`data/transfer/1_enoch.txt` lines 56-74) — and Jude explicitly
calls it "prophesied." That makes it a controlled anchor point: a seed-set verse and a
transfer-corpus verse that are (near-)identical text, where the prophetic-register label
isn't this project's own editorial judgment call like every other seed-set entry, but the
canon's. Worth having in the seed set specifically so later feature/classifier analysis can
check whether the trained model's score on this pair lines up with the ancient judgment
that they're the same genre.

**Alternatives considered:** Leaving it out as NT material when the rest of the prophetic
class is OT (Isaiah/Jeremiah/Ezekiel/Minor Prophets/Daniel/Psalms) — rejected; the
1-Enoch-quotation link is too directly relevant to the project's transfer-test design to
skip over for genre-of-book consistency alone.

---

## 2026-07-21 — Seed set built as a hardcoded reference list, not a programmatic genre pass over full books

**Decision:** `src/build_seed_set.py` pulls verse ranges from an explicit, hand-picked
`REFERENCES` list (book/chapter/verse-range/label) rather than labeling entire chapters or
books wholesale. 291 verses total (105 prophetic, 113 narrative, 73 law-wisdom). Full
rationale per passage is in `docs/seed-set.md`.

**Why:** The README's labeling unit is verse/pericope level specifically because genre
shifts within chapters — a narrative chapter can contain an embedded oracle. A programmatic
whole-book pass (e.g. "everything in Isaiah is prophetic") would mislabel narrative framing
verses inside prophetic books and oracle verses inside narrative books. Hand-picking ranges
per passage was the only way to honor that.

**Alternatives considered:** Labeling at chapter granularity (rejected — same
content-conflation problem the README already called out). Crowdsourcing or reusing an
existing genre outline (rejected earlier, in `docs/data-sources.md` — no existing
genre-tagged dataset was found, and the README explicitly avoids copyrighted genre
outlines).

---

## 2026-07-20 — Bahman Yasht page range: 4 pages (Observations + Ch. I–III), not the initially assumed 12

**Decision:** Scraped `sbe0556.htm`–`sbe0559.htm` from sacred-texts.com's SBE vol. 5 as the
Bahman Yasht text, after the first attempt (`sbe0544.htm`–`sbe0555.htm`, guessed from the
volume's chapter-count pattern) turned out to be the adjacent "Selections of Zâd-sparam"
text instead.

**Why:** SBE vol. 5 bundles four separate Pahlavi works (Bundahishn selections, Selections
of Zâd-sparam, Bahman Yasht, Shâyast lâ-Shâyast) back-to-back with continuous page numbering
and no machine-readable per-work TOC — the index page lists chapter labels ("Chapter I",
"Chapter II", ...) that reset per work, so a numeric page range can't be inferred from the
index alone. Confirmed the correct range by fetching individual page `<title>` tags (which
do carry the work name, e.g. "Bahman Yasht: Observations") until the boundary was found.

**Alternatives considered:** Trusting the chapter-count pattern from the surrounding TOC
list (rejected — that's exactly what produced the wrong range the first time).

---

## 2026-07-20 — sacred-texts.com scraping: browser User-Agent + 2s delay, not a bare `requests.get` loop

**Decision:** `src/setup_data.py` impersonates a browser User-Agent and spaces requests 2
seconds apart, with retry/backoff on non-200 responses.

**Why:** sacred-texts.com 403s the default `requests` User-Agent outright, and separately
throttles bursts of same-IP requests behind a Cloudflare challenge page (observed directly:
a tight loop of ~13 requests with only a 1.5s gap and no UA got blocked mid-run). A 2s gap
with a browser UA fetched all 133 pages across the three corpora without a single retry.

**Alternatives considered:** No delay (rejected — triggers Cloudflare's challenge page,
observed empirically during setup). Browser automation (Selenium/Playwright) to clear a JS
challenge — not needed once the UA + pacing fix alone proved sufficient.

---

## 2026-07-20 — Added `docs/context/` for decision log and status tracking

**Decision:** Track decision logs and current status in `docs/context/`, following the same
convention already used in the related `kjv-stylometry-repo` project.

**Why:** This content should be version-controlled with the code it explains, and keeping
the same file layout (`status.md` + `decisions.md`) as the sibling repo makes both projects
easy to navigate the same way.

**Alternatives considered:** Storing context files outside the git repo — rejected because
it wouldn't be tracked in history alongside the code changes it documents.

---

<!--
Template for new entries:

## YYYY-MM-DD — Short title

**Decision:** What was decided.

**Why:** The reasoning or constraint that drove it.

**Alternatives considered:** What else was on the table and why it was passed over.
-->
