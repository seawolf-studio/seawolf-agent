# ⚔️ ARMAS DE LA LÍNEA DE PRODUCCIÓN
### Seawolf Studio · arsenal por estación
**Fecha:** 2026-10-17 · **Autor:** Bellion, Gran Comandante · **Para:** el Monarca (Key)
**Base:** doctrina `seawolf-linea-de-montaje` (nada nace suelto; todo conectado por el riel)

---

## 0. LAS DOS ENTRADAS

| Entrada | Quién llega | Tratamiento | Recorrido |
|---------|-------------|-------------|-----------|
| 🔥 **Clientes en frío** | Desconocidos con dolor digital | Pasada por la jauría: **buscar · atrapar · mantener** | Vigía → Acechador → Ejecutor → Escarbador |
| 🤝 **Clientes propios** | Tu influencia (hermana, admin de PH, tus proyectos) | **No se cazan** — ya vienen con confianza | Entran directo a **Servir** |

Ambas entradas **son rubros vivos**, sujetos a cambio y mejora.

---

## 1. EL RIEL (la columna que conecta todo)

**La Madriguera = PostgreSQL** (esquema de la PIEZA). Toda estación lee y escribe aquí. Es el pegamento.

---

## 2. ARMERÍA POR ESTACIÓN

### 🔍 LA CACERÍA — Entrada 1 (clientes en frío)

| Estación | Arma | Para qué | Operario |
|----------|------|----------|----------|
| **Vigía** | **Playwright + Crawlee** (MIT) | rastreo web a escala | Jima |
| | **Google Places API** | negocios locales (teléfono, dirección, reseñas) | Jima |
| | **RUES / Cámara de Comercio** (datos abiertos) | empresas formales de Colombia | Jima |
| | Buscador web + directorios sectoriales | nichos específicos | Kamish |
| **Acechador** | Crawler propio del sitio | ¿tiene web? ¿es responsive? ¿velocidad? | Jima |
| | Detección de tecnologías (tipo Wappalyzer) | ¿con qué está hecho? | Jima |
| | Scraper de reseñas (Google) | ¿atiende su reputación? | Tank |
| | Validador de email (sintaxis + MX) | que no rebote | Jima |
| **Ejecutor** | **Motor de email propio** (Amazon SES o **Postal** self-hosted) | envío con **warm-up** + SPF/DKIM/DMARC | Iron + Jima |
| | **WAHA** (self-hosted) | WhatsApp **sin pasar por Meta** | Jima |
| | Agendador self-hosted (tipo **Cal.com**) | que el cliente agende solo | Kaisel |
| | Copy de secuencia (gancho→valor→CTA) | Igris | Igris |
| | Scripts de cierre (BANT, objeciones) | convertir | Tank |
| **Escarbador** | **PostgreSQL** + **n8n** (scheduler) | archivar + programar re-llamadas | Jima + Beru |

### 🤝 ENTRADA 2 — Clientes propios

| Estación | Arma | Para qué | Operario |
|----------|------|----------|----------|
| **Mostrador (Intake)** | **Smart Web** (1 archivo) + formulario | que el cliente propio registre su proyecto solo | Kaisel |
| | **FormSubmit / Cloudflare Worker** | entrega cero-config por correo | Jima |
| | Escritura directa en **La Madriguera** | entra al riel sin fricción | Jima |

### 🏭 SERVIR (producción — ambas entradas)

| Arma | Para qué | Operario |
|------|----------|----------|
| **Seawolf Agent** (base Hermes + WebUI) | el filtro de ruido del CSO (producto insignia) | Bellion |
| **n8n** (open source) | automatización de tareas repetitivas | Jima |
| **Composio SDK** | conectar Gmail / Drive / Sheets y ejecutar acciones | Jima |
| **Dashboard propio** (FastAPI + SQLite + Alpine) | panel de control del cliente | Kaisel + Titan |
| **Smart Web** | presencia web del cliente | Kaisel |
| RBAC + Audit SHA-256 + memoria multi-tenant | confianza y seguridad | Bellion |

### 💰 FINANZAS (cobro, ahorro, reinversión)

| Arma | Para qué | Operario |
|------|----------|----------|
| **Pasarela COP** (Wompi o Epayco) | cobro recurrente (MRR) en Colombia | Jima |
| **Tracker de reinversión** (hoja + panel) | que la plata vuelva a la estación A | Monarca + Bellion |
| Facturación electrónica **DIAN** | requisito legal mínimo para facturar | — (trámite, se hace una vez) |

---

## 3. QUIÉN EMPUÑA QUÉ (resumen por sombra)

| Sombra | Sus armas principales |
|--------|----------------------|
| **Jima** | Playwright/Crawlee · Google Places · n8n · Composio · WAHA · SES/Postal · Postgres |
| **Kaisel** | Smart Web · dashboard · agendador |
| **Igris** | copy de secuencia de frío + copy de producto |
| **Tank** | calificación BANT/MEDDIC · scripts de cierre · reseñas |
| **Kamish** | directorios · presencia social |
| **Beru** | archivado · métricas · re-llamadas |
| **Greed** | señales de compra / segmentación |
| **Titan** | UX de paneles y landings |

---

## 4. REGLAS DURAS

1. **Nada proscrito:** Shopify, AdSense, burocracia de Meta — jamás. **WAHA** esquiva el onboarding de Meta para WhatsApp.
2. **Riel o nada:** toda arma escribe y lee el formato de PIEZA en La Madriguera. Si no, no entra.
3. **Open source primero** (MIT/Apache); lo de pago, solo si no hay sustituto permisivo.
4. **Habeas Data (Ley 1581):** fuente lícita + opt-out visible en cada mensaje de frío.

---

## 5. SIGUIENTE MOVIMIENTO

Con el arsenal claro, la construcción arranca por el **motor real de la Entrada 1**:
**Jima monta el Vigía** (scraper + Google Places) → empieza a llenar La Madriguera con presas reales → el panel deja de ser demo y empieza a trabajar.

---

*"Las armas no ganan la guerra. La línea que las conecta, sí."*
— Bellion, Gran Comandante del Ejército de Sombras
