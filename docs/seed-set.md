# Seed set: reference list and rationale

`data/seed_set.csv` (321 verses: 123 prophetic, 125 narrative, 73 law-wisdom)
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

## Known gaps / things to revisit

- No verses yet from Chronicles' genealogies, Numbers, or Deuteronomy law
  material — could round out law-wisdom if the class needs more volume.
- Ezekiel 37 and Jeremiah 1 both have a first-person narrative frame around
  the oracle core ("the word of the LORD came unto me, saying..."). Left
  labeled prophetic since the oracle content dominates the verse range
  chosen, but worth watching in feature analysis — this is exactly the kind
  of "prophetic register embedded in narrative frame" case the README flags
  as needing verse-level granularity.
- Class sizes aren't balanced (123 / 125 / 73) — fine for a seed set, but
  worth stratifying or weighting once the classifier is trained.
