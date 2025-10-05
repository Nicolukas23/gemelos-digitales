import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')
print(f"Testing connection to: {DATABASE_URL}")

if not DATABASE_URL:
    print("❌ DATABASE_URL not found")
    exit(1)

try:
    # Asegurar formato para psycopg2
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Probar consulta simple
    cursor.execute("SELECT version();")
    result = cursor.fetchone()
    
    print(f"✅ Connection successful!")
    print(f"PostgreSQL version: {result[0]}")
    
    # Probar PostGIS
    cursor.execute("SELECT PostGIS_Version();")
    postgis_result = cursor.fetchone()
    print(f"PostGIS version: {postgis_result[0]}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
