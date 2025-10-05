from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API Gemelos Digitales - PRODUCCIÓN",
    description="MVP para optimización de ventas en campo con gemelos digitales",
    version="5.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Intentar importar Supabase
try:
    from supabase_config import supabase_client
    SUPABASE_AVAILABLE = True
    logger.info("✅ Supabase configurado correctamente")
except ImportError as e:
    SUPABASE_AVAILABLE = False
    logger.error(f"❌ Error importando Supabase: {e}")
except Exception as e:
    SUPABASE_AVAILABLE = False
    logger.error(f"❌ Error configurando Supabase: {e}")

@app.get("/")
async def root():
    status = "CONECTADO A SUPABASE" if SUPABASE_AVAILABLE else "CONFIGURANDO SUPABASE"
    return {
        "mensaje": f"🚀 API Gemelos Digitales - {status}",
        "version": "5.0",
        "base_datos": "Supabase PostgreSQL" if SUPABASE_AVAILABLE else "En configuración",
        "rutas_disponibles": [
            "/",
            "/ciudades", 
            "/tenderos",
            "/productos",
            "/supabase-status",
            "/health"
        ]
    }

@app.get("/supabase-status")
async def supabase_status():
    if not SUPABASE_AVAILABLE:
        return {
            "status": "❌ Supabase no disponible",
            "error": "Revisa las variables de entorno y la configuración",
            "proyecto": "Gemelos Digitales"
        }
    
    try:
        ciudades = supabase_client.get_ciudades()
        tenderos = supabase_client.get_tenderos()
        productos = supabase_client.get_productos()
        
        return {
            "status": "✅ Conectado a Supabase",
            "total_ciudades": len(ciudades),
            "total_tenderos": len(tenderos),
            "total_productos": len(productos),
            "proyecto": "Gemelos Digitales"
        }
    except Exception as e:
        return {
            "status": "❌ Error en Supabase",
            "error": str(e),
            "proyecto": "Gemelos Digitales"
        }

@app.get("/ciudades")
async def get_ciudades():
    if not SUPABASE_AVAILABLE:
        return {
            "ciudades": [
                {"id": 1, "nombre": "Bogotá", "poblacion": 8000000, "latitud": 4.7110, "longitud": -74.0721},
                {"id": 2, "nombre": "Medellín", "poblacion": 2500000, "latitud": 6.2442, "longitud": -75.5812},
                {"id": 3, "nombre": "Cali", "poblacion": 2200000, "latitud": 3.4516, "longitud": -76.5320}
            ],
            "mensaje": "⚠️ MODO LOCAL - Supabase no disponible",
            "total": 3
        }
    
    try:
        ciudades = supabase_client.get_ciudades()
        return {
            "ciudades": ciudades,
            "total": len(ciudades),
            "fuente": "Supabase PostgreSQL"
        }
    except Exception as e:
        return {
            "error": f"Error obteniendo ciudades: {str(e)}",
            "ciudades": [],
            "total": 0
        }

@app.get("/tenderos")
async def get_tenderos():
    if not SUPABASE_AVAILABLE:
        return {
            "tenderos": [
                {"id": 1, "nombre": "Tienda La Esperanza", "ciudad": "Bogotá", "ventas_mensuales": 15000000},
                {"id": 2, "nombre": "MiniMarket Central", "ciudad": "Medellín", "ventas_mensuales": 8000000},
                {"id": 3, "nombre": "Super Ahorro", "ciudad": "Cali", "ventas_mensuales": 12000000}
            ],
            "mensaje": "⚠️ MODO LOCAL - Supabase no disponible",
            "total": 3
        }
    
    try:
        tenderos = supabase_client.get_tenderos()
        return {
            "tenderos": tenderos,
            "total": len(tenderos),
            "fuente": "Supabase PostgreSQL"
        }
    except Exception as e:
        return {
            "error": f"Error obteniendo tenderos: {str(e)}",
            "tenderos": [],
            "total": 0
        }

@app.get("/productos")
async def get_productos():
    if not SUPABASE_AVAILABLE:
        return {
            "productos": [
                {"id": 1, "nombre": "Arroz Diana 1kg", "categoria": "Granos", "precio": 2500},
                {"id": 2, "nombre": "Aceite Gourmet 1L", "categoria": "Aceites", "precio": 12000},
                {"id": 3, "nombre": "Café Sello Rojo 500g", "categoria": "Bebidas", "precio": 8000}
            ],
            "mensaje": "⚠️ MODO LOCAL - Supabase no disponible",
            "total": 3
        }
    
    try:
        productos = supabase_client.get_productos()
        return {
            "productos": productos,
            "total": len(productos),
            "fuente": "Supabase PostgreSQL"
        }
    except Exception as e:
        return {
            "error": f"Error obteniendo productos: {str(e)}",
            "productos": [],
            "total": 0
        }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "Gemelos Digitales API",
        "supabase": "connected" if SUPABASE_AVAILABLE else "disconnected"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)