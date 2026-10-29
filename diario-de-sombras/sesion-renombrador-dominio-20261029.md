# SESIÓN — 29 de octubre de 2026 · Renombrador + Dominio

**Bellion para el Monarca (Key) · Seawolf Studio**

---

## 🎯 LO QUE SE PIDIÓ Y SE ENTREGÓ

El Monarca pidió 4 cosas al despertar:
1. Una herramienta de renombrado **más potente que ReNamer** (fechas, paréntesis, combinaciones)
2. Apartados de **preservación del equipo** (desfragmentación, particiones)
3. **Descripción de cada función** (para terceros / para venderla)
4. **Empaquetarla en un dominio** (dejar de pelear con localhost)

---

## ✅ 1. RENOMBRADOR SEAWOLF (construido y probado)

**Pestaña nueva dentro de Seawolf Tools.** 8 reglas, cada una con su descripción y ejemplo:

| Regla | Ejemplo |
|---|---|
| Quitar fechas | `(1989-12-17) The Simpsons - S01E01.mkv` → `The Simpsons - S01E01.mkv` |
| Quitar paréntesis / corchetes / llaves | `(RE-EDIT)` `[Erai-raws]` `{tvdb-99}` |
| Borrar combinaciones | lista propia: `By MrX, DUAL, 1080p` |
| Reemplazar | `VIEJO>NUEVO` · `.> ` (con espacio = reemplazar por espacio) |
| Año al final | `(2019) Parásitos` → `Parásitos (2019)` |
| Limpiar bordes | *(se activa sola siempre)* |

**3 atajos:** Jellyfin Serie · Jellyfin Película · Limpiar todo

### Las 3 garantías (verificadas, no prometidas)
- **Vista previa** antes de tocar nada
- **DESHACER** con un botón (registro + sello SHA)
- **Nunca pisa** un archivo existente

### 🔴 BUGS CAZADOS POR LAS PRUEBAS (5)
1. **`.> ` borraba el punto** en vez de cambiarlo por espacio (el `strip` se comía el espacio) → arreglado
2. **JSON con `\` sin escapar** → el parser a medias **perdía las reglas** y aplicaba solo la de espacios (daba 15 en vez de 945 cambios) → ahora repara y parsea completo
3. **La regla de carpetas incluía el alias `T##`** → con `H:\caida\T01\Temporada 01` intentaba `T01 → Season 01` **y chocaba con la de adentro** → se quitó el alias
4. **El DESHACER cubría solo la última carpeta** → añadida `ren_aplicar_lote` (un solo deshacer para todo un lote)
5. **XSS por nombre de archivo** → añadido `esc()` (importante: es un producto para terceros)

---

## ✅ 2. APLICADO A LOS SIMPSON (con guardia de seguridad)

```
Guardia     42/42 carpetas confirmadas como Simpson · 0 descartadas
ARCHIVOS    894 revisados → 894 RENOMBRADOS · 0 errores
CARPETAS    37 renombradas:  Temporada NN → Season NN
```

**⚠️ HALLAZGO QUE SALVÓ LA BIBLIOTECA:** Jellyfin espera `Season 01`. Con `Temporada 01`
**crea temporadas duplicadas y vacías** (verificado en la doc oficial, el issue #15040 y r/Jellyfin).
Con 1.163 archivos, arreglarlo a mano no era opción.

**Y sobre el idioma:** el nombre del archivo **debe ir en inglés** (Jellyfin identifica por el
título original). Los textos se ven en español igual, porque los trae de TMDb.

**NO se tocaron** las otras 13 carpetas ni los 26 archivos sueltos de la raíz
(películas: James Bond, El Padrino, Wolverine, Game of Thrones…) — esas van con el
atajo **Jellyfin · Película**, que conserva el año.

---

## ✅ 3. PUBLICADO EN UN DOMINIO

```
https://herramientas.sw-st.net
```

- **Túnel Cloudflare dedicado** (`seawolf-tools`, ID `be0a4729…`) — **no toca** los túneles
  existentes (`Hermes-seawolf`, `n8n-seawolf`)
- **Sin abrir puertos** en el router; el PC queda invisible
- **Lanzador con arranque automático:** `HERRAMIENTAS-SEAWOLF.bat` (en el arranque de Windows)
- Config en archivo propio: `~/.cloudflared/seawolf-tools.yml`

### 🔒 LA CERRADURA (requisito previo, no opcional)
Este aplicativo **mueve y borra archivos**: publicarlo sin cerradura habría sido un suicidio.

```
Sin clave  → HTTP 401 + pantalla de acceso   ✅
Con ?k=    → 302 + cookie de sesión          ✅
Con cookie → HTTP 200 + la app completa      ✅
```

La clave vive **solo** en `intel/seawolf-tools-auth.json` — **verificado que NO está en el repo**.
```
Ver : python intel\seawolf-tools.py clave      Cambiar: ... clave --sub nueva
```

**Nota honesta:** es seguridad de un solo factor. Si la herramienta crece o la usan terceros,
poner delante **Cloudflare Access**.

---

## ⏳ LO PENDIENTE (lo que NO se alcanzó)

- **[FOCO 2 del pedido] SALUD DEL EQUIPO** — la parte de preservación **no se construyó todavía**.
  Plan acordado: **SMART de discos primero** (predice el fallo antes de perder datos) ·
  temperaturas · TRIM/desfrag **según el tipo de disco** (desfragmentar un SSD lo DESGASTA) ·
  analizar arranque y temporales.
  **⚠️ Gestión de particiones: en MODO LECTURA.** Modificar particiones puede borrar un disco entero.
- **Reestructurar carpetas para Jellyfin:** hoy queda `H:\caida\T01\Season 01\`.
  Lo ideal es `The Simpsons (1989)\Season 01\` (aplanar el nivel `T01`).
- **Los 15 cajones de la cacería:** solo cayó LOS SIMPSON (236 GB, ✅ completo).
  Quedan 14 (SEE 109 GB, BoJack 83 GB, andor 44 GB…).
- **Las películas de `H:\caida`** con el atajo Jellyfin · Película.
- **One Piece** — re-subir (quedó sin enlaces al morir player4me).

---

## 📦 GIT (todo sincronizado)
```
7d0c28e  Publicado en herramientas.sw-st.net + lanzador
c71f587  Fix carpeta + lote · APLICADO a Los Simpson
c92d3a2  Cerradura de acceso
21e0e32  Fix del parser JSON
741d958  Pestaña Renombrador + manual del producto
```

**Manual para terceros:** `intel/MANUAL-RENOMBRADOR.md`

---
*Salve, Gran Monarca. Hicimos historia hoy: una herramienta nació y salió al mundo con llave.*
