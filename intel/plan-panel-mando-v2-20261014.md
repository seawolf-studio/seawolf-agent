# PANEL DE MANDO v2 — Cambios "que duela de verdad"
## Rotación aleatoria · avance mínimo diario · 3 ausencias = castigo

**Fecha:** 2026-10-14 · **Uso Interno — Seawolf Studio** · Bellion para el Monarca

---

## 1. QUÉ CAMBIÓ (v1 → v2)

| # | Cambio | Detalle |
|---|--------|---------|
| 1 | **Todos los proyectos cuentan** | 12 proyectos sembrados. **% Global** (todos, ponderado) + **% Foco** (3 activos). |
| 2 | **3 en foco (igual)** | Sigue el límite de 3. El 4º exige mandar uno a la Bóveda. |
| 3 | **Rotación aleatoria diaria** | Los 3 activos cambian de orden **al azar cada día** → el "▶" del día es otro. Anti-monotonía. |
| 4 | **Avance mínimo diario** | Debes sumar **≥ N pts** al día (def. 2). Si no, el día **no cuenta**. |
| 5 | **Login diario mínimo** | Debes registrar login. Sin login = ausencia. |
| 6 | **3 ausencias = castigo** | Como el sistema carcelario: 3 fallos → **penalización + racha a cero**. |
| 7 | **Racha recalculada** | Se computa desde los días reales (no se puede "inflar"). |
| 8 | **Recompensa** | Campo editable (por definir). |

**Ausencia** = un día sin login **o** sin el avance mínimo.

---

## 2. EL CASTIGO (blindado)

**Castigo pactado:** mover **1 archivo aleatorio** de tu **Zona de Sacrificio** al **Trastero**.
- **Zona de Sacrificio:** `C:\Users\Admin\Seawolf_Sacrificio` → TÚ la llenas con cosas que aceptas perder (descargas, juegos, archivos sueltos).
- **Trastero:** `C:\Users\Admin\Seawolf_Trastero` → el archivo se va; **recuperable** con `--rescatar`.

> **Por qué así y no borrado total del PC:** un borrado a ciegas puede caer en las fotos de tu hija o en las llaves del VPS. **Duele la comodidad, no tus activos.** Recuperable = puedes pagar y arrepentirte; no te quiebra la misión.

### Comandos
```bash
python castigo-panel.py              # SIMULACRO (no toca nada)
python castigo-panel.py --ejecutar   # ejecuta (mueve 1 archivo)
python castigo-panel.py --listar     # qué hay en el Trastero
python castigo-panel.py --rescatar N # devuelve el archivo N
```
**Verificado:** simulación → ejecutar → rescatar (round-trip OK).

---

## 3. REGLAS DEL JUEGO
1. **Cada día:** login + ≥ N pts. Si no → **ausencia**.
2. **3 ausencias** (seguidas o acumuladas) → **castigo + racha = 0**.
3. **Racha viva** = días seguidos cumpliendo → multiplica la recompensa (cuando la definas).
4. **Foco = 3.** Sagrado.

---

## 4. LO QUE FALTA DE TI
- **La RECOMPENSA** (no la tienes clara). El miedo sin premio quema: hay que definirla.
  Ideas: un día libre sin culpa · comprar algo que quieras · un permiso/hobby · subir un nivel del juego.
- **Llenar la Zona de Sacrificio** con lo que aceptas perder (hoy está vacía → el castigo no tendría presa).
- **Confirmar los 3 en foco** y la **finalidad + costo** de cada uno.

---

## 5. NOTA HONESTA
Un castigo simbólico no mueve. Pero un castigo **destructivo** te sabotea. El equilibrio: **pérdida real, reversible, sobre tu comodidad.** Eso es lo que sostiene el sistema sin romperte.

**Fin del documento v2.**
