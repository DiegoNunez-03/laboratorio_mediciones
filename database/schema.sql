CREATE SCHEMA IF NOT EXISTS lab_mediciones_db;
SET search_path TO lab_mediciones_db, public;

CREATE TABLE IF NOT EXISTS ciudad (
    id_ciudad   SERIAL PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL,
    provincia   VARCHAR(100) NOT NULL,
    pais        VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS rango (
    id_rango      SERIAL PRIMARY KEY,
    nombre_rango  VARCHAR(100) NOT NULL,
    temp_min      INTEGER,
    temp_max      INTEGER
);

CREATE TABLE IF NOT EXISTS mediciones (
    id_mediciones     SERIAL PRIMARY KEY,
    id_ciudad         INTEGER NOT NULL,
    id_rango          INTEGER NOT NULL,
    fecha             DATE NOT NULL DEFAULT CURRENT_DATE,
    humedad           VARCHAR(10) NOT NULL,
    sensacion_termica VARCHAR(10) NOT NULL,
    presion           VARCHAR(10) NOT NULL,
    velocidad_viento  VARCHAR(10) NOT NULL,
    descripcion       VARCHAR(100) NOT NULL,

    CONSTRAINT fk_mediciones_ciudad
        FOREIGN KEY (id_ciudad) REFERENCES ciudad (id_ciudad),

    CONSTRAINT fk_mediciones_rango
        FOREIGN KEY (id_rango) REFERENCES rango (id_rango)
);
