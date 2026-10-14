import json

with open(r'C:\Users\Admin\seawolf-store\dist\products.json', encoding='utf-8') as f:
    prods = json.load(f)

# Costos bajos
baratos = [p for p in prods if isinstance(p.get('dropi_cost'), (int,float)) and p['dropi_cost'] < 8000]
print(f'Productos con costo < 8.000: {len(baratos)}')
for p in sorted(baratos, key=lambda x: x['dropi_cost'])[:20]:
    print(f'  {p["sku"]} | {p["name"][:50]} | costo={p["dropi_cost"]} | precio={p.get("price","?")}')

# Distribución de costos
costs = [p.get('dropi_cost') for p in prods if isinstance(p.get('dropi_cost'), (int,float))]
print(f'\nDistribución de costos:')
if costs:
    costs.sort()
    n = len(costs)
    print(f'  Min: {costs[0]} | P25: {costs[n//4]} | Med: {costs[n//2]} | P75: {costs[3*n//4]} | Max: {costs[-1]}')
    print(f'  Count: {n}')

# Distribución de precios
prices = [float(p.get('price') or p.get('price_wc', 0)) for p in prods if p.get('price') or p.get('price_wc')]
print(f'\nPrecios actual: min={min(prices):,}, max={max(prices):,}, count={len(prices)}')
under20k = sum(1 for p in prices if p < 20000)
under30k = sum(1 for p in prices if 20000 <= p < 30000)
under50k = sum(1 for p in prices if 30000 <= p < 50000)
under100k = sum(1 for p in prices if 50000 <= p < 100000)
over100k = sum(1 for p in prices if p >= 100000)
print(f'  <20k: {under20k}, 20-30k: {sum(1 for p in prices if 20000<=p<30000)}, 30-50k: {under50k}, 50-100k: {under100k}, >100k: {over100k}')

# Veredicto distribution desde el CSV
import csv
with open(r'C:\Users\Admin\seawolf-store\mantenimiento\precios-real-20261013.csv', encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    counts = {}
    for r in reader:
        v = r['veredicto']
        counts[v] = counts.get(v, 0) + 1
print(f'\nVeredictos en CSV:')
for k, c in sorted(counts.items()):
    print(f'  {k}: {c}')
