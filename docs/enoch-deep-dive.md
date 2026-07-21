# Enoch across the canon (and why he matters to this project)

Every verse in the Protestant canon that mentions the Enoch of Genesis 5,
pulled straight from `data/Bible-kjv/`, plus the one direct textual link to
this project's 1 Enoch transfer corpus. Kept here rather than folded into
`docs/seed-set.md` because most of it is background/study material, not
seed-set rationale — only Genesis 5:21-24 and Jude 1:14-15 actually made it
into `data/seed_set.csv`.

## There are two Enochs — don't conflate them

- **Genesis 4:17-18** — Cain's son, for whom Cain names the first city built
  in the text. A different person; the name just recurs. Not part of this
  project's Enoch.
- **Genesis 5:18-24** — Jared's son, seventh generation from Adam (Jude
  1:14 confirms the count explicitly). This is the Enoch everything below is
  about.

## The full canonical record

| Ref | What it adds |
|---|---|
| Genesis 5:21-24 | The base account: genealogical notice + "Enoch walked with God: and he was not; for God took him." No dialogue, no oracle, no first-person material at all. |
| Luke 3:37 | Places him in Jesus's genealogy (Luke traces back through Adam), confirming his position: son of Jared, father of Methuselah. Purely genealogical, adds nothing narrative. |
| Hebrews 11:5 | Retrospective theological reading: "By faith Enoch was translated that he should not see death... for before his translation he had this testimony, that he pleased God." This is the verse that turns "he was not, for God took him" into a positive claim about *faith* specifically — Genesis itself doesn't use faith-language, Hebrews supplies it. |
| Jude 1:14-15 | The big one — see below. |

That's it for the Protestant canon. Four verses of narrative, one verse of
genealogy, one verse of theological commentary, and two verses that turn
out to be a quotation from outside the canon entirely.

## Jude 1:14-15: the canon quoting 1 Enoch as prophecy

Jude 1:14-15 (KJV):
> And Enoch also, the seventh from Adam, prophesied of these, saying,
> Behold, the Lord cometh with ten thousands of his saints, To execute
> judgment upon all, and to convince all that are ungodly among them of all
> their ungodly deeds which they have ungodly committed, and of all their
> hard speeches which ungodly sinners have spoken against him.

Compare 1 Enoch 1:9 (Charles, 1913 — `data/transfer/1_enoch.txt`, lines
56-74):
> And behold! He cometh with ten thousands of His holy ones, To execute
> judgement upon all, And to destroy all the ungodly: And to convict all
> flesh Of all the works of their ungodliness which they have ungodly
> committed, And of all the hard things which ungodly sinners...

That's not an allusion, it's a quotation — close enough that most modern
translations (NIV, ESV, NASB) print it as one, and textual critics treat
Jude 14-15 as the earliest surviving witness to 1 Enoch 1:9's wording
(older than most of the Ethiopic/Aramaic manuscript tradition it's
reconstructed from). Jude's word for it is *prophesied* (Greek
*proephēteusen*) — the only place in the entire canon that the label
"prophecy" gets attached to Enoch, and it's attached to a text that isn't
in the canon.

### Why this matters for the classifier specifically

This is a rare case where the question the project is asking —
*"is prophetic register a real, transferable linguistic signal, or is it
just genre-labeling by convention?"* — has a documented ancient answer on
record. Whoever wrote Jude read 1 Enoch's judgment-oracle material and
recognized it as belonging to the same category as canonical prophecy,
enough to cite it that way to a Christian audience. That's a 1st-century
literary judgment that the register transfers — independent of, and
centuries prior to, whatever this project's classifier finds. If the
trained classifier also scores 1 Enoch 1:9-ish material as prophetic-register,
that's modern stylometry agreeing with an ancient reader's genre judgment
made on different grounds entirely. If it doesn't, that's worth sitting
with rather than dismissing as noise.

Practically: `Jude 1:14-15` is now in `data/seed_set.csv` (prophetic
class) precisely because it's a same-register anchor point sitting right
next to the 1 Enoch transfer corpus — a controlled pair where the "ground
truth" prophetic label isn't just this project's editorial call, it's the
canon's own.

## For your own study: what Enoch's four verses are doing theologically

Genesis 5 is a genealogical chain — "X lived, begat Y, lived more years,
died" — repeated for nine generations before and after Enoch, all of them
ending in "and he died." Enoch's entry breaks the pattern twice: "Enoch
walked with God" appears (the only person besides Noah, later, to get that
phrase in Genesis), and the death formula never comes. In a text built
almost entirely out of repetition, both the language change and the
structural break are load-bearing — the passage is drawing your attention
to exactly one life in a list of nine by refusing to end it the way every
other entry ends.

Hebrews 11 reads that break as a statement about faith preceding reward —
Enoch's commendation ("he pleased God") is given *before* the narrative
says what happened to him, which the author takes as proof the pleasing
came first and the translation was consequence, not achievement. It's used
in Hebrews 11 as one entry in a chain of pre-Mosaic faith examples (Abel,
Enoch, Noah, Abraham...) built to argue that relationship with God never
depended on the Law — which fits the theological point of introducing
Enoch before Sinai exists at all in the narrative.

Jude's use is different in kind: not commendation but warning — Enoch's
one preserved "saying" in the canon is a coming-judgment oracle, cited by
Jude to warn a church about false teachers. So across the only three NT
references, Enoch accumulates three separate roles — genealogical link
(Luke), faith exemplar (Hebrews), and prophetic voice (Jude) — stacked onto
a base text that, on its own, supplies none of the three explicitly. It's
a useful case study in how later tradition doesn't just preserve a figure,
it actively assigns him work to do.
