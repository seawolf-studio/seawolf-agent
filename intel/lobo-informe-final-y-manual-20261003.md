# LOBO — INFORME FINAL Y MANUAL DE USO
## Del prototipo a producto: qué es, cómo está y cómo se usa (base del manual del cliente)

**Fecha:** 2026-10-03 · **Clasificación:** CRÍTICO — Uso Interno Seawolf Studio
**Elaborado por:** Bellion, Gran Comandante · **Para:** el Monarca (Key)
**Base tecnológica:** CopilotKit/OpenMuse (MIT) + motor propio · **Marca:** LOBO (Seawolf Studio)
**Despliegue:** VPS Hostinger `76.13.109.237` · Ubuntu 24.04

---

## 1. Resumen ejecutivo

**LOBO** es el **agente personal** de Seawolf Studio: un asistente que **escucha, piensa y habla**, corre **24/7 desde el servidor** (sin depender de la GPU del cliente ni de servicios cerrados) y está pensado para el **Cliente Súper Ocupado (CSO)**: empresarios, jefes de proyecto y profesionales no técnicos.

En **poco más de 3 días** se construyó lo que estaba planificado para **2 semanas**:
- Se eliminaron los **dos riesgos mortales**: el servicio cerrado de CopilotKit Intelligence y el *lock-in* de proveedor → **persistencia propia** + **gateway único de modelos** (OpenRouter).
- Se añadieron **memoria** (semántica + temporal), **voz** y **marca LOBO** completa (incluida mascota y tema oscuro por defecto).

**Estado:** ~90% listo para uso propio y para pruebas con clientes. Lo que resta son **minucias de acabado** y las fases de *producto vendible* (conectores ampliados, multi-tenant, cobro).

---

## 2. Qué es LOBO

- **Nombre:** LOBO — acróstico de marca: **L**ibera tu tiempo · **O**rdena tu día · **B**rinda calma · **O**bra por ti.
- **Mascota:** lobo negro estilo peluche 3D (transparente).
- **Colores:** `#121E1E` (fondo), acentos `#4CE8E7` / `#48E8D8`.
- **Modo por defecto:** **OSCURO** (con opción clara).
- **Constantes de marca:** modo claro/oscuro + **sello de unidad social** (diferencial frente a otros productos).
- **Arquitectura (resumen):**
  - **Front:** app React Native/Expo (versión web servida en el VPS).
  - **Back:** servidor TypeScript (puerto 8788) con persistencia propia en **PostgreSQL + pgvector**.
  - **Modelo:** **OpenRouter** como única puerta (chat gratis; fondo muy económico).
  - **Voz:** gateway por frases → VoiceBox (TTS).
  - **Memoria:** **Mem0** (semántica) + **Graphiti/Neo4j** (temporal).
  - **Servicios systemd:** `nereus-api`, `nereus-web`, `nereus-mem0`, `nereus-graphiti`, `seawolf-fw`.

---

## 3. Estado por fases

| Fase | Descripción | Estado |
|---|---|---|
| 0 | Clonado + build (Node 24, pnpm) | ✅ 100% |
| 1 | Persistencia propia (Postgres+pgvector, dual-mode) | ✅ 100% |
| 2 | Gateway OpenRouter (modelos gratis/baratos) | ✅ 100% |
| 3 | Voz (VoiceBox + gateway por frases + systemd) | ✅ ~85% (falta voz en el PC del cliente) |
| 4 | Memoria (Mem0 semántica + Graphiti temporal) | ✅ 100% |
| 5 | Conectores (Composio: Gmail/Calendar/herramientas) | ⏳ pendiente |
| 6 | OCR + Push | ⏳ pendiente |
| 7 | Continuidad multiplataforma | ⏳ pendiente |
| 8 | Avatar (Rive) | ⏳ pendiente |
| 9 | Multi-tenant + marca + despliegue | 🟡 marca y despliegue OK; **multi-tenant pendiente** |

---

## 4. MANUAL DE USO — paso a paso por función

> Esta sección es la **base del manual del usuario final**. Cada función: qué hace, cómo se usa.

### 4.1 Entrar (acceso)
1. Abra la app (en pruebas: la URL servida por el túnel/VPS).
2. En la pantalla de bienvenida (**"Bienvenido a LOBO"**) escriba la **Clave de acceso**.
3. Pulse **"Abrir espacio"**. Si la clave es válida, entra a su espacio de trabajo.

*Nota técnica:* en producción cada cliente tendrá **su propia cuenta** (pendiente Fase 9).

### 4.2 Cambiar el tema (claro / oscuro)
1. En el encabezado, pulse el botón **Sol/Luna** (arriba a la derecha).
2. Alterna **oscuro ↔ claro**. El oscuro es el **predeterminado**.

### 4.3 Chat (la función principal)
1. Entre a la pestaña **Chat**.
2. Escriba su petición en lenguaje normal (ej.: *"Ayúdame a planificar mi día"*).
3. LOBO responde y, si hace falta, **delega trabajo en el servidor** (continúa aunque cierre la app).
4. **Adjuntar documento:** pulse el botón de adjuntar; puede importar un **PDF** para usarlo en la conversación.
5. **Conversaciones:** el botón **menú (☰)** abre la lista de conversaciones (hilo principal + laterales).

### 4.4 El Agente (identidad)
1. Vaya a **Apps y configuración → Tu agente**.
2. Puede editar: **nombre** del agente, **tono** y **avatar/mascota**.
3. Guarde. El nombre aparece **bajo la mascota** en el encabezado.

### 4.5 Actividad (tareas y aprobaciones)
1. Pestaña **Actividad**.
2. Muestra los **planes y resultados** del trabajo delegado, con su **progreso paso a paso**.
3. Cuando una acción requiere su permiso, aparece **"Listo para revisar"**: revise **la acción y la cuenta exactas** antes de aprobar.
4. Puede **aprobar**, **editar** o **descartar**.

### 4.6 Ideas
1. Pestaña **Ideas**.
2. LOBO propone **próximos pasos útiles** basados en su mundo (correo, calendario, tareas).
3. Pulse una idea para convertirla en acción.

### 4.7 Metas
1. Pestaña **Metas**.
2. Cree una meta (ej.: *"Crear un fondo de emergencia de tres meses"*).
3. LOBO da **seguimiento** y guarda el progreso.

### 4.8 Vigilancia (monitores)
1. Desde el chat o la sección del agente, pida **vigilar** algo (ej.: *"Avísame cuando haya una mesa en mi restaurante favorito"*).
2. LOBO **compara** con la última observación y **avisa** cuando hay un cambio importante.

### 4.9 Apps y conectores
1. Pestaña **Apps**.
2. Vea **conexiones y capacidades** disponibles, y **lo que el agente recuerda**.
3. Conecte sus servicios (Google/correo/calendario) cuando estén disponibles.

### 4.10 Correo
1. Vaya a **Correo**.
2. Lea **hilos**, busque en la bandeja y abra conversaciones.
3. LOBO puede **redactar** y proponer respuestas.

### 4.11 Calendario
1. Vaya a **Calendario**.
2. Vea **eventos**, próximos días y **calendarios**.
3. Cree o edite eventos; LOBO avisa de **solapamientos**.

### 4.12 Navegador
1. Vaya a **Navegador**.
2. LOBO tiene **sesiones de navegación privadas y persistentes** (para leer/actuar en páginas públicas).
3. Puede **abrir**, **leer**, **navegar** y **ver** la sesión.

### 4.13 Archivos y PDF
1. Vaya a **Archivos**.
2. Aquí viven sus **documentos, formularios y copias rellenadas**.
3. LOBO puede **rellenar** un formulario PDF y guardar la copia.

### 4.14 Equipo (workspace Linux del agente)
1. Entre a **Equipo** (Computer).
2. Es un **espacio Linux** donde el agente **trabaja** (crea/edita archivos).
3. Usted puede **tomar el control** cuando lo necesite.

### 4.15 Voz
1. LOBO puede **hablar por frases** (gateway de voz → VoiceBox en el servidor).
2. En pruebas, la voz se genera en el VPS; llevarla al equipo del cliente es parte del pendiente.

### 4.16 Notificaciones
1. El botón **campana** (arriba a la derecha) muestra **novedades** y avisos.
2. Se marca su lectura; el contador indica pendientes.

### 4.17 Memoria
1. LOBO **recuerda** hechos suyos (memoria **semántica**) y **relaciones en el tiempo** (memoria **temporal**).
2. En **Contexto** puede **inspeccionar, corregir u olvidar** lo que recuerda.

---

## 5. Operación técnica (para el equipo)

- **Servicios:** `systemctl status nereus-api nereus-web nereus-mem0 nereus-graphiti`
- **Salud:** `curl http://127.0.0.1:8788/api/health`
- **Modelos:** se cambian en `.env` (`MODEL=openrouter/...`); chat gratis, fondo económico.
- **Reinicio de fábrica (limpiar pruebas antes de vender):** `bash /opt/nereus/reset-lobo.sh`
  → borra estado (records + Mem0 + Neo4j), deja **respaldo** y reinicia servicios.
- **Respaldo de datos:** `docker exec nereus-postgres pg_dump -U nereus -d nereus > respaldo.sql`

---

## 6. Pendientes honestos
1. **Multi-tenant real** (cada cliente con su cuenta y datos aislados) → Fase 9.
2. **Conectores** (Composio: Gmail/Calendar/WhatsApp) → Fase 5.
3. **Voz en el equipo del cliente** (VoiceBox local) y **avatar** → Fases 3/8.
4. **Cobro/suscripción** (no estaba en el roadmap; es imprescindible para vender).
5. **Acabado**: revisar los textos internos que quedan en inglés (por diseño del motor).
