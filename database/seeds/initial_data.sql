-- Datos iniciales para desarrollo

-- Ciudades principales (geometrías aproximadas)
INSERT INTO ciudades (nombre, geometry) VALUES 
('Bogotá', ST_GeomFromText('POLYGON((-74.2230 4.4730, -73.9890 4.4730, -73.9890 4.8350, -74.2230 4.8350, -74.2230 4.4730))', 4326)),
('Medellín', ST_GeomFromText('POLYGON((-75.7310 6.1300, -75.4810 6.1300, -75.4810 6.4500, -75.7310 6.4500, -75.7310 6.1300))', 4326)),
('Cali', ST_GeomFromText('POLYGON((-76.6200 3.3000, -76.4200 3.3000, -76.4200 3.5500, -76.6200 3.5500, -76.6200 3.3000))', 4326))
ON CONFLICT DO NOTHING;

-- Zonas de ejemplo para Bogotá
INSERT INTO zonas (nombre, ciudad_id, geometry) VALUES 
('Norte', 1, ST_GeomFromText('POLYGON((-74.2230 4.4730, -74.2230 4.8350, -74.1000 4.8350, -74.1000 4.4730, -74.2230 4.4730))', 4326)),
('Centro', 1, ST_GeomFromText('POLYGON((-74.1000 4.4730, -74.1000 4.8350, -73.9890 4.8350, -73.9890 4.4730, -74.1000 4.4730))', 4326))
ON CONFLICT DO NOTHING;

-- Tenderos de ejemplo
INSERT INTO tenderos (nombre, latitud, longitud, zona_id, geometry) VALUES 
('Tienda La Esquina', 4.7100, -74.1200, 1, ST_GeomFromText('POINT(-74.1200 4.7100)', 4326)),
('MiniMarket Central', 4.6500, -74.0800, 2, ST_GeomFromText('POINT(-74.0800 4.6500)', 4326)),
('Abastos Don Pedro', 4.6200, -74.0700, 2, ST_GeomFromText('POINT(-74.0700 4.6200)', 4326))
ON CONFLICT DO NOTHING;
