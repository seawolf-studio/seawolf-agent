#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MÓDULO DE DEMANDA — Google Trends (headless) para EL CÍRCULO PUBLICITARIO
Estación 1 (Concepto/Ángulo) recibe "Producto X + datos"  <-- esto son los "datos".
Estación 6 (Medición) también lo consume como señal de demanda.

Uso:
    python trends-demanda.py --geo CO --tf "today 12-m" --ancla nike \\
        --kw "tenis nike" "tenis adidas" "new balance" "jordan" "sneakers"
    python trends-demanda.py --relacionadas "new balance" "tenis nike"

Salida:
    - informe en Markdown (stdout y archivo .md)
    - datos crudos .json
No requiere API key ni navegador: usa la API interna de trends.google.com (stdlib).
Autor: Bellion (Gran Comandante) para Seawolf Studio.
"""
import argparse, json, sys, time, urllib.parse, urllib.request

BASE = "https://trends.google.com"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
MAX_POR_TANDA = 5  # límite duro de Google Trends


def _get(path, params):
    """GET a la API interna; limpia el prefijo anti-JSON )]}' y devuelve dict."""
    url = BASE + path + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    for intento in range(5):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                txt = r.read().decode("utf-8", "replace")
            txt = txt.replace(")]}'", "", 1).strip()
            return json.loads(txt)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 503):      # rate limit -> backoff
                time.sleep(3 * (intento + 1))
                continue
            raise
    raise RuntimeError("Google Trends no respondió tras varios intentos (rate limit?)")


def explore(keywords, geo, tf):
    req = {"comparisonItem": [{"keyword": k, "geo": geo, "time": tf} for k in keywords],
           "category": 0, "property": ""}
    return _get("/trends/api/explore", {"hl": "es", "tz": "300",
                                        "req": json.dumps(req)})


def _widget(data, wid):
    for w in data.get("widgets", []):
        if w.get("id") == wid:
            return w
    return None


def serie(keywords, geo, tf):
    """Devuelve {keyword: interes_promedio} para <=5 keywords."""
    data = explore(keywords, geo, tf)
    w = _widget(data, "TIMESERIES")
    if not w:
        return {k: 0.0 for k in keywords}
    md = _get("/trends/api/widgetdata/multiline",
              {"hl": "es", "tz": "300", "req": json.dumps(w["request"]), "token": w["token"]})
    tl = md.get("default", {}).get("timelineData", [])
    n = len(tl)
    if n == 0:
        return {k: 0.0 for k in keywords}
    acc = [0.0] * len(keywords)
    for punto in tl:
        for i, v in enumerate(punto.get("value", [])[:len(keywords)]):
            acc[i] += v
    return {k: round(acc[i] / n, 1) for i, k in enumerate(keywords)}


def relacionadas(keyword, geo, tf):
    """Devuelve (top, rising) listas de consultas relacionadas."""
    data = explore([keyword], geo, tf)
    w = _widget(data, "RELATED_QUERIES")
    if not w:
        return [], []
    rd = _get("/trends/api/widgetdata/relatedsearches",
              {"hl": "es", "tz": "300", "req": json.dumps(w["request"]), "token": w["token"]})
    rl = rd.get("default", {}).get("rankedList", [])
    f = lambda i: [x.get("query") for x in (rl[i].get("rankedKeyword", []) if i < len(rl) else [])]
    return f(0), f(1)


def barrido(keywords, geo, tf, ancla):
    """Normaliza entre tandas usando un término ancla común -> índice comparable."""
    ancla_val_global = None
    out = {}
    # primero medir el ancla sola para fijar la escala
    ancla_val_global = serie([ancla], geo, tf).get(ancla, 1.0) or 1.0
    resto = [k for k in keywords if k != ancla]
    for i in range(0, len(resto), MAX_POR_TANDA - 1):
        tanda = [ancla] + resto[i:i + MAX_POR_TANDA - 1]
        res = serie(tanda, geo, tf)
        a = res.get(ancla, 1.0) or 1.0
        for k in tanda:
            if k == ancla:
                continue
            out[k] = {"indice": round(res[k] / a * ancla_val_global, 1), "crudo": res[k]}
        time.sleep(1.2)  # cortesía con el rate limit
    return out, ancla_val_global


def main():
    ap = argparse.ArgumentParser(description="Módulo de demanda Google Trends (Círculo Publicitario)")
    ap.add_argument("--geo", default="CO")
    ap.add_argument("--tf", default="today 12-m")
    ap.add_argument("--ancla", default="nike")
    ap.add_argument("--kw", nargs="*", default=[])
    ap.add_argument("--relacionadas", nargs="*", default=[])
    ap.add_argument("--out", default="informe-trends")
    a = ap.parse_args()

    if not a.kw and not a.relacionadas:
        print("Nada que medir. Usa --kw y/o --relacionadas"); sys.exit(1)

    md = [f"# Informe de demanda — Google Trends", f"", f"- Geo: **{a.geo}** · Ventana: **{a.tf}** · Ancla: **{a.ancla}**", ""]
    dump = {"geo": a.geo, "tf": a.tf, "ancla": a.ancla}

    if a.kw:
        idx, ref = barrido(a.kw, a.geo, a.tf, a.ancla)
        ordenado = sorted(idx.items(), key=lambda x: -x[1]["indice"])
        md += [f"## Interés por keyword (índice, ancla `{a.ancla}`={ref})", "",
               "| # | Keyword | Índice |", "|---|---|---|"]
        for i, (k, v) in enumerate(ordenado, 1):
            md.append(f"| {i} | {k} | **{v['indice']}** |")
        md.append("")
        dump["keywords"] = {k: v["indice"] for k, v in ordenado}

    if a.relacionadas:
        md += ["## Consultas relacionadas", "", "| Semilla | TOP | 🚀 En ascenso |", "|---|---|---|"]
        dump["relacionadas"] = {}
        for k in a.relacionadas:
            top, ris = relacionadas(k, a.geo, a.tf)
            md.append(f"| **{k}** | {' · '.join(top[:6])} | {' · '.join(ris[:6])} |")
            dump["relacionadas"][k] = {"top": top, "rising": ris}
            time.sleep(1.2)
        md.append("")

    texto = "\n".join(md)
    print(texto)
    with open(a.out + ".md", "w", encoding="utf-8") as f:
        f.write(texto)
    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(dump, f, ensure_ascii=False, indent=2)
    print(f"\n[ok] guardado: {a.out}.md · {a.out}.json", file=sys.stderr)


if __name__ == "__main__":
    main()
