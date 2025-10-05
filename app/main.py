from flask import Flask, jsonify
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from pathlib import Path

# Cargar variables del archivo .env
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

app = Flask(__name__)

# Configuración de la base de datos
DATABASE_URL = os.environ.get('DATABASE_URL')
USE_SQLITE = os.environ.get('USE_SQLITE', 'false').lower() == 'true'

if DATABASE_URL:
    engine = create_engine(DATABASE_URL)
    print(f"✅ Conectado a: {'SQLite (desarrollo)' if USE_SQLITE else 'PostgreSQL (producción)'}")
else:
    engine = None

@app.route('/')
def home():
    db_type = "SQLite (desarrollo)" if USE_SQLITE else "PostgreSQL (producción)"
    return jsonify({
        "message": "🚀 MVP Gemelos Digitales - Georreferenciación",
        "status": "active",
        "version": "1.0",
        "database": db_type
    })

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/db-status')
def db_status():
    if not engine:
        return jsonify({"status": "not_configured"})
    
    try:
        with engine.connect() as conn:
            if USE_SQLITE:
                # SQLite
                result = conn.execute(text("SELECT sqlite_version();"))
                db_version = result.fetchone()[0]
                postgis_version = "No disponible en SQLite"
            else:
                # PostgreSQL
                result = conn.execute(text("SELECT version();"))
                db_version = result.fetchone()[0]
                result2 = conn.execute(text("SELECT PostGIS_Version();"))
                postgis_version = result2.fetchone()[0]
            
        return jsonify({
            "status": "connected", 
            "database_version": db_version,
            "postgis_version": postgis_version,
            "database_type": "SQLite" if USE_SQLITE else "PostgreSQL"
        })
    except Exception as e:
        return jsonify({
            "status": "connection_error",
            "error": str(e)
        }), 500

# Crear tablas básicas para SQLite
def init_sqlite_tables():
    if not engine or not USE_SQLITE:
        return
    
    try:
        with engine.connect() as conn:
            # Tabla de ciudades
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS ciudades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    latitud_norte REAL,
                    longitud_oeste REAL,
                    latitud_sur REAL,
                    longitud_este REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Tabla de tenderos
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS tenderos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    latitud REAL,
                    longitud REAL,
                    ciudad_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Insertar datos de ejemplo
            conn.execute(text("""
                INSERT OR IGNORE INTO ciudades (nombre, latitud_norte, longitud_oeste, latitud_sur, longitud_este) 
                VALUES 
                ('Bogotá', 4.8350, -74.2230, 4.4730, -73.9890),
                ('Medellín', 6.4500, -75.7310, 6.1300, -75.4810),
                ('Cali', 3.5500, -76.6200, 3.3000, -76.4200)
            """))
            
            conn.execute(text("""
                INSERT OR IGNORE INTO tenderos (nombre, latitud, longitud, ciudad_id) 
                VALUES 
                ('Tienda La Esquina', 4.7100, -74.1200, 1),
                ('MiniMarket Central', 4.6500, -74.0800, 1),
                ('Abastos Don Pedro', 4.6200, -74.0700, 1)
            """))
            
        print("✅ Tablas SQLite creadas con datos de ejemplo")
    except Exception as e:
        print(f"❌ Error creando tablas SQLite: {e}")

if __name__ == '__main__':
    # Inicializar tablas si usamos SQLite
    if USE_SQLITE:
        init_sqlite_tables()
    
    port = int(os.environ.get('PORT', 8000))
    app.run(host='127.0.0.1', port=port, debug=True)
