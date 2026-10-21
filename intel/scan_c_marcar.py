# -*- coding: utf-8 -*-
"""Escaneo de C: -> JSON para listado con checkboxes (Seawolf Tools)."""
import os, json, heapq, string, shutil
from datetime import datetime

ROOT = "C:\\"
SKIP = {"windows", "$recycle.bin", "system volume information", "recovery",
        "seawolf_papelera", "$windows.~bt", "config.msi", "onedrivetemp"}
out_files = []
heap = []
folders = {}
scanned = 0
errors = 0

def main():
    global scanned, errors
    for dp, dns, fns in os.walk(ROOT, topdown=True):
        dns[:] = [d for d in dns if d.lower() not in SKIP]
        for fn in fns:
            p = os.path.join(dp, fn)
            try:
                s = os.path.getsize(p)
            except OSError:
                errors += 1
                continue
            scanned += 1
            if len(heap) < 400:
                heapq.heappush(heap, (s, p))
            elif s > heap[0][0]:
                heapq.heapreplace(heap, (s, p))
            # carpeta de primer nivel
            rel = os.path.relpath(dp, ROOT)
            top = rel.split(os.sep)[0]
            folders[top] = folders.get(top, 0) + s
    heap.sort(reverse=True)
    try:
        tot, used, free = shutil.disk_usage(ROOT)
    except OSError:
        tot = used = free = 0
    data = {
        "generado": datetime.now().isoformat(timespec="seconds"),
        "root": ROOT, "scanned": scanned, "errors": errors,
        "total": tot, "used": used, "free": free,
        "folders": sorted([{"n": k, "b": v} for k, v in folders.items()], key=lambda x: -x["b"]),
        "files": [{"p": p, "b": s, "drv": p[:2]} for s, p in heap],
    }
    with open(r"C:\Users\Admin\intel\scan-c.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    print("SCAN OK", scanned, "archivos,", errors, "errores,", len(data["files"]), "pesados, libres", round(free/1e9, 1), "GB")

if __name__ == "__main__":
    main()
