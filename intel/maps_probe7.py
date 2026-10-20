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
    scripts = pg.eval_on_selector_all("script[type='application/ld+json']", "els=>els.map(e=>e.textContent)")
    print("ldjson count:", len(scripts))
    for s in scripts:
        print("LDJSON:", (s or "")[:300])
    html = pg.content()
    print("len(html):", len(html))
    hits = re.findall(r"aggregateRating.{0,180}", html)
    for h in hits[:5]:
        print("AGG:", h)
    hits2 = re.findall(r'"reviewCount"\s*:\s*"?\d+', html)
    print("reviewCount:", hits2[:5])
    hits3 = re.findall(r'"ratingValue"\s*:\s*"?[\d.]+', html)
    print("ratingValue:", hits3[:5])
    b.close()
