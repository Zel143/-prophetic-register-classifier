# Decision Log

Running log of notable decisions made on this project — what was decided, why, and what
alternatives were considered. Newest entries at the top.

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
