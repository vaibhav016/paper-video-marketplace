#!/usr/bin/env python3
"""count_posts.py THREAD.md [--limit 280]: character count per post in a thread file.
Posts are blocks after '**N/**' headings, ended by '---'. Lines like [VIDEO...]/[FIG...] are ignored;
[ARXIV_LINK] / any URL counts as 23 (X's fixed t.co length). Rewrites the 'Character counts' footer."""
import re, sys
f = sys.argv[1]; lim = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 280
t = open(f).read()
if "\nCharacter counts" in t:
    t = t[:t.index("\nCharacter counts")].rstrip() + "\n"
posts = re.findall(r"\*\*\d+/\*\*\n\n(.*?)\n---", t, re.S)
c = []
for p in posts:
    p = re.sub(r"\n*\[(VIDEO|FIG)[^\]]*\]\n*", "", p).strip()
    p = re.sub(r"\[ARXIV_LINK\]|https?://\S+", "x" * 23, p)
    c.append(len(p))
t += "\nCharacter counts (link counted as 23): " + " / ".join(map(str, c)) + ".\n"
open(f, "w").write(t)
for i, n in enumerate(c, 1):
    print(f"{i}/ {n}" + ("  OVER" if n > lim else ""))
