import time, re
from playwright.sync_api import sync_playwright

q = "Panaderia Pan Fino Bogota Colombia"
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
    pg = b.new_page(locale="es-CO")
    pg.goto("https://www.google.com/maps/search/" + q.replace(" ", "+") + "?hl=es", timeout=45000)
    time.sleep(4)
    pg.locator("a.hfpxzc").first.click()
    time.sleep(4)
    for name in [re.compile("reseñas"), re.compile("estrellas")]:
        try:
            pg.get_by_role("button", name=name).first.click()
            print("click ok:", name)
            time.sleep(4)
            break
        except Exception as e:
            print("click err:", name, e)
    labels = pg.eval_on_selector_all("[aria-label]", "els => els.map(e=>e.getAttribute('aria-label'))")
    for l in labels:
        if l and re.search(r"rese|estrella|hace|20\d\d", l):
            print("ARIA:", l)
    print("--- TEXT FINAL ---")
    print(pg.inner_text("body")[-2000:].replace("\n", " | "))
    print("URL:", pg.url[:220])
    b.close()
