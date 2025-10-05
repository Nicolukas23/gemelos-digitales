import os
from supabase import create_client, Client
import logging

logger = logging.getLogger(__name__)

# Configuración de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://rezoixadvuhucmsdbtyx.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJlem9peGFkdnVodWNtc2RidHl4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk2MjkwMDIsImV4cCI6MjA3NTIwNTAwMn0.QT9nBezWZSVkL3MZsjIyNvxqz89K-qNyuXjmRbcCLVI")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres.rezoixadvuhucmsdbtyx:gemelosdigitales1@aws-1-us-east-2.pooler.supabase.com:5432/postgres")

class SupabaseManager:
    def __init__(self):
        try:
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
    
    def insert_ciudad(self, ciudad_data):
        if not self.supabase:
            return None
        
        try:
            response = self.supabase.table('ciudades').insert(ciudad_data).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error insertando ciudad: {e}")
            return None
    
    def insert_tendero(self, tendero_data):
        if not self.supabase:
            return None
        
        try:
            response = self.supabase.table('tenderos').insert(tendero_data).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error insertando tendero: {e}")
            return None

# Instancia global
supabase_client = SupabaseManager()