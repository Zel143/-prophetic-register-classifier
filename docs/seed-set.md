# Seed set: reference list and rationale

`data/seed_set.csv` (510 verses: 184 prophetic, 180 narrative, 146 law-wisdom)
is built by `src/build_seed_set.py` from the reference list hardcoded in
that script. This doc explains the selection criteria and flags the
judgment calls, so the list can be revised without re-deriving the reasoning
from scratch.

## Selection criteria

- **Prophetic** — passages built around a divine-speech formula ("thus
  saith the LORD", "the word of the LORD came unto...") or the classic
  messianic-prophecy set named in the README. Drawn from Isaiah, Jeremiah,
  Ezekiel, the Minor Prophets, Daniel 9, Psalm 22 (messianic psalm,
  included even though Psalms as a book is mixed-genre), Jude 1:14-15
  (NT, explicitly labeled "prophesied" — see the Enoch section below), and
  seven angel-of-the-LORD theophany passages (see
  `docs/study-notes/angel-of-the-lord.md`) — the speech half of scenes where the angel
  talks in God's first person.
- **Narrative** — prose narrative with no embedded oracle verse. Passages
  were chosen specifically to *exclude* direct divine speech even when the
  surrounding chapter contains it — e.g. Genesis 12:1-9 stops short of
  isolating Abram's call-oracle wording as its own narrative unit is thin
  around it. Genesis 22 (Isaac's binding) was originally left out entirely
  for this reason too, but revisited once angel-of-the-LORD passages were
  being hunted specifically: verses 16-18 ("saith the LORD...") turned out
  to excise cleanly after all — see `docs/study-notes/angel-of-the-lord.md` and the
  2026-07-21 decisions.md entry. Verses 12-14 (command, ram, place-naming)
  are still genuinely narrative/instructional and remain excluded.
- **Law/wisdom** — Leviticus (legal code) and Proverbs (wisdom sayings), per
  the README's third-bucket rationale (so the classifier learns "prophetic
  vs. everything else," not just "prophecy vs. story").

## Angel-of-the-LORD theophanies (Hagar, Akedah, burning bush, Gideon, Samson's birth)

Seven scenes (Genesis 16 & 22, Exodus 3, Judges 6 & 13) where the angel of
the LORD appears in a narrative frame and then speaks, in first person, as
God. Each scene is split at the seam between the two: appearance/action
verses go to narrative, first-person-divine-speech verses go to prophetic.
Full rationale, the per-episode table, and what the extracted features show
for these pairs (the "speaks" half consistently scores higher on
second-person and future-modal density than the "appears/acts" half from
the same scene) are in `docs/study-notes/angel-of-the-lord.md`.

## Genesis 5:21-24 — Enoch

Included in the narrative set as the full canonical text about Enoch: four
verses, genealogical in form, no direct speech at all ("Enoch walked with
God: and he was not; for God took him."). Stylistically it's about as
minimal-narrative as the Bible gets — which makes it a useful low end of the
narrative-register range for the classifier to learn from.

It's also the reason 1 Enoch (Charles, 1913) is one of the three v1 transfer
corpora (see README's comparison-corpora table): pseudepigraphal tradition
took this four-verse fragment — a man who "walked with God" and was taken
rather than dying — and built an entire apocalyptic literature around it as
the visionary who saw the divine council, the fallen Watchers, and the end
of days. That expansion is a striking case of a genre (apocalyptic/prophetic
vision) being retrojected onto a figure the canonical text gives almost no
narrative content to. It's not something this project's stylometric method
measures directly, but it's the thread connecting the Genesis label (a
narrative-class data point) to a transfer-test corpus that's almost pure
prophetic register.

See `docs/study-notes/enoch.md` for the full canonical record (Genesis, Luke,
Hebrews, Jude) and, specifically, why Jude 1:14-15 — now also in the seed
set, prophetic class — is a near-verbatim quotation of 1 Enoch 1:9. That
pairing is a controlled anchor point between the biblical seed set and the
1 Enoch transfer corpus: unlike every other prophetic/narrative split in
this seed set, that one's "ground truth" isn't this project's editorial
call, it's the canon's own (Jude explicitly calls it "prophesied").

## Sinai (Exodus 19-20) — the prophetic/law-wisdom boundary

The Sinai theophany is the un-mediated counterpart to the angel-of-the-LORD
scenes above (no angelic intermediary), and it's split differently: not
narrative/prophetic, but prophetic/law-wisdom — the divine self-declaration
opening the Decalogue ("I am the LORD thy God...", Exodus 20:1-2) is
prophetic class, the commandments themselves (20:3-17) are law-wisdom.
That split is the seed set's clearest illustration of where the
prophetic/law-wisdom feature overlap noted in `docs/features.md` actually
comes from — see `docs/study-notes/sinai.md` for the full rationale and
what the extracted features show (the commandments turned out to have the
single highest second-person density of any passage in the seed set).
Also added: Micah 1:3-4, a later prophetic passage that reuses Sinai's
storm-theophany imagery as judgment poetry.

## 2026-07-22 growth pass (345 → 510 verses)

Grew all three classes at once, per `docs/classifier.md`'s conclusion that
345 rows was thin for 24+ features. Selection targeted this doc's own
known-gaps list plus a few deliberate methodological anchors:

- **Prophetic (+57):** more oracle *variety*, not just more volume — woe
  oracles (Isaiah 5:8-15, same woe-series form as 1 Enoch 94-96's "Woes for
  the Sinners" transfer pericope; Amos 5:18-24), a comfort oracle (Isaiah
  40:1-8), first-person divine retrospective (Hosea 11:1-4), the new
  covenant oracle (Jeremiah 31:31-34), the shepherd oracle (Ezekiel
  34:11-16), third-person theophany poetry (Nahum 1:2-8, rounding out the
  shape Micah 1:3-4 represents), day-of-the-LORD material (Obadiah
  1:15-18, Haggai 2:6-9), and NT apocalyptic (Revelation 18:4-8, chosen
  deliberately to mirror the Sibylline Oracles "Woe on Babylon" transfer
  pericope). Revelation 18 also personifies Babylon as a woman —
  her/she-dense *prophetic* text that directly counterweights the
  fw_her/fw_she-implies-narrative artifact found in the first classifier
  pass (and indeed, after this growth pass those columns dropped out of
  the full model's top coefficients entirely).
- **Narrative (+50):** patriarchal (Genesis 29:1-10, 41:37-43), exodus-era
  (Exodus 2:1-10), action (1 Samuel 17:48-51 — David felling Goliath,
  ranges chosen to exclude the taunt-speeches at 45-47), first-person
  memoir (Nehemiah 2:11-16, a narrator style the set didn't have), and NT
  narrative (Luke 2:1-7, Acts 27:39-44) so the NT isn't represented only
  by prophetic-class Jude/Revelation. All exclude embedded divine speech.
- **Law-wisdom (+58):** fills the Deuteronomy/Numbers gap (Deuteronomy
  6:4-9 — the Shema, a deliberate boundary case like the Decalogue:
  preached law with vocative and dense second person; Deuteronomy
  24:10-15; Leviticus 25:1-7; Numbers 15:37-41, whose closing "I am the
  LORD your God" refrain follows the Leviticus 19 precedent of keeping
  refrain-bearing law verses in law-wisdom), plus more wisdom volume
  (Proverbs 10:1-12, 15:1-7; Ecclesiastes 3:1-8, 12:1-7).

Class balance improved from 127/130/88 to 184/180/146.

## Known gaps / things to revisit

- Ezekiel 37 and Jeremiah 1 both have a first-person narrative frame around
  the oracle core ("the word of the LORD came unto me, saying..."). Left
  labeled prophetic since the oracle content dominates the verse range
  chosen, but worth watching in feature analysis — this is exactly the kind
  of "prophetic register embedded in narrative frame" case the README flags
  as needing verse-level granularity.
- Still no Chronicles genealogies (as a distinct low-end narrative style) or
  Job material (wisdom dialogue has a different shape than Proverbs'
  sayings) — candidates for a future pass.
- Class sizes are closer but still not equal (184 / 180 / 146) — fine for a
  seed set; worth stratifying or weighting if it starts to matter.
