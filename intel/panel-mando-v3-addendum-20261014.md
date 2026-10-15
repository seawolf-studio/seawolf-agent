# PANEL DE MANDO v3 — Addendum: Zonas, Modos, Traba y Recompensas

**Fecha:** 2026-10-14 · Uso Interno — Seawolf Studio · Bellion para el Monarca

---

## 1. ZONA DE CASTIGO POR CARPETAS (corregido)

**Problema que señalaste:** si eliges tú los archivos, el sistema es trampa.
**Solución:** configuras **CARPETAS** (no archivos). El sistema **saca al azar** de ahí. Tú no controlas qué cae.

### Configuración — `castigo-config.json` (junto al script)
```json
{
  "zonas": ["C:\\Users\\Admin\\Downloads", "C:\\Users\\Admin\\Desktop\\juegos"],
  "modo": "trastero",
  "dias_bloqueo": 7
}
```
- **zonas:** carpetas de riesgo. Recomendado: **Downloads** (y alguna de juegos). **NUNCA** Desktop/Documentos donde vive trabajo.
- **modo:** `trastero` (reversible) o `borrar` (permanente).
- **dias_bloqueo:** días que el archivo queda inaccesible antes de poder rescatarlo.

### Comandos
```bash
python castigo-panel.py --zonas           # ver carpetas y cuántos archivos
python castigo-panel.py                   # SIMULACRO (no toca nada)
python castigo-panel.py --ejecutar        # ejecuta el saqueo
python castigo-panel.py --modo borrar     # endurecer (irreversible)
python castigo-panel.py --listar
python castigo-panel.py --rescatar N      # bloqueado hasta pasar dias_bloqueo
```

### Las 3 capas de dureza
| Modo | Dolor | Riesgo |
|------|-------|--------|
| **trastero** | Pierdes acceso (archivo "desaparece") | Reversible tras el bloqueo |
| **trastero + dias_bloqueo largo** | Duele más (no recuperas pronto) | Reversible |
| **borrar** | Dolor máximo, sin red | **Irreversible** — sin vuelta atrás |

**Recomendación honesta:** empieza en `trastero` con bloqueo de 7-14 días. Eso ya duele (el archivo no está). Sube a `borrar` solo en carpetas que de verdad aceptas perder para siempre.

**Verificado:** simulación → ejecutar → bloquear rescate → forzar → round-trip OK.

---

## 2. OFERTAS DE RECOMPENSA (elige / combina)

| # | Recompensa | Por qué funciona |
|---|-----------|------------------|
| 1 | **Día libre sin culpa** (sábado entero para familia/aficiones) | Premia el objetivo real: tiempo |
| 2 | **Compra-capricho** (un objeto que quieras, con tope) | Premio tangible e inmediato |
| 3 | **Nivel del Panel** (título: Recruta→Sombra→Comandante) | Estatus dentro del sistema |
| 4 | **"Permiso" acumulable** (hobby que normalmente te niegas) | Convierte el trabajo en moneda |
| 5 | **Multiplicador de racha** (racha larga = recompensa x2) | Refuerza constancia |
| 6 | **Cena/especial con los tuyos** | Liga el premio a la misión raíz |

**Regla:** la recompensa debe ser **algo que de verdad quieras y que normalmente te niegas.** Si no te cuesta darte, no motiva.
**Sugerencia (combo):** semanal = *día libre sin culpa* si cumples meta · mensual = *compra-capricho* si la racha pasa de X.

---

## 3. EXPLICACIÓN DE LO QUE TE PEDÍ (#3) — sin enredos

Te pedí **confirmar 3 cosas** del Panel:

1. **Los 3 en foco:** de todos tus proyectos, el Panel solo "enciende" 3 a la vez. **¿Cuáles 3 AHORA?** (los demás quedan en Bóveda). Ej: *Seawolf Agent · Círculo Publicitario · Clientes en frío*.
2. **FINALIDAD:** en una frase, **el POR QUÉ** de cada uno (para qué existe, cómo sirve a tu misión raíz). Ej: *"Círculo = captar clientes"*.
3. **COSTO:** en una frase, **qué pierdes** si lo dejas a medias (el miedo). Ej: *"sin captación no hay clientes → no hay dinero para los míos"*.

Eso es todo: **qué 3, por qué, y qué pierdes.** Con eso el Panel deja de ser prototipo y se vuelve TU sistema.

---

## 4. SUBIR MÁS EL NIVEL (opciones)
- **Misiones diarias** rotativas (la rotación ya está) → cada día el Panel asigna el "objetivo del día".
- **Racha con castigo escalonado:** 3 ausencias = castigo; 5 = castigo x2; 7 = cambio de modo a `borrar` automático.
- **Jefe semanal:** la tarea más dura de la semana = doble castigo si no se hace.
- **XP comprable:** el XP acumulado "paga" el rescate de UN archivo (canje). Trabajo → rescate.

**Fin del addendum.**
