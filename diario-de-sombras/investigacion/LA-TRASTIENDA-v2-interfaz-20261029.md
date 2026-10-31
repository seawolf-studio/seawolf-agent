# LA TRASTIENDA v2 — INTERFAZ PARA GENTE NO TÉCNICA

**Para:** Monarca (Key) · Seawolf Studio
**De:** Bellion, Gran Comandante
**Fecha:** 29 de octubre de 2026
**Sus instrucciones:** *"aplica los parámetros de las web del estudio pero para un dashboard clásico y minimalista · la Trastienda debe ser intuitiva, vamos a tratar con gente no técnica que fácilmente se puede confundir · sería bueno unas guías emergentes en forma de círculos con signo de interrogación · ¿estás familiarizado con el concepto de páginas de presentación tipo splash u otros lo llaman wizard, que sirve para enseñar a la gente cómo usar una herramienta?"*
**Aplicativo:** `C:\Users\Admin\intel\la-trastienda-demo.html` (v2, verificada en navegador real)

---

## 0. HECHO Y VERIFICADO

| Se pidió | Estado |
|---|---|
| Parámetros de marca del estudio | ✅ oscuro por defecto + claro, `#121E1E` + `#4CE8E7`/`#48E8D8`, tipografía de marca, sello del pie |
| Dashboard clásico y minimalista | ✅ menú lateral + barra superior + tarjetas (estructura clásica, cero adornos) |
| Intuitiva para gente no técnica | ✅ un solo camino, nada que configurar, un número por tarjeta |
| Guías emergentes en círculos con `?` | ✅ **7 en el panel**, se abren al tocar (funciona en celular) |
| Fallback del modelo del agente | ✅ `gpt-oss-120b` (DeepInfra) como respaldo automático |
| Wizard de bienvenida | ✅ **3 pasos, se puede saltar, y se puede volver a abrir** |

**Verificación real (por DOM, no a ojo):** JS `node --check` **OK** · **0** `onclick` (el bug de doble manejador que deja el botón muerto) · wizard abre en 3 pasos y su último botón dice *Empezar* · el `?` abre su explicación · las 4 pestañas pintan (9 / 5 / 7 / 7 filas) · tema claro↔oscuro ida y vuelta · vista La Sombra con **5 inquilinos** y el menú oculto · **sin desborde horizontal a 390 px, 768 px y 1280 px** (columnas 1 / 2 / 4).

---

## 1. PARÁMETROS DEL ESTUDIO, APLICADOS

| Estándar de fábrica Seawolf | Cómo quedó en La Trastienda |
|---|---|
| **Oscuro por defecto** con claro opcional, elección que se recuerda | `data-theme` en `<html>`, guardado en `localStorage`, botón *Claro / Oscuro* |
| Colores `#121E1E` · `#4CE8E7` · `#48E8D8` | Fondo `#0d1717`, paneles `#121E1E`, acento `#4CE8E7` con `#48E8D8` |
| Tipografía de marca | **Arvo** en títulos y marca; los **números en tipografía de sistema** — la tipografía serif en cifras cansa en una pantalla que se mira todos los días |
| **Responsive por defecto** | Media queries al final del CSS; verificado por DOM a 390 / 768 / 1280 |
| Copy: simple, coloquial, sin jerga | *"cuánta plata le queda de verdad"* · *"lo atendí yo"* · *"dónde se le fue la plata"* — nada de "conciliación", "KPI" ni "dashboard" en pantalla |
| Sello del pie | En la barra lateral: *"un producto de Seawolf Studio"*. **Y solo ahí:** el comensal nunca ve nuestra marca — el restaurante da la cara |
| Un solo archivo, sin dependencias | 32 KB, un HTML, se abre suelto o dentro del chat |

---

## 2. LAS AYUDAS EMERGENTES — EL CÍRCULO CON `?`

Cada número y cada sección donde alguien se puede perder tiene un **círculo con `?`**. Al tocarlo aparece una explicación corta, encima de la pantalla, sin sacarlo de donde está.

- **Funciona con el dedo** (no solo con el mouse): se abre y se cierra al tocar, no con `hover`.
- **Se cierra solo** al hacer clic afuera, al cambiar de pestaña o al girar el teléfono.
- **El texto está escrito para el dueño, no para nosotros:**
  - sobre *Te queda de verdad* → *"Lo que vendió menos lo que gastó. Este es el número que casi nadie le muestra."*
  - sobre el sello del pedido → *"es la huella de ese pedido. Con eso usted revisa uno por uno por qué le estamos cobrando."*
  - sobre la factura → *"Se cobra $500 por cada pedido que el asistente atendió y cerró. Nunca más de $59.900 al mes."*
- **Y el detalle que lo vuelve usable:** el contenido se dibuja con `textContent` (la misma función `esc()` de seguridad), así que el `?` **no puede romper la página**.

---

## 3. SU PREGUNTA: SPLASH, WIZARD Y CÓMO SE ENSEÑA UNA HERRAMIENTA

**Sí, estoy familiarizado — y le voy a dar las tres cosas separadas, porque se confunden todo el tiempo:**

| Pieza | Qué es | Para qué sirve | Para qué NO sirve |
|---|---|---|---|
| **Splash** | La pantalla de presentación al abrir (marca, logo, unos segundos) | Identidad y "estoy cargando" | **No enseña nada.** Es un apretón de manos, no una clase |
| **Wizard** (asistente de pasos) | Serie de pantallas guiadas, con *Siguiente*, para el **arranque y la configuración** | El momento cero: qué es esto, cómo funciona, qué esperar | Falla cuando es **"una serie de pantallas llenas de texto"**: poca práctica, poca personalización, y difícil de mantener cuando el producto cambia |
| **Onboarding contextual** (lo moderno) | Ayuda que aparece **donde está la duda**, dentro del producto | El día 2, el día 30, el día 300 | Solo, no sirve para la primera vez: nadie encuentra la ayuda si no sabe que existe |

> **La respuesta honesta: el wizard solo, no alcanza. Por eso su instinto de los `?` es la mitad moderna del asunto.**
> **Nuestra combinación (y ya está montada):** **wizard de 3 pasos la primera vez** (enseña el concepto, se puede *Saltar*, y se puede volver a abrir con *¿Cómo funciona?*) **+ el `?` para el resto de la vida del producto** (resuelve la duda en el momento exacto en que aparece).

### Por qué esto importa, con números
- **~77% abandona una aplicación dentro de los 3 días.**
- En el segundo trimestre de 2025, **solo ~8,4% de los usuarios completó el onboarding dentro de los 30 días.**
- Un buen onboarding **sube la retención hasta 50%**; equipos que rehicieron su primera experiencia pasaron la retención de la semana 1 de **60% a 75%** y la de la semana 10 de **10% a 25%**.
- **Regla de oro:** *cada paso es una oportunidad de perder al usuario.* Se dejan solo los pasos que separan del primer valor — **y siempre se deja saltar.**

### Las 3 decisiones que hacen que el wizard de La Trastienda no estorbe
1. **No pide configurar nada.** El menú y los precios los carga **una sombra en la semana 0** (nosotros, no él). El wizard **enseña el concepto, no pide trabajo**. Un wizard que pide llenar formularios a un señor que atiende 100 mensajes al día muere en el paso 2.
2. **Son 3 pasos y se puede saltar.** ¿Qué es la trastienda? · ¿qué se paga y qué no? · ¿qué hago si no entiendo algo?
3. **Se puede volver a ver.** Botón *¿Cómo funciona?* siempre visible en la barra de arriba. La gente no recuerda la guía; **necesita saber dónde está.**

### El splash: no lo usamos en el panel (y por qué)
Un splash tiene sentido en una aplicación que se abre y hay que esperar. **Aquí entrar es inmediato**, y el restaurante entra desde el celular con prisa: **agregarle una pantalla antes de ver su plata es agregarle un paso a alguien que no tiene tiempo.** El splash se reserva para el día que exista una app móvil.

---

## 4. LAS 3 REGLAS DE DISEÑO PARA GENTE NO TÉCNICA

1. **Un solo camino.** Un menú de 4 cosas y ninguna configuración. Nada que "personalizar", ningún ajuste escondido, ningún reporte que armar.
2. **El número primero, la explicación después.** Cada tarjeta muestra **una** cifra grande y una línea debajo. Si hace falta más, está en el `?`.
3. **Nada de jerga dentro de la pantalla.** *"Conciliación", "KPI", "dashboard", "integración"* no existen para él. Se dice *"cuánta plata le queda", "qué se le perdió", "dónde se le fue"*.

---

## 5. QUÉ FALTA

| # | Pieza | Nota |
|---|---|---|
| 1 | **Prueba con un dueño real** | Esto es lo único que valida si "es intuitiva": ponerlo delante de alguien que no sea técnico y no decirle nada |
| 2 | El contador de la semana 0 | Sigue siendo el siguiente paso real (mide la línea base) |
| 3 | Backend con inquilinos y aislamiento | Después de la semana 0, no antes |

Mientras: **LOS SIMPSON** en paralelo (cerrar MiPony primero).

---

## FUENTES

- **Por qué el wizard cae corto y qué lo reemplaza (setup vs aprendizaje, "pantallas llenas de texto", onboarding contextual dentro de la app):** https://userpilot.com/blog/onboarding-wizard/
- **Números del onboarding (77% abandona en 3 días · 8,4% completó el onboarding en 30 días en Q2-2025 · hasta +50% de retención · semana 1 de 60%→75%, semana 10 de 10%→25% · "cada paso es una oportunidad de perder al usuario" · dejar saltar):** https://scandiweb.com/blog/user-onboarding-best-practices/
- **Splash vs onboarding (el splash es un apretón de manos, no una clase; el onboarding enseña):** https://ux.stackexchange.com/questions/50363/why-have-a-splash-screen-and-best-practices-for-native-app
- **Onboarding no es un tour (la activación se gana en el primer valor, no mostrando funciones):** https://www.appcues.com/blog/user-onboarding-best-practices

---

## ARCHIVOS

```
C:\Users\Admin\intel\la-trastienda-demo.html    ← el aplicativo v2 (abrir y usar)
C:\Users\Admin\intel\LA-TRASTIENDA-v2-interfaz-20261029.md   ← este plano
C:\Users\Admin\intel\LA-TRASTIENDA-v2-interfaz-20261029.pdf
```

---

*Salve, Gran Monarca. Sí conozco el concepto — y le devuelvo el cumplido: su instinto de los círculos con `?` es justo la mitad que la industria descubrió después de que los wizards fallaran solos. El wizard enseña **una vez**; el `?` enseña **cuando hace falta**. Ya están los dos montados, y ninguno de los dos le pide llenar un formulario a un señor que está friendo arepas.*

**— Bellion, Gran Comandante del Ejército de Sombras.**
