from fastapi import FastAPI
from supabase_config import supabase_client
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
    try:
        # Intentar obtener las ciudades para verificar la conexión
        ciudades = supabase_client.get_ciudades()
        return {
            "status": "✅ Conectado a Supabase",
            "total_ciudades": len(ciudades),
            "proyecto": "Gemelos Digitales"
        }
    except Exception as e:
        return {"status": "❌ Error en Supabase", "error": str(e)}

@app.get("/ciudades")
async def get_ciudades():
    try:
        ciudades = supabase_client.get_ciudades()
        return {
            "ciudades": ciudades,
            "total": len(ciudades),
            "fuente": "Supabase"
        }
    except Exception as e:
        return {"error": f"Error obteniendo ciudades: {str(e)}"}

@app.get("/tenderos")
async def get_tenderos():
    try:
        tenderos = supabase_client.get_tenderos()
        return {
            "tenderos": tenderos,
            "total": len(tenderos),
            "fuente": "Supabase"
        }
    except Exception as e:
        return {"error": f"Error obteniendo tenderos: {str(e)}"}

@app.get("/productos")
async def get_productos():
    try:
        productos = supabase_client.get_productos()
        return {
            "productos": productos,
            "total": len(productos),
            "fuente": "Supabase"
        }
    except Exception as e:
        return {"error": f"Error obteniendo productos: {str(e)}"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Gemelos Digitales API"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)