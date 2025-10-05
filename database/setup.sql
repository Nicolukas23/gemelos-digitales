-- Crear base de datos (ejecutar manualmente primero)
-- CREATE DATABASE gemelos_digitales;

-- Conectar a la base de datos gemelos_digitales y ejecutar:

-- Habilitar PostGIS
CREATE EXTENSION IF NOT EXISTS postgis;

-- Tabla de ciudades
CREATE TABLE IF NOT EXISTS ciudades (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    geometry GEOMETRY(POLYGON, 4326),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabla de zonas
CREATE TABLE IF NOT EXISTS zonas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ciudad_id INTEGER REFERENCES ciudades(id),
    geometry GEOMETRY(POLYGON, 4326),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabla de tenderos
CREATE TABLE IF NOT EXISTS tenderos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    latitud DECIMAL(10, 8),
    longitud DECIMAL(11, 8),
    zona_id INTEGER REFERENCES zonas(id),
    geometry GEOMETRY(POINT, 4326),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Índices para mejor performance
CREATE INDEX IF NOT EXISTS idx_zonas_ciudad_id ON zonas(ciudad_id);
CREATE INDEX IF NOT EXISTS idx_tenderos_zona_id ON tenderos(zona_id);
CREATE INDEX IF NOT EXISTS idx_tenderos_geometry ON tenderos USING GIST(geometry);
