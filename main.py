from fastapi import FastAPI
import sqlite3
import os
from typing import List, Dict, Any

app = FastAPI(title="API Gemelos Digitales", version="1.0")

# Función para conectar a la base de datos y crear tablas si no existen
def get_db_connection():
    conn = sqlite3.connect('gemelos_digitales.db')
    conn.row_factory = sqlite3.Row  # Para obtener resultados como diccionarios
    
    # Crear tablas si no existen
    cursor = conn.cursor()
    
    # Tabla ciudades
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ciudades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            poblacion INTEGER,
            latitud REAL,
            longitud REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla tenderos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tenderos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            ciudad_id INTEGER,
            direccion TEXT,
            latitud REAL,
            longitud REAL,
            ventas_mensuales REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ciudad_id) REFERENCES ciudades (id)
        )
    ''')
    
    # Verificar si hay datos, si no, insertar datos de ejemplo
    cursor.execute("SELECT COUNT(*) FROM ciudades")
    if cursor.fetchone()[0] == 0:
        # Insertar ciudades
        ciudades_data = [
            ('Bogotá', 8000000, 4.7110, -74.0721),
            ('Medellín', 2500000, 6.2442, -75.5812),
            ('Cali', 2200000, 3.4516, -76.5320),
            ('Barranquilla', 1200000, 10.9639, -74.7964),
            ('Cartagena', 1000000, 10.3910, -75.4794)
        ]
        cursor.executemany('''
            INSERT INTO ciudades (nombre, poblacion, latitud, longitud)
            VALUES (?, ?, ?, ?)
        ''', ciudades_data)
        
        # Insertar tenderos
        tenderos_data = [
            ('Tienda La Esperanza', 1, 'Calle 123 #45-67', 4.7110, -74.0721, 15000000),
            ('MiniMarket Central', 2, 'Carrera 80 #25-30', 6.2442, -75.5812, 8000000),
            ('Super Ahorro', 3, 'Avenida 5N #10-20', 3.4516, -76.5320, 12000000),
            ('Despensa Familiar', 4, 'Carrera 45 #72-15', 10.9639, -74.7964, 6000000)
        ]
        cursor.executemany('''
            INSERT INTO tenderos (nombre, ciudad_id, direccion, latitud, longitud, ventas_mensuales)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', tenderos_data)
        
        conn.commit()
    
    return conn

# Ruta principal
@app.get("/")
async def root():
    return {
        "mensaje": "🚀 API de Gemelos Digitales funcionando!", 
        "version": "1.0",
        "rutas_disponibles": [
            "/db-status",
            "/ciudades", 
            "/tenderos"
        ]
    }

# Ruta para verificar estado de la base de datos
@app.get("/db-status")
async def db_status():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        return {
            "status": "✅ Conectado", 
            "tablas": [table[0] for table in tables],
            "total_tablas": len(tables)
        }
    except Exception as e:
        return {"status": "❌ Error", "detalle": str(e)}

# Ruta para obtener ciudades
@app.get("/ciudades")
async def get_ciudades():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ciudades;")
        ciudades = cursor.fetchall()
        conn.close()
        
        return {"ciudades": [dict(ciudad) for ciudad in ciudades]}
    except Exception as e:
        return {
            "ciudades": [
                {"id": 1, "nombre": "Bogotá", "poblacion": 8000000},
                {"id": 2, "nombre": "Medellín", "poblacion": 2500000},
                {"id": 3, "nombre": "Cali", "poblacion": 2200000}
            ],
            "error": f"Usando datos de ejemplo: {str(e)}"
        }

# Ruta para obtener tenderos
@app.get("/tenderos")
async def get_tenderos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.*, c.nombre as ciudad_nombre 
            FROM tenderos t 
            LEFT JOIN ciudades c ON t.ciudad_id = c.id;
        """)
        tenderos = cursor.fetchall()
        conn.close()
        
        return {"tenderos": [dict(tendero) for tendero in tenderos]}
    except Exception as e:
        return {
            "tenderos": [
                {"id": 1, "nombre": "Tienda La Esperanza", "ciudad": "Bogotá", "ventas_mensuales": 15000000},
                {"id": 2, "nombre": "MiniMarket Central", "ciudad": "Medellín", "ventas_mensuales": 8000000},
                {"id": 3, "nombre": "Super Ahorro", "ciudad": "Cali", "ventas_mensuales": 12000000}
            ],
            "error": f"Usando datos de ejemplo: {str(e)}"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)