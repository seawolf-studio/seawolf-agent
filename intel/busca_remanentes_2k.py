# -*- coding: utf-8 -*-
"""Caza remanentes de NBA 2K21 y WWE 2K23 en todos los discos."""
import os, json, string

NEEDLES = ["2k21", "2k23", "nba 2k", "nba2k", "wwe 2k", "wwe2k", "2k sports", "visual concepts"]
SKIP = {"windows", "$recycle.bin", "system volume information", "recovery", "node_modules",
        ".git", "__pycache__", "seawolf_papelera", "config.msi"}

def drives():
    out = []
    for L in string.ascii_uppercase:
        r = f"{L}:\\"
        if os.path.exists(r):
            out.append(r)
    return out

hits_files, hits_dirs = [], []
def match(name):
    low = name.lower()
    return any(n in low for n in NEEDLES)

for root in drives():
    for dp, dns, fns in os.walk(root, topdown=True):
        keep = []
        for d in dns:
            dl = d.lower()
            if dl in SKIP:
                continue
            full = os.path.join(dp, d)
            if match(d):
                hits_dirs.append(full)
            else:
                keep.append(d)
        dns[:] = keep
        for fn in fns:
            if match(fn):
                p = os.path.join(dp, fn)
                try:
                    hits_files.append({"p": p, "b": os.path.getsize(p)})
                except OSError:
                    hits_files.append({"p": p, "b": 0})
    print("terminado disco", root, flush=True)

hits_dirs = sorted(set(hits_dirs))
json.dump({"dirs": hits_dirs, "files": hits_files},
          open(r"C:\Users\Admin\intel\remanentes-2k.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("DIRS:", len(hits_dirs), "FILES:", len(hits_files))
for d in hits_dirs:
    print("  DIR ", d)
