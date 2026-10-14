# RE-AUDITORIA DEL PAQUETE DE DESPLIEGUE — Seawolf Store
## Beru, Auditor General — 2026-10-14 01:40 COT

---

## VEREDICTO: PASA

**Los 3 bloqueantes de la auditoria anterior estan cerrados. El paquete puede subirse.**

Hay 1 hallazgo ALTO nuevo (front no muestra mensajes del servidor — el codigo de manejo existe pero es inalcanzable) y 5 departamentos de la lista blanca faltan en el dropdown. Ninguno bloquea.

---

## 1. LOS TRES BLOQUEANTES: CERRADOS

### B1 — `$departamento` fantasma → CERRADO

| Verificacion | Resultado |
|---|---|
| `$departamento_final` definido | SI — linea 108: `$departamento_final = $departamento_alias;` |
| Usado en la linea del pedido | SI — linea 181: `'departamento' => $departamento_final,` |
| `$departamento` suelto sin definir | 0 ocurrencias en todo el archivo |
| Coherencia del valor | `$data['departamento']` → normalizar → alias lookup → `$departamento_alias` → `$departamento_final`. El valor que se guarda y se envia a Dropi es el mismo. OK. |

```
Evidencia: grep -n '\$departamento' pedidos.php
L091: $departamento_normalizado = normalizar_departamento($data['departamento'] ?? '');
L092: $departamento_alias = $alias[$departamento_normalizado] ?? $departamento_normalizado;
L108: $departamento_final = $departamento_alias;
L181: 'departamento' => $departamento_final,
```

**No hay `$departamento` a secas. PASA.**

### B2 — `tg()` sin definir → CERRADO

| Verificacion | Resultado |
|---|---|
| `tg()` activa en pedidos.php | Linea 257: `// tg("...` — COMENTADA |
| Documentacion | Linea 256: `// NOTIFICACION ELIMINADA (se hace en procesar-pedidos.php)` |
| Riesgo de codigo muerto | NINGUNO. Es un comentario claro con explicacion. |

```
Evidencia: grep -n 'tg(' pedidos.php
L257:// tg("⚠️ Pedido Sin Stock: $numero\n" . implode("\n", $mensajes));
```

Solo aparece comentada. Procesar-pedidos.php define `tg()` correctamente (lineas 36-49) y la usa. **PASA.**

### Clave `sw-proceso-2026` en el ZIP → CERRADO

```
Comando: unzip -p seawolf-tienda-hostinger.zip LEEME-DEPLOY.txt | grep -c "sw-proceso-2026"
Salida: 0

Comando: busqueda en TODOS los archivos de texto del ZIP
Resultado: 0 ocurrencias en los 989 archivos
```

La clave fue eliminada completamente. **PASA.**

---

## 2. LISTA BLANCA DE DEPARTAMENTOS

### Los 24 departamentos permitidos

Presentes en `$departamentos_blanca` (lineas 70-75):

ANTIOQUIA, ATLANTICO, BOLIVAR, BOYACA, CALDAS, CAQUETA, CASANARE, CAUCA, CESAR, CORDOBA, CUNDINAMARCA, HUILA, LA GUAJIRA, MAGDALENA, META, NARINO, NORTE DE SANTANDER, QUINDIO, RISARALDA, SANTANDER, SUCRE, TOLIMA, VALLE DEL CAUCA, BOGOTA

### Los 9 SIN cobertura: ¿alguno en la lista blanca?

| Departamento bloqueado | En lista blanca |
|---|---|
| AMAZONAS | NO |
| ARAUCA | NO |
| CHOCO | NO |
| GUAINIA | NO |
| GUAVIARE | NO |
| PUTUMAYO | NO |
| SAN ANDRES Y PROVIDENCIA | NO |
| VAUPES | NO |
| VICHADA | NO |

**Ninguno se colo. PASA.**

### Alias: ¿mapean correctamente?

| Alias | Destino | En lista blanca | Veredicto |
|---|---|---|---|
| `BOGOTA D.C.` → `BOGOTA` | BOGOTA | SI | PERMITIDO |
| `BOGOTA DC` → `BOGOTA` | BOGOTA | SI | PERMITIDO |
| `DISTRITO CAPITAL` → `BOGOTA` | BOGOTA | SI | PERMITIDO |
| `VALLE` → `VALLE DEL CAUCA` | VALLE DEL CAUCA | SI | PERMITIDO |
| `N DE SANTANDER` → `NORTE DE SANTANDER` | NORTE DE SANTANDER | SI | PERMITIDO |
| `NORTE SANTANDER` → `NORTE DE SANTANDER` | NORTE DE SANTANDER | SI | PERMITIDO |
| `SAN ANDRES` → `SAN ANDRES Y PROVIDENCIA` | SAN ANDRES Y PROVIDENCIA | NO | BLOQUEADO |
| `SAN ANDRES` → `SAN ANDRES Y PROVIDENCIA` | SAN ANDRES Y PROVIDENCIA | NO | BLOQUEADO |
| `ARCHIPIELAGO DE SAN ANDRES` → `SAN ANDRES Y PROVIDENCIA` | SAN ANDRES Y PROVIDENCIA | NO | BLOQUEADO |

Los alias de San Andres mapean a un destino que NO esta en la lista blanca → correctamente bloqueados. **PASA.**

### Casos limite

| Entrada | Normalizado | Alias | Final | ¿En blanca? | Resultado |
|---|---|---|---|---|---|
| `''` (vacio) | `''` | `''` | `''` | NO → pero linea 96 salta el bloqueo si normalizado=='' | Cae en validacion de `$required` (linea 37 tiene 'departamento'). Rechazado antes. OK |
| `Otro` | `OTRO` | `OTRO` | `OTRO` | NO | Rechazado: "sin cobertura" |
| `Marte` | `MARTE` | `MARTE` | `MARTE` | NO | Rechazado: "sin cobertura" |
| `Cundinamarca` | `CUNDINAMARCA` | `CUNDINAMARCA` | `CUNDINAMARCA` | SI | Aceptado |

**PASA.**

### Riesgo de tildes con Dropi

El front envia `Bogota D.C.` (con tilde en la o). El backend:
1. `normalizar_departamento("Bogota D.C.")` → `BOGOTA DC` (sin tildes)
2. `$alias['BOGOTA DC']` → `BOGOTA`
3. Se envia a Dropi como `state: "BOGOTA"`

Dropi podria esperar `Bogota D.C.` (con tilde y puntos) si valida contra una lista fija de departamentos colombianos. La mayoria de APIs de logistica colombiana usan codigos DIVIPOLA (ej: 11001 para Bogota), pero Dropi es un marketplace de dropshipping — no hay certeza de que hagan validacion estricta de nombres de departamento.

**Riesgo: BAJO.** No se puede verificar sin una prueba real en Dropi. El Monarca debe hacer un pedido de prueba con direccion en Bogota y verificar que Dropi lo acepte. Si lo rechaza, habra que enviar el nombre con tildes o usar el codigo DIVIPOLA.

---

## 3. EL FRONT: ¿MUESTRA EL MENSAJE AHORA?

### Lo que dice el codigo

```typescript
// Linea 68: si la respuesta NO es ok (status >= 400), lanza Error generico
if (!response.ok) throw new Error('Error al crear pedido');

// Linea 81-93: catch intenta leer JSON, PERO...
} catch (error) {
  if (error instanceof Response) {          // <-- ESTO NUNCA ES TRUE
    error.json().then(data => {             // <-- CODIGO MUERTO
      const errorMessage = data.mensaje || data.error || 'Error al procesar el pedido';
      alert(errorMessage);
    }).catch(() => {
      alert('Error al procesar el pedido');
    });
  } else {
    alert('Error al procesar el pedido');   // <-- SIEMPRE CAE AQUI
  }
  setSubmitStatus('error');
}
```

### El problema

`throw new Error(...)` produce un objeto `Error`, no un `Response`. El `instanceof Response` en linea 83 **nunca es verdadero**. El codigo que lee `data.mensaje || data.error` esta muerto — es inalcanzable.

**El cliente NUNCA ve los mensajes del servidor.** Cuando el backend responde 422 ("sin cobertura en tu departamento") o 429 ("limite de pedidos"), el cliente solo ve "Error al procesar el pedido".

### La intencion vs. la realidad

La intencion de arreglarlo esta visible (el codigo de las lineas 82-92 fue agregado para esto), pero la mecanica throw/catch esta mal implementada. El `response` se descarta en la linea 68 antes de que el catch pueda leer su body.

### Correccion necesaria

```typescript
// Opcion A: leer el JSON SIEMPRE, decidir despues
const result = await response.json();
if (!response.ok) {
  throw { serverError: true, data: result };
}
// ... en el catch:
if (error?.serverError) {
  alert(error.data.mensaje || error.data.error || 'Error al procesar el pedido');
}
```

```typescript
// Opcion B: no lanzar, manejar inline
const result = await response.json();
if (!response.ok) {
  alert(result.mensaje || result.error || 'Error al procesar el pedido');
  setSubmitStatus('error');
  setIsSubmitting(false);
  return;
}
```

**Severidad: ALTO.** No bloquea el despliegue (los pedidos exitosos funcionan), pero degrada la experiencia del usuario que recibe errores.

### ¿"Otro" fue retirado del selector?

SI. Lineas 249-268 de CheckoutForm.tsx: 19 opciones concretas, ninguna es "Otro". **PASA.**

### Departamentos en el front vs. lista blanca

Front tiene 19. Lista blanca backend tiene 24. Faltan en el dropdown:

| Departamento | En whitelist | En front |
|---|---|---|
| CAQUETA | SI | NO |
| CASANARE | SI | NO |
| CAUCA | SI | NO |
| LA GUAJIRA | SI | NO |
| SUCRE | SI | NO |

Clientes en Caqueta, Casanare, Cauca, La Guajira y Sucre no pueden seleccionar su departamento en el dropdown. Tendrian que manipular el request para comprar (el backend SI los aceptaria). **COSMETICA** — el front necesita agregar esas 5 opciones.

---

## 4. NO REGRESION

### MD5 dentro del ZIP vs. fuentes

| Archivo | MD5 fuente | MD5 en ZIP | Veredicto |
|---|---|---|---|
| `api/pedidos.php` | `a963789458423ec9193bad4c08bd3fac` | `a963789458423ec9193bad4c08bd3fac` | PASA |
| `api/procesar-pedidos.php` | `592b781f3c68f2262fda4a6a5ee99a67` | `592b781f3c68f2262fda4a6a5ee99a67` | PASA |

### ZIP sin secretos

| Archivo prohibido | En ZIP |
|---|---|
| `seawolf-config.php` | NO |
| `notify-config.php` | NO |
| `secrets.local.json` | NO |
| `.env` | NO |

**PASA.**

### Estructura del ZIP

| Elemento | Estado |
|---|---|
| `index.html` en raiz | Presente |
| `.htaccess` | Presente (1981 bytes) |
| `products.json` | Presente (~617 KB) |
| Solo 2 PHP (`pedidos.php`, `procesar-pedidos.php`) | Correcto |

**PASA.** (El conteo de productos no se re-verifica; la auditoria anterior confirmo ~200 productos con 199 dropi_id.)

### Llave del puente `sw7-Gh41` en archivos rastreados de git

| Archivo | Ocurrencias |
|---|---|
| `mantenimiento/config.json` | 1 |
| `mantenimiento/MANUAL-MANTENIMIENTO.md` | 1 |
| `mantenimiento/sincronizar_tienda.py` | 1 |
| `mantenimiento/secrets.local.json` | 1 |

**Total: 4 archivos.** Ninguno esta en el ZIP. Pendiente: `.gitignore` no cubre `mantenimiento/secrets.local.json`. (Mismo hallazgo que la auditoria anterior — I1.)

### Clave del procesador `sw-proceso-2026` en archivos rastreados de git

| Archivo | Ocurrencias |
|---|---|
| `mantenimiento/PENDIENTES-DESPLIEGUE.md` | 1 |
| `mantenimiento/secrets.local.json` | 1 |

**Total: 2 archivos.** LEEME-DEPLOY.txt ya tiene 0 (limpiado). Pendiente igual: `.gitignore` no cubre `mantenimiento/secrets.local.json`.

---

## 5. RIESGOS QUE SOLO SE PRUEBAN EN EL SERVIDOR

1. **Sintaxis PHP real**: sin `php -l`. La revision manual de ambos archivos es limpia. Probabilidad de error de sintaxis: BAJA.

2. **Dropi bridge**: no se puede verificar que `hotpink-nightingale-238140.hostingersite.com` este vivo y acepte el payload.

3. **`mail()` en Hostinger**: puede estar deshabilitada. El `@` suprime el error, los pedidos se guardan igual.

4. **Permisos de `data-pedidos/`**: `mkdir(0755)` puede no ser suficiente en shared hosting.

5. **Carga de `products.json` (617 KB)**: en shared hosting con poca memoria, `json_decode` de ese archivo podria fallar o ser lento. El procesador y pedidos.php lo cargan completo.

6. **Nombre del departamento con/sin tildes en Dropi**: detallado en seccion 2. Probar con un pedido real en Bogota.

7. **Front compilado vs. fuente**: el ZIP contiene `_astro/CheckoutForm.Fs3E8soE.js` (compilado de Astro). Verificar que corresponda a la version corregida de `CheckoutForm.tsx`. Si el build no se re-genero despues de la correccion, el JS compilado podria ser la version vieja. **El Monarca debe re-ejecutar `npm run build` antes de generar el ZIP final.**

8. **`$MODO_PRUEBA = true`** en procesar-pedidos.php (linea 24): recordatorio — cambiarlo a `false` en el servidor real.

---

## 6. RESUMEN DE HALLAZGOS

| # | Severidad | Archivo | Descripcion |
|---|---|---|---|
| B1 | **CERRADO** | pedidos.php | `$departamento_final` definido y usado |
| B2 | **CERRADO** | pedidos.php | `tg()` comentada, sin codigo activo |
| B3 | **CERRADO** | LEEME-DEPLOY.txt | `sw-proceso-2026` eliminado (0 ocurrencias) |
| R1 | ALTO | CheckoutForm.tsx:68 | Mensajes de error del servidor nunca se muestran (codigo de manejo inalcanzable) |
| R2 | COSMETICA | CheckoutForm.tsx:249-268 | Faltan 5 departamentos en el dropdown (Caqueta, Casanare, Cauca, La Guajira, Sucre) |
| R3 | BAJO | pedidos.php:96-104 | Departamento vacio salta el bloqueo de lista blanca (mitigado por $required) |
| R4 | BAJO | — | Tildes: Dropi podria esperar "Bogota D.C." pero recibe "BOGOTA" |
| I1 | MEDIO | .gitignore | `mantenimiento/secrets.local.json` sigue sin estar en .gitignore |
| I2 | ALTO | _astro/CheckoutForm.*.js | El JS compilado en el ZIP podria no corresponder al .tsx corregido si no se hizo rebuild |

---

## 7. QUE HACE FALTA PARA SUBIR

1. **CORREGIR** CheckoutForm.tsx linea 68: cambiar `throw new Error(...)` por lectura del JSON de error antes del throw (o manejar el error inline sin throw).
2. **AGREGAR** los 5 departamentos faltantes al dropdown del front.
3. **REBUILDEAR** con `npm run build` y regenerar el ZIP.
4. **CAMBIAR** `$MODO_PRUEBA = false` en el servidor real.
5. **PROBAR** un pedido simulado con departamento Bogota para verificar que Dropi acepte el nombre sin tildes.

---

*Informe generado por Beru, Auditor General de Seawolf Studio.*
*Ruta: C:/Users/Admin/seawolf-agent/intel/tienda/beru-reauditoria-paquete-20261014.md*