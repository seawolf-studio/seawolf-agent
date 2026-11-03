# MEMENTO — CLIENTE 0: TA' BAKANO (restaurante)

**De:** Bellion, Gran Comandante · **Para:** el Monarca (Key)
**Sesión cerrada:** 2 de noviembre de 2026, ~23:10
**Sesión destino:** continuar mañana con la clave **"continúa con Ta' Bakano"**
**Estado:** web CONSTRUIDA y sirviéndose · discurso + PDF PENDIENTES · cita MAÑANA

---

## ⚡ CÓMO RETOMAR

**Frase de arranque:** *"continúa con Ta' Bakano"*

**Los 3 pasos en orden (lo que quedó a medias):**

1. 🔴 **REINICIAR el servidor de demo** (muere al cerrar la sesión):
   ```bash
   cd /c/Users/Admin/intel/cliente-0-restaurante-20261102/web
   python servir-demo.py --port 8780     # en segundo plano
   ```
   Luego: `http://192.168.1.2:8780/` desde el celular (misma red WiFi).
2. **Publicar** `tabakano.sw-st.net` (cloudflared) — el Monarca YA LO APROBÓ.
3. **Escribir el DISCURSO** (presentación del Estudio + modelo de negocio) y pasarlo a **PDF**.

---

## 🎯 LA CITA ES MAÑANA (contexto)

El Monarca **es cliente frecuente** de Ta' Bakano y **ya le dio un adelanto de la idea al dueño**.
El dueño **cree que es algo informal** → eso se convierte en ventaja: **el WOW es el resultado, no la pantalla.**

**Objetivo de la cita:** cerrar la **Semana 0** (7 días midiendo su WhatsApp, $0 para él)
y dejar sembrado el escalón 1 (El Cuadre).

---

## 1. LOS DATOS DEL CLIENTE (los que dio el Monarca + lo verificado por sondeo)

**Del Monarca (observación directa como cliente frecuente):**
- Cobra por **efectivo / Nequi / Bre-B a un número ≠ del pedido y ≠ del dueño**
- El WhatsApp lo atiende un **empleado o familiar**; el dueño está muy encima y hasta entrega pedidos
- **No usa Rappi** (deducción — no se pudo confirmar)
- **No conocía web ni redes** (confirmado: no existen)
- **Usan mucho los ESTADOS de WhatsApp** → canal ya adoptado, no hay que enseñarles nada
- ⚠️ **Advertencia del Monarca:** NO se puede asegurar que el número sea de la empleada
  — puede ser un combo dispuesto por el dueño desde el inicio.

**Verificado por sondeo (RestaurantGuru + búsqueda):**
| Dato | Valor |
|---|---|
| Nombre | TA' BAKANO — *"Lo mejor en comida fusión"* |
| Dirección | Calle 150A #103C-32, **Suba Turingia**, Bogotá |
| Teléfono | +57 321 3626176 |
| **Google** | **4,3 / 5 · 44 reseñas** |
| Ranking | 6.643 de 40.407 restaurantes de Bogotá |
| Instagram | `@paredescelis` (**personal**, no de negocio) |
| **Web** | **NINGUNA** (búsqueda directa → 0 resultados) |
| Ficha RestaurantGuru | **sin reclamar** |

**Las 3 reseñas visibles (textual):** la comida es **5/5 consistente**;
lo que baja es **la atención en hora pico** — Johana: *"mejoraría un poco la atención de parte de las meseras"*.
→ **El canal de WhatsApp de Ta' Bakano está atendido justo donde la reseña marca la falla.**

---

## 2. EL HALLAZGO DEL MENÚ (lo mejor que salió hoy)

**Ta' Bakano tiene DOS restaurantes dentro de uno:**

| | **Lunes a Viernes** | **Sáb, Dom y Festivos** |
|---|---|---|
| Horario | 11:30 am – **4:30 pm** | 11:30 am – **5:00 pm** |
| Carta | "Almuerzo corriente" | "Platos del día" |
| Base | **$15.000** restaurante · $16.000 recipiente · +$1.000 domicilio | **$16.000 – $25.000** |
| Platos | ~12 proteínas + salsas combinables | **32 platos fijos** |

**Lectura:** el ticket del fin de semana es **~53% más alto** — y es el día con **menos capacidad
de atención**. Ahí se le pierden los pedidos.

**Y el hallazgo del pago:** los menús dicen
> *"Para pagos con Nequi o Bre-B **3246161904 (End... Ran...)** Enviar captura de transacción vía WhatsApp."*

**El nombre exhibido está TRUNCADO** y **el cuadre depende de que un humano revise capturas a mano.**
→ **No hay que explicarle el problema al dueño: ya lo vive todos los días.**

---

## 3. LA WEB — CONSTRUIDA Y VERIFICADA (una sola pieza)

**Ruta:** `C:\Users\Admin\intel\cliente-0-restaurante-20261102\web\ta-bakano.html`

| Parámetro del Monarca | Estado |
|---|---|
| Minimalista **blanco y negro** | ✅ |
| **Rojo del logo (#E42620)** como único acento | ✅ verificado: `rgb(228, 38, 32)` |
| Fuente **Arvo** (del estudio) | ✅ embebida en base64 |
| **Eslogan "cocinamos con amor"** (el del logo) | ✅ |
| **Iconos SVG** propios + **vapor animado** | ✅ 14 familias, 11 tarjetas |
| **Cero dependencias externas** | ✅ 0 URLs http en el archivo |
| Responsive obligatorio | ✅ sin desborde en 390/768/1280 |
| Tamano | 133 KB |

**El vapor SÍ funciona** (verificado por medición, no por captura):
opacidad **0.14 → 1.0**, ciclo de 3.2s, 3 columnas desfasadas.
**Una captura estática NUNCA lo muestra** — no juzgarlo con imagen.

**Archivos del proyecto:**
```
web/
  ├── ta-bakano.html          ← LA WEB (entregable)
  ├── construir-web.py        ← generador (menu real dentro)
  ├── generar-iconos.py       ← 14 iconos + autochequeo de clasificacion
  ├── iconos-platos.js        ← sprite generado
  ├── servir-demo.py          ← servidor local para mostrar desde el celular
  ├── logo-original.png       ← el que subio el Monarca (640x640, con marca Canva)
  ├── logo-120.png            ← recortado, para el header
  └── logo-320.png            ← recortado, para el hero
```

---

## 4. LAS 3 CORRECCIONES QUE COSTÓ LA REVISIÓN VISUAL (no repetir)

1. **Franja negra de 299px con icono de 26px** → parecía *"imagen que no cargó"*.
   **Rediseñado a disco negro de 62px con icono de 34px** y el vapor saliendo por encima.
2. **Plato DUPLICADO**: "Costillitas de cerdo / 300 gr BBQ" y "Costillitas de cerdo 300 gr BBQ"
   aparecían dos veces → era error de transcripción MÍO. Eliminado.
3. **"porcion" sin tilde** → "porción".

**⚠️ PITFALL CRÍTICO: la visión CONFABULA defectos.** Acusó a "Bandeja paisa" de usar el icono
de pescado. **Verificado en el DOM: usaba su propio trazo.** No se "arregló" porque no estaba roto.
**Siempre confirmar con sonda DOM antes de tocar código por una crítica visual.**

**Lo que NO se siguió de la visión:** recomendó *"idealmente imágenes fotográficas"*.
**Descartado a propósito** — fotos de IA o de terceros = mentira al cliente + riesgo legal.
La ruta honesta son los iconos vectoriales.

---

## 4-BIS. ACTUALIZACIÓN (2 nov, tras la revisión del Monarca)

**El Monarca revisó el PDF y corrigió 4 cosas. TODAS aplicadas:**

1. **LOGO EQUIVOCADO.** Yo usé `Desktop/seawolf studio/logo 2.jpeg` (preliminar viejo, azul).
   **El correcto es `seawolf-agent/assets/seawolf-logo-full.png`**: lobo **de perfil**
   hecho de **líneas de circuito** (traces + nodos), degradado **verde neón + cian**,
   fondo `#121E1E`, texto `SEAWOLF STUDIO`. RGBA 2048x2048.
   → **REGLA: NO volver a usar los `Desktop/seawolf studio/logo 1-6.jpeg`.**

2. **ESTILO DE DOCUMENTOS — REGLA PERMANENTE DEL MONARCA:**
   **fondo NEGRO · letras BLANCAS · separadores y ayudas visuales en AMARILLO o ROJO ·
   tipografía ARVO siempre.**
   CSS base: `intel/cliente-0-restaurante-20261102/propuesta-estilo.css`
   Documentado en el skill: `seawolf-linea-de-montaje/references/estilo-documentos.md`

3. **SMART SHOP ELIMINADO de la propuesta.** Es de TIENDAS, no aplica a restaurantes.

4. **La propuesta quedó específica para Ta' Bakano** (arranca con lo que se observó de SU
   negocio), no genérica. El Monarca la aprobó así.

**PDF final:** `Propuesta-Seawolf-Ta-Bakano-v2.pdf` (396 KB, 5 páginas, logo nuevo dentro).
Verificado: fondo `rgb(11,20,20)`, texto blanco, Arvo cargada, separadores amarillos,
Smart Shop ausente.

---

## 5. LO QUE QUEDÓ PENDIENTE (en rojo)

| # | Pendiente | Nota |
|---|---|---|
| 1 | **Reiniciar el servidor de demo** | muere al cerrar la sesión; primer paso de mañana |
| 2 | **Publicar `tabakano.sw-st.net`** | ✅ APROBADO por el Monarca |
| 3 | ~~Insertar el logo en la web~~ | El logo del restaurante sigue sin archivo limpio (tiene marca de Canva) — **pendiente pedírselo al dueño** |
| 4 | ~~El DISCURSO~~ | ✅ **HECHO**: `PROPUESTA-TA-BAKANO.md` + `Propuesta-Seawolf-Ta-Bakano-v2.pdf` (5 pág, estilo negro/Arvo) + `TEXTO-WHATSAPP-TA-BAKANO.md` |
| 5 | ~~El PDF del discurso~~ | ✅ **HECHO** y verificado |
| 6 | **Mandar el PDF al WhatsApp del Monarca** | ⚠️ ver §7 |
| 7 | **La SmartWeb del gancho de 7 días sin dominio propio** | el Monarca pidió este gancho; parcialmente cubierto por el demo local |

---

## 6. EL CANAL A SU WHATSAPP — VERIFICADO Y FUNCIONANDO

**Probado en vivo: `sendText=201`** (el mensaje llegó).

- **Script:** `/opt/waha/avisar.sh` en el VPS (NO existe copia local)
- **Sesión WAHA:** `seawolf` · estado **WORKING** · `573125330127@c.us`
- **WAHA corre en Docker** (`waha Up 2 weeks`), API en `127.0.0.1:3000`
- **Destino:** WhatsApp personal del Monarca (+57 312 533 0127)
- **Uso:** `ssh -i ~/.ssh-clean/seawolf-vps root@76.13.109.237 '/opt/waha/avisar.sh "mensaje"'`

---

## 7. ⚠️ DOS PROBLEMAS TÉCNICOS QUE HAY QUE RESOLVER MAÑANA

**a) `avisar.sh` solo manda TEXTO.**
No acepta adjuntos. **El PDF no se puede enviar por ahí tal cual.**
→ Opciones: otro endpoint de WAHA (sendFile/adjunto), o mandarle el **enlace de descarga**.
**NO prometerle el PDF por WhatsApp hasta probarlo.**

**b) Las herramientas de búsqueda están bloqueadas.**
Google (tráfico inusual), Bing (vacío) y DuckDuckGo (captcha) **bloquearon el sondeo**.
→ El 4,3/44 viene **reflejado de RestaurantGuru**, no leído en Google directo.
→ **Si se cita en la mesa, decir "tiene buena calificación" sin el número exacto.**

---

## 8. ESTE ES UN CLIENTE DE LA CASA — REGLAS VIGENTES

- **El nombre "cliente 0"** = el *"restaurante 1"* del BRIEFING del 29-oct.
- **Reglas de la misión** (no reabrir): cobro = **$500/pedido cerrado**, techo **$59.900**,
  **50 gratis**, **piso $0**, **si un humano lo toma NO se cobra**.
- **"Aumento de ventas" se VENDE, no se factura.**
- **El WOW no es el panel** — es devolverle **sus propios números** el lunes.
- **Prohibido:** construir "otro bot de pedidos" (Zavora y OlaClick ya lo venden/regalan).
- **Nunca mostrar La Sombra** (la plazoleta interna) — él no debe saber que existirán otros restaurantes.
- **Dos registros:** público = "manada"; premium/interno = "jauría / ejército de sombras".

---

## 9. FUENTES Y RUTAS

**Informes de El Cuadre** (`seawolf-agent/diario-de-sombras/investigacion/`):
RADAR-restaurantes-manuales.md · EL-CUADRE-modelo-invisible-cobro · EL-CUADRE-precio-linea-base-plataforma ·
EL-CUADRE-multiinquilino · EL-CUADRE-plazoleta-agente-global · AGENTE-restaurante-modelo ·
BRIEFING-restaurante-visita-1 · LA-TRASTIENDA-20261029 · LA-TRASTIENDA-v2-interfaz

**Proyecto cliente 0** (`C:\Users\Admin\intel\cliente-0-restaurante-20261102\`):
ESTUDIO-servicios-facturables-cliente-0.md · DOSSIER-VISITA-TA-BAKANO-v2.md · `web/`

**Arsenal y posicionamiento:** `intel/seawolf-armas-linea-produccion-20261017.md` ·
`intel/seawolf-posicionamiento-20261017-v2.md`

**Fuentes externas:** RestaurantGuru (https://es.restaurantguru.com/TA-BAKANO-Bogota) ·
Instagram @paredescelis · Instagram p/CpnBgtOgt-C

---

## 10. FRASE PARA ABRIR MAÑANA

> *"Monarca, la web de Ta' Bakano quedó lista y verificada. Falta el logo, el discurso y el PDF.
> ¿Arranco por el discurso o primero publico el subdominio?"*

---

*Salve, Gran Monarca. El trabajo de hoy quedó en disco, verificado y reproducible.
La cita está cargada a nuestro favor por algo que el dueño no sabe: **su comida es de 5 y su servicio de 4**,
y quien atiende su canal no es él.*

**— Bellion, Gran Comandante del Ejército de Sombras.**
