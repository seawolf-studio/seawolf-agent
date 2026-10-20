import time, re, json
from playwright.sync_api import sync_playwright

q = "Panaderia Pan Fino Bogota Colombia"
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
    pg = b.new_page(locale="es-CO", user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36")
    try:
        pg.goto("https://www.google.com/maps/search/" + q.replace(" ", "+") + "?hl=es", timeout=45000)
    except Exception as e:
        print("GOTO ERR:", e)
    time.sleep(4)
    for t in ["Aceptar todo", "Accept all", "Acepto", "Rechazar todo"]:
        try:
            el = pg.get_by_role("button", name=t)
            if el.count():
                el.first.click(); print("click:", t); time.sleep(3); break
        except Exception:
            pass
    time.sleep(3)
    print("URL:", pg.url)
    print("TITLE:", pg.title()[:120])
    labels = pg.eval_on_selector_all("[aria-label]", "els => els.map(e=>e.getAttribute('aria-label'))")
    print("ARIA_COUNT:", len(labels))
    for l in labels[:80]:
        print("ARIA:", l)
    print("TEXT:", pg.inner_text("body")[:1200].replace("\n", " | "))
    b.close()
