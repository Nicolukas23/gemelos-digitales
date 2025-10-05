from fastapi import FastAPI
import os

app = FastAPI(
    title="API Gemelos Digitales - PRODUCCIÓN",
    description="MVP para optimización de ventas en campo con gemelos digitales", 
    version="3.0"
)

@app.get("/")
async def root():
    return {
        "mensaje": "🚀 API Gemelos Digitales - PRODUCCIÓN CON SUPABASE",
        "version": "3.0",
        "base_datos": "Supabase PostgreSQL", 
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
    return {
        "status": "🔧 Configurando Supabase...",
        "mensaje": "Las tablas necesitan ser creadas en Supabase",
        "proyecto": "Gemelos Digitales"
    }

@app.get("/ciudades")
async def get_ciudades():
    return {
        "ciudades": [
            {"id": 1, "nombre": "Bogotá", "poblacion": 8000000, "latitud": 4.7110, "longitud": -74.0721},
            {"id": 2, "nombre": "Medellín", "poblacion": 2500000, "latitud": 6.2442, "longitud": -75.5812},
            {"id": 3, "nombre": "Cali", "poblacion": 2200000, "latitud": 3.4516, "longitud": -76.5320}
        ],
        "mensaje": "⚠️ Datos de ejemplo - Conecta Supabase para datos reales",
        "total": 3
    }

@app.get("/tenderos")
async def get_tenderos():
    return {
        "tenderos": [
            {"id": 1, "nombre": "Tienda La Esperanza", "ciudad": "Bogotá", "ventas_mensuales": 15000000},
            {"id": 2, "nombre": "MiniMarket Central", "ciudad": "Medellín", "ventas_mensuales": 8000000},
            {"id": 3, "nombre": "Super Ahorro", "ciudad": "Cali", "ventas_mensuales": 12000000}
        ],
        "mensaje": "⚠️ Datos de ejemplo - Conecta Supabase para datos reales",
        "total": 3
    }

@app.get("/productos")
async def get_productos():
    return {
        "productos": [
            {"id": 1, "nombre": "Arroz Diana 1kg", "categoria": "Granos", "precio": 2500},
            {"id": 2, "nombre": "Aceite Gourmet 1L", "categoria": "Aceites", "precio": 12000},
            {"id": 3, "nombre": "Café Sello Rojo 500g", "categoria": "Bebidas", "precio": 8000}
        ],
        "mensaje": "⚠️ Datos de ejemplo - Conecta Supabase para datos reales", 
        "total": 3
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Gemelos Digitales API"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)