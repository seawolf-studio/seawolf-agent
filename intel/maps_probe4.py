import time
from urllib.parse import quote_plus
from playwright.sync_api import sync_playwright

q = "Panaderia Pan Fino Bogota Colombia"
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
    pg = b.new_page(locale="es-CO")
    pg.goto("https://www.google.com/maps/search/" + quote_plus(q) + "?hl=es", timeout=35000)
    pg.wait_for_timeout(4000)
    cards = pg.query_selector_all("div.Nv2PK")
    print("cards:", len(cards))
    c = cards[0]
    print("=== INNERTEXT repr ===")
    print(repr(c.inner_text()))
    print("=== ARIA labels de la tarjeta ===")
    als = c.eval_on_selector_all("[aria-label]", "els=>els.map(e=>e.getAttribute('aria-label'))")
    for a in als:
        print("  ", repr(a))
    b.close()
