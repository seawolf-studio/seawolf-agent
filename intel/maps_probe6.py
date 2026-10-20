import time, re
from urllib.parse import quote_plus
from playwright.sync_api import sync_playwright

q = "Panaderia Pan Fino Bogota Colombia"
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
    pg = b.new_page(locale="es-CO")
    pg.goto("https://www.google.com/maps/search/" + quote_plus(q) + "?hl=es", timeout=35000)
    pg.wait_for_timeout(4000)
    try:
        pg.locator("a.hfpxzc").first.click()
        pg.wait_for_timeout(4000)
    except Exception as e:
        print("click err", e)
    # buscar cualquier patron "N reseñas" o "(N)"
    t = pg.inner_text("body")
    for m in re.finditer(r"([\d.,]+)\s*rese", t):
        print("RESE MATCH:", repr(m.group(0)))
    # aria labels con rese
    labels = pg.eval_on_selector_all("[aria-label]", "els=>els.map(e=>e.getAttribute('aria-label'))")
    for l in labels:
        if l and "rese" in l.lower():
            print("ARIA RESE:", repr(l))
    print("PANEL HEAD:", t[:900].replace("\n", " | "))
    b.close()
