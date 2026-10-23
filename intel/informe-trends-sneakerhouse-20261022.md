# INFORME DE DEMANDA — Google Trends
## Tienda fantasma "SNEAKER HOUSE" (calzado deportivo)

**Generado por:** Bellion (Gran Comandante) · **Para:** Monarca (Key)
**Fecha:** 2026-10-22 · **Fuente:** Google Trends (API interna, headless)
**Geo:** Colombia · **Ventana:** últimos 12 meses · **Índice:** relativo 0–100 (ancla `nike` = 47.4)

---

## 1. Interés por keyword (índice normalizado)

| # | Keyword | Índice | Lectura |
|---|---|---|---|
| 1 | **jordan** | **20.3** | 🥇 Imán (⚠️ se mezcla con Jordania, la selección) |
| 2 | **new balance** | **10.5** | 🥈 Imán |
| 3 | tenis adidas | 4.3 | Alto |
| 4 | tenis nike | 3.4 | Alto |
| 5 | sneakers | 2.2 | Medio |
| 6 | adidas samba | 2.2 | Medio |
| 7 | zapatillas hombre | 1.5 | Bajo |
| 8 | zapatillas nike | 1.4 | Bajo |
| 9 | zapatillas mujer | 1.4 | Bajo |
| 10 | nike air max | 1.4 | Bajo |
| 11 | zapatillas adidas | 1.2 | Bajo |
| 12 | air force 1 | 1.1 | Bajo |
| 13 | zapatillas colombia | 0.8 | Bajo |
| 14 | tenis originales | 0.8 | Bajo |
| 15 | zapatillas originales | 0.1 | Muy bajo |

*Control validado: `nike` = 47.4, `zapatillas` = 12.7 → la API funcionaba; los ceros son reales.*

---

## 2. Los 3 hallazgos que cambian el copy

1. **En Colombia se dice "TENIS", no "zapatillas".**
   `tenis adidas` (4.3) supera **3.6×** a `zapatillas adidas` (1.2). Títulos, menú y SEO deben usar **`tenis`**.
2. **Los imanes son JORDAN y NEW BALANCE — y están en el catálogo.**
   Jordan (21 productos) y New Balance (incl. 9060 y 530, que ya ganan en arbitraje).
3. **El modificador ganador es "mujer".**
   `tenis nike mujer`, `nike mujer`, `tenis mujer` dominan la lista.

---

## 3. Long-tail (consultas relacionadas — TOP y en ascenso)

| Semilla | TOP | 🚀 En ascenso |
|---|---|---|
| **new balance** | new balance mujer · new balance tenis · new balance colombia · 530 · 9060 | 204L mujer · ellipse · 1080 v15 · 408 |
| **tenis nike** | tenis nike mujer · nike mujer · tenis hombre · adidas tenis | shox · vomero · metcon 10 · tenis salomon |
| **jordan** | jordan retro · michael jordan · jordan air | (se mezcla con Jordania/país) |

→ **Munición de copy:** "tenis New Balance mujer", "tenis Nike Shox", "Jordan Retro".

---

## 4. Lectura estratégica

- El **nombre de marca** no se elige por volumen (una marca nueva = 0 por definición); se elige por
  **dominio libre + entidad sin ambigüedad (GEO)**. → **SNEAKER HOUSE**.
- El **motor de tráfico** lo dan las keywords de categoría: **"tenis" + New Balance + Jordan + mujer**.
- Dominio recomendado: **`sneakerhouse.co`** (`.com` ocupado; `.com.co` y `.co` probables libres).

---

## 5. Herramienta — módulo reutilizable

Script: `seawolf-agent/intel/trends-demanda.py`
- `--geo CO --tf "today 12-m" --ancla nike --kw ... --relacionadas ...`
- Salida: informe `.md` + datos `.json`.
- **Modos de ejecución:** (a) vía navegador/sesión (probado, fiable); (b) CLI headless (Google
  rate-limita sin cookies de sesión → usar backoff o cookie de sesión).
- **Límite honesto:** índice relativo, no volumen absoluto. Para volumen exacto: Keyword Planner / Semrush.

**Fin del informe.**
