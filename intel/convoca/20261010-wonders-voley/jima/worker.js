/**
 * worker.js — Smart Web Wonder's · Capa IA (proxy OpenRouter)
 * ============================================================
 * Cloudflare Worker (formato módulo ES).
 *
 * Expone UN SOLO endpoint tipo OpenAI:
 *   POST /api/chat
 *   body: { messages: [{role, content}], model?, temperature?, max_tokens?, stream? }
 *
 * La clave de OpenRouter NUNCA viaja al navegador. Vive solo como
 * secreto del Worker: env.OPENROUTER_API_KEY (ver smart-endpoint.md).
 *
 * Club Deportivo Wonder's — «6 en la pista, 1 corazón».
 * Smart Web by Seawolf Studio.
 * ============================================================
 */

const DEFAULT_MODEL = 'qwen/qwen3.8-flash';

// ---- Límites de seguridad / abuso (reglas de JIMA: idempotencia, límite y errores)
const MAX_MESSAGES = 40;          // nº máximo de mensajes por request
const MAX_MESSAGE_CHARS = 8000;   // longitud máx por mensaje
const MAX_SYSTEM_CHARS = 3000;    // longitud máx del system prompt interno
const DEFAULT_MAX_TOKENS = 600;   // respuesta razonable para chat en vivo
const MAX_TOKENS_CAP = 4000;      // techo duro de tokens de salida

// ---- System prompt del asistente (identidad Wonder's)
const SYSTEM_PROMPT = `Eres «Wonder's», el asistente virtual del Club Deportivo Wonder's, una
escuela y club de voleibol en Madrid (España) enfocado en el desarrollo deportivo de jóvenes.
Lema: «6 en la pista, 1 corazón». Palmarés 2026: Campeonas AMB & Copa Stars 2026. Eslogan:
«Talento, equipo y valores». Misión del club: formar tanto deportistas como personas.

Tu trabajo es ayudar a familias y jugadoras con:
- Inscripciones y proceso de alta (extraescolares, escuelas, campamento, tecnificación).
- Horarios de entrenamiento (extraescolares: martes y jueves; categorías Infantil y Cadete,
  de 17:00 a 18:00 h; confirmar siempre la sede y franja vigente según la temporada).
- Categorías y franjas de edad (infantil, cadete, juvenil, senior… — no inventes edades exactas
  que no estén confirmadas por el club).
- Precios / cuotas por categoría (solo lo que el club haya publicado; si no lo sabes, dilo y
  deriva al contacto del club). No inventes tarifas.
- Dudas generales de familias: qué necesita una niña para empezar, pruebas, material, valores
  que se enseñan, próximos eventos, temporada 2026/2027, campamento de verano (junio-agosto 2027)
  y tecnificación (1-30 julio 2027).

Tono y reglas:
- Respondes SIEMPRE en español, con trato cercano, cálido y familiar: como una persona del club
  que conoce a las familias, sin jerga técnica. Usa frases cortas y directas.
- Si no tienes un dato confirmado (un precio, un horario concreto, una sede), NO lo inventes:
  responde que lo confirmes por las vías oficiales del club.
- Contacto oficial para derivar: email clubdeportivowonders@gmail.com · WhatsApp/telefono
  +34 614 696 077.
- Nunca pidas ni manejes datos bancarios ni claves de pago en el chat.
- Cierra cada respuesta con un siguiente paso claro (inscribirse, escribir al WhatsApp, hablar
  con una entrenadora) cuando ayude a la familia.

Eres la capa de inteligencia de la Smart Web del club, firmada discreta «Smart Web by Seawolf Studio».`;

// ---- Cabeceras CORS (permitir que el navegador del sitio llame al Worker)
function corsHeaders(env) {
  const origin = (env && env.ALLOWED_ORIGIN) ? env.ALLOWED_ORIGIN : '*';
  return {
    'Access-Control-Allow-Origin': origin,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Max-Age': '86400',
    'Content-Type': 'application/json; charset=utf-8',
  };
}

// ---- Respuestas de error uniformes (siempre con CORS)
function jsonError(message, status, hint, env) {
  return new Response(JSON.stringify({
    ok: false,
    error: { message, hint: hint || null },
  }), {
    status,
    headers: corsHeaders(env),
  });
}

/**
 * Punto de entrada del Worker (módulo ES).
 */
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const method = request.method;

    // ---- Pre-flight CORS (OPTIONS)
    if (method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders(env) });
    }

    // ---- Rutas permitidas: solo POST /api/chat (y GET como health-check opcional)
    if (url.pathname !== '/api/chat') {
      return jsonError('Ruta no encontrada. Usa POST /api/chat.', 404, 'El endpoint único es /api/chat.', env);
    }
    if (method !== 'POST') {
      return jsonError('Método no permitido. Usa POST.', 405, 'Solo se acepta POST a /api/chat.', env);
    }

    // ---- La clave es un secreto server-side: sin ella no hay servicio
    if (!env.OPENROUTER_API_KEY) {
      return jsonError(
        'Servicio no configurado del lado del servidor.',
        500,
        'El Monarca debe ejecutar: wrangler secret put OPENROUTER_API_KEY',
        env
      );
    }

    // ---- Leer y validar el cuerpo
    let payload;
    try {
      payload = await request.json();
    } catch {
      return jsonError('Body inválido: no es JSON.', 400, 'Enviar { messages: [{role, content}] }.', env);
    }

    const rawMessages = Array.isArray(payload.messages) ? payload.messages : null;
    if (!rawMessages || rawMessages.length === 0) {
      return jsonError('Campo messages requerido y no vacío.', 400, 'Ej: { "messages": [{ "role":"user", "content":"..." }] }', env);
    }
    if (rawMessages.length > MAX_MESSAGES) {
      return jsonError(`Demasiados mensajes (máx ${MAX_MESSAGES}).`, 413, `Enviar hasta ${MAX_MESSAGES} mensajes por request.`, env);
    }

    // ---- Sanear y limitar cada mensaje
    const messages = [];
    for (const m of rawMessages) {
      const role = (m && m.role) || '';
      const content = (m && typeof m.content === 'string') ? m.content : '';
      if (!['system', 'user', 'assistant'].includes(role) || content.length === 0) {
        return jsonError('Cada mensaje requiere role válido (system|user|assistant) y content no vacío.', 400, null, env);
      }
      if (content.length > MAX_MESSAGE_CHARS) {
        return jsonError(`Mensaje demasiado largo (máx ${MAX_MESSAGE_CHARS} caracteres).`, 413, null, env);
      }
      // Sanear: quitar roles que no sean del cliente salvo que sean legítimos
      messages.push({ role, content });
    }

    // ---- Construir el prompt final: system (identidad) + historial del cliente
    const sys = (SYSTEM_PROMPT.length > MAX_SYSTEM_CHARS)
      ? SYSTEM_PROMPT.slice(0, MAX_SYSTEM_CHARS)
      : SYSTEM_PROMPT;
    const chatMessages = [{ role: 'system', content: sys }, ...messages];

    // ---- Parámetros del modelo (con techos)
    const model = (typeof payload.model === 'string' && payload.model.trim() !== '')
      ? payload.model.trim()
      : DEFAULT_MODEL;
    let maxTokens = (Number.isInteger(payload.max_tokens) && payload.max_tokens > 0)
      ? payload.max_tokens
      : DEFAULT_MAX_TOKENS;
    if (maxTokens > MAX_TOKENS_CAP) maxTokens = MAX_TOKENS_CAP;
    const temperature = (typeof payload.temperature === 'number' && payload.temperature >= 0 && payload.temperature <= 2)
      ? payload.temperature
      : 0.6;

    const body = {
      model,
      messages: chatMessages,
      max_tokens: maxTokens,
      temperature,
      stream: false,
    };

    // ---- Llamada a OpenRouter (chat completions, formato OpenAI)
    let upstream;
    try {
      upstream = await fetch('https://openrouter.ai/api/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${env.OPENROUTER_API_KEY}`,
          'HTTP-Referer': (env.SITE_URL) ? env.SITE_URL : 'https://wonders.club',
          'X-Title': 'Wonders Smart Web',
        },
        body: JSON.stringify(body),
      });
    } catch (err) {
      return jsonError('No se pudo contactar con el proveedor de IA.', 502, 'Red/upstream falló.', env);
    }

    // ---- Reintento simple con backoff (JIMA: reintentos con backoff)
    if (upstream.status === 429 || upstream.status >= 500) {
      const backoffMs = 700;
      await new Promise((r) => setTimeout(r, backoffMs));
      try {
        upstream = await fetch('https://openrouter.ai/api/v1/chat/completions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${env.OPENROUTER_API_KEY}`,
            'HTTP-Referer': (env.SITE_URL) ? env.SITE_URL : 'https://wonders.club',
            'X-Title': 'Wonders Smart Web',
          },
          body: JSON.stringify(body),
        });
      } catch {
        return jsonError('Error del proveedor tras reintento.', 502, null, env);
      }
    }

    const raw = await upstream.text();

    // ---- Mapear errores del proveedor a una respuesta limpia
    if (!upstream.ok) {
      let detail = raw.slice(0, 500);
      let status = upstream.status === 429 ? 429 : 502;
      let hint = null;
      if (upstream.status === 401 || upstream.status === 403) {
        status = 500; hint = 'Revisa el secreto OPENROUTER_API_KEY (wrangler secret put).';
      } else if (upstream.status === 429) {
        hint = 'Límite de cuota del proveedor alcanzado.';
      }
      return jsonError(`El proveedor de IA respondió ${upstream.status}.`, status, hint, env);
    }

    // ---- Éxito: devolver respuesta con CORS y cabeceras de seguridad
    return new Response(raw, {
      status: 200,
      headers: {
        ...corsHeaders(env),
        'Cache-Control': 'no-store',
        'X-Content-Type-Options': 'nosniff',
        'Strict-Transport-Security': 'max-age=63072000; includeSubDomains; preload',
      },
    });
  },
};