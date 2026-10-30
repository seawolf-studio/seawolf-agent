# Cálculo de costos del modelo (29-oct-2026)

## Supuestos

```
TRM              = 3.164 COP/USD
catálogo         = 2.500 tokens (prefijo FIJO, cacheable: reglas + menú del restaurante)
turnos/conversación = 8
tokens nuevos/turno = 300  (mensaje del cliente + historial que crece)
tokens salida/turno  = 60
conversaciones/pedido cerrado = 3
tarifa del producto   = $500 COP/pedido cerrado
```

## Modelo: tokens por conversación

```
entrada  sin cache = 22.400 (= 2.500 × 8 + 300 × 8)
entrada  con cache =  4.400 (= 2.500 × 0,10 × 8  +  300 × 8)  →  80 % menos
salida             =    480 (= 60 × 8)
```

## Costo por conversación (input con caché, precios USD/M de cada host)

```
DeepSeek V4 Flash (DeepInfra)    0,00048 USD  →  1,5 COP
gpt-oss-120b (DeepInfra)         0,00024 USD  →  0,8 COP
Gemini 2.5 Flash-Lite            0,00063 USD  →  2,0 COP
Morph DeepSeek V4 Flash (1M)     0,00082 USD  →  2,6 COP
Llama 3.1 8B (DeepInfra)         0,00010 USD  →  0,3 COP
```

## Costo por pedido cerrado (×3 conversaciones)

```
DeepSeek V4 Flash (DeepInfra)    4,6 COP    → 0,9 % de la tarifa
gpt-oss-120b (DeepInfra)         2,3 COP    → 0,5 %
Gemini 2.5 Flash-Lite            6,0 COP    → 1,2 %
Morph DeepSeek V4 Flash (1M)     7,7 COP    → 1,5 %
Llama 3.1 8B (DeepInfra)         1,0 COP    → 0,2 %
```

## Escala mensual con el recomendado

```
300 conversaciones/mes   →   458 COP/mes    (0,14 USD)
1.000 conversaciones/mes → 1.526 COP/mes    (0,48 USD)
3.000 conversaciones/mes → 4.579 COP/mes    (1,45 USD)
```

## Verificación contra factura real

```
40 pedidos/mes  → factura $20.000 COP, modelo $183 COP   →  0,92 % del ingreso
120 pedidos/mes → factura $59.900 COP, modelo $549 COP   →  0,92 % del ingreso
```

## Voz (nota de voz ~40 s)

```
faster-whisper LOCAL (ya instalado) = 0 COP  · el audio no sale del equipo
Groq whisper                       = 0,001 USD/min → 2,1 COP por nota
```

## Reproducible

```python
TRM=3164.0
catalogo=2500; turnos=8; extra_in=300; out_turno=60
sin_cache = catalogo*turnos + extra_in*turnos          # 22.400
con_cache = catalogo*0.10*turnos + extra_in*turnos     #  4.400
outs      = out_turno*turnos                           #    480
# costo(pin, pout, ins, outs) = ins/1e6*pin + outs/1e6*pout
```

## Conclusión numérica

**El modelo cuesta menos del 1 % de lo que se le cobra al restaurante. La palanca de ahorro real está en cachear el catálogo (−80 % de tokens de entrada), no en cambiar de modelo ni en pasar al tier gratuito.**
