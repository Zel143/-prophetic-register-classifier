# Study notes

Passage write-ups that grew out of building the seed set — kept separate
from the rest of `docs/` because they're a different kind of writing than
everything else in this repo. The technical docs (`docs/seed-set.md`,
`docs/features.md`, `docs/data-sources.md`) explain *engineering*
decisions: what was selected, why, what a script does. These explain the
*passages themselves* — cross-references, background, what later tradition
did with a text — for anyone reading the Bible, not just anyone reading
this codebase.

## Scope note

This project's stated scope (see the main README) is computational
linguistics: it measures textual style, and explicitly does not evaluate
or adjudicate any prophecy's fulfillment or any tradition's theological
claims. These notes sometimes go further than that — e.g. noting the
traditional reading of "the angel of the LORD" as a pre-incarnate
Christophany — because that's genuinely relevant background for a reader,
even though it's not something the stylometric method could ever confirm
or deny. Treat that distinction as live throughout: passage background and
cross-references are one kind of claim, "the classifier detected X" is a
different kind, and these notes try to keep the two visibly apart rather
than letting one borrow the other's authority.

## Index

- [`enoch.md`](enoch.md) — every canonical mention of Enoch (Genesis 4 vs.
  5 — two different people; Luke 3; Hebrews 11; Jude 1), and the discovery
  that Jude 1:14-15 is a near-verbatim quotation of 1 Enoch 1:9, explicitly
  called "prophesied."
- [`angel-of-the-lord.md`](angel-of-the-lord.md) — the seven angel-of-the-LORD
  theophanies in the seed set (Hagar, the Akedah, the burning bush, Gideon,
  Samson's birth), plus background on why the angel of the LORD sometimes
  speaks and is addressed with unqualified divine authority.

Both files started as answers to specific questions asked mid-project (what
does the rest of the canon say about Enoch; what about the angel-of-the-LORD
verses) and turned out to double as real seed-set design work — see each
file's connection back to `docs/seed-set.md` for how.
