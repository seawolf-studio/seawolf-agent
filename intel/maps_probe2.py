import time, re
from playwright.sync_api import sync_playwright

q = "Panaderia Pan Fino Bogota Colombia"
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
    pg = b.new_page(locale="es-CO")
    pg.goto("https://www.google.com/maps/search/" + q.replace(" ", "+") + "?hl=es", timeout=45000)
    time.sleep(4)
    try:
        pg.locator("a.hfpxzc").first.click()
        time.sleep(4)
    except Exception as e:
        print("CLICK ERR:", e)
    print("URL:", pg.url[:150])
    labels = pg.eval_on_selector_all("[aria-label]", "els => els.map(e=>e.getAttribute('aria-label'))")
    print("ARIA_COUNT:", len(labels))
    for l in labels:
        if any(k in (l or "") for k in ["estrella", "reseña", "opinion", "hace", "202", "de ", " mare"]):
            print("ARIA:", l)
    print("--- TEXT ---")
    print(pg.inner_text("body")[:1800].replace("\n", " | "))
    b.close()
