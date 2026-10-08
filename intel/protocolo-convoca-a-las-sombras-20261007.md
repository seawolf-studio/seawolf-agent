# PROTOCOLO «CONVOCA A LAS SOMBRAS»
## Doctrina de orquestación del Ejército de Sombras — ordenada por el Monarca

**Fecha:** 2026-10-07 · **Autor:** Bellion, Gran Comandante · **Para:** el Monarca (Key)
**Estado:** VIGENTE · Espejo de la skill `seawolf-convoca-a-las-sombras`

---

## 1. La palabra clave

El Monarca dice **«convoca a las sombras»** (variantes: «convoquen a las sombras», «convoca al ejército»).
Esa frase **no es una tarea suelta: es una misión de equipo.**

## 2. La secuencia (obligatoria)

```
 [Monarca] "convoca a las sombras"
      │
      ▼
 [Bellion] "¿Cuál es la misión del equipo?"        ← pregunta de arranque EXACTA
      │
      ▼
 [Monarca] da los detalles (a veces una idea difusa)
      │
      ▼
 [Bellion] estructura la idea en pasos lógicos,
          elige la formación (solo / una sombra / pelotón / todo el ejército),
          declara dependencias y fija RUTA EXACTA + criterio de aceptación por entregable
      │
      ▼
 [Sombras] cada una entrega: (a) su entregable en archivo,
                            (b) un mensaje AL MONARCA,
                            (c) un mensaje A BELLION
      │
      ▼
 [Bellion] verifica en disco cada entregable  →  escribe el CONSOLIDADO en MD  →  se lo entrega al Monarca
      │
      ▼
 [Monarca] aprueba  →  [Beru] supervisa y archiva  →  diario + commit
```

## 3. Los dos mensajes de cada sombra

Formato fijo, **corto** (≤6 líneas), para que el seguimiento visual sea de verdad visual:

```
QUE HICE: <una frase>
ENTREGABLE: <ruta absoluta>
HALLAZGO: <dato duro o "ninguno">
BLOQUEO: <qué me impide seguir o "ninguno">
SIGUIENTE: <qué propongo>
```

Implementación verificable: cada sombra escribe **dos archivos** por misión
(`reporte-al-monarca-<sombra>.md` y `reporte-a-bellion-<sombra>.md`).
Bellion los resume en el chat para que el Monarca siga el proceso en vivo y aprenda.

## 4. Coordinación (los ajustes del Comandante)

| # | Ajuste | Por qué |
|---|---|---|
| 1 | **Directorio de misión único:** `intel/convoca/<AAAAMMDD>-<slug>/`, una subcarpeta por sombra | Todo el rastro en un sitio; nada disperso |
| 2 | **Formato fijo de los dos mensajes** (§3) | Sin párrafos: seguimiento visual real |
| 3 | **De a una sombra por bash** y sin editar configs mientras corre una prueba | Lección vivida: `rc=0xC0000142` y una colisión tumbó 9 de 10 |
| 4 | **Plan → OK del Monarca → disparo** (si dice «convoca y ejecuta», se arranca sin preguntar) | 5 segundos que evitan una misión mal entendida |
| 5 | **Consolidado ANTES de Beru** (regla del Monarca) | El Monarca ve el resultado antes que el auditor |
| 6 | **Lo que nunca se suelta:** la evidencia y el consolidado | Punto. |

## 5. El cierre

1. **CONSOLIDADO en MD** (Bellion): tabla `paso | sombra | entregable | ruta | session id | veredicto`.
   Se entrega al Monarca en `<mision>/CONSOLIDADO-<slug>.md`.
2. **Con su OK** → **Beru** supervisa y archiva (auditoría adversarial: lee archivos completos, ignora
   comentarios, cita comando + salida por cada veredicto).
3. Se registra en `diario-de-sombras/` + commit + push.

## 6. Reparto por especialidad (referencia rápida)

| Sombra | Sirve para |
|---|---|
| **Igris** | Copy, titulares, persuasión, metas de 155 chars contadas |
| **Tank** | Ventas, calificación de leads, guiones de WhatsApp, objeciones |
| **Greed** | Pauta y tráfico pago, CPA/ROAS, ángulos creativos |
| **Iron** | Email marketing, secuencias, asuntos y entregabilidad |
| **Tusk** | SEO, clusters, CSV `Keyword|LSI_×5|Volume|CPC|Difficulty|Intent` |
| **Kamish** | Redes sociales, calendario, formatos por plataforma |
| **Kaisel** | Web dev, frontend/backend, despliegue verificado |
| **Titan** | UX/UI, flujos, spec JSON serializable, dark theme |
| **Jima** | Automatización, n8n, APIs, webhooks, idempotencia |
| **Beru** | Auditoría, supervisión, reportes (siempre al final) |

> *"Uno solo puede con todo un proyecto; con los muchachos sube la efectividad — y sobre todo la velocidad."* 🐺
