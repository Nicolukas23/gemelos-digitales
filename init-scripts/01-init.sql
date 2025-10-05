-- Habilitar PostGIS
CREATE EXTENSION IF NOT EXISTS postgis;

-- Tabla de ciudades
CREATE TABLE ciudades (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    geometry GEOMETRY(POLYGON, 4326)
);

-- Tabla de zonas
CREATE TABLE zonas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ciudad_id INTEGER REFERENCES ciudades(id),
    geometry GEOMETRY(POLYGON, 4326)
);

-- Tabla de tenderos
CREATE TABLE tenderos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    latitud DECIMAL(10, 8),
    longitud DECIMAL(11, 8),
    zona_id INTEGER REFERENCES zonas(id),
    geometry GEOMETRY(POINT, 4326)
);

-- Insertar datos de ejemplo
INSERT INTO ciudades (nombre, geometry) VALUES 
('Bogotá', ST_GeomFromText('POLYGON((-74.2230 4.4730, -73.9890 4.4730, -73.9890 4.8350, -74.2230 4.8350, -74.2230 4.4730))', 4326)),
('Medellín', ST_GeomFromText('POLYGON((-75.7310 6.1300, -75.4810 6.1300, -75.4810 6.4500, -75.7310 6.4500, -75.7310 6.1300))', 4326)),
('Cali', ST_GeomFromText('POLYGON((-76.6200 3.3000, -76.4200 3.3000, -76.4200 3.5500, -76.6200 3.5500, -76.6200 3.3000))', 4326));
