# INFORME DE EJECUCIÓN — FASE 0 "SEAWOLF NEREUS"
## Clone + build local del original (CopilotKit/openmuse) en el VPS

**Fecha de ejecución:** 2026-09-30 · **Prioridad:** MÁXIMA · **Clasificación:** CRÍTICO — Uso Interno Seawolf Studio
**Elaborado por:** Bellion (Gran Comandante) — misión en solitario · **Encargado por:** Monarca (Key)
**Objetivo de la fase:** `git clone` del original + `pnpm install` + build local + verificación real, confirmando qué arranca y qué no sin el servicio cerrado.
**Resultado:** ✅ **FASE 0 COMPLETADA — build reproducible y binario ejecutable en el VPS.** El único bloqueo de arranque total es `CPK_INTELLIGENCE_API_KEY` (el "rehén" que la Fase 1 elimina).

---

## 1. PLAN DE ACCIÓN EJECUTADO (orden numerada)

1. Reconocimiento del VPS (hardware, servicios vivos, prerrequisitos de toolchain).
2. Instalación **no invasiva** de **Node 24 LTS (v24.21.0)** en `/opt/node24` (el sistema traía v22).
3. Preparación de **pnpm 11.19.0** exacto vía corepack (el `packageManager` del repo).
4. `git clone` de `CopilotKit/OpenMuse` en `/opt/nereus/openmuse` (commit `d0b3a6b`).
5. `pnpm install --frozen-lockfile`.
6. `pnpm build:server` (tsc) + `pnpm build:web` (Expo export web).
7. Export multi-plataforma `--platform all` (web + iOS Hermes + Android Hermes).
8. Batería de verificación real: `typecheck`, `worker typecheck`, `lint`, suite de tests.
9. Arranque del binario compilado y prueba de `/api/health` + artefacto web servido por HTTP.
10. Recolección de evidencia y cierre.

---

## 2. TERRENO — VPS HOSTINGER (76.13.109.237)

| Recurso | Valor |
|---------|-------|
| SO | Ubuntu 24.04.4 LTS · kernel 6.8.0-136 |
| CPU | 2 vCPU |
| RAM | 7.8 GB (sin swap al inicio → se añadió swapfile 4 GB de seguridad) |
| Disco | 96 GB · **65 GB libres** tras el build |
| Node del sistema | v22.23.1 → **se instaló v24.21.0 aparte en `/opt/node24`** |
| pnpm | 11.9.0 del sistema → **activado 11.19.0 por corepack** |
| Servicios preexistentes | nginx (80/443), Hermes (9119), Docker (Portainer 9443/8000, n8n 5678, hermes-agent), cloudflared, tailscale |

> **Regla de oro respetada:** la instalación de Node se hizo **aislada** en `/opt/node24`; **no se tocó** el Node del sistema ni ninguno de los servicios vivos. El build de NEREUS vive en `/opt/nereus` y no interfiere con ninguno.
>
> ⚠️ **Hallazgo:** el puerto **8787 ya está ocupado por otro servicio Seawolf** (proceso `python3`, pid 853720). NEREUS se arrancó en **8788** para evitar colisión. Decisión de puerto definitivo → Fase 9 (despliegue).

---

## 3. RESULTADO DEL BUILD — TODO EN VERDE

| Etapa | Comando | Resultado |
|-------|---------|-----------|
| Dependencias | `pnpm install --frozen-lockfile` | ✅ **EXIT=0** (1m 07s, 1.2 GB en `node_modules`) |
| Build servidor | `pnpm build:server` | ✅ **EXIT=0** → `dist/apps/server/src/index.js` (876 KB) |
| Build web | `pnpm build:web` | ✅ **EXIT=0** → bundle JS 5.12 MB + `index.html` |
| Export multi-plataforma | `expo export --platform all` | ✅ **EXIT=0** → web + iOS `.hbc` 8.61 MB + Android `.hbc` 8.57 MB |
| Typecheck (raíz) | `pnpm typecheck` | ✅ **EXIT=0** |
| Typecheck (worker) | `pnpm --dir apps/worker typecheck` | ✅ **EXIT=0** |
| Lint (Biome) | `pnpm lint` | ✅ **EXIT=0** |
| **Suite de tests** | `pnpm test` | ✅ **276/276 pasan · 0 fallos · 0 skipped** (175.9 s) |

> **Nota vs. inteligencia previa:** el diario citaba **154 tests**; el repo a fecha `d0b3a6b` ya trae **276**. El original creció — buena señal de mantenimiento.

---

## 4. VERIFICACIÓN DE RUNTIME — QUÉ ARRANCA Y QUÉ NO

### 4.1 El binario SÍ es ejecutable y sirve la API
```
$ curl -s http://127.0.0.1:8788/api/health
{"ok":true,"mode":"sample","agentConfigured":true,"browserConfigured":false}

$ curl -s http://127.0.0.1:8788/
{"name":"OpenMuse","app":"http://localhost:8081","health":"/api/health"}
```

### 4.2 El artefacto web exportado SÍ sirve por HTTP
```
HTTP 200 | 1208 bytes   -> /index.html
<title>OpenMuse — a little room for everything</title>
HTTP 200 | 5,120,349 bytes -> /_expo/static/js/web/index-*.js
```

### 4.3 ⚠️ EL REHÉN, CONFIRMADO EN CARNE PROPIA
Sin clave del servicio, el proceso **aborta** — comportamiento idéntico en **todos** los modos (sample incluido):
```
Error: OpenMuse requires CPK_INTELLIGENCE_API_KEY. Run `npx copilotkit@latest login` and
`npx copilotkit@latest project select`, then set the generated server-only key.
    at readConfig (dist/apps/server/src/config.js:83:29)
```
Esto **no es un fallo de infraestructura ni del build**: es exactamente el **contra nº1** identificado en la inteligencia — CopilotKit Intelligence es un **servicio cerrado obligatorio, fuera de la licencia MIT**. El binario arranca (con clave dummy para la prueba de health) y sirve la API, pero **la capa de hilos/replay queda secuestrada** por el servicio externo. **La Fase 1 existe precisamente para arrancarle esa dependencia y poner persistencia propia (Postgres + pgvector).**

### 4.4 Alcance de lo que NO se probó (honestidad brutal)
- **Chat con modelo real:** no probado — requiere proveedor de pago (Fase 2: OpenRouter).
- **Navegador (Playwright/Chromium real):** no iniciado (`browserConfigured:false`) — el worker de navegador es un servicio aparte (Fase siguiente).
- **Computadora Linux (Docker):** no activada (`COMPUTER_ENABLED=false`).
- **Google (Gmail/Calendar):** no conectado — requiere OAuth real.
- **iOS/Android:** solo se validó el **bundle Hermes**; **NO** hay binarios firmados (Xcode/Android tooling no presentes, y no es objetivo de la Fase 0).

---

## 5. REPRODUCIBILIDAD — CÓMO RE-ARMAR TODO

```sh
# VPS (root@76.13.109.237)
export PATH=/opt/node24/bin:$PATH
export COREPACK_HOME=/opt/nereus/.corepack
cd /opt/nereus/openmuse
pnpm install --frozen-lockfile
pnpm build:server
pnpm build:web
# verificación completa
pnpm typecheck && pnpm --dir apps/worker typecheck && pnpm lint && pnpm test
# export multiplataforma
pnpm --dir apps/mobile exec expo export --platform all --output-dir dist/release
```

**Fijado para trazabilidad:** repo `CopilotKit/OpenMuse` @ `d0b3a6b3ea461bc938a5dea6c46e65eefdb1b933` · Node `v24.21.0` · pnpm `11.19.0`.

---

## 6. ESTADO Y PENDIENTES

- ✅ Fase 0 ejecutada y verificada end-to-end (clone + install + build + tests + runtime smoke).
- ✅ Toolchain aislado (`/opt/node24`) sin afectar servicios vivos del VPS.
- ✅ Evidencia de build reproducible y binario ejecutable.
- ⏳ **PENDIENTE → Fase 1:** cirugía del rehén. Sustituir CopilotKit Intelligence por persistencia propia (Postgres + pgvector) para hilos/replay. **Es el desbloqueo real del proyecto.**
- ⏳ Decisión de puerto definitivo (8787 ocupado por servicio Seawolf `python3`).
- ⏳ Reporte para auditoría de **Beru**.

---

## 7. VEREDICTO DEL COMANDANTE

La base **es sólida y compila limpia** en nuestro VPS. El original no es un juguete: 276 tests en verde, builds multiplataforma, arquitectura modular. **El único muro es el servicio cerrado**, y ya sabemos cómo tumbarlo. La cancha está preparada; la Fase 1 es la primera operación de cirugía real.

> **Recomendación:** autorizar **Fase 1** (persistencia propia Postgres+pgvector).

**Fin del informe de Fase 0.** Listo para auditoría de Beru.
