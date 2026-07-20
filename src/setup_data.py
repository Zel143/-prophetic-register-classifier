"""
One-time data setup: clones the KJV source repo and scrapes the three
public-domain transfer-test corpora (Sibylline Oracles, 1 Enoch, Bahman
Yasht) from sacred-texts.com into flat .txt files.

See docs/data-sources.md for licensing/provenance notes on each source.

Usage:
    python src/setup_data.py            # do everything
    python src/setup_data.py --kjv-only
    python src/setup_data.py --transfer-only
"""
import argparse
import os
import re
import subprocess
import sys
import time

import requests
from bs4 import BeautifulSoup

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, "data")
TRANSFER_DIR = os.path.join(DATA_DIR, "transfer")

KJV_REPO_URL = "https://github.com/aruljohn/Bible-kjv.git"
KJV_DIR = os.path.join(DATA_DIR, "Bible-kjv")

# sacred-texts.com 403s a bare `requests` UA and rate-limits bursts of
# requests behind Cloudflare, so we impersonate a browser and space
# requests out (REQUEST_DELAY_SECONDS) rather than hammering it.
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
REQUEST_DELAY_SECONDS = 2.0


def clone_kjv():
    if os.path.isdir(KJV_DIR):
        print(f"skip: {KJV_DIR} already exists")
        return
    subprocess.run(["git", "clone", KJV_REPO_URL, KJV_DIR], check=True)


# --- Transfer corpora ---

# Each entry: output filename -> (base URL, [page slugs in reading order]).
# Page ranges were determined by inspecting each work's index/TOC page by
# hand (see docs/data-sources.md for the index URLs); sacred-texts.com has
# no machine-readable TOC, so these are hardcoded rather than crawled.
CORPORA = {
    "sibylline_oracles": {
        "base": "https://sacred-texts.com/cla/sib/",
        "pages": [f"sib{n:02d}.htm" for n in range(3, 15)],  # Book I - Book XIV
    },
    "1_enoch": {
        "base": "https://sacred-texts.com/bib/boe/",
        "pages": [f"boe{n:03d}.htm" for n in range(4, 113)],  # Chapter I - Chapter CVIII
    },
    "bahman_yasht": {
        "base": "https://sacred-texts.com/zor/sbe05/",
        "pages": [f"sbe05{n:02d}.htm" for n in range(56, 60)],  # Observations + Chapter I - III
    },
}

PAGE_MARKER_RE = re.compile(r"^\{?p\.\s*\d+\.?\}?$", re.IGNORECASE)


def fetch_page(session, url, retries=3):
    for attempt in range(1, retries + 1):
        resp = session.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200 and "Just a moment" not in resp.text:
            return resp.text
        wait = 10 * attempt
        print(f"  retry {attempt}/{retries} for {url} (status {resp.status_code}), waiting {wait}s")
        time.sleep(wait)
    raise RuntimeError(f"failed to fetch {url} after {retries} retries")


def clean_page_text(html):
    """Strip nav chrome, footnotes, and page markers; return body text."""
    soup = BeautifulSoup(html, "html.parser")

    if soup.head:
        soup.head.decompose()
    for tag in soup.find_all(["script", "style", "nav"]):
        tag.decompose()
    for tag in soup.find_all("div", class_="filenav"):
        tag.decompose()
    # Footnote blocks are consistently wrapped in a small <font size="2">.
    for tag in soup.find_all("font", size="2"):
        tag.decompose()
    # Top breadcrumb nav (a bare <center> of "Sacred Texts / Previous / Next" links).
    for center in soup.find_all("center"):
        if center.find("a", string=re.compile("Sacred Texts")):
            center.decompose()
    # Byline paragraph ("<title>, <translator>, [<year>], at sacred-texts.com").
    for p in soup.find_all("p"):
        if "sacred-texts.com" in p.get_text():
            p.decompose()

    lines = [line.strip() for line in soup.get_text("\n").splitlines()]
    lines = [ln for ln in lines if ln and not PAGE_MARKER_RE.match(ln)]
    return "\n".join(lines)


def fetch_corpus(name, spec):
    session = requests.Session()
    chunks = []
    for i, page in enumerate(spec["pages"]):
        url = spec["base"] + page
        print(f"[{name}] fetching {url} ({i + 1}/{len(spec['pages'])})")
        html = fetch_page(session, url)
        chunks.append(clean_page_text(html))
        if i < len(spec["pages"]) - 1:
            time.sleep(REQUEST_DELAY_SECONDS)

    os.makedirs(TRANSFER_DIR, exist_ok=True)
    out_path = os.path.join(TRANSFER_DIR, f"{name}.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(chunks) + "\n")
    print(f"[{name}] wrote {out_path}")


def fetch_transfer_corpora(only=None):
    for name, spec in CORPORA.items():
        if only and name != only:
            continue
        fetch_corpus(name, spec)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--kjv-only", action="store_true")
    parser.add_argument("--transfer-only", action="store_true")
    parser.add_argument("--corpus", choices=list(CORPORA), help="fetch a single transfer corpus")
    args = parser.parse_args()

    if not args.transfer_only:
        clone_kjv()
    if not args.kjv_only:
        fetch_transfer_corpora(only=args.corpus)


if __name__ == "__main__":
    sys.exit(main())
