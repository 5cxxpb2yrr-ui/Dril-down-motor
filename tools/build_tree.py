#!/usr/bin/env python3
"""Convert a Dogeware-style index page (nested <ul>/<li class='li-folder'>) into tree.json.
Usage: python build_tree.py INDEX.html "Manual Name" > tree.json
Upload result to R2 as:  <Vehicle>/<Manual Name>/tree.json
Leaf pages (pages/N.html) go in R2 as:  <Vehicle>/pages/N.html"""
import re, sys, json, html
from html.parser import HTMLParser
src, title = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8", errors="ignore").read()
s = s[s.find("<ul>", s.find("collapse-all")):]
root = {"c": []}
class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack=[root]; self.last=None; self.href=None; self.txt=None
    def handle_starttag(self, t, a):
        a = dict(a)
        if t == "a": self.href, self.txt = a.get("href"), ""
        elif t == "ul" and self.last is not None: self.stack.append(self.last)
    def handle_endtag(self, t):
        if t == "a" and self.txt is not None:
            n = {"n": html.unescape(self.txt).strip()}
            if self.href:
                m = re.search(r"(\d+)\.html", self.href); n["p"] = int(m.group(1)) if m else self.href
            else: n["c"] = []
            self.stack[-1].setdefault("c", []).append(n); self.last = n; self.txt = None
        elif t == "ul" and len(self.stack) > 1: self.stack.pop(); self.last = None
    def handle_data(self, d):
        if self.txt is not None: self.txt += d
P().feed(s)
# drop stray non-page links (e.g. footer "About" link captured after the tree)
def clean(n):
    n["c"]=[c for c in n["c"] if not (isinstance(c.get("p"),str))]
    for c in n["c"]:
        if "c" in c: clean(c)
clean(root)
print(json.dumps({"title": title, "c": root["c"]}, separators=(",", ":"), ensure_ascii=False))
