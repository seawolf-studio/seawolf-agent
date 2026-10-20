import time, re
from urllib.parse import quote_plus
from playwright.sync_api import sync_playwright

q = "Panaderia Pan Fino Bogota Colombia"
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
    pg = b.new_page(locale="es-CO")
    pg.goto("https://www.google.com/maps/search/" + quote_plus(q) + "?hl=es", timeout=35000)
    pg.wait_for_timeout(4000)
    for sel in ["div.Nv2PK", "div[role=feed] > div", "a.hfpxzc", "div.lI9IFe", "div.bfdHYd"]:
        try:
            print(sel, "->", len(pg.query_selector_all(sel)))
        except Exception as e:
            print(sel, "err", e)
    # volcar classes de los hijos del feed
    try:
        cls = pg.eval_on_selector_all("div[role=feed] > div", "els => els.map(e=>e.className).slice(0,6)")
        print("feed classes:", cls)
    except Exception as e:
        print("feed err", e)
    b.close()
