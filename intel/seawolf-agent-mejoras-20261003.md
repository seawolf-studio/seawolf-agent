# SEAWOLF AGENT — MEJORAS A IMPLEMENTAR SIN DAÑAR LA BASE HERMES
## Lista de características nacidas del proyecto relámpago LOBO

**Fecha:** 2026-10-03 · **Clasificación:** CRÍTICO — Uso Interno Seawolf Studio
**Elaborado por:** Bellion, Gran Comandante · **Para:** el Monarca (Key)

---

## 0. Principio rector: EXTENDER, NO MODIFICAR

**Regla de oro:** toda mejora entra como **una de estas cinco formas** — y **nunca** tocando el núcleo de Hermes:

1. **Plugin** de Hermes (capacidad nueva empaquetada).
2. **Servidor MCP** (herramientas externas por el protocolo estándar).
3. **Skill** (procedimiento reutilizable para el agente).
4. **Configuración** (`config.yaml`, variables de entorno).
5. **Tema / UI** (capa de presentación).

**Criterio de descarte:** si una mejora exige **fork del núcleo** de Hermes → se descarta o se **rediseña como extensión**. Así la base se actualiza sin rompernos.

**Lo que NO se toca jamás:** el bucle de razonamiento, los *tools* nativos, la CLI y el *gateway* de mensajería de Hermes. Todo lo demás se **monta encima**.

---

## A. Confianza y cumplimiento — *el foso defensivo*
1. **Audit Trail SHA-256 encadenado**: cada acción firmada; cadena de hashes **exportable** al cliente. *Extensión: plugin + tabla propia.*
2. **RBAC con panel**: roles (dueño, admin, operador, auditor) con permisos por acción. *Plugin + UI.*
3. **Aprobaciones explícitas (deny-by-default)**: nada se ejecuta sin permiso; queda registrado. *Plugin.*
4. **Multi-tenant con aislamiento por chat** (ya es diferenciador): cada cliente, sus datos, su cuota. *Config + plugin.*
5. **Cifrado de secretos** (Fernet) y **rotación de claves**. *Plugin.*

## B. Coste y modelos
6. **Gateway de modelos con presupuesto por tenant** y **fallback** (gratis → barato → premium). *Config + plugin.*
7. **Medidor de uso de tokens** y **alertas de gasto** por cliente. *Plugin de observabilidad.*

## C. Memoria
8. **Memoria dual por tenant** (semántica + temporal) con **inspeccionar / corregir / olvidar**. *MCP (Mem0 + Graphiti).*
9. **Retención y borrado por política** (cumplimiento de datos). *Plugin.*

## D. Voz y experiencia
10. **Voz por frases** con TTS **local** (Kokoro Apache-2.0 / Piper MIT) y **voz premium opcional**. *MCP de voz.*
11. **Modo claro/oscuro con oscuro por defecto** (constante de marca de todos los proyectos). *Tema.*
12. **Sello de unidad social** visible como diferencial. *Tema/UI.*

## E. Operación y producto
13. **Provisioning 1-click** de tenant (onboarding sin técnicos). *Plugin + script.*
14. **Español nativo** en toda la interfaz (i18n). *Capa de textos.*
15. **Observabilidad**: salud, uso, **alertas por Telegram/n8n**. *MCP/cron.*
16. **Backups y reinicio de fábrica por tenant**. *Script + plugin.*
17. **Manual del usuario + onboarding guiado**. *Documentación.*

## F. Integraciones
18. **Conectores vía Composio** (Gmail, Calendar, etc.) con **permisos granulares**. *MCP.*
19. **OCR + Push**. *MCP.*
20. **Continuidad multiplataforma** (móvil/escritorio). *Extensión.*

---

## G. Matriz de prioridad (esfuerzo × impacto)

| Prioridad | Característica | Esfuerzo | Por qué |
|---|---|---|---|
| **1** | Multi-tenant aislado + cuotas | Medio | **Sin esto no se vende** |
| **1** | Provisioning 1-click | Medio | El cliente no técnico no perdona fricción |
| **1** | Audit Trail + RBAC visibles | Medio | Es **el argumento de venta** al corporativo |
| **2** | Gateway con presupuesto + alertas | Bajo | Protege el margen (aprendido en LOBO) |
| **2** | Español nativo | Bajo | Diferenciador inmediato |
| **2** | Backups/reset por tenant | Bajo | Operación segura y repetible |
| **3** | Memoria dual | Medio | Ya probada en LOBO |
| **3** | Voz por frases | Medio | El "wow" que fideliza |
| **4** | Conectores Composio / OCR / Avatar | Alto | Valor, pero después de cobrar |

---

## H. Lo que aprendimos en LOBO y aplica directo
- **Gateway único de modelos** evita el *lock-in* y controla el gasto → **replicar**.
- **Persistencia propia** en vez de servicio cerrado → **replicar** (soberanía del dato).
- **Reinicio de fábrica** antes de entregar → **replicar** como paso de provisioning por tenant.
- **Separar "cara" (LOBO) de "motor" (Seawolf Agent)**: una sola base, dos empaques.
