# PLAN — NEREUS COMO PRODUCTO COMERCIAL
## Vender "lo que vende Meta" a clientes NO técnicos

**Fecha:** 2026-10-02 · **Clasificación:** CRÍTICO — Uso Interno Seawolf Studio
**Elaborado por:** Bellion (Gran Comandante) · **Encargado por:** Monarca (Key)

---

## 1. LA VERDAD DE NEGOCIO (lo que acaba de decir el Monarca)
NEREUS no es un juguete interno ni un proyecto open-source: es un **producto comercial**, y el cliente ideal **no es técnico ni está involucrado** en la tecnología. Quiere el resultado: *un agente personal que trabaja por él, habla, y le da tranquilidad* — como el Muse de Meta, pero sin la dependencia ni la barrera de lo "hecho en casa".

### Qué compra realmente un cliente NO técnico
1. **Experiencia terminada** — nada de comandos, claves, ni `pnpm`. Se paga por una sensación de producto pulido.
2. **Cero fricción de arranque** — si hay que configurar >1 minuto, se pierde. (Nuestro diferenciador #5: **setup 1-click**.)
3. **Confianza** — no entiende la IA, así que **teme que haga algo mal**. El **Audit Trail + aprobaciones** no es un extra: es el argumento de venta. (#2, #3.)
4. **Idioma y trato** — **español nativo**, cálido, sin jerga. (#4.)
5. **Privacidad** — sus datos, de él. (Multi-tenant aislado; #1.)
6. **El "wow"** — juzgan por la experiencia: **voz** y, después, **avatar**.

> **Consecuencia táctica:** todo lo "de ingeniero" (arquitectura limpia, 276 tests, OpenRouter) es **invisible** para el comprador. Es necesario, pero **no vende**. Lo que vende es **producto + confianza + español**.

---

## 2. BRECHA: QUÉ TENEMOS vs. QUÉ FALTA PARA VENDER
| Capacidad | Estado |
|-----------|--------|
| Motor de agente, tareas durables, persistencia propia | ✅ |
| Gateway de modelo (OpenRouter, gratis/barato) | ✅ |
| Voz (pasarela por frases, TTFA 0,75 s) | 🟡 listo en VPS; falta llevarlo a cliente |
| Memoria semántica + temporal (Mem0 + Graphiti) | ✅ |
| **Onboarding 1-click / instalación sin técnico** | ⬜ **CRÍTICO** |
| **Multi-tenant + RBAC + aislamiento por chat** | ⬜ **CRÍTICO** |
| **Audit Trail visible (confianza)** | 🟡 backend sí; falta vista para el cliente |
| **Facturación / cobro / planes** | ⬜ **CRÍTICO (no estaba en el roadmap)** |
| **Marca, web de venta, tutoriales** | ⬜ |
| **Soporte / SLA / documentación para no técnicos** | ⬜ |
| Avatar (Rive) | ⬜ (fase 8) |
| Conectores (Composio), OCR, Push | ⬜ (fases 5-6) |

---

## 3. CAMINO CRÍTICO A LA PRIMERA VERSIÓN VENDIBLE (orden propuesto)
1. **Fase 5 — Conectores (Composio):** el cliente no técnico quiere "conectar mi Gmail/WhatsApp/calendario" y que funcione.
2. **Fase 6 — OCR + Push:** documentos reales y avisos — sin eso, no parece producto.
3. **Fase 9a — Multi-tenant + RBAC + aislamiento:** sin esto **no se puede vender a varios** (seguridad y legal).
4. **Fase 9b — Onboarding 1-click + auditoría visible + marca (español):** la capa que hace amable lo complejo.
5. **Comercial (nuevo) — facturación, planes, términos, soporte.**
6. **Fase 7 — Continuidad multiplataforma** (empezar en PC, seguir en móvil).
7. **Fase 8 — Avatar** (el diferenciador visual del "wow").

---

## 4. RIESGOS (honestidad brutal)
- **El "no técnico" no tolera errores.** Un fallo visible mata la reputación; por eso la confianza (auditoría/aprobaciones) es la prioridad real.
- **Vender infraestructura propia a no técnicos** exige soporte humano; hay que presupuestarlo.
- **Dependencia de proveedor (OpenRouter):** aceptable, pero el cliente no debe saberlo.
- **Marca:** "Muse/OpenMuse" es de Meta → **NEREUS** y marca Seawolf desde el día uno.

---

## 5. RECOMENDACIÓN DEL COMANDANTE
El avance técnico va bien (~35 %), pero **el 35 % restante que vende aún no ha empezado**: es la capa de **producto + confianza + español + cobro**. Propongo **cambiar el orden** para atacar primero lo que hace vendible:
> **Conectores → OCR/Push → Multi-tenant/RBAC → Onboarding+Auditoría visual+Marca → Cobro.**

**Fin del plan.**
