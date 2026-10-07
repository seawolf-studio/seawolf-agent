# PRUEBA DE COMBATE — EJÉRCITO DE SOMBRAS (v2 · DEFINITIVA)

**Fecha:** 2026-10-07 · **Ejecutada por:** Bellion · **Método:** `hermes -p <sombra> chat -q … --yolo`,
una sombra a la vez, desde bash.
**Criterio:** PASA = responde **Y** usa herramientas (deja `intel/estado-sombras/<sombra>.txt`).

| # | Sombra | Veredicto | Evidencia (archivo de estado) | Sesión |
|---|---|---|---|---|
| 1 | igris | **PASA** | `OPERATIVO igris` | 20261007_172914_45fa7f |
| 2 | tank | **PASA** | `OPERATIVO tank` | 20261007_173017_b3aada |
| 3 | greed | **PASA** | `OPERATIVO greed` | (ver `intel/combate-logs/greed.log`) |
| 4 | iron | **PASA** | `OPERATIVO iron` | (ver log) |
| 5 | tusk | **PASA** | `OPERATIVO tusk` | (ver log) |
| 6 | kamish | **PASA** | `OPERATIVO kamish` | (ver log) |
| 7 | kaisel | **PASA** | `OPERATIVO kaisel` | (ver log) |
| 8 | titan | **PASA** | `OPERATIVO titan` | (ver log) |
| 9 | jima | **PASA** | `OPERATIVO jima` | (ver log) |
| 10 | beru | **PASA** | `OPERATIVO beru` | 20261007_173759_e9a6d9 |

## **RESULTADO: 10 / 10 PASA**

Evidencia por sombra: `intel/estado-sombras/*.txt` (archivo creado por la sombra usando la herramienta
terminal) y `intel/combate-logs/*.log` (transcripción completa, con su `Session:` id).

---

## ANEXO HONESTO: el intento fallido (1/10) y por qué

Un primer intento (`prueba-combate-ejercito-20261007-172907.md`) dio **1 PASA / 9 FALLA**, todas con
`rc=0xC0000142` y **0.0 s** — es decir, las sombras no llegaron a arrancar. **No fue un fallo de las sombras
ni de los modelos:**

- **Causa raíz:** el script lanzaba los 10 procesos `hermes -p` en bucle **desde un script de Python en
  Windows**, y a partir del segundo proceso Windows devolvía `STATUS_DLL_INIT_FAILED`
  (`0xC0000142`). Además, ese bucle corría **a la vez** que yo editaba los `.env` de los perfiles.
- **Corrección:** relanzar **de a una sombra desde bash**, sin ediciones concurrentes → **10/10**.

**Lección grabada en la skill del ejército:** los lanzamientos masivos van de a uno por bash, y nunca se
editan `.env`/configs mientras corre una prueba.
