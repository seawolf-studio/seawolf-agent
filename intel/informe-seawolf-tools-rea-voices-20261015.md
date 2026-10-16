# INFORME — REA, Comunidad, VoiceBox vs VoiceStudio y arranque de SEAWOLF TOOLS
**Fecha:** 2026-10-15 · Uso Interno — Seawolf Studio · Bellion para el Monarca

---

## 1. REA — INSTALADO ✅

| Dato | Valor |
|------|-------|
| Paquete | **`rea-agents` v6.5.0** (MIT) |
| Registrado en | **Hermes** (`config.yaml`, línea 2273) + clientes detectados (Gemini CLI, Antigravity, Copilot CLI, VS Code) |
| Backup | `config.yaml.rea.backup` ✅ |
| Skill | `reverse-engineer-anything` instalada en `~/.agents/skills/` ✅ |
| Uso | `npx -y rea-agents@6.5.0 mcp` (MCP) · o CLI: `rea analyze <app>` |

### Motores de análisis (doctor)
- **node 26.7 OK.** Para binarios nativos hace falta un motor: **Ghidra (gratis, Apache)**, Hopper (pago) o IDA (pago).
- **Recomendación:** instalar **Ghidra** (libre) y apuntar `GHIDRA_INSTALL_DIR`. Sin motor, REA aún analiza **JavaScript/Electron, webs, .NET, SQLite, Go, Rust, APKs (con jadx), firmware**.
- **Pendiente opcional:** Ghidra + JADX.

---

## 2. QUÉ ESTÁ SIENDO AUDITADO CON REA (comunidad)

Fuentes: Hacker News (thread de 805 pts / **337 comentarios**), Reddit (r/BestGitHubRepos, r/singularity, r/bioinformatics, r/tech_x), dev.to.

**Casos reales reportados:**
| Qué | Para qué |
|-----|----------|
| Cliente **RDP de Windows** | Parchear 2 bugs (NOP + offset de pila) |
| **Insta360 Studio** (editor de video) | Shim para GPU AMD integrada + **quitar bloat/telemetría** del APK |
| **nvcc / CUDA** (NVIDIA) | "Open source" del compilador |
| **APKs a escala** (100 ROMs) | Cazar bugs/RCE (con `droidasc` por la lentitud de jadx) |
| **GUI de bioinformática** (Geneious) | Interoperabilidad |
| **Suite Adobe** | Clones *clean-room* (familia `storytold/*craft`) |
| **Juegos PC-98 / DOS** | Reconstrucción (showcase TH04) |
| **CUDA, VSTs, impresoras, backends bancarios** | Interoperabilidad / doc |

**Debate clave (y oro para nosotros):** el equipo de **`storytold/*craft`** (los clones de Adobe/Word) dijo en HN: *"usamos Claude Code pero **NO tocamos Ghidra ni decompilamos**, para no exponernos a infracción"*.
→ **Ese es el camino limpio:** reimplementar por **comportamiento observado + APIs públicas**, sin decompilar el original.

**Aviso de hype (honesto):** muchos comentarios dudan del "volumen" (270k★) y de que reconstruya apps completas. **Real, pero inflado.**

---

## 3. VOICEBOX vs VOICESTUDIO (para NEREUS)

| Criterio | **VoiceBox** (jamiepine) | **VoiceStudio** (debpalash) |
|----------|--------------------------|------------------------------|
| ★ | 57.596 | 69.154 |
| **Licencia** | **MIT** ✅ | **AGPL-3.0** ❌ (copyleft) |
| Lenguaje | Python | Python |
| Creado | 2026-01 | 2026-04 |
| Fuerte en | **Voice I/O para agentes**: clonar, dictar, generar voz, "hablar con agentes en tus voces"; stack local; qwen3-tts + whisper | Clonar, **diseñar voz**, **dubbing de video**, dictado, transcripción, audiolibros; **646 idiomas** |
| Encaje Seawolf | ✅ **NEREUS** (voz de agente) | Studio de medios amplio |

**Veredicto:** **VoiceBox (MIT) para el producto.** VoiceStudio es más rico pero **AGPL** — su uso en red (SaaS) obliga a liberar el código → **riesgo para Seawolf**. Se puede usar VoiceStudio solo como **herramienta interna aislada**, nunca embebida en el producto cerrado.

---

## 4. SEAWOLF TOOLS — arranque del módulo de OPTIMIZACIÓN ✅

**Nombre clave:** SEAWOLF TOOLS (recopilatorio de herramientas y funciones propias).

### 4.1 Módulo 1 — Optimizador de disco (CONSTRUIDO y PROBADO)
`intel/seawolf-tools.py` — código propio, limpio. Reimplementa lo que usabas de AVG TuneUp:
| Función | Comando |
|---------|---------|
| **Ranking de archivos más pesados** | `python seawolf-tools.py scan "C:\ruta" --top 30` |
| **Buscador de duplicados** (por hash, no por nombre) | `python seawolf-tools.py dupes "C:\ruta" --min 1` |
| **Mover a Papelera Seawolf** (reversible) | `... limpiar --paths "a","b"` |
| **Rescatar** | `... rescatar N` |
| **Borrado permanente** (opcional) | añadir `--hard` |
| **Aplicativo web local** | `python seawolf-tools.py serve "C:\ruta"` → UI en el navegador |

**Probado en vivo:** rankeó por tamaño y detectó 2 copias idénticas. ✅
**Seguridad:** mueve (reversible) por defecto; `--hard` borra de verdad; manifiesto para rescatar; nunca toca nada sin orden.

### 4.2 Candidatos para el catálogo Seawolf Tools (por construir)
1. Optimizador de disco (✅ v1).
2. **Editor de video propio** sobre base **OpenCut** (MIT).
3. Impulsor de contenido ("Círculo Publicitario").
4. Analista REA (estudio interno).

---

## 5. FUENTES
- GitHub API (morluto/rea, voicebox, VoiceStudio) — 2026-10-15.
- Hacker News ítem 50028275 (337 comentarios) · Reddit · dev.to · rea.tools.

**Fin del informe.**
