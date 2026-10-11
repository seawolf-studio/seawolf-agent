# SMART ENDPOINT — Capa IA del Club Deportivo Wonder's
> Especificación funcional del endpoint /api/chat (proxy a OpenRouter vía Cloudflare Worker).
> Proyecto: Smart Web Wonder's · Misión 2026-10-10 · Especialista: JIMA (automatización/APIs).
> Firmante: «Smart Web by Seawolf Studio».

---

## 1. DECISIÓN DE MODELO (VERIFICADA contra el catálogo vivo)

Verificado 2026-10-10 contra https://openrouter.ai/api/v1/models (458 modelos, catálogo en vivo,
no supuesto). Criterio para chat en vivo en español de un club: barato, fiable, baja latencia,
texto→texto, buen español, low-rate de servidores.

### RECOMENDADO PRIMARIO
**`qwen/qwen3.8-flash`**
- Precio: 0,15 USD / M tokens prompt · 0,47 USD / M tokens completion.
- Contexto: 1.000.000 tokens (espacio de sobra para el historial del chat).
- Salida: texto→texto. Soporta `response_format`/`structured_outputs` (fiable y extensible).
- Por qué: gama Flash de Qwen = latencia baja y respuesta fluida para chat en vivo; calidad
  muy sólida en español; coste por conversación típica (≈600 tokens out) ≈ 0,0003 USD.
- Nota precio: con la política de precio por 1.000.000 tokens de OpenRouter, la conversación
  promedio del widget cuesta fracciones de centavo. Tonelada de margen antes de preocuparse.

### ALTERNATIVAS (verificadas)
- `anthropic/claude-haiku-5.5` — 0,10 / 0,50 USD por M, 1M ctx. Excelente fiable pero sin exigencias
  de latencia tan bajas; buen plan B si se quiere marca Anthropic.
- `deepseek/deepseek-v3.2` — 0,26 / 0,80 USD por M, 164k ctx. Alternativa económica y muy capaz.

### NO USAR
- Modelos `:free` o `-free` (sin contrato de disponibilidad para prod; pueden caer).
- Modelos con salida multimodal/imagen/video (el asistente solo responde texto).
- Routers sin precio estable (`openrouter/fusion`, etc.). Preferir un modelo concreto conocido.

> El modelo se puede cambiar en runtime enviando `model` en el body, o en `DEFAULT_MODEL` dentro
> de worker.js sin tocar el navegador.

---

## 2. CONTRATO DEL ENDPOINT

### Request

```
POST https://<worker-url>/api/chat
Headers:
  Content-Type: application/json
  (CORS: el navegador puede llamar directo; pre-flight OPTIONS resuelto por el Worker)

Body (JSON):
{
  "messages": [
    { "role": "system"|"user"|"assistant", "content": "texto" }
  ],
  "model": "qwen/qwen3.8-flash",   // opcional (tiene default)
  "temperature": 0.6,              // opcional (default 0.6, rango 0-2)
  "max_tokens": 600,               // opcional (default 600, techo 4000)
  "stream": false                  // fijo a false en esta v1
}
```

El Worker inyecta por su cuenta el `role:"system"` con la identidad del Club Deportivo Wonder's;
el cliente solo envía el historial de `user`/`assistant`.

Límites del servidor (reglas JIMA: límite de longitud y protección de abuso):
- Máximo 40 mensajes por request (413 si se excede).
- Máximo 8.000 caracteres por mensaje (413 si se excede).
- `max_tokens` acotado a [1, 4000]; `temperature` acotado a [0, 2].
- Falta la clave del servidor → 500 con aviso (nunca se expone la clave).

### Response (éxito, 200)

Cuerpo idéntico al formato de OpenAI Chat Completions (passthrough de OpenRouter):

```
{
  "id": "gen-...",
  "object": "chat.completion",
  "model": "qwen/qwen3.8-flash",
  "choices": [
    {
      "index": 0,
      "message": { "role": "assistant", "content": "¡Hola! Claro, te cuento sobre la inscripción..." },
      "finish_reason": "stop"
    }
  ],
  "usage": { "prompt_tokens": ..., "completion_tokens": ..., "total_tokens": ... }
}
```

El texto a mostrar en el chat es: `data.choices[0].message.content`.

### Errores (conviven con CORS)

| status | significado | comportamiento |
|--------|-------------|----------------|
| 400    | body inválido / messages mal formado | el cliente muestra error amigable |
| 405    | método no POST | |
| 404    | ruta distinta de /api/chat | |
| 413    | request demasiado grande | cortar el historial del lado del cliente |
| 429    | cuota del proveedor alcanzada | el cliente reintenta con backoff y avisa |
| 500    | clave no configurada / clave inválida | alerta al responsable (solo Monarca/Bellion), nunca expone detalle de seguridad |
| 502    | upstream/proveedor caído tras reintento | mensaje de «vuelve a intentarlo en un momento» |

Comportamiento del servidor ante fallo (JIMA): reintento simple con backoff de 700 ms ante 429/5xx
antes de rendirse; error anónimo (sin volcar la clave ni trazas sensibles) y cabeceras de seguridad
(`Cache-Control: no-store`, `X-Content-Type-Options`, HSTS).

---

## 3. CLIENTE (navegador) — snippet JavaScript

La clave JAMÁS aparece aquí. El navegador solo conoce la URL pública del Worker.

```js
// constelacion.js — chat de la Smart Web de Wonder's (fragmento del widget)
const WONDERS_API_URL = 'https://smart-wonders.<TU-SUBDOMINIO>.workers.dev/api/chat';
const MODELO = 'qwen/qwen3.8-flash';

async function enviarMensaje(historial, textoUsuario) {
  const mensajes = [...historial, { role: 'user', content: textoUsuario }];

  // Cortar por seguridad si el historial crece demasiado (límite servidor: 40 msgs / 8k chars)
  const recortado = mensajes.slice(-12);

  const res = await fetch(WONDERS_API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      messages: recortado,
      model: MODELO,
      temperature: 0.6,
      max_tokens: 600,
    }),
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error((body.error && body.error.message) || `Error ${res.status}`);
  }

  const data = await res.json();
  return data.choices[0].message.content; // texto de la respuesta a pintar en el chat
}

// Ejemplo de uso:
// const respuesta = await enviarMensaje([], '¿Cómo inscribo a mi hija en extraescolares?');
```

Nota: este snippet es la llamada de red. El widget completo (diseño, burbujas, temas oscuro/claro,
`prefers-reduced-motion`) lo construye la fase de Smart Web; aquí solo se define el canal de IA.

---

## 4. DESPLIEGUE EN CLOUDFLARE (comandos exactos con Wrangler)

Requisitos: Node.js 18+ y la CLI de Wrangler (`npm i -g wrangler`), cuenta Cloudflare, y la clave
de API de OpenRouter creada en https://openrouter.ai/keys.

### 4.1 Estructura del proyecto

```
wonders-ia/
├── wrangler.toml
├── worker.js          <- copia EXACTA del archivo entregado jima/worker.js
└── src/               <- (el sitio web se despliega por separado; este es el worker IA)
```

### 4.2 `wrangler.toml` (raíz del proyecto)

```toml
name = "smart-wonders"
main = "worker.js"
compatibility_date = "2025-01-01"
workers_dev = true   # URL pública de prueba: https://smart-wonders.<sub>.workers.dev

# Ruta del endpoint IA (regla de ruteo, opcional si el worker se llama solo por su URL)
# Si quieres servir también desde tu propio dominio en Cloudflare:
# routes = [{ pattern = "wonders.es/api/*", custom_domain = true }]

[vars]
# Variables públicas (NO la clave). Se pueden sobrescribir con `wrangler secret put`.
SITE_URL = "https://tudominio.temporal" # usado en cabecera HTTP-Referer/X-Title
ALLOWED_ORIGIN = "*"                   # o fija tu dominio: "https://wonders.es"
```

La clave NO va en `wrangler.toml` (sería visible en el repo). Va como secreto (4.4).

### 4.3 Publicar el worker

```bash
cd wonders-ia
npm i -g wrangler          # si aún no está instalado
npx wrangler login         # autenticación en el navegador (1 sola vez)
npx wrangler deploy        # sube el worker.js y lo publica
```

Tras `deploy` te devuelve la URL:
`https://smart-wonders.<TU-SUBDOMINIO>.workers.dev` → el endpoint queda en `/api/chat`.
Usa esa URL en `WONDERS_API_URL` del cliente.

### 4.4 Guardar la clave como SECRETO (procedimiento crítico de seguridad)

```bash
# Interactivo: te pregunta la clave y NO la imprime ni la guarda en disco:
npx wrangler secret put OPENROUTER_API_KEY

# Verificar que quedó guardada (devuelve solo la existencia, no el valor):
npx wrangler secret list

# Rotación / actualización cuando cambie la clave: repetir el mismo `put`.
```

Reglas de seguridad (obligatorias):
- La clave SOLO existe como secreto del Worker (`env.OPENROUTER_API_KEY`). NUNCA pegarla en
  HTML/JS del navegador, ni en el repo, ni en `wrangler.toml`, ni en logs.
- El navegador solo ve la URL del worker; el secreto vive server-side y se llama `env` / `secret`.
- Si aparece la clave en git, rotarla de inmediato en OpenRouter.

### 4.5 Prueba real (requerida por estándar de entrega — evidencia o no existe)

```bash
curl -X POST https://smart-wonders.<TU-SUBDOMINIO>.workers.dev/api/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role":"user","content":"¿Cómo inscribo a mi hija en extraescolares de vóley?"}]}'

# Esperado: JSON con "choices[0].message.content" en español respondiendo sobre inscripciones.
# Código 200 = éxito real. Un 200 sin payload válido NO es éxito.
```

Pruebas negativas mínimas:
- SIN body → esperar 400.
- `model` inexistente → 502/error del proveedor con mensaje anónimo.
- Con la clave eliminada temporalmente (`npx wrangler secret delete OPENROUTER_API_KEY` y redeploy)
  → 500 con hint de configuración. (Luego volver a poner con `put`.)

---

## 5. SEGURIDAD Y OPERACIÓN (resumen JIMA)

| Tema | Decisión |
|------|----------|
| Clave de API | Solo secreto del Worker. Punto único de fallo = si no está configurada, 500 (aviso claro). |
| CORS | `*` por defecto; fijar `ALLOWED_ORIGIN` al dominio real en producción. |
| Costo | Modelo Flash barato + `max_tokens` 600 (techo 4000) = control de factura. |
| Abuso | Límite de mensajes (40) y por mensaje (8k chars). |
| Disponibilidad | Reintento con backoff 700 ms ante 429/5xx. Punto único de fallo = Cloudflare Worker (es la nube de Cloudflare, alto SLA; respaldo = segundo worker/dominio si el proveedor de IA cae). |
| Idioma | Español obligatorio por system prompt; el modelo soporta español nativamente. |
| Datos del club | La IA deriva a contacto oficial cuando no conoce un dato; no inventa precios/horarios. |
| Proscritas | Shopify, AdSense, burocracia Facebook/Meta: ausentes por protocolo. |

---

## 6. PROXIMO PASO SUGERIDO (para Bellion)
1. Monarca/Bellion crea el worker con `npx wrangler deploy` + `secret put OPENROUTER_API_KEY`.
2. La hermana confirma el dominio final (mm. del dossier: migración desde Hostinger a Cloudflare)
   y se fija `ALLOWED_ORIGIN` / `SITE_URL` definitivos.
3. Pendiente de requisitos: confirmar precio real por categoría, horarios/sede exactos e historial
   del club para enriquecer el system prompt del worker (dossier puntos FALTAN 4-7).
4. Fase Smart Web construye el widget de chat y lo conecta a `/api/chat`.

— Fin de especificación. /* Smart Web by Seawolf Studio */