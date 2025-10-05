import os
from supabase import create_client, Client
import logging

logger = logging.getLogger(__name__)

# Configuración de Supabase - REEMPLAZA CON TUS CREDENCIALES REALES
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://zxzpavkwzvmbluywmanb.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp4enBhdmt3enZtYmx1eXdtYW5iIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk2Nzk2OTQsImV4cCI6MjA3NTI1NTY5NH0.2C4fxNP3_3kD0ZKeKwMvQ-SjPh3ijBkQpuvdleLwkF0")

class SupabaseManager:
    def __init__(self):
        try:
            # Crear cliente de Supabase SIN parámetro proxy
            self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
            logger.info("✅ Conectado a Supabase exitosamente")
        except Exception as e:
            logger.error(f"❌ Error conectando a Supabase: {e}")
            self.supabase = None
    
    def get_ciudades(self):
        if not self.supabase:
            return []
        try:
            response = self.supabase.table('ciudades').select('*').execute()
            return response.data
        except Exception as e:
            logger.error(f"Error obteniendo ciudades: {e}")
            return []
    
    def get_tenderos(self):
        if not self.supabase:
            return []
        try:
            response = self.supabase.table('tenderos').select('*, ciudades(nombre)').execute()
            return response.data
        except Exception as e:
            logger.error(f"Error obteniendo tenderos: {e}")
            return []
    
    def get_productos(self):
        if not self.supabase:
            return []
        try:
            response = self.supabase.table('productos').select('*').execute()
            return response.data
        except Exception as e:
            logger.error(f"Error obteniendo productos: {e}")
            return []

# Instancia global
supabase_client = SupabaseManager()