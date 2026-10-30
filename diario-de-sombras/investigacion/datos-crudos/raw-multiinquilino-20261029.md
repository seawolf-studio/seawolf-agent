# DATOS CRUDOS — Investigación "albergar varios clientes" (29-oct-2026, 20:04)

## Consultas ejecutadas (5)

1. `WhatsApp Business API pricing per message 2026 Colombia Meta conversation`
2. `WAHA WhatsApp HTTP API multiple sessions scalability one server`
3. `multi-tenant SaaS architecture WhatsApp per tenant session isolation`
4. `white label restaurant ordering platform reseller pricing Colombia`
5. `self-hosted multi-tenant SaaS cost per tenant VPS 2026`

## Documentos extraídos completos (5 de 5)

| URL | Qué se extrajo |
|---|---|
| https://contactship.ai/en/blog/whatsapp-business-api-pricing-latin-america-2026 | Tarifa oficial Meta por mensaje, LatAm, vigente 1-oct-2026. Colombia: servicio/utilidad/auth USD 0,0008 · marketing 0,0125. Primeras 1.000 respuestas de servicio gratis/mes/número. Mensajes entrantes gratis. Ejemplo: 9.000 respuestas = USD 6,40 (CO) vs 240 (PE). Descuentos por volumen solo en utilidad/auth, desde 100.000 msj/mes (5%) hasta 30 M (25%) |
| https://simplewa.com/blogs/whatsapp-api-for-saas-platforms | Aislamiento: **un contenedor Docker por SESIÓN (no por inquilino)**. Baileys ≈ 50 MB/sesión vs navegador ≈ 10× RAM. Modelo de datos `Tenant 1─* Session 1─* Message`, toda fila con `session_id` + `tenant_id`. Validar `session_id` contra el inquilino autenticado = el error #1 de fuga entre clientes. Onboarding por QR autorefrescable. Borrar la sesión por API al dar de baja |
| https://waha.devlike.pro/blog/waha-scaling (404 en extracción; dato desde el espejo dev.to y GitHub) | WAHA escala vertical: **hasta 50 sesiones (WEBJS) o 500 sesiones (NOWEB)** por servidor |
| https://kolonell.com/en/blog/multi-tenant-saas-architecture-hosting-cost-2026 | 3 modelos de aislamiento con sobrecosto de desarrollo, costo hosting/cliente, clientes cómodos. Base por inquilino = **19–75% del ingreso** en infraestructura. Base compartida + RLS = 2,3–7,5%. Sobrecosto dev +15–30%. Híbrido Enterprise +EUR 300–800/mes. Migrar 1 cliente a dedicada: 2–4 semanas; fusionar: 2–3× más caro. 5–10 días para RLS + aislamiento + portabilidad |
| https://supaorder.com/partners | Modelo marca blanca probado: un socio canadiense corre **100+ apps** sobre una plataforma. Banda de precio de **Colombia (banda C): USD 45 → 31 por local/mes**. Exclusividad ganada: ≥10 locales → 12 meses; mantener con +3 netos/trimestre y churn ≤10%. Registro de prospectos 90 días |
| https://rapiwa.com/blog/multi-tenant-whatsapp-api-saas-architecture | Número, llave de API y enrutamiento dedicados por cliente; aislamiento total entre inquilinos |
| https://wati.io/en/blog/mcp-multi-tenant-data-isolation | Patrones de aislamiento pool/bridge/silo; atar cada sesión a un inquilino en el momento de autorizar, nunca dejar que un argumento o el texto del modelo elija la cuenta |
| https://techplained.com/top-backend-platforms-saas | Patrón de claves multi-inquilino (`PK = TENANT#<id>`), costos de VPS/backend 2026 |
| https://scrampi.com/mejor-pos-restaurantes-colombia · https://menuthere.com/alternatives/toteat | Piso del POS de restaurante en Colombia: **$46.000–$139.900 COP/mes**; varios cobran complementos |

## Cifras de control usadas en el informe

- Precio propuesto El Cuadre: **$29.900 COP/mes**
- TRM usada: **USD 1 = 3.164 COP** ($29.900 ≈ US$9,45; banda C US$45 ≈ $142.000)
- 9.000 respuestas de servicio en Colombia = **USD 6,40/mes** (con las 1.000 gratis)
- Costo marginal por cliente: **< US$3,5/mes**
