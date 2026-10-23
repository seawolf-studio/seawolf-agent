# 🆓 INFORME — Las 11 IA gratis del video ("Cancelarás Suscripciones")
**Analista:** Bellion (Gran Comandante) · **Para:** Monarca · **Fecha:** 2026-10-22
**Fuente:** https://www.youtube.com/watch?v=Q_QMdobAWWw — *Alejavi Rivera* (22 oct 2026, 28:23)
**Verificación:** licencias y estrellas consultadas en GitHub API en vivo (no se repite lo que dice el video)

---

## 0. RESUMEN
El video promete **11 alternativas gratuitas** a 11 suscripciones de IA (que suman **$566,99/mes ≈ $6.804/año**).
**Verifiqué cada una.** Lo más valioso para nosotros: **OpenShorts** (es nuestro Círculo Publicitario),
**FreeLLMAPI** (ataca directo el gasto de tokens), **Vane** (investigaciones a costo cero) y **CopilotKit/openmuse**
(que ya es la base de NEREUS).
**Alerta honesta:** 2 son **AGPL-3.0** (copyleft fuerte) y 1 es "open core" con partes propietarias.

---

## 1. LAS 11 HERRAMIENTAS (verificadas)

### 1. Meetily — reemplaza a Granola ($14/mes)
- **32.082 ⭐ · MIT ·** `Zackriya-Solutions/meetily` · https://meetily.ai/
- Asistente de reuniones **local-first**: transcripción en vivo (Parakeet/Whisper, 4× más rápido), **diarización**
  (quién dijo qué), resumen con IA, puntos clave y **tareas accionables**. Funciona con Zoom/Meet/Teams/presencial.
- Corre con **modelos locales** (hasta LLaMA-3 1B ≈ 1 GB RAM) → privacidad total. Windows/Mac.
- 🟢 **NOS SIRVE:** sí. Las reuniones del Monarca y las del **Cliente Súper Ocupado** que Seawolf Agent atiende.

### 2. OpenShorts — reemplaza a OpusClip ($15+/mes)
- **7.015 ⭐ · MIT ·** `mutonby/openshorts` · https://www.openshorts.app/
- Video largo → **shorts verticales 9:16**: detección de momentos virales, seguimiento de cara, **subtítulos**,
  titulares, reencuadre (cámara arriba / pantalla abajo) y **score de viralidad**. Desde URL o archivo.
- Autoalojable e **ilimitado** (la nube gratis tiene cupo).
- 🟢 **EL QUE MÁS NOS SIRVE:** es exactamente **el Círculo Publicitario** — resuelve el cuello de botella
  "10 piezas buenas de 100".

### 3. Presenton — reemplaza a Gamma ($12/mes)
- **11.287 ⭐ · Apache-2.0 ·** `presenton/presenton` · https://presenton.ai/
- Prompt o documento → **presentación** (hasta 20 slides), plantillas profesionales, imágenes IA, **API**.
  Local o nube.
- 🟢 **NOS SIRVE:** propuestas y pitch decks para **captación B2B**. Licencia limpia.

### 4. VoiceStudio — reemplaza a ElevenLabs ($22/mes)
- **82.389 ⭐ · ⚠️ AGPL-3.0 ·** `debpalash/VoiceStudio` · https://voicestudio.sh/
- Estudio de voz: **clonación**, **diseño de voces** desde descripción, **doblaje/traducción** de video,
  audiolibros, transcripciones. Win/Mac/Linux/Docker.
- 🔴 **AGPL-3.0 = copyleft fuerte.** Regla del Studio: **cero copyleft en producción.**
  Autoalojado para uso interno = legal; **incrustarlo en un producto que se vende = ❌.**
- 🟡 **NUESTRA RUTA YA DECIDIDA:** **VoiceBox** (`jamiepine/voicebox`, **58.361 ⭐, MIT**) — mismo propósito,
  licencia limpia. TTS alterno: **Kokoro-82M (Apache-2.0)**.

### 5. CopilotKit — reemplaza a OpenAI PRO ($200/mes)
- **38.191 ⭐ · MIT ·** `CopilotKit/CopilotKit` · https://www.copilotkit.ai/
- Stack de frontend para **agentes y UI generativa** (React/Angular/Mobile/Slack). Sus productos clonan lo premium:
  - **OpenDots** (`CopilotKit/OpenDots`, 5.918 ⭐, MIT) → los "dots" agentes del plan de $200
  - **OpenBot** (`CopilotKit/OpenBot`, 6.983 ⭐, MIT) → el equivalente a GrowthBot
  - **openmuse** (`CopilotKit/openmuse`, **5.471 ⭐, MIT**) → el equivalente a Operator
- 🟢 **NOS SIRVE DOBLE:** (a) **es la base de NEREUS** (ya la habíamos elegido); (b) OpenDots/OpenBot para
  los agentes de Seawolf Agent.

### 6. OpenNotebook — reemplaza a NotebookLM / Gemini Notebook
- **40.498 ⭐ · MIT ·** `lfnovo/open-notebook` · https://www.open-notebook.ai/
- Cuadernos privados: metes **fuentes** (URL/archivo/texto), **chateas** con ellas, notas y **genera podcast**.
  **Se puede autoalojar en un VPS y tenerlo 24/7.**
- 🟢 **NOS SIRVE:** base de conocimiento del Studio en nuestro VPS — cargar los informes de `intel/` y consultarlos.

### 7. FreeLLMAPI — reemplaza el gasto de API (≈20 licencias Max de Claude)
- **39.911 ⭐ · MIT ·** `tashfeenahmed/freellmapi` · https://freellmapi.co/
- Agrega los **free tiers** de **34 proveedores** (635 endpoints de modelos) tras **un solo endpoint
  OpenAI-compatible `/v1`**: router que elige el mejor modelo, **failover** ante rate-limit, uso por clave,
  claves cifradas. **7.400 millones de tokens/mes gratis.**
- 🟢 **NOS SIRVE ENORME** → ataca nuestro **problema #1 (gasto de tokens)**.
- 🟡 **HONESTIDAD:** son límites de **terceros** (pueden cambiar). Sirven para **trabajo de fondo**
  (barridos, catálogos, resúmenes), **no** para el modelo fijado de Bellion. Y hay que respetar los ToS de cada proveedor.

### 8. Vane — reemplaza a Perplexity Pro ($20/mes)
- **37.666 ⭐ · MIT ·** `ItzCrazyKns/Vane` · https://github.com/ItzCrazyKns/Vane
- Motor de respuestas con **búsqueda profunda**, interfaz casi calcada de Perplexity. Fuentes: internet,
  académicas, sociales. Nivel de razonamiento, librería. Se conecta a **FreeLLMAPI** → gratis.
- 🟢 **NOS SIRVE MUCHO:** **nuestras investigaciones de intel** (como esta misma) a costo cero.

### 9. Upscayl — reemplaza a Topaz Labs (~$29/mes)
- **50.904 ⭐ · ⚠️ AGPL-3.0 ·** `upscayl/upscayl` · https://upscayl.org/
- Escalado de imágenes con IA (hasta 4×), **local y privado**, Win/Mac/Linux + versión nube.
- 🟡 **NOS SIRVE (interno):** recuperar/mejorar **fotos de producto** del catálogo de zapatillas y assets de marca.
  Uso interno = legal; **incrustado en producto distribuido = ❌** (AGPL).

### 10. Dyad — reemplaza a Lovable Pro ($25/mes)
- **22.043 ⭐ · Apache-2.0 + `src/pro/` propietario ·** `dyad-sh/dyad` · https://www.dyad.sh/
- Constructor de apps con IA **local**: prompt → app con **base de datos, autenticación y publicar**. Le adjuntas
  la **identidad de marca** (colores/fuentes). Trabaja con APIs gratis o **modelos locales (Ollama)**.
- 🟡 **NOS SIRVE:** prototipar rápido paneles/apps (Seawolf Tools, Centro de Mando).
  **⚠️ Ojo:** el directorio `src/pro/` **no es libre** — usar solo el core Apache-2.0.

### 11. Treblo — reemplaza a Suno Pro ($10/mes)
- **Sin repositorio · servicio web propietario, gratis ·** https://treblo.com/ (ex-**Sonauto**)
- Generador de **canciones con IA ilimitadas y gratis**: voz, letra, **4.160 estilos**, **derechos comerciales
  incluidos**, duración configurable (+4:30).
- 🟢 **NOS SIRVE:** música para contenido del Círculo Publicitario, jingles de marca.
- 🟡 Es **propietario y no autoalojable** (depende del servicio). Es un extra, no algo crítico.

---

## 2. TABLA MAESTRA (licencia = lo que decide si entra a producción)

| # | Herramienta | Reemplaza | Ahorro/mes | ⭐ | Licencia | ¿Entra? |
|---|---|---|---|---|---|---|
| 2 | **OpenShorts** | OpusClip | $15 | 7.015 | ✅ MIT | 🥇 SÍ |
| 7 | **FreeLLMAPI** | Gasto API | ~$200 | 39.911 | ✅ MIT | 🥇 SÍ |
| 8 | **Vane** | Perplexity Pro | $20 | 37.666 | ✅ MIT | 🥇 SÍ |
| 5 | **CopilotKit** | OpenAI PRO | $200 | 38.191 | ✅ MIT | 🥇 SÍ (base NEREUS) |
| 6 | **OpenNotebook** | NotebookLM | — | 40.498 | ✅ MIT | 🥈 SÍ |
| 1 | **Meetily** | Granola | $14 | 32.082 | ✅ MIT | 🥈 SÍ |
| 3 | **Presenton** | Gamma | $12 | 11.287 | ✅ Apache-2.0 | 🥈 SÍ |
| 9 | **Upscayl** | Topaz | $29 | 50.904 | ⚠️ AGPL | 🥉 Interno |
| 10 | **Dyad** | Lovable Pro | $25 | 22.043 | 🟡 Apache + pro | 🥉 Con cuidado |
| 11 | **Treblo** | Suno Pro | $10 | — | 🟡 Propietario | 🥉 Extra |
| 4 | VoiceStudio | ElevenLabs | $22 | 82.389 | 🔴 AGPL | ❌ usar **VoiceBox (MIT)** |

**Total que se dejaría de pagar: $566,99/mes ≈ $6.804/año.**

---

## 3. QUÉ NOS SIRVE Y POR QUÉ (ordenado por impacto en Seawolf)

1. **OpenShorts → EL CÍRCULO PUBLICITARIO.** Es literalmente la máquina que convierte 1 video en N piezas
   virales, con subtítulos y score. Era el **cuello de botella** del Círculo. MIT = entra a producción.
2. **FreeLLMAPI → el gasto de tokens.** Nuestro problema #1 histórico. 34 proveedores gratis detrás de una sola
   API compatible con OpenAI. Ideal para **sombras de fondo** y trabajos mecánicos. (No para Bellion.)
3. **Vane → inteligencia.** Reemplaza Perplexity Pro para las investigaciones del `intel/`, conectado a FreeLLMAPI.
4. **CopilotKit (+ openmuse) → NEREUS.** Ya era nuestra base; ahora confirmamos que es **MIT** y que trae
   OpenDots/OpenBot (los agentes del plan de $200).
5. **OpenNotebook → la memoria del Studio.** Base de conocimiento 24/7 en nuestro VPS, alimentada con `intel/`.
6. **Meetily → reuniones.** Para el Monarca y para el Cliente Súper Ocupado (el caso de uso central de Seawolf Agent).
7. **Presenton → ventas.** Propuestas B2B para el frente frío de captación.
8. **Upscayl → catálogo.** Mejorar fotos del catálogo de zapatillas (uso interno).
9. **Dyad → prototipado.** Paneles y apps en minutos (core Apache).
10. **Treblo → contenido.** Música para las piezas del Círculo.
11. **VoiceStudio → NO.** Misma función que **VoiceBox (MIT)** pero con AGPL. Nos quedamos con VoiceBox.

---

## 4. ALERTAS (la letra chica que el video no dice)
- **AGPL-3.0 (VoiceStudio, Upscayl):** si el software se **distribuye** o se expone como servicio, la AGPL
  obliga a liberar el código. **Interno = sí. Producto vendido = no.**
- **Dyad:** el core es Apache-2.0, pero `src/pro/` tiene licencia propia (**no libre**).
- **Treblo:** gratis pero **propietario** — dependemos de un tercero; no es infraestructura crítica.
- **FreeLLMAPI / free tiers:** son límites **de terceros**, cambian sin aviso. Para trabajo de fondo, con respaldo.
- **Privacidad ≠ igual en todas:** las versiones **cloud** de estos servicios ven tus datos. Las **autoalojadas**
  no. Para material del Monarca/cliente → **siempre local o VPS propio**.

## 5. PROPUESTA DE ARRANQUE (cuando el Monarca diga)
1. **OpenShorts en el VPS** → primera pieza del **Círculo Publicitario**.
2. **FreeLLMAPI en el VPS** → API gratuita unificada para las sombras de fondo.
3. **Vane en el VPS** → motor de investigación del `intel/`.
4. **OpenNotebook en el VPS** → base de conocimiento del Studio.
5. **Meetily en el PC** → reuniones del Monarca.

*Todo autoalojado, todo en nuestro servidor, cero suscripciones.* 🐺
