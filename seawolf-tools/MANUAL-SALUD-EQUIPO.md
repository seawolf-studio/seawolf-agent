# 🩺 SALUD DEL EQUIPO — Manual de uso

**Módulo de Seawolf Tools** · Diagnóstico y mantenimiento del hierro.

> # 🚨 ZONA DELICADA
>
> **Todo lo de este módulo toca el disco físico y el sistema de archivos.**
>
> - **Optimizar NO borra tus archivos**, pero **NUNCA se interrumpe** ni se apaga el equipo mientras corre.
> - **Este módulo NO modifica particiones.** Un cambio mal hecho ahí puede borrar un disco entero.
> - **Si no estás seguro de algo, NO lo ejecutes.** Pregunta antes. El disco no perdona.
>
> *Analizar (leer) es 100% seguro: no cambia nada. **Ejecutar** es lo que hay que pensar dos veces.*

---

## ¿Qué es?

La pestaña **🩺 Salud** de Seawolf Tools: mira el estado real de su equipo y hace el
mantenimiento que a cada disco le corresponde — **el correcto, no el que suena bien**.

Se entra por `http://localhost:8770` o por `https://herramientas.sw-st.net` (pestaña **🩺 Salud**).

---

## 🔑 LA IDEA QUE LO HACE ÚTIL (y lo hace seguro)

**El TIPO de disco decide el mantenimiento. Nunca al revés.**

| Disco | Lo que le toca | Por qué |
|---|---|---|
| **SSD** (incluido NVMe) | **TRIM** | Le devuelve el espacio de lo borrado y lo mantiene rápido. **NO lo desgasta.** |
| **HDD** (mecánico) | **Desfragmentar** | Junta los datos repartidos para que el cabezal no salte tanto. **Necesita espacio libre.** |
| **USB / extraíble** | **🚫 NO SE TOCA** | Si se desconecta a mitad, el daño puede ser grave. Y el mantenimiento rara vez aporta. |
| **Tipo sin confirmar** | **🚫 NO SE TOCA** | Sin certeza no hay acción. Ante la duda, abstenerse. |

> **Esto no es teoría:** en este equipo hay **2 SSD y 2 HDD**. Si el módulo tratara a todos igual,
> le estaría **desgastando los SSD** o **desfragmentando un disco que no debe**.

---

## 🛡️ LAS DOS GUARDIAS QUE **IMPIDEN** EL DAÑO

No basta con advertir: el módulo **se niega a ejecutar** cuando el riesgo es real.

### Guardia 1 — Disco extraíble o sin confirmar
```
J:  ->  "no pude confirmar si es SSD o HDD. POR SEGURIDAD no toco nada."   ⛔
```
Devuelve el mensaje y **no ejecuta absolutamente nada.**

### Guardia 2 — HDD casi lleno
```
D:  ->  "solo 12% libre (116 GB). Desfragmentar un disco casi lleno es lento,
         poco efectivo y puede quedarse a medias. Libere espacio primero
         (deje ~15%) y vuelva a intentarlo. NO lo ejecuto."              ⛔
```
Desfragmentar necesita hueco. Por debajo del **15% libre**, la guardia lo bloquea.

---

## LAS FUNCIONES (cada una explicada)

### 💽 Discos: tipo y salud
Cada disco físico con su **tipo real** (SSD / HDD / NVMe / USB), su **estado de salud**
(`Healthy`) y su **estado operativo** (`OK` / `Online`). Debajo de cada uno se dice **qué
mantenimiento le toca** y **por qué**.

### 📦 Espacio por volumen
Total, libre y **porcentaje libre** de cada unidad, **ordenadas de más a menos apretadas**.
Un disco lleno por encima del 90% trabaja mal y envejece más rápido.

Avisos automáticos:
```
12% libre  ->  [Vigilar]
10% o menos -> [Atencion: poco espacio]
 5% o menos -> [CRITICO: casi lleno]
```

### ⚡ Optimizar (TRIM o desfragmentar, **automático según el tipo**)
El botón no pregunta qué disco es: **lo averigua él** (`Get-Partition → Get-Disk → Get-PhysicalDisk`)
y ejecuta lo que corresponde.

> **Antes de ejecutar**, sale una confirmación que dice exactamente qué va a pasar,
> que puede tardar, y que **no se interrumpe**.
>
> **Requiere permisos de administrador.** Si faltan, lo dice claramente en vez de fallar en silencio.

### 🔍 Verificar disco (**solo lectura**)
Revisa la integridad del disco y del sistema de archivos con `chkdsk /scan` (modo en línea):
**NO repara, NO borra, NO cambia nada.** Detecta errores antes de que se conviertan en pérdida
de datos. Puede **tardar bastante** en discos grandes. Requiere administrador.

### 🧠 Procesador y memoria
Uso del CPU y memoria libre, con semáforo (verde / ámbar / rojo). Si la RAM libre baja de forma
sostenida, el equipo empieza a usar el disco como memoria y todo se vuelve lento.

### 🗺️ Mapa de particiones — **SOLO LECTURA**
Qué disco físico contiene qué unidad, de qué tamaño y con qué formato.

> **🚫 Este módulo NO modifica particiones.** Cambiar particiones puede **borrar un disco entero**.
> Para eso hace falta una herramienta dedicada **y un respaldo hecho antes**.

### 🚀 Arranque de Windows
Todo lo que arranca solo. Cada programa alarga el arranque y consume memoria desde el primer
segundo del día. **Aquí solo se muestra**: para desactivar algo, Administrador de tareas (Ctrl+Shift+Esc)
→ pestaña **Inicio**.

### 🌡️ Temperatura y desgaste — **requiere un extra**
Temperatura real, desgaste y horas de encendido **NO vienen en Windows**: hacen falta herramientas
como `smartmontools`. **Sin ellas, este módulo no muestra un dato inventado** — lo dice y ya.

---

## Cómo se usa

```
1.  Pestaña  🩺 Salud
2.  Pulse    🔍 Analizar el equipo        (esto NO toca nada)
3.  Lea los AVISOS que aparecen arriba
4.  Para mantenimiento: ⚡ Optimizar o 🔍 Verificar en la unidad que quiera
5.  Lea la confirmación y decida
```

**Análisis de consola** (sin abrir el navegador):
```
python intel\seawolf-tools.py salud
```

---

## Lo que hay que tener claro

| ✅ Seguro | ⛔ Pensar dos veces |
|---|---|
| Analizar el equipo | Optimizar (TRIM/defrag) — **no interrumpir** |
| Ver el mapa de particiones | Verificar (tarda, y necesita admin) |
| Leer los avisos | **Cualquier cosa con particiones: NO aquí** |

### Y las tres reglas de oro
1. **Nunca interrumpas** un TRIM, un desfrag o una verificación a medias.
2. **Nunca toques particiones** sin respaldo hecho y verificado.
3. **Ante la duda, no ejecutes.** El módulo te avisa; la decisión es tuya.

---

*Salud del Equipo · parte de Seawolf Tools · código propio · Seawolf Studio.*
