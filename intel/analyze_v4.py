import csv, collections
c = collections.Counter(); cat = collections.Counter(); priv = collections.Counter()
n = 0
for r in csv.reader(open("presas_v4.csv", encoding="utf-8")):
    if not r or r[0] == "nombre":
        continue
    n += 1
    op = (r[4].strip().lower() or "(sin etiqueta)") if len(r) > 4 else "(?)"
    c[op] += 1
    cat[r[1]] += 1
    if op == "private":
        priv[r[1]] += 1
print("total:", n)
print("tipo_operador:", dict(c))
print("top categorias:", cat.most_common(12))
print("top categorias PRIVATE:", priv.most_common(15))
