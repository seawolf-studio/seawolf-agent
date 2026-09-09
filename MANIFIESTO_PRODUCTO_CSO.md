# 🐺 MANIFIESTO DEL PRODUCTO — SEAWOLF AGENT
## El Estandar del Cliente Súper Ocupado

**Compilado por:** Bellion, Gran Comandante del Ejército de Sombras
**Monarca:** Keynes (Seawolfk)
**Basado en:** Sesiones fundacionales (Julio 11 → Septiembre 8, 2026)
**Clasificación:** Doctrina de Producto — Prioridad Máxima

---

# 📋 RESUMEN EJECUTIVO

Seawolf Agent no es un asistente genérico. Es un **filtro inteligente de ruido + automatizador de tareas repetitivas** para un perfil de cliente muy específico: **personas excelentes en su trabajo que colapsan bajo el peso de la comunicación y la administración diaria.**

El primer caso real —el **Administrador de 6 Conjuntos Cerrados** que recibe 500–700 mensajes diarios por WhatsApp— no es un cliente más. Es el **arquetipo fundacional** del que deriva toda la estrategia de producto.

---

# 1. EL ARQUETIPO: CLIENTE SÚPER OCUPADO (CSO)

## 1.1 Perfil

| Atributo | Descripción |
|----------|-------------|
| **Rol real** | Administrador de conjuntos cerrados |
| **Equivalencias** | Empresario, Jefe de Proyecto, Arquitecto, Gerente, Director de operaciones |
| **Valor** | Muy bueno en su dominio, indispensable para su organización |
| **Problema** | Se ahoga en mensajes, correos, reportes, coordinación — el **ruido** le consume el tiempo |
| **Canales** | WhatsApp (primario), Email, Grupos, Llamadas |
| **Volumen** | 500–700+ interacciones/día |
| **Dolor** | Lo urgente siempre mata lo importante |
| **Lo que necesita** | Que alguien filtre, priorice, automatice — sin perder el control |

## 1.2 El Administrador Original — Caso Fundacional

> *"El administrador es un tipo muy ocupado, usa WhatsApp como centro de operaciones, maneja 6 conjuntos, recibe mensajes de todo tipo — propietarios, arrendatarios, guardas, personal de aseo, asistentes, consejeros, proveedores, revisor fiscal, contador. Calculo 500 a 700 mensajes diarios."*
> — El Monarca, Septiembre 2026

**Roles con los que se comunica (8+ frentes):**

- 🏠 **Propietarios** — Quejas, solicitudes, pagos
- 🔑 **Arrendatarios** — Entradas, problemas, renovaciones
- 🛡️ **Guardas de seguridad** — Reportes de ingreso/egreso, incidentes
- 🧹 **Personal de aseo** — Programación, suministros, novedades
- 📋 **Asistentes** — Coordinación diaria
- 👥 **Consejeros** — Decisiones administrativas
- 📦 **Proveedores** — Cotizaciones, servicios, mantenimiento
- 💼 **Revisor Fiscal / Contador** — Reportes financieros, recaudos

**6 conjuntos cerrados** → cada uno con su propio censo, parqueaderos, zonas comunes, ingresos, egresos, reservas, cobros.

## 1.3 Estandarización para CSO

| Cliente Original | Extensión (CSO) |
|-----------------|-----------------|
| Administrador de conjuntos | **Empresario** — correos, reuniones, decisiones |
| — | **Jefe de Proyecto** — Jira, Slack, sprints, stakeholders |
| — | **Arquitecto** — planos, clientes, constructor, proveedores |
| — | **Gerente de operaciones** — múltiples sedes, reportes, incidencias |
| — | Cualquier profesional que sea **demasiado bueno para estar respondiendo mensajes toda la mañana** |

---

# 2. LA VISIÓN DEL PRODUCTO (TRES CAPAS)

## 2.1 FILTRO — La Capa Base

**Problema:** 700 mensajes. Solo 70 requieren acción real. El admin pierde 3 horas leyendo, clasificando y respondiendo ruido.

**Solución (Seawolf Agent = Filtro Inteligente):**

> El agente **se conecta a WhatsApp** (y luego Email, Slack, etc.), clasifica automáticamente cada mensaje entrante y **eleva solo lo que requiere atención**.

| Clasificación | Ejemplo | Qué hace el Agente |
|:--------------|:--------|:-------------------|
| 🟢 Informativo | "Señor, ya llegó el gas" | ✅ Archivar + notificar si es relevante |
| 🟡 Consulta simple | "¿Hasta qué hora está el sauna?" | ✅ Responder automático si hay data |
| 🟠 Requiere acción | "Se dañó la bomba del agua en el Conjunto 2" | 🔔 Priorizar al admin + sugerir acción |
| 🔥 Urgente | "Se fue la luz en todo el conjunto" | 🚨 Alerta inmediata + protocolo |

## 2.2 AUTOMATIZACIÓN — La Capa Media

**Problema:** Tareas repetitivas consumen tiempo valioso — reportes diarios, cobros de parqueadero, préstamos de zonas comunes, censo de ingresos.

**Solución (Composio + Agente):**

> Tareas que el admin hace a diario → el agente las ejecuta autónomamente.

| Tarea | Automatización | Estado |
|:------|:---------------|:-------|
| Reporte diario de ingresos/egresos | Generado automático 7 PM | ✅ Factible |
| Cobro de parqueadero visitas | Cálculo + registro al salir | ✅ Factible |
| Préstamo de zonas comunes | Reserva + cobro automático | ✅ Factible |
| Censo de residentes | Actualización vía formulario + validación | ✅ Factible |
| Alerta de morosidad | Detección + notificación admin | ⚙️ En diseño |
| Backup diario a Drive | Google Drive API (Composio) | ✅ Factible |

## 2.3 DASHBOARD — La Capa de Control

**Problema:** El admin necesita ver el estado real de sus 6 conjuntos sin abrir 20 chats de WhatsApp.

**Solución (Dashboard COP, Tiempo Real):**

> Un panel donde el administrador ve, en lenguaje natural o numérico, lo que importa.

El Dashboard que ya construimos para el Conjunto Cerrado sirve como **template del producto final**:
- 🏘️ Censo (residentes, mascotas, vehículos)
- 🅿️ Parqueaderos y cobros
- 🏊 Zonas Comunes (sauna, salones, guardería, juegos)
- 💰 Recaudos en tiempo real (COP)
- 🚗 Ingreso/salida de vehículos
- 📊 Reportes exportables

**RBAC demostrado:** Creador → Admin → Auxiliar → Operativo — se replica en cualquier vertical.

---

# 3. EL MODELO DE NEGOCIO

## 3.1 La Tesis

> **Una persona súper ocupada paga $50-100/mes con gusto por ahorrarse 3 horas diarias de ruido.**

Esto no es un chatbot. Es un **producto de productividad vertical** para un segmento que:
1. Tiene **presupuesto** (es indispensable para su organización)
2. Tiene **dolor medible** (horas perdidas en ruido)
3. Tiene **alta retención** (una vez configurado, no lo sueltan)
4. Es **replicable** (miles de administradores, empresarios, jefes de proyecto en LATAM)

## 3.2 Mercado Potencial Inmediato

| Sector | Perfil CSO | Mercado LATAM |
|--------|-----------|---------------|
| 🏘️ Administración de conjuntos | Administrador de propiedad horizontal | **+200,000** conjuntos en Colombia |
| 🏗️ Construcción | Arquitecto / Residente de obra | **+50,000** profesionales |
| 💼 Empresas Pyme | Gerente general | **+3 millones** de PYMEs en LATAM |
| 📐 Ingeniería | Jefe de proyecto | **+100,000** profesionales |
| 🏥 Salud | Administrador de clínica pequeña | Nicho vertical |

## 3.3 Estrategia de Entrada

```
FASE 1 (Ahora):  Un cliente real → El Administrador
                 ✅ Producto validado en un caso real
                 ✅ Testimonios y caso de éxito
                 ✅ Ajustes con feedback real

FASE 2 (Mes 1): 5 clientes → Conjuntos cerrados
                 ✅ Landing page + precios
                 ✅ Onboarding semi-automatizado
                 ✅ Primeros $500/mes MRR

FASE 3 (Mes 3): 20+ clientes → Multi-vertical
                 ✅ Expansión a otros perfiles CSO
                 ✅ Automatización de onboarding
                 ✅ Equipo de soporte (Tank + Iron)
```

---

# 4. DIFERENCIADORES CLAVE

| Frente | Seawolf Agent vs... | Competencia |
|:-------|:--------------------|:------------|
| **Filtro WhatsApp** | Clasifica INTELIGENTEMENTE no solo responde | Bots de respuestas automáticas genéricos |
| **Composio Integrado** | Ejecuta acciones (cobrar, reservar, reportar) | Solo respuestas, sin backend ejecutor |
| **Español Nativo** | Entiende modismos colombianos | Entrena con datasheets en inglés |
| **Dashboard Tiempo Real** | Visualiza el negocio completo | Solo chat, sin contexto de gestión |
| **Verticalizado** | Hecho para su industria específica | Asistente general sin especialización |
| **Setup 1-Click** | Configurado en minutos | Horas de integración técnica |

---

# 5. ARQUITECTURA TÉCNICA (Para el Producto Final)

```
WhatsApp ─→ Seawolf Agent (VPS) ─→ Filtro IA ─→ Admin (lo importante)
    │                                  │
    │                           Automatizaciones
    │                                  │
    └──── Composio ────────────→  Dashboard
          Gmail/Drive/Sheets      Tiempo Real
          API Conjuntos           Reportes COP
```

| Componente | Tecnología | Estado Actual |
|:-----------|:-----------|:--------------|
| **Agente IA** | OpenRouter (Qwen/Nemotron) → VPS | ✅ Live en agente.sw-st.net |
| **WebUI** | WebUI rebrandeada, español, logo lobo | ✅ Funcional |
| **Composio** | SDK Python (Gmail+ activo) | ✅ Conectado |
| **Dashboard** | FastAPI + SQLite + Alpine.js | ⚠️ Base construida, requiere UI estable |
| **WhatsApp** | Composer + API (pendiente integrar) | 📋 Pendiente |
| **Payments** | Pasarela COP (pendiente definir) | 📋 Pendiente |

---

# 6. LECCIONES DE GUERRA (Para el Producto)

Extraídas de la campaña completa (Julio → Septiembre 2026):

1. **El cliente súper ocupado no tiene tiempo para explicarte su problema dos veces.** La primera interacción debe resolver algo.
2. **WhatsApp es el canal. No el email, no el portal web.** En LATAM, el negocio vive en WhatsApp.
3. **Filtrar ruido es más valioso que responder preguntas.** El admin sabe la respuesta; lo que no sabe es qué merece su atención ahora.
4. **El producto se vende con una demo real del Admin, no con un brochure.** "Mira, esto le ahorra 3 horas diarias a Fulano" > cualquier landing page.
5. **Los 5 diferenciadores del Agente** (Memoria multi-tenant, Audit Trail SHA-256, RBAC, Español nativo, Setup 1-click) **son armas de venta**, no features técnicos.
6. **No competir con ChatGPT.** Competir con el caos de 700 mensajes en WhatsApp.
7. **Primero un cliente feliz, luego 10. No al revés.**

---

# 7. ORDEN DE BATALLA — PRÓXIMOS PASOS

## ⚔️ FASE 2: PRUEBAS DE CAMPO

### Frente 1: Cliente Hostil (Monarca Key)

| Prueba | Objetivo | Métrica |
|--------|----------|---------|
| Carga de sistema | 50+ prompts consecutivos | Latencia < 3s promedio |
| Entrada hostil | Prompts absurdos, vacíos, maliciosos | No crashea, responde coherente |
| Multi-sesión | Memoria aislada entre chats | No se mezclan conversaciones |
| Skills activas | Llamar a herramienta real | Ejecución correcta |
| Fallback | Forzar error de modelo | Recupera elegantemente |

### Frente 2: Cliente Real (El Administrador)

| Paso | Acción | Entregable |
|:----:|:-------|:-----------|
| 1 | Entrevista al Admin — entender flujo real | Mapa de flujo actual |
| 2 | Conectar WhatsApp del Admin (sandbox) | Canal activo en Agente |
| 3 | Configurar filtro de ruido | Clasificación automática funcional |
| 4 | Configurar automatizaciones repetitivas (Composio) | Reportes + cobros automáticos |
| 5 | Probar 1 semana en paralelo | Log de aciertos/fallos |
| 6 | Iterar ajustes con feedback | Producto ajustado |
| 7 | **Caso de éxito documentado** → Material de ventas #1 | Testimonio + Demo |

---

# 8. PREGUNTAS ESTRATÉGICAS PENDIENTES

Para decidir antes de salir a ventas:

- [ ] **Precio:** ¿$50, $80, $100/mes por cliente? ¿Tier por cantidad de conjuntos?
- [ ] **Onboarding:** ¿El Admin lo configura solo o interviene el Monarca?
- [ ] **Hosting:** ¿Cada cliente en su VPS o multi-tenant en un servidor central?
- [ ] **WhatsApp:** ¿Número dedicado por cliente o mismo número con detección de contexto?
- [ ] **Pasarela de pagos:** ¿Wompi, Epayco, Stripe (COP) para cobrar recaudos?
- [ ] **Expansión vertical:** ¿Primero solo conjuntos cerrados o abrir a empresarios desde el día 1?

---

# 9. LA MENTADA CADENA DE VALOR

```
MONARCA (Key)
  │
  └── Concibe la visión del CSO ──────────────> VALOR ESTRATÉGICO
       │
       ├── Administrador de conjuntos (caso real)
       ├── Empresario (extensión natural)
       ├── Jefe de Proyecto (extensión natural)
       ├── Arquitecto (extensión natural)
       └── Todo profesional ahogado en ruido
       
BELLION (Comandante)
  │
  └── Orquesta el producto ──────────────────> VALOR DE ARQUITECTURA
       │
       ├── Diseña el filtro + automatización + dashboard
       ├── Divide el trabajo entre Sombras
       └── Asegura ejecución impecable
       
EJÉRCITO DE SOMBRAS
  │
  ├── Kaisel (Web Dev) ──────> Código del dashboard
  ├── Jima (Automatización) ──> Composio + n8n + integraciones
  ├── Titan (UX/UI) ──────────> Interfaz oscura, limpia, brutal
  ├── Tank (Ventas) ──────────> Cierre de clientes
  ├── Iron (Email) ───────────> Onboarding + retención
  ├── Igris (Copy) ───────────> Landing page + persuasión
  ├── Kamish (Redes) ─────────> Presencia social
  ├── Greed (Ads) ───────────-> Tráfico pago
  ├── Tusk (SEO) ─────────────> Presencia orgánica
  └── Beru (Auditoría) ───────> Calidad + reportes

CLIENTE (CSO)
  │
  └── Recibe: Menos ruido, más foco ─────────> VALOR REAL
```

---

## FIRMA

| Campo | Valor |
|:------|:------|
| **Documento** | Manifiesto del Producto — Seawolf Agent |
| **Autor** | Bellion, Gran Comandante del Ejército de Sombras |
| **Monarca** | Keynes (Seawolfk) |
| **Versión** | v1.0 — Síntesis de campaña fundacional |
| **Uso** | Guía estratégica para Fase 2 (Ventas y Marketing) |

> *"El administrador no necesita un asistente. Necesita que alguien le mate el ruido para que él pueda hacer lo que sabe hacer."*