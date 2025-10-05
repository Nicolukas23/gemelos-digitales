import os
from dotenv import load_dotenv
from pathlib import Path

print("🔍 Diagnóstico de variables de entorno:")
print(f"Directorio actual: {Path.cwd()}")

# Intentar cargar .env desde diferentes ubicaciones
env_paths = [
    Path('.env'),
    Path('../.env'),
    Path(__file__).parent / '.env',
    Path(__file__).parent.parent / '.env'
]

for env_path in env_paths:
    print(f"Buscando en: {env_path} -> Existe: {env_path.exists()}")
    if env_path.exists():
        load_dotenv(env_path)
        break

print(f"DATABASE_URL: {os.environ.get('DATABASE_URL', 'NO ENCONTRADA')}")
print(f"PORT: {os.environ.get('PORT', 'NO ENCONTRADO')}")
