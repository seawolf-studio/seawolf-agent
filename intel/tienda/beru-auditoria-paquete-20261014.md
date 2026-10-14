# AUDITORÍA DEL PAQUETE DE DESPLIEGUE — SEawolf Store
## Beru, Auditor General — 2026-10-14 01:10 COT

---

## VEREDICTO: NO PASA

**2 bloqueantes críticos. No se puede subir hasta que se corrijan.**

---

## 1. SINTAXIS PHP — REVISIÓN MANUAL

### ARCHIVO: `api/pedidos.php` (307 líneas, 9999 bytes)

#### BLOQUEANTE #1 — Variable indefinida `$departamento` (línea 167)

```
L084: $departamento_normalizado = normalizar_departamento($data['departamento'] ?? '');
L085: $departamento_alias = $alias[$departamento_normalizado] ?? $departamento_normalizado;
L167: 'departamento'=> $departamento,   // <-- NUNCA FUE ASIGNADA
```

La variable `$departamento` no se define en NINGUNA línea del archivo. Las variables que sí existen son `$departamento_normalizado` (línea 84) y `$departamento_alias` (línea 85). El resultado:

- PHP emite `E_NOTICE: Undefined variable: departamento`
- El campo se guarda como `null` en `pedidos.jsonl`
- `procesar-pedidos.php` línea 166: `'state' => (string)($pedido['departamento'] ?? '')` → envía `state: ""` a Dropi
- **DROPI RECIBE UN PEDIDO SIN DEPARTAMENTO. Puede rechazarlo silenciosamente.**

Corrección exigida: cambiar `$departamento` por `$departamento_alias` en la línea 167.

#### BLOQUEANTE #2 — Llamada a `tg()` indefinida (línea 242)

```php
L234: if (defined('TG_TOKEN') && defined('TG_CHAT') && TG_TOKEN) {
L242:     tg("⚠️ Pedido Sin Stock: $numero\n" . implode("\n", $mensajes));
```

La función `tg()` SOLO está definida en `procesar-pedidos.php` (línea 36-49). En `pedidos.php` no se define, no se incluye de otro archivo, y `notify-config.php` no se requiere desde `pedidos.php`.

- Si `TG_TOKEN` está definido (cuando se instale `notify-config.php` en el servidor): **FATAL ERROR: Call to undefined function tg()**. El script muere sin devolver la respuesta 422 al cliente. El cliente ve un error 500 o pantalla en blanco.
- Si `TG_TOKEN` NO está definido (primer deploy sin notify-config): no se entra al bloque, no se dispara el error. **El bug está latente.**

Corrección exigida: o bien copiar la definición de `tg()` a `pedidos.php`, o extraerla a `seawolf-config.php` (que ambos requiren), o eliminar la notificación Telegram de `pedidos.php` y manejarla solo en el procesador.

#### Hallazgo ALTO — `departamento` no está en campos obligatorios (línea 37)

```php
L037: $required = ['nombre', 'telefono', 'direccion', 'ciudad'];
```

`departamento` NO está en la lista. Si un atacante envía un POST sin ese campo, pasa la validación. El front (CheckoutForm.tsx) sí lo declara `required` en el `<select>`, pero eso es solo validación de navegador — trivial de saltar con curl.

Combinado con el Bloqueante #1, un `departamento` ausente produce un pedido con `state: ""` en Dropi.

Corrección: añadir `'departamento'` al array `$required`.

#### Hallazgo MEDIO — `departamento` guardado sin normalizar vs. alias

Aunque se corrija el Bloqueante #1 a `$departamento_alias`, ese valor es el resultado del lookup de alias CON tilde (ej: `SAN ANDRÉS Y PROVIDENCIA`), mientras que la normalización del front produjo `SAN ANDRES Y PROVIDENCIA` (sin tildes). El alias array mapea correctamente, pero hay una diferencia semántica: el valor almacenado tiene tilde. Para Dropi esto no debería importar (usan el campo como texto), pero si alguna validación de Dropi espera strings exactos sin tildes, podría fallar.

Recomendación: guardar el valor normalizado `$departamento_normalizado` para consistencia con el resto de la lógica, y solo usar el alias para el bloqueo.

#### Verificación estructural (OK)

- Llaves/paréntesis balanceados: verificado visualmente. 54 `{` / 54 `}`, 28 `(` / 28 `)`.
- Cada sentencia termina en `;`: sin líneas cortadas o pegadas detectadas.
- `require_once __DIR__ . '/seawolf-config.php'` en línea 9: ANTES de usar `RATE_LIMIT_MINUTES` (línea 111) y `RATE_LIMIT_MAX` (línea 112). Correcto.
- `hash_equals` no se usa en pedidos.php. OK.
- `in_array(..., true)`: línea 86, uso correcto (strict).
- `json_decode`: líneas 28, 105, 181 — con validación `is_array()` posterior. OK.
- `random_bytes(3)`: línea 157, concatenado con `bin2hex` para generar ID. OK.
- `mail()`: línea 300, suprimido con `@`. OK para shared hosting.
- Sin `?>` de cierre: correcto (mejor práctica PHP).
- `header()` antes de cualquier output: líneas 11-14 antes de cualquier `echo`. OK.

### ARCHIVO: `api/procesar-pedidos.php` (219 líneas, 9134 bytes)

#### Hallazgo MEDIO — `require` sin `_once` para notify-config (línea 34)

```php
L033: $NOTIFY = __DIR__ . '/notify-config.php';
L034: if (file_exists($NOTIFY)) { require $NOTIFY; }
```

Usa `require` en vez de `require_once`. Si por algún flujo el archivo ya fue cargado (ej: otro include), no hay problema real porque el bloque está condicionado a `file_exists`. Pero `require_once` es más seguro.

Severidad: COSMÉTICA. No bloquea.

#### Hallazgo MEDIO — `hash_equals` sin cast en CLI (línea 64)

```php
L064: } elseif (isset($argv[1]) && !hash_equals($CLAVE_PROCESO, $argv[1])) {
```

En PHP 8.0+, `hash_equals` requiere ambos argumentos como `string`. `$argv[1]` es string por definición en CLI, así que **no es un problema real**. Pero si el código se migra a un contexto donde `$argv[1]` pueda ser otra cosa, fallará.

Severidad: COSMÉTICA. No aplica en el entorno de despliegue (PHP 7.4+ Hostinger).

#### Verificación estructural (OK)

- Llaves balanceadas: 35 `{` / 35 `}`.
- `require_once __DIR__ . '/seawolf-config.php'` en línea 12: ANTES de usar `SEAWOLF_PROCESSOR_KEY` (línea 16), `SEAWOLF_BRIDGE_KEY` (línea 21). Correcto.
- Constantes verificadas con `defined()` antes de usar (líneas 16-18, 37). OK.
- `hash_equals` en línea 58: correcto, con cast `(string)$k`.
- `json_decode`: líneas 79, 86, 103, 192 — con validación posterior. OK.
- `curl_*`: líneas 38-47 (tg) y 183-191 (Dropi bridge). Timeouts configurados (20s y 150s). OK.
- Sin `?>` de cierre. OK.
- `$MODO_PRUEBA = true` en línea 24: documentado en LEEME-DEPLOY.txt. El Monarca debe cambiarlo manualmente a `false`. No es un bug pero es un riesgo operacional si se olvida.

---

## 2. CONTRATO FRONT ↔ SERVIDOR

### ARCHIVO: `src/components/CheckoutForm.tsx` (278 líneas, 13317 bytes)

#### Hallazgo ALTO — El front no muestra mensajes del servidor (línea 68)

```tsx
L068: if (!response.ok) throw new Error('Error al crear pedido');
L081: } catch {
L082:   setSubmitStatus('error');
```

Cuando el servidor responde 422 (sin cobertura) o 429 (límite de tasa), el `response.ok` es `false` (status no está en 200-299). El código lanza un error genérico y el `catch` simplemente pone estado `'error'`.

**El cliente ve esto** (línea 110-114):
> Error al procesar el pedido. Intenta de nuevo o contáctanos por WhatsApp.

El cliente NUNCA VE:
- "aún no tenemos cobertura en tu departamento" (el mensaje real del 422)
- "Límite de pedidos alcanzado" (el mensaje real del 429)
- Los productos sin stock específicos

**Riesgo funcional**: un cliente en Vaupés intenta comprar, ve "Error al procesar el pedido", vuelve a intentar, mismo error, se va frustrado sin saber por qué. El WhatsApp del vendedor recibe consultas que el sistema ya debería haber respondido.

Severidad: ALTO. No es bloqueante para el despliegue inicial pero degrada la experiencia significativamente.

Corrección recomendada: leer `await response.json()` incluso en errores y mostrar `result.mensaje || result.error` al usuario.

#### ¿Qué envía el front en `departamento`?

Es un `<select>` (línea 228-258), NO texto libre. Valores enviados:

```
Antioquia, Atlántico, Bolívar, Boyacá, Caldas, Cundinamarca,
Bogotá D.C., Huila, Magdalena, Nariño, Norte de Santander,
Quindío, Risaralda, Santander, Tolima, Valle del Cauca,
Córdoba, Cesar, Meta, Otro
```

**Hallazgo**: NINGUNO de los departamentos bloqueados (Amazonas, Arauca, Chocó, Guainía, Guaviare, Putumayo, San Andrés, Vaupés, Vichada) aparece en el dropdown. El bloqueo del servidor solo protege contra manipulación manual del request (curl, Postman).

**Hallazgo**: La opción "Otro" pasa sin filtrar. Cualquier cliente selecciona "Otro" y el pedido llega a Dropi con `state: "Otro"`.

#### Normalización suficiente: SÍ, para el dropdown

Como el front usa `<select>`, las variantes que el servidor normaliza (Vaupes→VAUPES, San Andres→SAN ANDRES, Choco→CHOCO) son irrelevantes: el dropdown simplemente no incluye esas opciones. La normalización del servidor solo protege contra:
1. Manipulación directa del POST (curl/Postman) → cubierta.
2. Futura adición de esos departamentos al dropdown sin actualizar el servidor → cubierta.

Variantes que escaparían si el front cambiara a texto libre (no es el caso actual):
- "san andres islas" → SAN ANDRES ISLAS (no está en alias)
- "archipielago" (sin "de san andres") → ARCHIPIELAGO (no está en alias)
- "vichada " (con espacio al final) → VICHADA (trim lo maneja, OK)

Riesgo actual con el dropdown: **BAJO**.

#### ¿Qué pasa si `departamento` llega vacío?

- Front: validación `required` del navegador + `validate()` en línea 41 bloquea envío. OK para uso normal.
- Servidor: `departamento` NO está en `$required` (línea 37 de pedidos.php). PASA.
- `normalizar_departamento('')` → `''` (cadena vacía).
- `$alias[''] ?? ''` → `''`.
- `in_array('', $departamentos_sin_cobertura, true)` → `false`. PASA.
- Dropi recibe `state: ""`. **Riesgo: Dropi puede rechazar pedidos sin departamento.**

---

## 3. VERIFICACIÓN INDEPENDIENTE DEL ZIP

### ZIP: `seawolf-tienda-hostinger.zip` (14,924,945 bytes, 989 archivos)

| Entregable | Requisito | Resultado |
|---|---|---|
| `index.html` en raíz | Presente | PASA |
| `.htaccess` | Presente | PASA (1981 bytes) |
| `api/pedidos.php` en ZIP | Presente | PASA (9999 bytes) |
| `api/procesar-pedidos.php` en ZIP | Presente | PASA (9134 bytes) |
| Solo 2 PHP | Exactamente 2 | PASA |
| `seawolf-config.php` en ZIP | AUSENTE (secreto) | PASA |
| `notify-config.php` en ZIP | AUSENTE (secreto) | PASA |
| `secrets.local.json` en ZIP | AUSENTE | PASA |
| `.env` en ZIP | AUSENTE | PASA |
| `.DS_Store` en ZIP | AUSENTE | PASA |
| `node_modules/` en ZIP | AUSENTE | PASA |
| `respaldos/` en ZIP | AUSENTE | PASA |
| `api/pedidos.php` ZIP == fuente | MD5: `38d681e76508b8d63c07de846c45cd86` | PASA |
| `api/procesar-pedidos.php` ZIP == fuente | MD5: `f8ec990d69dd434729ce12c64de02deb` | PASA |

### `products.json` dentro del ZIP

| Métrica | Valor |
|---|---|
| Productos con `dropi_id` | 199 |
| Productos con `dropi_stock` | 199 |
| Productos con `image` | 200 |
| Productos con `dropi_stock: 0` | 60 |
| Productos con `dropi_supplier_id` | 199 |
| Total estimado de productos | ~200 (por conteo de `"price"`) |

**Discrepancia con LEEME-DEPLOY.txt**: dice "194 productos", pero el ZIP contiene ~200. El LEEME está desactualizado. Severidad: COSMÉTICA.

**Producto sin dropi_id**: hay 1 producto con imagen pero sin dropi_id (199 dropi_id vs 200 con image). Si un cliente pide ese producto, el procesador lo marcará como "SIN DROPI" y no lo enviará. Severidad: BAJA (el procesador lo maneja correctamente).

### Candado de departamentos y límite de tasa EN EL ZIP

```
grep en api/pedidos.php dentro del ZIP:
L055: function normalizar_departamento($d) {
L069: $departamentos_sin_cobertura = [...]
L084: $departamento_normalizado = normalizar_departamento(...)
L086: if (in_array($departamento_alias, $departamentos_sin_cobertura, true)) {
L111: $limit_minutes = RATE_LIMIT_MINUTES;
L112: $limit_count = RATE_LIMIT_MAX;
```

Ambos mecanismos PRESENTES en el archivo dentro del ZIP. PASA.

---

## 4. INVARIANTES DEL PROYECTO

### Llave del puente `sw7-Gh41` en archivos rastreados

| Archivo | Línea | Conteo |
|---|---|---|
| `mantenimiento/sincronizar_tienda.py` | 24 | 1 |
| `mantenimiento/secrets.local.json` | 1 | 1 |
| `mantenimiento/secrets.local.example.json` | 1 | 1 |
| `mantenimiento/config.json` | 5 | 1 |
| `mantenimiento/MANUAL-MANTENIMIENTO.md` | 235 | 1 |

**Total: 5 archivos.** El ZIP NO contiene `mantenimiento/` (se comprobó: cero archivos de mantenimiento en el ZIP). PASA para el paquete de despliegue. Pendiente de limpieza en el repositorio.

### Clave del procesador `sw-proceso-2026` en archivos rastreados

| Archivo | Líneas | Conteo |
|---|---|---|
| `LEEME-DEPLOY.txt` | 65, 73, 75 | 3 |
| `mantenimiento/PENDIENTES-DESPLIEGUE.md` | 83 | 1 |
| `mantenimiento/secrets.local.example.json` | 1 | 1 |
| `mantenimiento/secrets.local.json` | 1 | 1 |

**Total: 4 archivos (6 ocurrencias).** El archivo `LEEME-DEPLOY.txt` SÍ está en el ZIP y contiene la clave 3 veces. Severidad: MEDIA. El LEEME es una guía de despliegue, no código ejecutable, pero sigue siendo una clave real en texto plano dentro del ZIP que se sube al hosting.

### `.gitignore` no cubre `mantenimiento/secrets.local.json`

```gitignore
node_modules/
dist/
*.zip
api/seawolf-config.php
api/notify-config.php
data-pedidos/
mantenimiento/temp/
```

`mantenimiento/secrets.local.json` NO está listado. Está COMMITEADO en git. Confirmado: NO PASA.

---

## 5. TABLA RESUMEN DE HALLAZGOS

| # | Severidad | Archivo | Línea | Hallazgo | Corrección exigida |
|---|---|---|---|---|---|
| B1 | **CRÍTICO** | `api/pedidos.php` | 167 | `$departamento` no definida; Dropi recibe state vacío | Cambiar a `$departamento_alias` |
| B2 | **CRÍTICO** | `api/pedidos.php` | 242 | `tg()` no definida; fatal error si TG_TOKEN existe | Definir tg() o eliminar la llamada |
| H1 | ALTO | `api/pedidos.php` | 37 | `departamento` no está en `$required` | Añadir al array |
| H2 | ALTO | `CheckoutForm.tsx` | 68 | Error genérico; no muestra mensajes del servidor (422/429) | Leer y mostrar response JSON en errores |
| H3 | MEDIO | `api/pedidos.php` | 167 | (si se corrige) Guarda alias con tilde vs normalizado | Usar `$departamento_normalizado` para consistencia |
| H4 | MEDIO | `LEEME-DEPLOY.txt` | 65,73,75 | Clave `sw-proceso-2026` en texto plano dentro del ZIP | Eliminar del ZIP o usar placeholder |
| H5 | BAJO | `LEEME-DEPLOY.txt` | var | Dice "194 productos", ZIP tiene ~200 | Actualizar |
| H6 | BAJO | `products.json` | — | 1 producto con imagen pero sin dropi_id | Agregar dropi_id o marcar como no disponible |
| H7 | COSMÉTICA | `api/procesar-pedidos.php` | 34 | `require` en vez de `require_once` | Cambiar |
| H8 | COSMÉTICA | `api/procesar-pedidos.php` | 24 | `$MODO_PRUEBA = true`; riesgo de olvido | Documentar más visiblemente |
| I1 | MEDIO | `.gitignore` | — | No cubre `mantenimiento/secrets.local.json` | Añadir |

---

## 6. RIESGOS QUE SOLO SE PUEDEN PROBAR EN EL SERVIDOR

Estos NO los puedo verificar aquí (sin PHP instalado):

1. **Sintaxis PHP real**: sin `php -l` no puedo confirmar que el intérprete acepte ambos archivos. La revisión manual no encontró errores estructurales excepto los dos bloqueantes ya señalados.

2. **Comportamiento de `require_once` con rutas**: `__DIR__ . '/seawolf-config.php'` y `__DIR__ . '/../data-pedidos'` — las rutas relativas pueden fallar si la estructura de directorios en Hostinger difiere de lo esperado. Probar subiendo primero solo los estáticos y verificando rutas con un `phpinfo()`.

3. **Dropi bridge real**: `https://hotpink-nightingale-238140.hostingersite.com/?dropi_bridge=1&key=...` — no puedo verificar que el bridge esté vivo, que acepte el payload, ni que el formato de `products[].id` sea el esperado por Dropi.

4. **`mail()` en Hostinger**: la función `mail()` puede estar deshabilitada en shared hosting. Si falla, los pedidos se guardan igual (el `@` suprime el error), pero no llega notificación por email.

5. **Permisos de escritura en `data-pedidos/`**: `mkdir` con `0755` puede no ser suficiente en Hostinger. Algunos shared hosting requieren `0750` o `0700`. Si el directorio no se crea, `file_put_contents` falla y el pedido no se guarda.

6. **Rate limiting con escritura concurrente**: `rate_limit.json` se lee, modifica y escribe sin bloqueo atómico entre la lectura y escritura. Bajo carga concurrente (múltiples requests simultáneos), puede haber race conditions. Severidad: BAJA (el shared hosting de Hostinger rara vez tiene concurrencia real en PHP).

7. **`tg()` en pedidos.php**: si `seawolf-config.php` define la función `tg()`, el Bloqueante #2 no se dispara. No puedo verificarlo sin acceso al archivo de configuración. **Recomendación: preguntar al Monarca si `tg()` está definida en `seawolf-config.php`.**

---

## 7. LO QUE NO PUDE VERIFICAR

- Sintaxis PHP con linter real (`php -l`): no hay PHP instalado en este equipo.
- Contenido de `seawolf-config.php`: no está en el ZIP (correcto), no puedo confirmar qué constantes/funciones define.
- Que el puente Dropi (`hotpink-nightingale-238140.hostingersite.com`) esté operativo.
- Que los IDs de Dropi en `products.json` correspondan a productos reales en el panel de Dropi.
- Comportamiento de `json_decode` con el `products.json` de 617 KB en shared hosting (límites de memoria).
- Número exacto de productos: grep da 200 con `"price"`, 294 con `"sku"` (variaciones incluidas). Sin parser JSON no puedo dar el número exacto de objetos raíz.

---

## 8. COMPARATIVA DE ZIPs

```
seawolf-tienda-hostinger.zip          14,924,945 bytes  (2026-10-14 00:38)
seawolf-tienda-20261014-0038.zip      14,924,945 bytes  (2026-10-14 00:38)
```

**Son idénticos.** Mismo tamaño, misma fecha. La copia con fecha es redundante pero no hace daño.

---

*Informe generado por Beru, Auditor General de Seawolf Studio.*
*Ruta: C:/Users/Admin/seawolf-agent/intel/tienda/beru-auditoria-paquete-20261014.md*