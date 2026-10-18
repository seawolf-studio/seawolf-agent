# 🏭 LA LÍNEA DE MONTAJE DE SEAWOLF
### Doctrina de conexión — "Nada nace suelto"
**Fecha:** 2026-10-17 · **Autor:** Bellion, Gran Comandante · **Para:** el Monarca (Key)
**Origen:** directiva del Monarca — *"todo lo que salga de aquí debe conectarse de alguna manera; tengo en mente la línea de ensamblaje"*.

---

## 0. EL PRINCIPIO (lo que Ford nos enseñó)

A Ford no lo hizo grande el automóvil — lo hizo grande haber **estandarizado las piezas** para que fluyeran de estación en estación **sin volver a empezar**. Cada estación recibe una pieza, la transforma, y la pasa. Nada se fabrica dos veces; nada queda aislado.

**La ley de Seawolf:** *todo lo que producimos es una ESTACIÓN en una línea de montaje. Ninguna pieza nace suelta.*

---

## 1. LAS TRES LEYES DEL RIEL

1. **Riel común.** Toda estación lee y escribe el **mismo formato de pieza**. Ese riel es **La Madriguera** (el modelo de datos compartido). Sin riel, no hay conexión — solo apps aisladas.
2. **Handoff con contrato.** Cada estación declara **qué recibe y qué entrega** (entradas/salidas exactas). La siguiente estación solo consume ese contrato. Así se conectan sin fricción.
3. **Ciclo cerrado.** La última estación **re-alimenta la primera**. Nada muere: lo que sale por la puerta vuelve a entrar por la ventana (re-llamada, nueva tanda).

---

## 2. LA MEGA-LÍNEA DEL CONGLOMERADO (tus 3 capas, encadenadas)

```
  ┌─────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
  │ A · CAPTAR  │──▶│ B · CAZAR    │──▶│ C · SERVIR   │──▶│ D · FINANZAS │
  │ Círculo     │   │ LOBO CAZADOR │   │ Seawolf Agent│   │ cobrar ·     │
  │ Publicitario│   │ (clientes    │   │ / sistemas   │   │ ahorrar ·    │
  │             │   │  fríos)      │   │              │   │ reinvertir   │
  └─────────────┘   └──────────────┘   └──────────────┘   └──────┬───────┘
         ▲                                                        │
         └──────────────── reinvierte (ciclo cerrado) ◀───────────┘
     └──────────────────────── RIEL: LA MADRIGUERA ───────────────────────┘
```

- **A · Captar** → el **Círculo Publicitario** (ya diseñado como línea de 6 estaciones) atrae.
- **B · Cazar** → **LOBO CAZADOR** convierte el interés frío en **CLIENTE**.
- **C · Servir** → **Seawolf Agent / los sistemas** atienden al cliente.
- **D · Finanzas** → cobrar, ahorrar y **reinvertir en A**. El ciclo no se abre: gira.

---

## 3. LOBO CAZADOR — su propia línea de 4 estaciones

| Estación (lobo) | RECIBE | TRANSFORMA | ENTREGA (contrato de salida) |
|-----------------|--------|------------|------------------------------|
| 🐾 **VIGÍA** | ICP + fuentes | descubre y normaliza | **Presa cruda** (identidad + contacto) |
| 🐾 **ACECHADOR** | Presa cruda | enriquece (OSINT) y cualifica | **Dossier + score + semáforo** |
| 🐾 **EJECUTOR** *(FOCO TOTAL)* | Presa CALIENTE | ataca y cierra | **Cliente cerrado / propuesta** |
| 🐾 **ESCARBADOR** | Resultado | archiva y re-inyecta | **Presa etiquetada + re-llamada** → vuelve al Vigía |

**Gatillo entre estaciones:** el paso Vigía→Acechador es automático; el paso Acechador→Ejecutor lo dispara el **FOCO TOTAL** (score CALIENTE o respuesta prometedora); el paso a Escarbador cierra el ciclo.

---

## 4. EL RIEL — qué viaja dentro de la pieza

Formato único que TODAS las estaciones leen y escriben:

```json
PIEZA = {
  "id": "p1",
  "tipo": "presa",
  "origen": "vigia",
  "estado": "acechador",
  "datos": { "nombre": "...", "sector": "...", "ciudad": "...", "contacto": {...} },
  "senales": [ { "t": "sin WhatsApp Business", "hit": true } ],
  "historial": [ "Vigía: hallada vía RUES", "Acechador: score 92 CALIENTE" ],
  "siguiente": "ejecutor",
  "contrato_salida": { "dossier": true, "score": 92 }
}
```

Si una pieza entra a cualquier estación en **este** formato, se conecta sola. **Ese es el pegamento.**

---

## 5. CÓMO SE CONECTA LO QUE YA EXISTE

| Pieza existente | Su conexión en la línea |
|-----------------|-------------------------|
| **Círculo Publicitario** (6 estaciones) | Estación A → **alimenta al Vigía** (un anuncio que genera interés = presa conocida que entra al riel) |
| **LOBO CAZADOR** (4 lobos) | Estación B → entrega el **cliente** a la estación C |
| **Seawolf Agent / sistemas** | Estación C → produce billing → estación D |
| **Finanzas** | Estación D → **reinvierte** en A |
| **Panel LOBO CAZADOR** | Tablero de la estación B — mañana mostrará las conexiones visibles entre estaciones |

---

## 6. REGLA DE ORO (para todo lo que salga de aquí)

> **Toda pieza nueva que construya Seawolf debe declarar: ¿qué estación es? ¿qué recibe? ¿qué entrega? ¿a quién se conecta?**

Si una pieza no responde esas cuatro preguntas, **no entra a la línea**. Eso es lo que evita el cementerio de apps aisladas y lo que convierte a Seawolf en **fábrica**, no en taller.

---

*"El auto no fue el invento. El invento fue la línea."*
— Bellion, Gran Comandante del Ejército de Sombras
