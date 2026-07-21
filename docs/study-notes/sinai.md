# Sinai: seed-set case study and background

The Sinai theophany (Exodus 19-20) is the third case study added to the
seed set on the same "find the seam and split at it" method as
[`enoch.md`](enoch.md) and [`angel-of-the-lord.md`](angel-of-the-lord.md) —
but where those two split *narrative* from *prophetic*, Sinai splits
*prophetic* from *law-wisdom*, which is the more interesting boundary for
this project because it's exactly the one `docs/features.md` flagged as
blurry: second-person and imperative density don't cleanly separate
prophetic oracle from legal code, because both are commanding-voice
registers. Sinai is where that overlap comes from.

## Why Sinai, specifically

Every angel-of-the-LORD scene in the seed set has an intermediary — the
text is careful to say "the angel of the LORD" spoke, even while the
speech itself carries unqualified divine authority (see
`angel-of-the-lord.md`'s discussion of that tension). Sinai has no
intermediary at all: "And God spake all these words, saying, I am the
LORD thy God, which have brought thee out of the land of Egypt" (Exodus
20:1-2) — direct address, first person, no angel, no vision-frame, nothing
standing between speaker and hearer. It's the paradigm case of unmediated
theophany, and it's also the narrative origin point of the Law itself: the
Decalogue *is* the Sinai theophany's content. Leviticus's legal code (three
of this seed set's law-wisdom passages) is downstream of this same event.

## What's now in the seed set

| Ref | Class | Why |
|---|---|---|
| Exodus 19:16-20 | narrative | Thunder, thick cloud, trumpet, quaking mountain — pure scene-setting, no direct speech to the people yet. |
| Exodus 20:1-2 | prophetic | "I am the LORD thy God, which have brought thee..." — divine self-declaration, same self-revelation pattern as Exodus 3:6 (the burning bush, already in the seed set). |
| Exodus 20:3-17 | law-wisdom | The Ten Commandments proper — legal content, split from the divine-speech opening at the exact seam where content shifts from who-is-speaking to what-is-commanded. |
| Micah 1:3-4 | prophetic | "The LORD cometh forth out of his place... the mountains shall be molten under him" — Sinai's storm-theophany imagery reused two thousand years later as prophetic judgment poetry. |

## What the numbers show

Pulled from `results/seed_set_features.csv` after re-running feature
extraction on the split:

- **Exodus 19:16-20 (narrative) scores zero on every address/tense feature**
  checked — no `second_person_density`, no `future_modal_density`. It's
  the cleanest possible narrative baseline: description with no speech act
  at all.
- **Exodus 20:3-17 (the commandments) drove the law-wisdom class's average
  `second_person_density` up from 54.75 to 68.42** — several individual
  commandments ("Thou shalt not kill," "Thou shalt not steal") hit
  200-250 per 1000 words, the highest second-person scores anywhere in the
  seed set, prophetic passages included. This sharpens the finding already
  in `docs/features.md`: it's not just that law-wisdom's second-person
  density rivals prophetic's — the single most second-person-dense passage
  in the whole seed set is a legal text, not an oracle.
- **Micah 1:3-4 is a different flavor of prophetic than most of the seed
  set's other entries**: zero second-person density (it describes God in
  third person — "the LORD cometh," not "thus saith the LORD unto thee"),
  but high `future_modal_density` (43-67). Worth remembering once feature
  weighting starts: "prophetic register" isn't one shape, it's at least two
  — direct oracle-address and third-person theophany-description — and
  Sinai imagery is specifically the source of the second one recurring in
  later prophetic poetry (Habakkuk 3, Judges 5:4-5, Psalm 68:7-8 all echo
  the same storm-theophany vocabulary — mountains shaking, smoke, fire —
  outside this seed set).

## Background: Sinai in the rest of the canon

Sinai isn't a one-time event the text moves past — it gets retold and
reinterpreted repeatedly:

- **Deuteronomy 4-5** has Moses retell Sinai to the next generation, adding
  a detail Exodus doesn't state outright: "the LORD talked with you face
  to face in the mount out of the midst of the fire" (Deut 5:4), then
  immediately qualifies it — the people were too afraid to hear God
  directly and asked Moses to mediate from then on (Deut 5:25-27). Sinai is
  remembered as the one time Israel *almost* didn't need a prophet as
  go-between, and the fact that it terrified them into wanting one anyway
  is presented as the reason the office of prophet exists at all (Deut
  18:16-18 draws that line explicitly: God raises up prophets "according
  to all that thou desiredst of the LORD thy God in Horeb").
- **Hebrews 12:18-24** (NT) contrasts Sinai explicitly with "mount Sion" —
  "Ye are not come unto the mount that might be touched, and that burned
  with fire... (so terrible was the sight, that Moses said, I exceedingly
  fear and quake)... but ye are come unto mount Sion." Sinai becomes the
  literary type for law-under-terror, set against grace approached without
  the mountain's barrier.
- **Judges 5:4-5** (the Song of Deborah, one of the oldest poems in the
  Hebrew Bible) already treats Sinai as a stock image for divine
  intervention in battle: "LORD, when thou wentest out of Seir... the
  earth trembled... the mountains melted... even that Sinai" — written
  centuries before Micah, suggesting the storm-theophany vocabulary was
  already a fixed poetic convention very early, not something the classical
  prophets invented.

None of this is something the stylometric method can weigh in on — it's
included as background for anyone reading the passages, per the scope note
in `docs/study-notes/README.md`.
