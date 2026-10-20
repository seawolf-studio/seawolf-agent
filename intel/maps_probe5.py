import time
from urllib.parse import quote_plus
from playwright.sync_api import sync_playwright

q = "Panaderia Pan Fino Bogota Colombia"
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
    pg = b.new_page(locale="es-CO")
    pg.goto("https://www.google.com/maps/search/" + quote_plus(q) + "?hl=es", timeout=35000)
    pg.wait_for_timeout(5000)
    labels = pg.eval_on_selector_all("[aria-label]", "els=>els.map(e=>e.getAttribute('aria-label'))")
    res = [l for l in labels if l and "estrella" in (l or "")]
    print("estrellas labels:", len(res))
    for l in res:
        print("   ", repr(l))
    names = pg.eval_on_selector_all("div.Nv2PK", "els=>els.map(e=>e.innerText.split('\\n')[0])")
    print("card names:", names)
    try:
        feed = pg.inner_text("div[role=feed]")
    except Exception:
        feed = pg.inner_text("body")
    print("FEED SNIPPET:", feed[:700].replace("\n", " | "))
    b.close()
