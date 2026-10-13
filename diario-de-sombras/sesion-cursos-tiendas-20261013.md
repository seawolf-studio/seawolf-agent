# Sesión 2026-10-13 — MEMENTO (Protocolo Memento)
**Comandante:** Bellion · **Monarca:** Key · **Tema:** Retoma de la destilación → cierre de Fase 0 «Cursos de Dropshipping Local + Smart Shop»

> El Monarca volvió y ordenó retomar el proceso desde `PLAN-CURSOS-TIENDAS.md`. Estado al llegar: precios ya aprobados (commit `54ce192`) y un manual v1 escrito por TANK **sin auditar**.

---

## 1. LO QUE SE CERRÓ (con evidencia en disco)

**Cadena completa escribir → auditar → re-auditar, hasta el PASA:**

| Ronda | Sombra | Entregable | Resultado |
|---|---|---|---|
| 1 | **TANK** | `MANUAL-MAESTRO-tiendas.md` (724 L, 35.773 B) | base heredada |
| 1 | **TANK** | `MANUAL-MAESTRO-tiendas-v2.md` (878 L, 47.115 B) | erratas + doctrina + Anexo A (Google Sites) |
| 1 | **BERU** | `beru/auditoria-manual-v2.md` (15.763 B) | **NO PASA** — 3 hallazgos máximos |
| 2 | **TANK** | `MANUAL-MAESTRO-tiendas-v3.md` (927 L, 52.670 B) | 16 correcciones + demolición Meta + logo IA + 2FA Dropi |
| 2 | **BERU** | `beru/auditoria-manual-v3.md` (17.692 B) | **NO PASA** — la reescritura degradó ortografía y metió infidelidad ("Canva" donde el curso dijo ChatGPT) |
| 3 | **TANK** | `MANUAL-MAESTRO-tiendas-v4.md` (944 L, 56.237 B) | ronda final: fidelidad + ortografía + glosario |
| 3 | **BERU** | `beru/verificacion-final-v4.md` (8.911 B) | ✅ **PASA** — 9/9 verificaciones, 13/13 cifras intactas, 0 Meta operativo |
| 4 | **TANK** | `MANUAL-MAESTRO-tiendas-v5.md` | pulido cosmético (14 tildes de §4.5, "Montesori" → "Montessori") |
| — | **IGRIS** | `igris/guiones-N1/` (7 archivos, 7.723 palabras) | ✅ los 6 guiones del Nivel 1 para **Kaelen** |

Todo vive en `seawolf-agent/intel/curso-dropshipping-local/`. Rutas de sesión: tank `20261013_152425_5635bb` · beru `20261013_154503_e47777`.

## 2. DECISIONES DEL MONARCA APLICADAS
1. **Precios aprobados** (ya venían): N1 55.000 · N2 118.000 · Bundle 139.000 · Smart Shop 620.000 · Mantenimiento 49.000/mes (COP).
2. **Nivel 2 = GOOGLE SITES** (no WordPress). WordPress/WooCommerce queda en el Anexo A como **referencia del curso**.
3. **Enlace de registro Dropi:** sirve **cualquier enlace que otorgue la exoneración** (~$5.000 COP/venta). No importa de quién sea el enlace.
4. **Burocracia Meta PROSCRITA** (doctrina permanente, aplicada sin esperar respuesta): la sección 6 se demolió — fuera Fan Page con 2FA, Business Manager, Pixel, grupos de Facebook, Instagram profesional. Canales permitidos: **WhatsApp/estados, TikTok y contenido orgánico**.
5. **Nivel 1 · módulo 5 = [MÉTODO SEAWOLF]**: el curso de referencia NO enseña a vender por redes (solo infraestructura de anuncios). Ese módulo es nuestro; así está marcado en el índice y en el guion.

## 3. LECCIONES DURAS (para no repetirlas)
1. **Un defecto mal reportado se vuelve defecto fantasma.** El Comandante reportó "negrita sin cerrar" en L275: era un **signo de exclamación faltante**. TANK "corrigió" un fantasma y el Anexo C **mintió sobre su propio trabajo** — el peor hallazgo posible. **Verificar el defecto antes de ordenar la corrección.**
2. **La palabra "radiar"** (verbo de radio para decir "validar") sobrevivió al v1, al v2 y a la lectura del Comandante. Solo cayó con lupa de auditor.
3. **Cada reescritura introduce defectos NUEVOS** (la sección 6 reescrita perdió ~30 tildes). El ciclo no es escribir→auditar, es **escribir→auditar→RE-AUDITAR**.
4. **El informe final de un auditor NO es superconjunto de su informe anterior:** BERU encontró 4 hallazgos reales (Binance/ByteDance, "menos de 3 minutos", "sin restricciones de energía", "tasa 30-40% inventada") en una corrida que murió, y su informe siguiente los perdió. **Rescatarlos del log.**
5. **Un one-shot en primer plano se pierde:** una corrida de BERU murió a los 7 min por el timeout de la herramienta (log cortado a media frase, sin entregable). Cura: **`background=true` + `notify=true`** y, en el encargo, **escribir el entregable temprano y reescribirlo por bloques**.
6. **El curso NO enseña redes orgánicas** (~45 min de Fan Page + Business Manager + cuenta publicitaria). Lo que no está en la fuente, no se inventa: se declara y se cubre con método propio marcado.
7. **Auditor sin proporción = cacería infinita.** La ronda de cierre se pide **acotada** (la lista + regresión) y con instrucción explícita de bloquear solo lo que afecte a la verdad o a lo vendible.

## 4. PENDIENTES
- [ ] **Verificación real de Google Sites** (el manual lo marca PENDIENTE-VERIFICAR: los pasos son ruta propia, no del transcript).
- [ ] **Empaquetado del Smart Course** (HyperFrames + Kaelen) — kaisel.
- [ ] **Capa IA del Smart Shop + tutor del curso** — jima.
- [ ] **Fase 1: afinar nuestras tiendas** (checklist aplicado) — kaisel + beru.
- [ ] Guiones de los niveles 2 y 3 (mismo molde que el N1).

## 5. FOCO PRÓXIMA SESIÓN
> **Empaquetado del Nivel 1**: llevar los 6 guiones de IGRIS a video con **Kaelen** y armar la micro-web del Smart Course (4 capas: Información → Video → Evaluación → Tutor IA).

---
*Memento generado por Bellion · evidencia o no existe.*