"""
Builds the hand-labeled seed set: pulls verse ranges named in REFERENCES
below out of the KJV JSON (data/Bible-kjv/) and writes them to
data/seed_set.csv with one row per verse.

The reference list itself is the actual editorial work of this step (which
passages count as prophetic/narrative/law-wisdom) — see docs/seed-set.md for
the full rationale per passage. This script is just the mechanical pull.

Usage:
    python src/build_seed_set.py
"""
import csv
import json
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KJV_DIR = os.path.join(REPO_ROOT, "data", "Bible-kjv")
OUT_PATH = os.path.join(REPO_ROOT, "data", "seed_set.csv")

# Each entry: (book, chapter, verse_start, verse_end, note).
# note is a short human-readable label for what the passage is / why it's
# included — carried into the CSV so the seed set is self-documenting
# without a separate lookup into docs/seed-set.md.
REFERENCES = {
    "prophetic": [
        ("Isaiah", 1, 2, 4, "opening oracle, divine-speech formula"),
        ("Isaiah", 6, 9, 13, "call vision"),
        ("Isaiah", 53, 1, 12, "messianic prophecy"),
        ("Jeremiah", 1, 4, 10, "prophetic call, divine speech"),
        ("Jeremiah", 7, 1, 11, "temple sermon, 'thus saith the LORD'"),
        ("Ezekiel", 2, 1, 7, "call, 'thus saith the Lord GOD'"),
        ("Ezekiel", 37, 1, 14, "valley of dry bones oracle"),
        ("Amos", 1, 3, 5, "'for three transgressions' judgment oracle"),
        ("Micah", 5, 2, 4, "messianic prophecy (Bethlehem)"),
        ("Joel", 2, 28, 32, "'I will pour out my spirit' oracle"),
        ("Zephaniah", 1, 14, 18, "day-of-the-LORD oracle"),
        ("Habakkuk", 2, 2, 4, "'write the vision' oracle"),
        ("Zechariah", 9, 9, 10, "messianic prophecy (triumphant king)"),
        ("Malachi", 3, 1, 3, "messenger oracle"),
        ("Daniel", 9, 24, 27, "seventy weeks prophecy"),
        ("Psalms", 22, 1, 18, "messianic psalm"),
        ("Jude", 1, 14, 15, "Enoch's judgment oracle, explicitly framed as prophecy; near-verbatim quote of 1 Enoch 1:9"),
        # Angel-of-the-LORD theophanies: in each case the angel's own speech
        # (first-person divine voice) is split out from the surrounding
        # narrative frame below, per the README's "oracle-bearing verses
        # excluded even within narrative books" rule.
        ("Genesis", 16, 9, 12, "angel of the LORD's birth-oracle to Hagar (Ishmael)"),
        ("Genesis", 22, 16, 18, "angel of the LORD: 'saith the LORD' covenant/blessing oracle to Abraham"),
        ("Exodus", 3, 4, 6, "burning bush: divine self-revelation to Moses"),
        ("Judges", 6, 14, 14, "angel of the LORD commissions Gideon: 'Go in this thy might'"),
        ("Judges", 6, 16, 16, "angel of the LORD to Gideon: 'Surely I will be with thee'"),
        ("Judges", 6, 23, 23, "angel of the LORD to Gideon: 'Peace be unto thee; fear not'"),
        ("Judges", 13, 3, 5, "angel of the LORD's birth-oracle to Manoah's wife (Samson)"),
        # Sinai: the un-mediated counterpart to the angel-of-the-LORD scenes
        # above (no angelic intermediary), and the source of the
        # prophetic/law-wisdom boundary case flagged in docs/features.md --
        # split at the seam between the divine self-declaration and the
        # commandments proper. See docs/study-notes/sinai.md.
        ("Exodus", 20, 1, 2, "Sinai: divine self-declaration opening the Decalogue, 'I am the LORD thy God'"),
        ("Micah", 1, 3, 4, "Sinai-theophany imagery reused as judgment oracle: 'the LORD cometh forth... mountains molten'"),
    ],
    "narrative": [
        ("Genesis", 5, 21, 24, "Enoch: 'walked with God ... and he was not'"),
        ("Genesis", 12, 1, 9, "Abram's call and journey (narrated, not the oracle verses)"),
        ("Genesis", 24, 15, 27, "Isaac and Rebekah at the well"),
        ("Genesis", 37, 23, 28, "Joseph sold into slavery"),
        ("Genesis", 16, 7, 8, "angel of the LORD finds Hagar (narrative frame, no oracle yet)"),
        ("Genesis", 16, 13, 13, "Hagar names God (narrative resolution)"),
        ("Genesis", 22, 11, 11, "angel of the LORD calls 'Abraham, Abraham' (bare address, no oracle content)"),
        ("Exodus", 3, 2, 3, "angel of the LORD appears in the burning bush (narrative frame)"),
        ("Judges", 6, 11, 13, "angel of the LORD sits under the oak; Gideon's skeptical reply"),
        ("Judges", 13, 19, 21, "angel of the LORD ascends in the altar flame (narrative, no speech)"),
        ("Exodus", 19, 16, 20, "Sinai theophany: thunder, cloud, trumpet, quaking mountain (narrative frame, no direct speech to the people yet)"),
        ("Ruth", 1, 1, 18, "Ruth and Naomi"),
        ("Ruth", 4, 9, 17, "Boaz redeems Ruth"),
        ("Esther", 2, 15, 18, "Esther made queen"),
        ("Esther", 7, 1, 10, "Haman's downfall"),
        ("1 Kings", 3, 16, 28, "Solomon's judgment"),
        ("2 Kings", 5, 1, 14, "Naaman healed"),
        ("2 Chronicles", 34, 1, 13, "Josiah's reforms (narrated account)"),
    ],
    "law-wisdom": [
        ("Exodus", 20, 3, 17, "the Ten Commandments proper, split from the Sinai divine-speech opening above"),
        ("Leviticus", 11, 1, 8, "dietary law"),
        ("Leviticus", 19, 9, 18, "holiness code"),
        ("Leviticus", 23, 1, 8, "feast law"),
        ("Proverbs", 1, 1, 7, "purpose of proverbs"),
        ("Proverbs", 3, 1, 12, "wisdom instruction"),
        ("Proverbs", 6, 6, 11, "sluggard wisdom saying"),
        ("Proverbs", 31, 10, 31, "virtuous woman"),
    ],
}


def load_book(book_name):
    filename = book_name.replace(" ", "") + ".json"
    path = os.path.join(KJV_DIR, filename)
    with open(path, encoding="utf-8-sig") as f:
        return json.load(f)


def extract_verses(book_data, chapter, verse_start, verse_end):
    for ch in book_data["chapters"]:
        if int(ch["chapter"]) == chapter:
            return [
                v for v in ch["verses"]
                if verse_start <= int(v["verse"]) <= verse_end
            ]
    raise ValueError(f"chapter {chapter} not found in {book_data['book']}")


def build():
    if not os.path.isdir(KJV_DIR):
        sys.exit(f"error: {KJV_DIR} not found — run src/setup_data.py first")

    rows = []
    book_cache = {}
    for label, refs in REFERENCES.items():
        for book, chapter, v_start, v_end, note in refs:
            if book not in book_cache:
                book_cache[book] = load_book(book)
            verses = extract_verses(book_cache[book], chapter, v_start, v_end)
            if not verses:
                raise ValueError(f"no verses found for {book} {chapter}:{v_start}-{v_end}")
            for v in verses:
                rows.append({
                    "book": book,
                    "chapter": chapter,
                    "verse": v["verse"],
                    "ref": f"{book} {chapter}:{v['verse']}",
                    "label": label,
                    "note": note,
                    "text": v["text"].strip(),
                })

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["book", "chapter", "verse", "ref", "label", "note", "text"])
        writer.writeheader()
        writer.writerows(rows)

    counts = {}
    for r in rows:
        counts[r["label"]] = counts.get(r["label"], 0) + 1
    print(f"wrote {len(rows)} verses to {OUT_PATH}")
    for label, n in sorted(counts.items()):
        print(f"  {label}: {n}")


if __name__ == "__main__":
    build()
