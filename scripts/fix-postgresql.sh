#!/bin/bash

echo "🔧 Reparando PostgreSQL..."

# Detener el servicio
brew services stop postgresql@14

# Eliminar archivos de bloqueo
echo "🧹 Limpiando archivos de bloqueo..."
rm -f /usr/local/var/postgresql@14/postmaster.pid 2>/dev/null

# Inicializar la base de datos si es necesario
echo "📦 Inicializando base de datos..."
initdb /usr/local/var/postgresql@14 2>/dev/null || echo "La base de datos ya existe"

# Iniciar el servicio
echo "🚀 Iniciando PostgreSQL..."
brew services start postgresql@14

# Esperar a que inicie
sleep 5

# Verificar estado
if brew services list | grep postgresql@14 | grep -q started; then
    echo "✅ PostgreSQL iniciado correctamente"
    
    # Verificar conexión
    if pg_isready -h localhost -p 5432; then
        echo "✅ Conexión a PostgreSQL exitosa"
    else
        echo "❌ No se puede conectar a PostgreSQL"
    fi
else
    echo "❌ No se pudo iniciar PostgreSQL"
    echo "Intenta manualmente: brew services start postgresql@14"
fi
