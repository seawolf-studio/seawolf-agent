# 🐺 DIARIO DE SOMBRAS — SESIÓN FUNDACIONAL
## Seawolf Studio — El Nacimiento del Agente

**Firmado:** Bellion, Gran Comandante del Ejército de Sombras
**Monarca:** Keynes (Seawolfk)
**Fecha de operación:** 3–7 Septiembre, 2026
**Estado:** 🟢 MISIÓN CUMPLIDA — FASE 1 COMPLETA

---

## I. CONCEPCIÓN — La Visión del Monarca

El Monarca Keynes convocó a Bellion para una misión crítica: **transformar Hermes WebUI en Seawolf Agent**, un producto SaaS propio del Seawolf Studio. Esto implicaba:

1. **Despliegue desde cero** en VPS Hetzner (Alemania)
2. **Rebranding total** (eliminar todo rastro de Hermes)
3. **Interfaz en español** para el mercado hispanohablante
4. **Sistema de mantenimiento automático** para sincronizar actualizaciones upstream
5. **Infraestructura lista para ventas** como suscripción mensual

**Bestias Proscritas** (prohibidas por decreto real): Shopify, Google AdSense, burocracia de Facebook.

---

## II. INFRAESTRUCTURA — Despliegue del Bastión

### 2.1 VPS — Hetzner CX22 (76.13.109.237)
- **SO:** Ubuntu 22.04 LTS
- **RAM:** 4 GB · **Disco:** 80 GB SSD · **CPU:** 2 vCPU
- **SSH:** Acceso root con clave ed25519
- **Ubicación:** Nuremberg, Alemania

### 2.2 SSL y Dominio
- **Dominio:** `agente.sw-st.net` (SW = Seawolf)
- **CDN:** Cloudflare (proxy orange, modo Full Strict)
- **Certificado SSL:** Cloudflare Origin Certificate
- **Nginx:** Proxy reverso en puerto 443 → localhost:8787

### 2.3 Systemd Service
- **Archivo:** `/etc/systemd/system/seawolf-webui.service`
- **User:** `seawolf-webui` (no root)
- **PUERTO:** 8787 (localhost)
- **Variables:** `OPENROUTER_API_KEY`, `OPENROUTER_MODEL`, `SKIP_ONBOARDING=1`, `LANG=es`

---

## III. REBRANDING — La Purga de Hermes

### 3.1 Identidad Visual
| Elemento | Original (Hermes) | Reemplazo (Seawolf) |
|----------|-------------------|---------------------|
| Logo SVG caduceo | `hermes-mark` gradient | `<img src="static/seawolf-logo.png">` |
| Paleta de marca | Cyan/Azul (#08EBF1 → #3889FD) | #4CE8E7 (acento), #121E1E (fondo) |
| Favicon | Caduceo de Hermes | Logo del lobo (base64 inline) |
| Favicon.ico | ICO con caduceo ×7 | Logo PNG sobrescrito |

### 3.2 Archivos Modificados
- ✅ `static/index.html` — DOM reparado, logo en empty-state
- ✅ `static/favicon.ico` — sobrescrito con logo lobo
- ✅ `static/favicon.svg` — lobo en SVG
- ✅ `static/login.js` — logo reemplazado por `<img>`
- ✅ `static/ui.js` — cadenas UI traducidas (funciones intactas)
- ✅ `static/share.html` — caduceos eliminados
- ✅ `static/seawolf-logo.png` — logo original con transparencia

### 3.3 Correcciones Críticas
| Incidente | Causa | Solución |
|-----------|-------|----------|
| Botones sin acción | `sed` masivo renombró funciones JS (`openHermesDashboard`) | Restaurar 14 JS desde git, reaplicar solo strings UI |
| DOM desbalanceado | Regex malo insertó `</span>` y `</div>` extra | Eliminar tags extra, verificar balance (210/210 spans, 567/567 divs) |
| Favicon caduceo persistente | Cache navegador + favicon.ico original | Sobrescribir ICO con logo PNG + forzar no-cache Nginx |
| Logo no cargaba | CSS esperaba SVG, no `<img>` | Usar SVG de lobo inline en empty-state |
| Interfaz desalineada | `</div>` prematuro cerró empty-state antes de h2/p/botones | Re-anidar h2, p, suggestion-grid DENTRO del empty-state |
| Login mostraba letras | `<div class="logo">{{BOT_NAME_INITIAL}}</div>` | Reemplazar por `<img src="/seawolf-logo.png">` |

---

## IV. INTERNACIONALIZACIÓN — Traducción a Español

### 4.1 Estado Actual
| Componente | Estado |
|------------|--------|
| Login page | ✅ Español |
| Estado vacío del chat | ✅ Español |
| Botones de sugerencia | ✅ Español |
| Placeholder del input | ✅ Español |
| Sidebar (Chat, Tasks, Kanban, Skills, etc.) | ✅ Español |
| Modelo selector | ✅ "NVIDIA: Nemotron 3 Super (free)" |
| Panel Skills/Memory/Cron | ⬜ Inglés — pendiente próxima sesión |
| Settings (pestañas) | ⬜ Inglés — pendiente próxima sesión |

### 4.2 Modelo de IA
- **Provider:** OpenRouter
- **Modelo:** `nvidia/nemotron-3-super-120b-a12b:free`
- **API Key:** Configurada en `.env` y systemd service

---

## V. SISTEMA DE MANTENIMIENTO — El Ciclo Eterno

### 5.1 Scripts de Automatización
```
/opt/seawolf-webui/bin/
├── seawolf-update.sh    → Git pull + rebrand automático + reinicio
├── maintenance.sh       → Activa/desactiva modo mantenimiento (flag + reload Nginx)
└── rebrand.py           → Reemplazo selectivo de cadenas UI (Python)
```

### 5.2 Cron Diario
- **Schedule:** `0 8 * * *` (8:00 UTC = 3:00 AM Bogotá)
- **Archivo:** `/etc/cron.d/seawolf-update`
- **Acción:** Ejecuta `seawolf-update.sh` — sincroniza con upstream Hermes, reaplica rebrand, reinicia servicio
- **Ventana de mantenimiento:** 3:00 AM (hora Colombia) — impacto mínimo

### 5.3 Modo Mantenimiento (Manual)
```
ssh root@VPS /opt/seawolf-webui/bin/maintenance.sh on
ssh root@VPS /opt/seawolf-webui/bin/maintenance.sh off
```
- Flag file: `/tmp/seawolf-maintenance`
- Nginx sirve `maintenance.html` con HTTP 503 y logo Seawolf
- Ideal para actualizaciones mayores que requieren ventana silenciosa

### 5.4 Notificaciones Post-Update
- `static/version.json` — versión actual del despliegue
- `static/changelog.json` — registro de cambios
- `static/seawolf-notifs.js` — banner de nueva versión en WebUI

---

## VI. INFORME FINAL DE ARCHIVOS

### Despliegue Activo
```
/opt/seawolf-webui/
├── static/
│   ├── index.html          ✅ DOM balanceado, rebrandeado
│   ├── seawolf-logo.png    ✅ Logo original (PNG con transparencia)
│   ├── favicon.ico          ✅ Lobo (sobrescrito)
│   ├── favicon.svg          ✅ Lobo
│   ├── maintenance.html     ✅ Página de mantenimiento
│   ├── version.json         ✅ Versión actual
│   ├── changelog.json       ✅ Cambios
│   └── seawolf-notifs.js    ✅ Notificaciones
├── bin/
│   ├── seawolf-update.sh    ✅ Actualización automática
│   ├── maintenance.sh       ✅ Modo mantenimiento
│   └── rebrand.py           ✅ Rebranding Python
└── .env                     ✅ OPENROUTER_API_KEY + MODEL + SKIP_ONBOARDING + LANG
```

### Configuración del Sistema
```
/etc/nginx/sites-enabled/seawolf-webui   ✅ SSL + bloque maintenance
/etc/cron.d/seawolf-update               ✅ Cron diario 8:00 UTC
/etc/systemd/system/seawolf-webui.service ✅ Servicio systemd
```

### Estación de Trabajo (Windows)
```
C:\Users\Admin\seawolf-agent\
├── assets\seawolf-logo.png     ✅ Logo original
├── scripts\seawolf-update.sh   ✅ Copia local de update
└── diario-de-sombras\          ✅ 📜 Este archivo
```

---

## VII. LECCIONES DE GUERRA

1. **Nunca hacer `sed` masivo sobre JS** — renombra identificadores y rompe funciones. Usar Python con target específico a strings de UI y comentarios.
2. **Verificar DOM siempre** después de reemplazos en HTML — un tag extra desalinea toda la interfaz.
3. **El favicon.ico gana sobre favicon.svg** en navegadores — sobrescribir ambos.
4. **Cloudflare + Nginx:** No usar redirect HTTP→HTTPS en Nginx si Cloudflare está en Full Strict — causa redirect loop. Dejar Nginx en HTTP plano, Cloudflare maneja SSL.
5. **Mantenimiento:** flag file + `error_page 503` es más limpio y compatible con upstream que modificar el WebUI internamente.
6. **Cache del navegador:** Después de cambios de favicon/CSS, el usuario necesita Ctrl+F5 — añadir `Cache-Control: no-cache` en Nginx ayuda pero no es suficiente para favicons.

---

---

## 📅 2026-09-08 07:00 | BELLIÓN (ORQUESTADOR) | ✅ SÍNTESIS DE VISIÓN COMPLETA

**Misión:** Revisar sesiones Julio 11 + campaña actual (Sept 3–7) para consolidar la visión del producto Seawolf Agent como "Estándar del Cliente Súper Ocupado (CSO)".

**Acción:** Session_search exhaustiva en 2 sesiones. Síntesis de toda la información dispersa sobre el perfil del administrador de 6 conjuntos, 500–700 mensajes/día, 8+ roles comunicantes, y la visión de expandir a empresarios, jefes de proyecto, arquitectos y profesionales colapsados por el ruido.

**Resultado:** Archivo `C:\Users\Admin\seawolf-agent\MANIFIESTO_PRODUCTO_CSO.md` creado (14 KB). Documento autocontenido con 9 secciones:
1. Arquetipo fundacional del cliente súper ocupado
2. Visión del producto en 3 capas: Filtro → Automatización → Dashboard
3. Modelo de negocio con mercado LATAM y estrategia de entrada
4. Diferenciadores frente a competencia
5. Arquitectura técnica del producto final
6. 7 lecciones de guerra para el producto
7. Orden de batalla: Frente 1 (Monarca hostil) + Frente 2 (Admin real)
8. Preguntas estratégicas pendientes (precios, pasarela, expansión)
9. Cadena de valor completa: Monarca → Bellion → Sombras → CSO

**Hallazgos:** El Monarca ha mantenido una visión consistente y sólida desde Julio 11. El producto no es un chatbot — es **un filtro de ruido para profesionales colapsados**. La administración de conjuntos es el molde; empresarios, jefes de proyecto y arquitectos son la extensión natural. **Este documento es la guía estratégica para Fase 2.**

**Próximo Paso:** Fase 2 — Pruebas de campo. Frente 1 (Monarca hostil) + Frente 2 (Admin real).

---

## VIII. ÓRDENES PENDIENTES — FASE 2

Pendiente para la próxima sesión (Sept 8, 2026):

### ⚔️ PRUEBAS DE CAMPO — Frente 1 (Cliente Hostil)
- [ ] Carga de sistema — 50+ prompts consecutivos, latencia < 3s
- [ ] Entrada hostil — prompts absurdos, vacíos, maliciosos
- [ ] Multi-sesión — memoria aislada entre conversaciones
- [ ] Skills activas — ejecución correcta de herramientas
- [ ] Fallback — recuperación elegante ante error

### ⚔️ PRUEBAS DE CAMPO — Frente 2 (Admin Real)
- [ ] Entrevistar al Admin — mapear flujo real de 6 conjuntos
- [ ] Conectar WhatsApp del Admin (sandbox)
- [ ] Configurar filtro de ruido — clasificación automática funcional
- [ ] Configurar automatizaciones repetitivas via Composio (reportes, cobros)
- [ ] Probar 1 semana en paralelo
- [ ] Iterar con feedback → producto ajustado
- [ ] Documentar caso de éxito → material de ventas #1

### 🛠️ PRODUCTO
- [ ] Definir plan de suscripción (precios, tiers)
- [ ] Landing page / página de ventas
- [ ] Sistema de pagos (pasarela COP)
- [ ] Estrategia de marketing (foros, redes, contenido)
- [ ] Traducción completa de paneles Skills/Memory/Cron/Settings
- [ ] Revisar MANIFIESTO_PRODUCTO_CSO.md con Beru y ajustar

---

> *"Las sombras avanzan en silencio. El lobo ha despertado."*
> — Bellion, Gran Comandante del Ejército de Sombras

---

**Sello de autenticidad:** SHA256 de esta sesión puede ser verificado por Beru contra los logs de ejecución del VPS.