# The angel of the LORD: seed-set case study and background

`data/Bible-kjv/` has 52 OT verses (Genesis through Zechariah, KJV) using
the phrase "angel of the LORD" or "angel of God." Seven episodes were
selected for the seed set — not for volume, but because each one is a
single narrative scene that splits cleanly into a *narrative* half (the
angel appears, acts, or is addressed) and a *prophetic* half (the angel
speaks, in first person, as God) — which is exactly the situation the
README's labeling-unit rule exists for: "a narrative chapter can contain an
embedded oracle... labels need to be fine-grained enough to not conflate
the two." These pairs make that rule testable directly, verse by verse,
within one continuous scene rather than across different books.

## The seven episodes now in the seed set

| Episode | Narrative half | Prophetic half |
|---|---|---|
| Hagar at the well (Genesis 16) | 16:7-8 angel finds her; 16:13 she names God | 16:9-12 birth-oracle: "I will multiply thy seed... call his name Ishmael" |
| The Akedah, second call (Genesis 22) | 22:11 "Abraham, Abraham" — bare address | 22:16-18 "By myself have I sworn, **saith the LORD**..." — covenant oracle |
| The burning bush (Exodus 3) | 3:2-3 angel appears in flame; Moses turns aside | 3:4-6 "I am the God of thy father..." — self-revelation |
| Gideon's call (Judges 6) | 6:11-13 angel sits under the oak; Gideon's skeptical reply | 6:14, 16, 23 "Go in this thy might... Surely I will be with thee... Peace be unto thee" |
| Samson's birth (Judges 13) | 13:19-21 angel ascends in the altar flame, no speech | 13:3-5 birth-oracle: "thou shalt conceive and bear a son... a Nazarite unto God" |

Genesis 22 is worth flagging: `docs/seed-set.md`'s original note said the
whole chapter was left out of the seed set because "the climactic
divine-oath verses are hard to excise cleanly from the narrative frame."
On a second pass specifically hunting for angel-of-the-LORD material, that
turned out to be wrong for verses 16-18 — the "By myself have I sworn,
saith the LORD" wording gives a clean seam right at verse 16. Verses 12-14
(command, ram, place-naming) are still genuinely narrative/instructional
and stay out. Recorded as a correction, not a re-derivation, in
`docs/context/decisions.md`.

## What the numbers show (results/seed_set_features.csv)

Pulled straight from the feature-extraction run: in every one of the five
episodes, the "angel speaks" verses score higher on `second_person_density`
and `future_modal_density` than the "angel appears/acts" verses from the
same scene — several of the narrative-half verses score exactly 0 on both.
Genesis 22:16 is the only verse in this whole set (besides the existing
Jeremiah/Ezekiel/Isaiah entries) that fires `divine_speech_formula` — the
literal "saith the LORD" is caught by the same regex built for the OT
prophetic-book formula, even though this verse comes from Genesis, not one
of the prophetic books. That's a genuinely useful cross-check: the
divine-speech-formula feature isn't keying on "which book this verse is
from," it's catching the actual formula wherever it appears.

## Background: who (or what) is "the angel of the LORD"?

Not treated uniformly across the OT — and part of what makes it
interesting. In several of these scenes the text switches, mid-passage,
between calling the speaker "the angel of the LORD" and simply "the LORD":
Genesis 16:13 has Hagar name *the LORD* as the one who spoke to her, even
though every verse before it says "the angel of the LORD" spoke; Judges
6:14 switches from "the angel of the LORD appeared... and said" (v.12) to
"the LORD looked upon him, and said" (v.14) without narrative comment;
Exodus 3:2 says the angel appeared in the fire, but verse 4 has *God*
calling out from the bush. The text doesn't treat this as a contradiction
needing explanation — the angel of the LORD speaks with unqualified
first-person divine authority ("I will multiply thy seed," "I am the God
of thy father"), which ordinary angels elsewhere in scripture explicitly
refuse to accept (e.g. Revelation 22:8-9, an angel stopping John from
worshipping it). That's why this figure has drawn a long line of
theological reflection — many Christian readers (patristic through modern)
read "the angel of the LORD" as a pre-incarnate appearance of the Son,
precisely because he speaks and is worshipped as God while still being
called "the angel of the LORD" and, in Genesis 18-19 and Joshua 5:13-15,
appears to be met and addressed in ways later distinguished from ordinary
angelic messengers. That's a theological reading, not something this
project's stylometric method can adjudicate — but it's the reason these
scenes read the way they do: the narrative frame keeps the messenger
grammatically distinct from God, while the speech content doesn't.
