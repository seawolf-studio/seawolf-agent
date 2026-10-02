# INFORME — BENCHMARK DE VOZ NEREUS (TTFA y escalado)
## Decisión de nodo de voz para producción

**Fecha:** 2026-10-02 · **Clasificación:** CRÍTICO — Uso Interno Seawolf Studio
**Elaborado por:** Bellion (Gran Comandante) · **Encargado por:** Monarca (Key)
**Objetivo:** medir el rendimiento real de la capa de voz en el VPS para decidir el **nodo de voz** de producción.

---

## 1. METODOLOGÍA
- Motor: **Kokoro preset ES** (`em_alex`), el más ligero con español.
- Cliente de streaming real (urllib, lectura incremental de chunks) sobre `POST /generate/stream`.
- Texto de prueba: frase de ~5.15 s de audio.
- Pruebas: 1 calentamiento + **5 secuenciales** + **concurrencia x2** y **x4**.
- Muestreo de CPU/RAM del host durante la prueba.

## 2. RESULTADOS

### Secuencial (1 usuario)
| Métrica | Valor |
|---------|-------|
| TTFA / total | **≈ 2.1 s** (para 5.15 s de audio) |
| Real-time factor | **≈ 0.42** (más rápido que tiempo real) |
| Estabilidad | ✅ consistente (2.03–2.19 s) |

### Concurrencia (CPU-bound)
| Usuarios simultáneos | TTFA medio | Lectura |
|----------------------|-----------|---------|
| 1 | **2.1 s** | Aceptable para nota de voz |
| 2 | **4.3 s** | Degrada lineal |
| 4 | **8.5 s** | Insufrible para conversación |

### Recursos del host (2 vCPU)
- Load: 0.0 → **1.53** durante la prueba (limitado por 2 núcleos).
- RAM: **5.7–6.2 GB / 7.9 GB** — el contenedor toca su tope de 6 GiB.

## 3. HALLAZGOS

1. **El endpoint `/generate/stream` NO entrega audio incremental**: devuelve el clip completo. Por eso TTFA = tiempo total del clip.
2. **El escalado es lineal y CPU-bound**: cada usuario consume ~0.42 × duración de audio de CPU. Con 2 núcleos, solo ~2–3 usuarios antes de que la latencia arruine la experiencia.
3. **La RAM está al límite**: el modelo pesado (1.7B) provoca OOM; incluso 0.6B deja el contenedor al 95%.
4. **El software es correcto y ligero (RTF 0.42)**; el cuello de botella es **hardware**, no la elección de motor.

## 4. LA CORRECCIÓN BARATA QUE LO CAMBIA TODO (software)
Como el audio se entrega completo, la clave para fluidez real es **trocear por frases**:
- Sintetizar **la primera frase corta** primero → el audio arranca en **~0.4–0.6 s** en vez de esperar el párrafo completo.
- Mantener el motor **cargado** en memoria (evitar recarga por petición).
- Mínimo absoluto de palabras en la primera frase ("Claro," / "Listo,").

Esto convierte la ruta ligera en **conversacional aceptable incluso en CPU modesta** — sin clonación y con licencia comercial limpia.

## 5. RECOMENDACIÓN DE NODO
| Escenario | Nodo sugerido |
|-----------|---------------|
| **Piloto / uso interno (1–2 usuarios)** | VPS actual con **streaming por frase** (software) — sin coste nuevo |
| **Producción / venta a clientes** | **Nodo de voz dedicado**: GPU pequeña (T4/4060-class) **o** CPU de 8–16 núcleos |
| Clonación | Premium opcional sobre el nodo GPU, cuando la infra lo permita |

## 6. DECISIÓN FIJADA
- **Voz de producto:** preset ligero (Kokoro, Apache-2.0), sin clonación en la ruta crítica.
- **Nodo de voz:** separado del core; se dimensiona por **TTFA medido**, no por corazonada.
- **Uso interno:** la voz curada del Monarca será **privativa de Seawolf** (no se distribuye).
- **Regla del cascarón:** nada se entrega a un cliente sin haberlo probado en el mismo hierro.

---

## 7. VEREDICTO DEL COMANDANTE
El software **cumple y es ligero**. El hierro actual **no da para conversación viva** con más de un par de usuarios. Con **streaming por frase** el piloto se salva hoy; para **vender**, hace falta **nodo de voz dedicado**. Datos, no promesas.

**Fin del informe de benchmark.**
