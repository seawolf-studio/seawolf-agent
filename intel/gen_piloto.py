# -*- coding: utf-8 -*-
# Generador del PILOTO LOBO CAZADOR — 10 SmartWebs personalizadas + asistente IA por sector.
# Salida: C:/Users/Admin/intel/piloto-smartwebs/<slug>.html  +  piloto-smartwebs.zip
import os, zipfile, re

OUT = "C:/Users/Admin/intel/piloto-smartwebs"
ASSISTANT_ENDPOINT = "https://mando.sw-st.net/asistente"  # se cablea al backend en el VPS

NEGOCIOS = [
    dict(nombre="Floristería Roma", sector="Floristería", ciudad="Cali", tel="+57 2 2592140",
         tagline="Flores frescas y arreglos que enamoran",
         servicios=["Ramos y arreglos florales", "Flores para ocasiones especiales", "Decoración de eventos", "Domicilios el mismo día"],
         prom="Eres el asistente de Floristería Roma (Cali). Ayudas a pedir ramos, arreglos y decoración de eventos. Das precios referenciales, tomas pedidos y agendas domicilios. Cercano, cálido y breve."),
    dict(nombre="Litografía Fullcolor Impresos", sector="Imprenta / Litografía", ciudad="", tel="+57 606 7458259",
         tagline="Tus impresos, a color y a tiempo",
         servicios=["Tarjetas personales", "Volantes y afiches", "Facturas y talonarios", "Diseño de marca"],
         prom="Eres el asistente de Litografía Fullcolor Impresos. Cotizas impresos (tarjetas, volantes, talonarios), explicas tiempos y tomas el pedido. Directo y comercial."),
    dict(nombre="El Nido — Ecolodge", sector="Turismo / Hospedaje", ciudad="", tel="+57 318 8031393",
         tagline="Descansa en medio de la naturaleza",
         servicios=["Hospedaje ecológico", "Cabañas para parejas", "Senderismo guiado", "Desayunos de la región"],
         prom="Eres el asistente de El Nido, un ecolodge. Informas sobre hospedaje, cabañas, actividades y tarifas, y tomas reservas. Amable y relajado."),
    dict(nombre="Bicicletas J.J", sector="Bicicletas", ciudad="", tel="+57 318 2217463",
         tagline="Venta, repuestos y taller de bicicletas",
         servicios=["Venta de bicicletas", "Repuestos y accesorios", "Mantenimiento y taller", "Accesorios de ciclismo"],
         prom="Eres el asistente de Bicicletas J.J. Ayudas a elegir bici, cotizas repuestos y agendas taller. Entusiasta y técnico sin complicar."),
    dict(nombre="AutoSport", sector="Automotriz", ciudad="", tel="+57 607 6310071",
         tagline="Tu carro en las mejores manos",
         servicios=["Mantenimiento preventivo", "Reparación de motor", "Alineación y balanceo", "Cambio de aceite"],
         prom="Eres el asistente de AutoSport. Cotizas mantenimiento y reparaciones, explicas tiempos y agendas la revisión. Claro y confiable."),
    dict(nombre="Outfit Store", sector="Moda / Ropa", ciudad="Santa Rosa de Cabal", tel="+57 311 7159380",
         tagline="Estilo que se nota",
         servicios=["Ropa de moda", "Accesorios", "Asesoría de look", "Pedidos por encargo"],
         prom="Eres el asistente de Outfit Store. Muestras prendas, das tallas y precios, y tomas pedidos. Fresco y con buena vibra."),
    dict(nombre="Herby Ltda — Reparación de Computadores", sector="Servicio técnico de PC", ciudad="", tel="+57 310 4346478",
         tagline="Tu computador, como nuevo",
         servicios=["Mantenimiento de portátiles y PC", "Eliminación de virus", "Cambio de disco / SSD", "Recuperación de datos"],
         prom="Eres el asistente de Herby Ltda. Diagnosticas fallas comunes, cotizas reparaciones y agendas el servicio. Técnico pero entendible."),
    dict(nombre="Tecnodrywall", sector="Construcción / Drywall", ciudad="", tel="+57 606 7399959",
         tagline="Techos, muros y acabados en drywall",
         servicios=["Muros y divisiones", "Techos y cielos rasos", "Acabados y pintura", "Cotización de obra"],
         prom="Eres el asistente de Tecnodrywall. Cotizas muros, techos y acabados en drywall, pides medidas y agendas visita. Profesional y directo."),
    dict(nombre="Ultrapan", sector="Panadería", ciudad="", tel="+57 305 7173518",
         tagline="Pan fresco todos los días",
         servicios=["Pan artesanal", "Tortas y postres", "Pedidos para eventos", "Pasabocas"],
         prom="Eres el asistente de Ultrapan. Informas productos y precios, tomas pedidos y agendas entregas. Cálido y antojador."),
    dict(nombre="OptiSalud del Valle", sector="Óptica / Salud visual", ciudad="", tel="+57 602 5581520",
         tagline="Ve mejor, cuida tus ojos",
         servicios=["Examen de optometría", "Monturas y lentes", "Lentes de contacto", "Ajuste y reparación"],
         prom="Eres el asistente de OptiSalud del Valle. Exploras síntomas simples, informas servicios y agendas cita de optometría. Cuidadoso y profesional."),
]

TPL = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__NOMBRE__ — __TAGLINE__</title>
<style>
  :root{ --bg:#0b1414; --card:#122121; --ink:#eaf7f7; --mut:#93b3b3; --acc:#4CE8E7; --acc2:#48E8D8; --b:#1e3232; }
  *{box-sizing:border-box;} html,body{background:var(--bg);} body{margin:0;color:var(--ink);font-family:ui-sans-serif,system-ui,"Segoe UI",Roboto,Arial,sans-serif;}
  .wrap{max-width:1040px;margin:0 auto;padding:0 20px;}
  header{padding:22px 0 8px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;}
  .logo{font-weight:800;font-size:20px;} .logo b{color:var(--acc);}
  .sect{color:var(--mut);font-size:12.5px;}
  .cta{background:var(--acc);color:#08201f;border:none;border-radius:9px;padding:10px 16px;font-weight:700;cursor:pointer;font-size:13.5px;text-decoration:none;}
  .hero{padding:34px 0 26px;border-bottom:1px solid var(--b);}
  .hero h1{font-size:34px;margin:0 0 8px;line-height:1.1;}
  .hero p{color:var(--mut);font-size:16px;margin:0 0 18px;max-width:620px;}
  .grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;padding:26px 0;}
  .card{border:1px solid var(--b);background:var(--card);border-radius:13px;padding:16px 18px;}
  .card h3{margin:0 0 5px;font-size:15px;color:var(--acc);} .card p{margin:0;color:var(--mut);font-size:13px;}
  .sec-t{font-size:13px;letter-spacing:.4px;color:var(--acc);margin:6px 0 12px;}
  footer{border-top:1px solid var(--b);padding:20px 0 60px;color:var(--mut);font-size:12px;}
  /* asistente */
  #chatBtn{position:fixed;right:20px;bottom:20px;background:var(--acc);color:#08201f;border:none;border-radius:30px;padding:14px 20px;font-weight:800;cursor:pointer;font-size:14px;box-shadow:0 8px 30px rgba(76,232,231,.3);z-index:50;}
  #chat{position:fixed;right:20px;bottom:20px;width:360px;max-width:92vw;height:520px;max-height:82vh;background:#0e1b1b;border:1px solid var(--b);border-radius:16px;display:none;flex-direction:column;overflow:hidden;z-index:60;box-shadow:0 20px 60px rgba(0,0,0,.6);}
  #chat.on{display:flex;}
  #chat header{background:#102020;padding:12px 14px;display:flex;justify-content:space-between;align-items:center;}
  #chat .tit{font-size:13.5px;font-weight:700;} #chat .st{font-size:10.5px;color:var(--acc);}
  #msgs{flex:1;overflow-y:auto;padding:12px;}
  .m{margin:8px 0;max-width:85%;font-size:13px;line-height:1.4;padding:9px 12px;border-radius:12px;}
  .m.bot{background:#152a2a;border:1px solid var(--b);}
  .m.me{background:var(--acc);color:#08201f;margin-left:auto;}
  #chat form{display:flex;border-top:1px solid var(--b);}
  #chat input{flex:1;background:transparent;border:none;color:var(--ink);padding:12px;font-size:13px;outline:none;}
  #chat button.send{background:var(--acc);border:none;color:#08201f;font-weight:800;padding:0 16px;cursor:pointer;}
  .x{background:transparent;border:none;color:var(--mut);font-size:18px;cursor:pointer;}
  .trial{display:inline-block;margin-top:10px;border:1px dashed var(--b);border-radius:8px;padding:6px 10px;font-size:11.5px;color:var(--acc);}
</style>
</head>
<body>
<header><div><div class="logo">__NOMBRE_PART__</div><div class="sect">__SECTOR____CIUDAD_TXT__</div></div>
<a class="cta" href="tel:__TEL_RAW__">📞 Llamar</a></header>

<section class="wrap hero">
  <h1>__TAGLINE__</h1>
  <p>En <b>__NOMBRE__</b> hacemos las cosas bien. Escríbenos y te atendemos al instante — incluso de noche.</p>
  <a class="cta" href="https://wa.me/__TEL_RAW__" target="_blank">💬 Escríbenos por WhatsApp</a>
  <div class="trial">✨ Propuesta creada por Seawolf Studio — sitio en período de prueba</div>
</section>

<section class="wrap">
  <div class="sec-t">NUESTROS SERVICIOS</div>
  <div class="grid">__SERVICIOS__</div>
</section>

<footer class="wrap">__NOMBRE__ · __SECTOR__ · __TEL__ &nbsp;|&nbsp; Hecho por <b style="color:var(--acc)">Seawolf Studio</b> — agencia de sistemas e IA.</footer>

<button id="chatBtn">🤖 Habla con nuestro asistente</button>
<div id="chat">
  <header><div><div class="tit">Asistente de __NOMBRE__</div><div class="st">● en línea</div></div><button class="x" onclick="document.getElementById('chat').classList.remove('on')">✕</button></header>
  <div id="msgs"><div class="m bot">¡Hola! 👋 Soy el asistente de __NOMBRE__. ¿En qué te ayudo?</div></div>
  <form id="f"><input id="inp" placeholder="Escribe tu mensaje..." autocomplete="off"><button class="send">➤</button></form>
</div>

<script>
(function(){
  var ENDPOINT="__ENDPOINT__", SLUG="__SLUG__", PROMPT=__PROMPT_JS__;
  var chat=document.getElementById('chat'), msgs=document.getElementById('msgs');
  document.getElementById('chatBtn').onclick=function(){ chat.classList.add('on'); };
  function add(t,c){ var d=document.createElement('div'); d.className='m '+c; d.textContent=t; msgs.appendChild(d); msgs.scrollTop=msgs.scrollHeight; return d; }
  document.getElementById('f').addEventListener('submit',function(e){
    e.preventDefault();
    var inp=document.getElementById('inp'); var t=inp.value.trim(); if(!t) return; inp.value='';
    add(t,'me'); var b=add('...','bot');
    fetch(ENDPOINT,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({slug:SLUG,prompt:PROMPT,msg:t})})
      .then(function(r){return r.json();}).then(function(d){ b.textContent=d.reply||'Disculpa, intenta de nuevo.'; })
      .catch(function(){ b.textContent='Estoy en modo demostración. Escríbenos por WhatsApp y te atendemos ya. 🙂'; });
  });
})();
</script>
</body>
</html>"""

def slug(s):
    import unicodedata
    s = "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s

def tel_raw(t):
    return re.sub(r"[^0-9]", "", t)

os.makedirs(OUT, exist_ok=True)
files = []
for n in NEGOCIOS:
    s = slug(n["nombre"])
    servicios = "".join('<div class="card"><h3>%s</h3><p>Te lo atendemos rápido y bien. Pregúntale al asistente por detalles y precios.</p></div>' % x for x in n["servicios"])
    html = (TPL
            .replace("__NOMBRE_PART__", n["nombre"].split("—")[0].strip())
            .replace("__NOMBRE__", n["nombre"])
            .replace("__SECTOR__", n["sector"])
            .replace("__CIUDAD_TXT__", (" · " + n["ciudad"]) if n["ciudad"] else "")
            .replace("__TAGLINE__", n["tagline"])
            .replace("__TEL_RAW__", tel_raw(n["tel"]))
            .replace("__TEL__", n["tel"])
            .replace("__SERVICIOS__", servicios)
            .replace("__ENDPOINT__", ASSISTANT_ENDPOINT)
            .replace("__SLUG__", s)
            .replace("__PROMPT_JS__", 'JSON.parse(' + __import__("json").dumps(__import__("json").dumps(n["prom"])) + ')'))
    p = os.path.join(OUT, s + ".html")
    open(p, "w", encoding="utf-8").write(html)
    files.append(p)
    print("escrito:", p)

zp = "C:/Users/Admin/intel/piloto-smartwebs.zip"
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    for p in files:
        z.write(p, os.path.basename(p))
print("ZIP:", zp, "con", len(files), "archivos")
