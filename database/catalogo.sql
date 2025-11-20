INSERT INTO rango (nombre_rango, temp_min, temp_max)
VALUES
    ('MUY FRIO',   NULL, 0),
    ('FRIO',        0,   10),
    ('TEMPLADO',    10,  20),
    ('CALIDO',      20,  25),
    ('MUY CALIDO',  25,  NULL)
ON CONFLICT (nombre_rango) DO NOTHING;