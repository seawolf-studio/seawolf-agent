import json

with open(r'C:\Users\Admin\seawolf-store\dist\products.json', encoding='utf-8') as f:
    prods = json.load(f)

ENVIO = 10000
DEV_RATE_HI = 0.40
RESERVE_FACTOR = 0.45
SANOS_THRESHOLD = 0.25

def min_price(costo):
    return (costo + ENVIO * (1 + DEV_RATE_HI * RESERVE_FACTOR)) / (1 - SANOS_THRESHOLD)

# Todos los productos baratos con su análisis
print("=== TODOS LOS PRODUCTOS CON COSTO < 8000 ===")
for p in sorted(prods, key=lambda x: x.get('dropi_cost') or 999999):
    costo_raw = p.get('dropi_cost')
    if not isinstance(costo_raw, (int, float)): continue
    costo = float(costo_raw)
    if costo >= 8000: break
    
    precio = p.get('price') or p.get('price_wc')
    pv = float(precio) if precio else None
    pm = min_price(costo)
    ratio = pm / pv if pv else float('inf')
    
    status = "RETIRAR" if ratio >= 3.0 or pm > 75000 else ("SUBIR" if pv and pv < pm - 5000 else "CERCA")
    
    print(f"  {p['sku']} | costo={costo:>7,.0f} | precio={pv if pv else '---':>10} | pm_min={pm:>10,.0f} | ratio={ratio:>5.1f}x | -> {status}")
