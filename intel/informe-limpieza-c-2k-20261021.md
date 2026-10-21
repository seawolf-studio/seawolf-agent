# INFORME — Erradicación de NBA 2K21 / WWE 2K23 + Seawolf Tools v5 (checks)
**Fecha:** 2026-10-21 · Uso Interno — Seawolf Studio · Bellion para el Monarca (Key)

---

## 1. ERRADICACIÓN COMPLETA — 184,5 GB liberados
**C: pasó de 5,8 GB → 190,3 GB libres.** Orden del Monarca: "ya acabé con ellos".

| Elemento | Tamaño |
|---|---|
| `C:\Games\NBA 2K21` | 96,3 GB |
| `C:\Program Files (x86)\Steam\steamapps\common\WWE 2K23` | 80,1 GB |
| `C:\Users\Admin\AppData\Local\WWE 2K23` (caché PreBakeCache) | 8,0 GB |
| Steam `appmanifest_1942660.acf` (para que Steam lo olvide) | 877 B |
| `AppData\Roaming\2K Sports` (config NBA 2K21) | 14,7 KB |
| `AppData\Roaming\WWE2K23SaveData` | 0 B |
| `Documents\WWE2K23` | 607 B |
| `Desktop\WWE 2K23.url` + `Public\Desktop\NBA 2K21.lnk` | — |
| Torrents NBA 2K21 (Descargas + E:\torrents\finalizados) | 595 KB |
| Steam cloud saves `userdata\219646227\1942660` | 5,0 MB |

**Registro:** revisado `HKCU\Software\2K Sports` / `Saber Interactive` / `WWE 2K23` → **no existían**, nada que limpiar.

### ⚠️ NO tocado (requiere tu decisión — son OTROS juegos)
- `E:\Ajugar\NBA 2K12 (USA).zip` (858,7 MB) y `NBA 2K13 (USA).zip` (858,9 MB) → **no son 2K21**.
- `...CoinOPS LEGENDS\...\NBA 2K2 (USA).lrtl` (87 B) → log de emulador de **NBA 2K2**.
- `D:\Nueva carpeta (2)\rescate\Escritorio\K\NBA 2K21.url` (283 B) → acceso directo muerto dentro de tu **carpeta de rescate**.
- Iconos en caché de Windows Search (36 KB, se regeneran solos).

---

## 2. SEAWOLF TOOLS v5 — sistema de CHECKS (estilo TuneUp) ✅
Integrado y **probado**:
- Casillas por archivo + **"Marcar visibles"** + contador **"N marcados · X GB"**.
- **♻️ Mover marcados** (a la Papelera Seawolf, reversible).
- **💀 Borrar marcados** (permanente, con doble confirmación).
- Endpoint `/mover-muchos` probado: 3 archivos borrados + 1 a papelera. ✔

**Bug real encontrado y corregido en pruebas:** el servidor **se caía con JSON malformado** (parseo sin protección) → ahora devuelve control en vez de reventar. *Honestidad de ingeniería: se encontró probando, no leyendo.*

---

## 3. FUENTES
- Escaneo propio de 1.489.712 archivos en C: (0 errores).
- Búsqueda multi-disco de remanentes (C, D, E, F, H, I, J).
- Verificación de disco antes/después.

**Fin del informe.**
