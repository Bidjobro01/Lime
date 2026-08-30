import os
import sys
import urllib.request
from datetime import datetime, timezone

SUB_NAME = "🍋🟩Lime"
OUTPUT = "Lime.txt"
SOURCES = "sources.txt"
USER_AGENT = "Mozilla/5.0 (Lime Subscription Updater)"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8", errors="replace")


def read_sources(path):
    urls = []
    if not os.path.exists(path):
        return urls
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                urls.append(line)
    return urls


def extract_links(text):
    links = []
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            links.append(line)
    return links


def main():
    urls = read_sources(SOURCES)
    if not urls:
        print("No source URLs found in sources.txt")
        sys.exit(1)

    seen = set()
    merged = []
    for url in urls:
        print(f"Fetching: {url}")
        try:
            links = extract_links(fetch(url))
        except Exception as e:
            print(f"  ERROR: {e}")
            continue
        added = 0
        for link in links:
            if link not in seen:
                seen.add(link)
                merged.append(link)
                added += 1
        print(f"  +{added} unique links (total: {len(merged)})")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    header = (
        f"# {SUB_NAME} - custom VPN subscription",
        f"# Updated: {now}",
        f"# Unique servers: {len(merged)}",
    )
    with open(OUTPUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(header) + "\n\n" + "\n".join(merged) + "\n")

    print(f"Done. Wrote {len(merged)} unique links to {OUTPUT}")


if __name__ == "__main__":
    main()