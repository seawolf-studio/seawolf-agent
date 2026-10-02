# INFORME — STREAMING POR FRASES EN NEREUS (implementación)
## La ruta ligera ya da conversación fluida en el VPS actual

**Fecha:** 2026-10-02 · **Clasificación:** CRÍTICO — Uso Interno Seawolf Studio
**Elaborado por:** Bellion (Gran Comandante) · **Encargado por:** Monarca (Key)

---

## 1. QUÉ SE IMPLEMENTÓ
**`voice-gateway.py`** — pasarela de voz que trocea la respuesta en **frases** y entrega el audio de cada una **en cuanto está lista**, en vez de esperar al párrafo completo.
- Entrada: `POST /speak {text, profile_id?, engine?}`.
- Salida: flujo `[uint32 BE largo][WAV]` por frase (una tras otra, con `flush`).
- Motor: VoiceBox local (Kokoro ES), **sin clonación**, Apache-2.0.
- Enrutado: `GET /health`.

## 2. RESULTADOS MEDIDOS (VPS 2 vCPU, sin GPU)

| Métrica | Baseline (párrafo entero) | **Gateway por frases** |
|---------|---------------------------|------------------------|
| **TTFA (inicio de audio)** | **6.17 s** | **0.75 s** |
| Total de audio | 6.17 s | 6.87 s |
| Entrega | Bloque único al final | 5 frases en flujo |
| Mejora percibida | — | **≈ 8× menos espera** |

- El **total** sube ligeramente (coste por frase), pero lo que **oye el usuario** aparece **8 veces antes**.
- Consistente entre intentos (TTFA 0.70–0.78 s).

## 3. POR QUÉ IMPORTA
- Confirma que **el software ligero es conversacional** en hardware modesto: la espera está en **0.75 s** (umbral aceptable).
- **No requiere GPU ni clonación** para el producto base → **licencia limpia y coste bajo**.
- La clonación (mi voz / la del Monarca) queda como **premium opcional** cuando la infraestructura lo permita.

## 4. PITFALL CORREGIDO
El primer framing (HTTP chunked + longitud interna) desincronizaba al cliente → audio corrupto. Se migró a **framing binario simple** (`Connection: close`, longitud explícita por frase) → entrega **verificada íntegra** (661 KB, 5 frases).

## 5. ESTADO
- ✅ Pasarela de voz operativa en el VPS (`127.0.0.1:8799`).
- ✅ TTFA conversacional demostrado (0.75 s) sin GPU.
- ⏳ Integrar la pasarela al flujo de NEREUS (que el agente hable por ella).
- ⏳ Decide nodo de voz para venta (GPU o CPU multinúcleo).
- ⏳ Persistencia/servicio (systemd) y exposición segura.

## 6. VEREDICTO DEL COMANDANTE
**La espera se mató con ingeniería, no con dinero.** El pilar de voz del producto **ya funciona en el VPS actual**. El premium de clonación espera a la infraestructura, como se decidió. Avanzamos con base sólida.

**Fin del informe de streaming por frases.**
