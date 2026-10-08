#!/usr/bin/env python3
"""PRUEBA DE REGRESION DEL CRITERIO (Capa 1).
Cada caso declara el minimo aceptable. Se compara contra la clasificacion real del modelo.
Uso: python3 probar_criterio.py"""
import sys

sys.path.insert(0, "/opt/waha")
import criterio  # noqa: E402

# minimo esperado por caso: 'nunca_verde' | nivel exacto | 'min:amarillo' ...
CASOS = [
    ("HURTO/paquete (mensaje real de la prueba)", "nunca_verde",
     "Buenas noches, para conocimiento de un residente q acabo de poner una queja q tiene perdido "
     "un paquete de Dafiti sin un par de zapatos la señora es del apartamento 1004"),
    ("HURTO en curso", "rojo",
     "Se estan llevando las bicicletas del parqueadero, hay dos tipos cortando las guayas ahora mismo"),
    ("Fuga de agua", "naranja",
     "Se rompio el tubo del bano del apto 501 y esta inundando el pasillo"),
    ("Persona sospechosa", "rojo",
     "Hay un hombre raro mirando los carros en el parqueadero desde hace media hora"),
    ("Queja de servicio", "nunca_verde",
     "Llevo tres semanas esperando que arreglen la reja del parque infantil, esto es un abandono"),
    ("Consulta simple", "amarillo",
     "A que hora es la reunion del consejo de administracion?"),
    ("Saludo", "verde",
     "Buenos dias, muchas gracias por la informacion"),
]

ORDEN = {"verde": 0, "amarillo": 1, "naranja": 2, "rojo": 3}
ok = fallos = 0
print("=" * 96)
for nombre, esperado, texto in CASOS:
    try:
        c = criterio.classify(texto)
        cat = str(c.get("cat", "")).lower()
        accion = str(c.get("accion") or "")
    except Exception as e:
        print("  %-40s ERROR %s" % (nombre, str(e)[:60]))
        fallos += 1
        continue
    if esperado == "nunca_verde":
        pasa = cat != "verde"
    else:
        pasa = ORDEN.get(cat, -1) >= ORDEN.get(esperado, 99)
    marca = "OK  " if pasa else "FALLA"
    if pasa:
        ok += 1
    else:
        fallos += 1
    print("  [%s] %-38s esperado>=%-9s real=%-8s | %s" % (marca, nombre, esperado, cat, accion[:70]))
print("=" * 96)
print("RESULTADO: %d OK / %d FALLA de %d" % (ok, fallos, len(CASOS)))
if fallos:
    print("  -> el criterio NO esta como el Monarca lo quiere: revisar criterio.py")
    sys.exit(1)
