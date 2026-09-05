#!/usr/bin/env python3
"""Pre-publish scan. Blocks a commit if any staged file contains a term
from the blocklist. Generic terms live here; names and codenames live in
.ip_blocklist.local, which is gitignored and can never be committed."""
import re, subprocess, sys, pathlib

BLOCKLIST = [
    r"\badobe\b", r"\bsdr\+?\b", r"\brenewal agent\b", r"\bautonomous renewal\b",
]

def load_local():
    p = pathlib.Path(".ip_blocklist.local")
    if not p.exists():
        return []
    return [l.strip() for l in p.read_text().splitlines() if l.strip() and not l.startswith("#")]

def staged_files():
    out = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
                         capture_output=True, text=True).stdout
    return [f for f in out.split("\n") if f]

def main():
    pattern = re.compile("|".join(BLOCKLIST + load_local()), re.IGNORECASE)
    hits = []
    for f in staged_files():
        if f == ".ip_blocklist.local":
            hits.append((f, 0, "local blocklist must never be committed")); continue
        try:
            text = pathlib.Path(f).read_text(errors="ignore")
        except (IsADirectoryError, FileNotFoundError):
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if pattern.search(line):
                hits.append((f, i, line.strip()[:80]))
    if hits:
        print("IP SCAN BLOCKED THIS COMMIT:")
        for f, i, l in hits: print(f"  {f}:{i}: {l}")
        sys.exit(1)
    print("ip_scan: clean")

if __name__ == "__main__":
    main()
