-- LA MADRIGUERA — riel de la línea de montaje de Seawolf Studio
-- Esquema PIEZA v1 · 2026-10-17 · Bellion
-- Toda estación lee y escribe aquí. Muchos accesos, una sola verdad.

CREATE TABLE IF NOT EXISTS piezas (
  id          TEXT PRIMARY KEY,
  tipo        TEXT NOT NULL DEFAULT 'presa',        -- presa | cliente | lead
  origen      TEXT NOT NULL,                        -- frio | propio
  estado      TEXT NOT NULL DEFAULT 'vigia',        -- vigia|acechador|ejecutor|escarbador|servir|finanzas
  nombre      TEXT NOT NULL,
  sector      TEXT,
  ciudad      TEXT,
  score       INT DEFAULT 0,
  datos       JSONB DEFAULT '{}'::jsonb,             -- contacto, etc.
  senales     JSONB DEFAULT '[]'::jsonb,             -- señales de dolor
  creado_en   TIMESTAMPTZ DEFAULT now(),
  actualizado TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS eventos (                 -- línea de tiempo / historial
  id       BIGSERIAL PRIMARY KEY,
  pieza_id TEXT REFERENCES piezas(id) ON DELETE CASCADE,
  estacion TEXT,
  detalle  TEXT NOT NULL,
  en       TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS entradas (                -- BUZÓN (input de cualquier canal)
  id       BIGSERIAL PRIMARY KEY,
  canal    TEXT NOT NULL,
  texto    TEXT NOT NULL,
  estado   TEXT NOT NULL DEFAULT 'nuevo',            -- nuevo | triajeado | asignado
  pieza_id TEXT REFERENCES piezas(id) ON DELETE SET NULL,
  recibida TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS agenda (
  id      BIGSERIAL PRIMARY KEY,
  titulo  TEXT NOT NULL,
  vence   DATE,
  urgente BOOLEAN DEFAULT false,
  hecho   BOOLEAN DEFAULT false
);

CREATE TABLE IF NOT EXISTS finanzas (
  id       BIGSERIAL PRIMARY KEY,
  concepto TEXT NOT NULL,
  monto    NUMERIC(14,2) DEFAULT 0,
  tipo     TEXT,                                     -- cobro | ingreso | inversion
  en       TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_piezas_estado  ON piezas(estado);
CREATE INDEX IF NOT EXISTS idx_piezas_origen  ON piezas(origen);
CREATE INDEX IF NOT EXISTS idx_eventos_pieza  ON eventos(pieza_id);
CREATE INDEX IF NOT EXISTS idx_entradas_estado ON entradas(estado);

-- Semilla de prueba (idempotente)
INSERT INTO piezas (id,tipo,origen,estado,nombre,sector,ciudad,score,datos,senales) VALUES
 ('f1','presa','frio','acechador','Conjunto Valle del Refous II','Propiedad horizontal','Bogotá',92,
  '{"tel":"+57 312 ...","web":"vallefous.co","email":"admin@vallefous.co"}',
  '[{"t":"Sin WhatsApp Business","hit":true},{"t":"500-700 mensajes/dia","hit":true}]'),
 ('c1','cliente','propio','servir','Club Wonder''s Voley - Kennya','Deporte','Madrid',0,'{}','[]')
ON CONFLICT (id) DO NOTHING;

INSERT INTO eventos (pieza_id,estacion,detalle) VALUES
 ('f1','vigia','Hallada via RUES'),
 ('f1','acechador','Score 92 -> CALIENTE')
ON CONFLICT DO NOTHING;

INSERT INTO entradas (canal,texto,estado) VALUES
 ('Via hermana (Espana)','Amigo quiere un SmartWeb para pasado manana','nuevo'),
 ('WhatsApp personal','Amigo necesita un SmartShop para vender Dropi','nuevo');
