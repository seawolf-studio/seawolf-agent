# Sesión 2026-10-13/14 — MEMENTO · TIENDA SEAWOLF: DEL OLVIDO AL DESPLIEGUE
**Comandante:** Bellion · **Monarca:** Key · **Tema:** retomar el proyecto **tienda** (desviación autorizada antes del Nivel 1 de Cursos) y dejarlo listo para subir

> Orden del Monarca: *"antes del nivel uno hay que hacer una pequeña desviación… dejar la tienda lista para funcionar y luego la hacemos smart… esa será la promesa que venderemos: tiendas automáticas que venden solas con autorización de sus dueños (intervención humana)."*

---

## 1. LO QUE SE ENCONTRÓ (proyecto abandonado ~15 días)

| Pieza | Estado al llegar |
|---|---|
| Puente **Dropi Bridge v3** (WordPress de Shopio) | ✅ **VIVO** (PHP 8.2.34 · WP 7.0.7 · WooCommerce 11.2.0 · token presente) |
| Catálogo vivo | 246 entradas → **199 SKUs únicos** (hay ~45 listados duplicados) |
| Tienda construida (Astro) | 200 productos · 199 con ID de Dropi · 14,2 MB |
| **Despliegue** | ❌ **NUNCA se hizo** |
| **Envío real a Dropi** | ❌ **jamás probado** (`$MODO_PRUEBA = true`) |
| Git del proyecto | ❌ no existía |
| 🔴 **Seguridad** | la **llave del puente** viajaba **en texto plano dentro del ZIP público** (esa llave crea pedidos reales) |
| 🔴 **Los 9 departamentos sin cobertura** | NO estaban bloqueados |
| Precios | 104 sanos / 95 a revisar (criterio viejo) |

**Alarma mía que resultó FALSA:** creí que faltaban 46 productos. Medido: **0 faltantes** — el catálogo tiene SKUs duplicados y la tienda los colapsa bien. *(Verificar la fuente antes de acusar.)*

## 2. LAS MEJORAS INYECTADAS DESDE LA DESTILACIÓN
Informe completo: `seawolf-agent/intel/TIENDA-seawolf-mejoras-desde-destilacion-20261013.md` (12 mejoras, 16 tareas repartidas). Las 5 que más pesan:
1. **Bloqueo de los 9 departamentos** sin cobertura (hoy convertido en **lista blanca** de 24 permitidos: mejor que lista negra).
2. **Huella propia por teléfono** (verde/naranja/rojo) — el error #1 más caro del manual (40-50% del flete).
3. **Compuerta de confirmación** — no crear en Dropi sin confirmar (mata al cliente fantasma).
4. **Seguimiento de los 9 estados** → mensajes automáticos al cliente (hoy el pipeline "crea y olvida").
5. **Copys GADO + ángulo por ocasión** — el copy era el crudo del proveedor.

**LA PROMESA, HECHA ARQUITECTURA:** cobertura → huella propia → stock/monto → **autorización del dueño por Telegram** (con *rompe-rojo*) → creación en Dropi → post-venta por estados → **todo auditado** (`approved_by`). Reutiliza el patrón **C3 (reglas preaprobadas)** ya probado en el Seawolf Agent.

## 3. PRECIOS — 4 RONDAS HASTA CUADRAR (TANK)
El primer intento subía **199 de 200** precios (mismo error caro de septiembre); el segundo retiraba **97**; el tercero escondía 55 perdedores como "MANTENER". El fallo de raíz eran **mis reglas** (diagóstico y acción mezclados).

**Veredicto final v4** (`seawolf-store/mantenimiento/precios-real-20261013-v4.csv`, 200 filas, 13 columnas):
| Diagnóstico | | Acción | |
|---|---|---|---|
| SANOS (≥25%) | 97 | **MANTENER** (no se toca) | **114** |
| A_REVISAR | 17 | **DECISION_MONARCA** | **63** |
| FLACO (5-15%) | 19 | SUBIR_SUAVE | 11 |
| **PÉRDIDA (<5%)** | **66** | PACK | 10 |
| SIN_COSTO | 1 | RETIRAR_CANDIDATO | 1 |
**Hallazgo estructural:** `< $20.000` es inviable (20 de 23 en pérdida con flete de $10.000); el punto dulce es **$40.000-$100.000**. **Lista que necesita la palabra del Monarca: 85 productos.**

## 4. LO QUE ENTREGÓ CADA SOMBRA (y dónde fallaron)
- **KAISEL (build):** ⚠️ **5 rondas, 5 fallos parciales**. Lo bueno: git, normalización de departamentos, `dist/` con hashes idénticos, `.gitignore`, `seawolf-config.php`. Lo malo: introdujo **2 bloqueantes** (`$departamento` sin definir → **ningún pedido se habría creado**; `tg()` sin definir → fatal error), dejó las llaves en el archivo de *ejemplo*, y en la última ronda fabricó un **ZIP basura de 795 bytes** declarándolo entregable. **El pipeline final (build + empaquetado) lo ejecutó el Comandante** — el ZIP nuevo es de las **01:25**.
- **BERU (auditor):** ⭐ **el salvador de la jornada.** 2 auditorías. Encontró lo que ningún hash ve: los 2 bloqueantes de lógica y **la clave del procesador 3 veces dentro del `LEEME-DEPLOY.txt` que se sube en el ZIP**.
- **TANK (números):** 4 rondas; informe honesto con supuestos declarados y autocorrección documentada.
- **IGRIS (copy):** 25 SKUs con GADO completo, `[FALTA INFO]` honesto, **el normalizador `normalizar_copys.py`** en el repositorio y el hallazgo de que **el filtro por ocasión de la tienda está muerto** (`tags` vacío → 0 productos).

## 5. EL PAQUETE (verificado con evidencia)
`C:/Users/Admin/Desktop/seawolf-tienda-hostinger.zip` + `seawolf-tienda-20261014-0125.zip` · 989 archivos · 14,2 MB
- Hash ZIP ↔ fuente **idéntico** en las 2 PHP · `departamento_final` y **lista blanca** dentro · `tg()` activo: 0 · **cero secretos** · clave del procesador: **0** · `index.html` en la raíz · 200 productos.
- **BERU re-auditando al cierre de esta sesión.**

## 6. LECCIONES DURAS (todas ya grabadas en la skill del ejército)
1. **El exit code no prueba nada: verifica el artefacto** (mtime + tamaño + volver a medir el defecto). 5 falsos "éxitos" en una noche.
2. **Tu propio contador puede mentir**: contar acentos por subcadena da **falsos positivos** (*confir**mas***, *cre**mas***, slug `dia-madre`). Usa **límites de palabra** y excluye identificadores. **Costó 3 rondas persiguiendo un fantasma mío.**
3. **Escribir un archivo existente exige `read_file` primero**; prohibido `echo`/heredoc en misiones de sombra.
4. **NO metas un archivo enorme en una misión de edición**: al leer 600 KB se le compactó la orden a IGRIS y **pidió el brief en vez de trabajar**.
5. **Los hashes no auditan la lógica**: un paquete con hashes perfectos puede ser incapaz de crear un pedido.
6. **Verificar la fuente antes de acusar** (el "desfase de 46 productos" no existía).

## 7. LO QUE FALTA (en orden)
- [ ] **BERU re-auditoría del paquete** → si PASA: **el Monarca sube**.
- [ ] **Rotar la llave del puente y la clave del procesador** (mañana, en WordPress con el Monarca) — estuvieron en el ZIP viejo y en el historial de git.
- [ ] **Higiene pendiente**: llaves en `secrets.local.example.json` / `config.json` / `docs`; y el `.gitignore` ya está.
- [ ] **Desplegar** en dominio temporal → **simulado** → **orden REAL de prueba** (autorizada).
- [ ] **Motor de reglas + autorización por Telegram + seguimiento de 9 estados** (JIMA) — el corazón de la promesa.
- [ ] **Segunda ola**: inyectar copys + precios (114 MANTENER no se tocan; 85 esperan su palabra).
- [ ] Pendiente del curso: **verificar Google Sites** (PASA en el manual como *PENDIENTE-VERIFICAR*).

---
*Memento de Bellion · evidencia o no existe · "el lobo recuerda, el lobo no olvida."*
