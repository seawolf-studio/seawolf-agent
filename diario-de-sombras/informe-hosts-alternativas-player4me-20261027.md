# ALTERNATIVAS A PLAYER4ME — informe de hosts de video
**Seawolf Studio · 27 de octubre de 2026 · Bellion (Gran Comandante)**

---

## 1. Punto de partida: por qué murió player4me

**Medición objetiva (Internet Archive):**

| Dato | Valor |
|---|---|
| Primera captura del dominio | **marzo de 2025** |
| Estado hoy | **MUERTO** — `player4me.com` sin IP; `4meplayer.pro` entra a Cloudflare pero el origen **no contesta** (timeout) |
| Vida útil | **~1 año** |

**Conclusión:** player4me no era un host con trayectoria. **Era un proyecto nuevo** que cerró antes de cumplir dos años. Esto fija el criterio principal de esta búsqueda.

> **Regla que saco de esto:** los hosts de este sector tienen una **vida media de ~5 años** (dato de un uploader veterano en WJunction). Un host nuevo **no tiene historia que perder** y es el primero que cae. **Siempre se eligen hosts con años encima, y siempre se mantienen TRES vivos a la vez.**

---

## 2. Las 5 recomendadas (para dar de alta)

### 1️⃣ DoodStream — *la que más paga*
| | |
|---|---|
| **En línea desde** | **2020** (6 años) |
| **Vivo hoy** | ✅ HTTP 200 |
| **Tarifa** | **Hasta $33 por 10.000 vistas** (EE.UU./Canadá/Reino Unido/Australia); $22 Europa; $11 resto; **$5 "otros"** |
| **Mínimo de pago** | **$10** ✅ (el más bajo junto a streamtape) |
| **Pago** | Procesado en **menos de 24 h** (máximo 1 semana) |
| **Archivos** | Gratis: borra inactivos a los 60 días · Premium: nunca |
| **Vistas contadas** | 3 por IP/24 h |
| **⚠️ Riesgo** | Es el host con **más historial legal** del sector: cayó y volvió. **Alta rentabilidad, alta volatilidad** |

### 2️⃣ LuluStream — *la equilibrada*
| | |
|---|---|
| **En línea desde** | **2018** (7 años) |
| **Vivo hoy** | ✅ HTTP 200 |
| **Tarifa** | **$25–$40 por 10.000 vistas** |
| **Mínimo de pago** | **$20** |
| **Pago** | **Dentro de 24 horas** ✅ (el más rápido) |
| **Subida** | Navegador, **FTP, remoto y API** ✅ |
| **Extras** | Sin límite de ancho de banda · 4 vistas/IP/24 h · adulto legal permitido |

### 3️⃣ Vidoza — *la más veterana*
| | |
|---|---|
| **En línea desde** | **2014** (11 años) — la 2ª más antigua del sector |
| **Vivo hoy** | ✅ HTTP 200 *(muestra "acceso restringido" para ciertos países/IP de datacenter — normal en ellos)* |
| **Subida** | FTP, remoto, torrent, API |
| **Ventaja** | **La trayectoria más larga** = la menos probable de caer sin avisar |
| **⚠️ Nota** | Tarifa y mínimo **no publicados sin cuenta** |

### 4️⃣ VidMoly — *la nerviosa pero cumplidora*
| | |
|---|---|
| **En línea desde** | **2019** (6 años) |
| **Mínimo de pago** | **$15** |
| **Pago** | **Dentro de 48 horas** |
| **⚠️ Nota** | Su web principal se comporta raro desde IPs de datacenter/curl; en navegador normal funciona |

### 5️⃣ FileMoon — *la popular de hoy*
| | |
|---|---|
| **En línea desde** | **2022** (4 años) |
| **Vivo hoy** | ✅ HTTP 200 |
| **Ventaja** | Es **la que más usan los sitios pares hoy** — el "estándar de facto" actual |
| **⚠️ Nota** | 4 años la hace la **más joven** de las cinco. Vigilar su salud |

---

## 3. Descartadas (y por qué)

| Host | Motivo |
|---|---|
| **StreamHub** (`streamhub.to`) | ❌ **MUERTO** — HTTP 000, sin respuesta |
| **MixDrop** (`mixdrop.co`) | ❌ **Dominio muerto** — HTTP **410 Gone**. El vivo es **`mixdrop.ag`** (usar ese si se quiere) |
| **StreamWish** (`streamwish.to`) | ⚠️ **En problemas HOY** — respondió 522 (origen caído) y 403. No dar de alta ahora |
| **VidHide** (`vidhide.com`) | ⚠️ **Solo 2,5 años** (2023) y su web se muestra ya como *"EarnVids"* (rebranding en curso — señal de movimiento interno). Mínimo $20 |
| **StreamHG / BigWarp / Earnvids** | ⚠️ Demasiado nuevos (finales de 2024) — recién nacidos |

---

## 4. Compatibilidad con su FileUploader — **honestidad total**

**NO pude verificar la lista de hosts de su FileUploader.** Razón técnica: el programa es un ensamblado .NET **ofuscado** y su configuración (`FileUploader.nast`) está **cifrada** — no es legible ni SQLite. **Tampoco existe una lista pública documentada** de ese programa en concreto.

**Lo que SÍ sé, por evidencia de su propio registro:**
- Sube a `voe.sx`, `streamtape.com` y `player4me.com[APi]`
- **Ese sufijo `[APi]` es la pista importante:** significa que su FileUploader **admite hosts configurados por API**, no solo los que trae de fábrica.

**Y las cinco recomendadas cumplen el requisito técnico:**
> **Todas publican API de subida** (DoodStream, LuluStream, Vidoza, VidMoly y FileMoon documentan API/FTP/remoto). Es el mismo camino que ya usó con player4me.

**Verificación de 10 segundos (suyo):** al abrir FileUploader, mire el desplegable de hosts. Si alguna no está, se le añade por API como hizo con player4me.

---

## 5. Recomendación final

**Dar de alta estas cuatro** (la 5ª, FileMoon, solo si quiere 5):

| Prioridad | Host | Por qué |
|---|---|---|
| **1** | **DoodStream** | La que más paga, mínimo $10 |
| **2** | **LuluStream** | 7 años, paga en 24 h, sube por API |
| **3** | **Vidoza** | 11 años — la más difícil de que caiga |
| **4** | **VidMoly** | 6 años, mínimo $15 |
| **5** | **FileMoon** | La más usada hoy por los sitios pares |

**Junto a las dos que ya tiene (Streamtape 13 años · VoE 5 años) = 6-7 destinos.**

### Y la regla de oro que le dejo
> **Nunca menos de 3 hosts vivos, nunca un host con menos de 3 años, y nunca confiar en que uno esté ahí mañana.**
> **El negocio no puede depender de un solo host** — player4me lo acaba de demostrar con 12 episodios a medio subir.

---

## 6. Fuentes

- **Internet Archive (CDX)** — primera captura de cada dominio (antigüedad verificada)
- **DoodStream** — página oficial de pagos (`doodstream.com/earn-money`): tarifas por tier y mínimo $10
- **LuluStream** — web oficial + hilo de WJunction ($20 mínimo) + ficha de TechRadar ($25-40/10k)
- **VidMoly** — página oficial `make-money`: mínimo $15, pago en 48 h
- **WJunction / BlackHatWorld** — hilos de uploaders: vida media de un host ~5 años; streamtape mínimo $10; recomendaciones cruzadas
- **Awesome-file-hosts (GitHub)** — métodos de subida y API de cada host
- **Pruebas propias en vivo** (27-oct-2026): estado HTTP de 11 dominios y DNS de player4me

---

# 🔄 ACTUALIZACIÓN — decisión del Monarca (27-oct-2026, tarde)

## Vetados por decisión propia
| Host | Motivo |
|---|---|
| **DoodStream** | **VETADO** — ya lo dejó tirado una vez. *(quien traiciona no vuelve)* |
| **FileMoon** | **VETADO** — mismo motivo |

## Confirmado por el Monarca
**Vidoza y VidMoly están en la lista de hosts de su FileUploader** ✅ → compatibilidad verificada en el campo.

## Las 3 que faltan (verificadas en vivo)

### A) LuluStream — 2018 (7 años) · HTTP 200 ✅
Mínimo **$20** · paga en **24 h** · HLS · FTP/remoto/**API** · sin límite de ancho de banda.

### B) MixDrop — servicio desde 2019 (6 años) · `mixdrop.ag` HTTP 200 ✅
Web oficial con **sección de afiliados** activa · embebido de video y audio · sin límites.
⚠️ **Usar `mixdrop.ag`** (el `mixdrop.co` que circula está muerto, 410 Gone).

### C) NetU (`netu.to`) — veterano de la escena · HTTP 200 ✅
Varios años en el sector · **muy usado en el público hispano** · subida múltiple, remoto y **FTP** · máximo 8096 MB / 500 min · tiene programa de webmasters con monetización.

## Alternos (si alguno no está en su FileUploader)

### D) StreamRuby — dominio desde 2021 (4 años) · HTTP 200 ✅
**El más transparente de todos:** publica **$3M+ pagados**, 264M vistas/mes, 527 TB alojados.
250 GB gratis que crecen · HLS adaptativo · **5 métodos de subida** · API.
🎯 **Joyita operativa:** tiene **"Clone Upload" — clona archivos desde OTRO host sin volver a subirlos.** Es decir: lo que ya subió a Streamtape o VoE se puede clonar a StreamRuby **sin gastar subida**.

### E) StreamA2Z — dominio desde 2018 (7 años) · HTTP 200 ✅
Programa de recompensa por vistas + referidos.
⚠️ Sus cifras publicadas (10.999.999+ vistas, 1000+ usuarios) **parecen de mercadeo** — no me fío de ellas.

## Descartados por estado técnico
`streamhub.to` (muerto) · `mixdrop.co` (muerto) · `streamwish.to` (522 hoy) · `vidguard.to` (000) · `goodstream.one` (000) · `1uploadflix.net` y `dropload.pro` (demasiado nuevos)

## Recomendación final de Bellion
**Dar de alta: LuluStream · MixDrop(`.ag`) · NetU** → con Streamtape, VoE, Vidoza y VidMoly = **7 destinos**.
**Alternos a tener a mano:** StreamRuby (por el clonado) y StreamA2Z.

> **Regla de oro:** nunca menos de 3 vivos · nunca uno con menos de 3 años · y el negocio **nunca** colgando de un solo host.

---
*Informe generado por Bellion — Seawolf Studio. Datos verificables; lo no verificable se marca como tal.*
