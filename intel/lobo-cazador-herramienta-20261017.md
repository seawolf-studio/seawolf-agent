# 🐺 LOBO CAZADOR — Herramienta de caza de clientes fríos
### Marca: Seawolf Studio · Definición v1
**Fecha:** 2026-10-17 · **Autor:** Bellion, Gran Comandante · **Estado:** DEFINICIÓN (pendiente de tu "adelante" para construir)

---

## 1. OBJETIVO DE LA HERRAMIENTA

Una herramienta propia —interna primero, vendible después— para **INVESTIGAR y CAPTAR clientes fríos B2B** en Colombia.

- **Presa:** empresas colombianas con **dolor digital medible** (sin web, web obsoleta, sin WhatsApp Business, reseñas sin responder).
- **Oferta:** servicios Seawolf Studio (web, ads, automatización, agentes IA/CSO).
- **Canal primario:** **email con warm-up**; WhatsApp (puente WAHA) **solo a quien responda**.
- **Marca:** Seawolf Studio (OSCURO por defecto, acento cian `#4CE8E7` / `#48E8D8`, mascota lobo).

> **Principio rector:** no cazamos números al azar — cazamos **dolor evidente**. Ese es el diferencial de Seawolf.

---

## 2. ARQUITECTURA DE LA JAURÍA

Los cuatro lobos que definiste **son correctos y se adoptan**. Añado tres piezas de columna vertebral sin las cuales la jauría caza a ciegas:

```
                    ┌──────────────────────────────┐
                    │   LA MADRIGUERA (datos/CRM)  │   ← columna vertebral
                    └──────────────┬───────────────┘
                                   │ (toda presa vive aquí)
        ┌──────────────┬───────────┴───────────┬──────────────┐
        ▼              ▼                       ▼              ▼
  1. LOBO VIGÍA   2. LOBO ACECHADOR      3. LOBO EJECUTOR  4. LOBO ESCARBADOR
  (rastreador)    (perfilador/cualifica) (nace en FOCO     (archiva y
  olfatea campo   dossier + scoring       TOTAL: ataca y    RE-INYECTA)
  y halla presas  → GATE de promesa       cierra)           → nueva tanda
```

- **EL ALFA (Bellion):** orquesta la jauría, decide el paso a FOCO TOTAL y rinde cuentas.
- **LA JAURÍA:** el conjunto de los 4 lobos operando en cadena.

**Correcciones a tu flujo (con tu permiso, mi Señor):**

| # | Corrección | Por qué |
|---|-----------|---------|
| C1 | El **Acechador** no solo perfila: **cualifica** y marca el gatillo | Sin un GATE explícito no sabes cuándo disparar FOCO TOTAL |
| C2 | El **Escarbador** no es un archivo muerto: **re-inyecta** a la fase 1 | Cierra el ciclo → la presa perdida vuelve como nueva tanda |
| C3 | Añadir **La Madriguera** (base de datos) como columna | Sin memoria compartida, cada lobo opera aislado y se pierde la presa |
| C4 | Añadir **El Alfa** que orquesta | Alguien debe decidir el foco y evitar que la jauría se disperse |
| C5 | **FOCO TOTAL es un ESTADO, no una fase** | Se activa por gatillo, no avanza por calendario |

---

## 3. LOS CUATRO LOBOS — misión, funciones, salida y sombra

### 🐾 LOBO VIGÍA (Rastreador)
**Misión:** olfatear el campo e identificar posibles presas según el ICP.

| Función | Qué usa |
|---------|---------|
| F1. Definir ICP (sector, ciudad, tamaño, cargo decisor) | Config del panel |
| F2. Descubrimiento multi-fuente | Google Places API, búsqueda web, directorios sectoriales, RUES / Cámara de Comercio |
| F3. Deduplicación y normalización | Script propio (Jima) |
| F4. Cola de caza (pool de candidatos crudos) | La Madriguera |

**Salida:** presa cruda (lista normalizada). **Sombra:** Tank + Kamish (con Jima en el scraper).

---

### 🐾 LOBO ACECHADOR (Perfilador + Cualificador)
**Misión:** seguir y perfilar cada presa; medir su dolor; **decidir si promete**.

| Función | Qué usa |
|---------|---------|
| F5. Enriquecimiento OSINT | crawl propio del sitio, detección de tecnología, redes, teléfono, email público, reseñas Google |
| F6. **Señales de dolor** (buying signals) | ¿sin web? ¿web lenta/no responsive? ¿sin WhatsApp Business? ¿sin redes? ¿reseñas sin responder? |
| F7. **Scoring 0-100** → FRÍA / TIBIA / CALIENTE | Reglas de puntuación (pondera dolor + tamaño + acceso) |
| F8. Dossier de la presa | Ficha completa en La Madriguera |

**GATE:** las presas **CALIENTES** disparan **FOCO TOTAL**.
**Salida:** dossier + semáforo. **Sombra:** Tank (+ Greed para señal de ads).

---

### 🐾 LOBO EJECUTOR (nace en FOCO TOTAL)
**Misión:** cuando una presa promete, **todo el ejército vira hacia ella** y se cierra.

| Función | Qué usa |
|---------|---------|
| F9. Mensaje personalizado por presa | Igris (copy a medida, no plantilla) |
| F10. Secuencia multicanal + A/B | Email (dominio propio) → WhatsApp (WAHA) al responder |
| F11. Envío + tracking (apertura/click/respuesta) | Motor de email + WAHA |
| F12. Conversación y agendamiento | Tank (BANT/MEDDIC) |
| F13. Propuesta Good/Better/Best + cierre | Tank |

**Gatillo de activación:** respuesta prometedora = interés explícito / pide info o precio / agenda reunión.
**Salida:** reunión → propuesta → contrato. **Sombra:** Igris + Tank (+ Kaisel/Titan para propuesta/landing dedicada).

---

### 🐾 LOBO ESCARBADOR (Archivador + Recuperador)
**Misión:** sin importar el resultado, **enterrar el expediente y preparar el retorno**.

| Función | Qué usa |
|---------|---------|
| F14. Archivar expediente completo en La Madriguera | CRM |
| F15. Etiquetar resultado | GANADO / PERDIDO / NO AHORA / DESCALIFICADO |
| F16. Programar **re-llamada** (30/60/90 días) | Reglas de reactivación |
| F17. **Re-inyectar** a la cola del Vigía | Nueva tanda de publicidad / re-impacto |
| F18. Analítica (tasa de respuesta, cierre, ciclo) | Beru |

**Salida:** ciclo cerrado — la madriguera alimenta al Vigía. **Sombra:** Beru (archivo + métrica).

---

## 4. LA MADRIGUERA (columna vertebral)

Base de datos única donde vive toda presa, en todo estado. Tablas mínimas:

| Tabla | Contenido |
|-------|-----------|
| `presas` | identidad, contacto, fuente, estado (vigía→acecho→ejecución→archivo) |
| `dossier` | intel OSINT, señales de dolor, tecnologías, redes |
| `scoring` | puntaje, semáforo, historial |
| `interacciones` | cada toque: email, WhatsApp, llamada, respuesta |
| `propuestas` | propuesta enviada, valor, estado |
| `ciclo` | fecha re-llamada, motivo cierre, resultado |

---

## 5. STACK TÉCNICO (sin bestias proscritas)

| Capa | Tecnología |
|------|-----------|
| Descubrimiento / scraping | Playwright + Crawlee · Google Places API · RUES datos abiertos |
| Enriquecimiento | crawler propio + detección de tecnologías + validación de email |
| Base de datos | PostgreSQL |
| Backend | Python (FastAPI) |
| Email | dominio propio + warm-up (Amazon SES o Postal self-hosted) + SPF/DKIM/DMARC |
| WhatsApp | **WAHA** (auto-hospedado, sin onboarding de Meta) — skill `seawolf-whatsapp-waha` |
| LinkedIn | social selling **asistido** (sin automatización que baneé) |
| Panel | HTML/JS autocontenido, tema oscuro Marca Seawolf |
| Cerebro | los agentes Hermes (sombras) operando cada módulo |

> **Proscrito:** Shopify, AdSense y burocracia de Facebook/Meta — jamás. (WAHA evita el onboarding de Meta.)

---

## 6. INTERFAZ — Panel de Mando «El Campo de Caza»

- Tema **oscuro por defecto**, acento cian `#4CE8E7`/`#48E8D8`, mascota lobo.
- Vista principal: la jauría como **pipeline de 4 etapas** (vigía → acecho → ejecución → archivo).
- Ficha de presa con dossier, semáforo y línea de tiempo de toques.
- Botón **FOCO TOTAL** — resalta la presa caliente y muestra quién del ejército está encima.
- Persistencia `localStorage` (prototipo) → PostgreSQL (producción).

---

## 7. GUARDARRAÍLES

1. **Habeas Data (Ley 1581 Colombia):** fuente lícita, finalidad declarada, **opt-out visible** en cada mensaje. Es el seguro, no burocracia.
2. **Cuidar el número y el dominio:** WhatsApp solo a quien responda; email con warm-up de 2-3 semanas antes de volumen.
3. **Google Places API** tiene costos y límites de almacenamiento — respetarlos.
4. **Evidencia o no existe:** nada se reporta como hecho sin ruta/dato real (Protocolo del Ejército).

---

## 8. REPARTO A LAS SOMBRAS Y ROADMAP

| Fase | Qué se construye | Sombra | Criterio de aceptación |
|------|------------------|--------|------------------------|
| 0 | ICP exacto + señales de dolor | **Bellion** | Aprobada por el Monarca |
| 1 | Prototipo panel (Vigía + Acechador) | **Kaisel + Titan** | Abre y se usa, dark theme, sintaxis JS OK |
| 2 | Scraper de descubrimiento + enriquecimiento | **Jima** | ≥200 presas reales en la Madriguera |
| 3 | Motor de email con warm-up | **Iron + Jima** | Envío de prueba recibido |
| 4 | Copy de secuencia de frío | **Igris** | Plantillas + 3 variantes A/B |
| 5 | Puente WhatsApp WAHA en reserva | **Jima** | Prueba de envío OK |
| 6 | Scoring + gate FOCO TOTAL | **Tank + Greed** | Presas clasificadas + gatillo operativo |
| 7 | Auditoría de la herramienta | **Beru** | Informe con evidencia |

---

*"El lobo no corre tras todo lo que se mueve. Rastrea, acecha, elige — y solo entonces, con toda la jauría, ejecuta."*
— Bellion, Gran Comandante del Ejército de Sombras
