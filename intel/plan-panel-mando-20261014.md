# PLAN — "PANEL DE MANDO" (Dashboard de Proyectos Gamificado)
## Sistema anti-abandono para mente dispersa

**Fecha:** 2026-10-14 · **Clasificación:** Uso Interno — Seawolf Studio
**Elaborado por:** Bellion (Gran Comandante) · **Encargado por:** Monarca (Key)
**Propósito:** Que ningún proyecto de Seawolf quede a la mitad. Convertir "finalidad + miedo" en un sistema mecánico.

---

## 1. VERDAD CRUDA (antes de diseñar)

1. **Un dashboard reporta; no obliga.** El músculo que te hace terminar es **la consecuencia**, no la barra de progreso.
2. **La pérdida pega ~2× más que la ganancia** (aversión a la pérdida). → Tu "miedo" es el motor correcto. Debe ser **real y pactado**, no simbólico.
3. **Más proyectos visibles = más dispersión.** Un panel con todo encendido te hunde. → **Máximo 3 proyectos ACTIVOS**; el resto a la Bóveda.
4. **La finalidad tiene que estar a la vista siempre.** Cada proyecto apunta a la MISIÓN RAÍZ (la gente que te importa). Sin eso, el miedo se vuelve ansiedad y la ansiedad paraliza.

---

## 2. MECÁNICA CENTRAL

### 2.1 Progreso dinámico
- Cada **proyecto** = conjunto de **tareas** con peso (pts).
- **% del proyecto** = pts hechas / pts totales.
- **% TOTAL** = promedio **ponderado** de los proyectos **ACTIVOS** (no toda la bóveda).
- Sube al completar tareas, **baja** si una tarea vencida se marca perdida o si entras en déficit.

### 2.2 Sueldo semanal (el "trabajo tradicional")
- Meta semanal de **% TOTAL** (ej. 20%).
- **Cumples** → ganas recompensa (sueldo/XP/accesión).
- **No cumples** → **pierdes algo pactado** (el miedo). Regla: la pérdida debe doler de verdad (dinero al bote, trabajo extra, privilegio perdido).

### 2.3 Gamificación (para que sea agradable)
- **XP** por tarea hecha → **Nivel**.
- **Racha** (días seguidos cumpliendo la meta mínima diaria).
- **Logros** (primer proyecto al 100%, 7 días de racha, etc.).
- **Bóveda**: proyectos en pausa, accesibles pero silenciosos.

### 2.4 Foco forzado
- **3 activos máximo.** Si quieres activar un 4º, debes mandar uno a la Bóveda. Dura elección = foco.

---

## 3. MODELO DE DATOS

```
Proyecto {
  id, nombre,
  estado: ACTIVO | BOVEDA,
  finalidad:  "POR QUÉ" (link a la MISIÓN RAÍZ)
  costo:      "QUÉ PIERDO si lo dejo a medias"   ← el miedo
  peso:       1-5 (importancia relativa)
  deadline,
  tareas: [ { texto, pts, hecha } ]
}
% proyecto = Σ pts hechas / Σ pts
% TOTAL    = Σ (peso × %proy) / Σ peso   (solo ACTIVOS)
XP = Σ pts hechas ·  Nivel = XP / 100
Racha = días seguidos ≥ meta diaria mínima
```

---

## 4. REVISIÓN (ritual, no opcional)
- **Diaria (2 min):** marcar tareas, ver % y racha.
- **Semanal (10 min):** liquidar sueldo (gano o pierdo), mover proyectos entre Activo/Bóveda.
- **Mensual:** ¿los 3 activos avanzan? Si no → el problema es el foco, no el sistema.

---

## 5. QUÉ ENTREGAR
1. **Aplicativo** (`panel-mando-app.html`): funciona, guarda en el navegador, con tus proyectos reales sembrados.
2. Tú afinas: **los 3 activos**, **la finalidad y el costo** de cada uno, y **la meta del sueldo**.

## 6. RIESGOS (honestos)
- Si el "costo" es simbólico, **no funciona**. Debe doler.
- Si activas 10 proyectos, **vuelves a dispersarte**. La regla de 3 es sagrada.
- El panel es una herramienta, no magia: **sin revisión diaria, muere en 1 semana.**

**Fin del plan.**
