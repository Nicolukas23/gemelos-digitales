#!/bin/bash

echo "🚀 Configurando base de datos para Gemelos Digitales..."

# Verificar si PostgreSQL está instalado
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL no está instalado. Instálalo con:"
    echo "   brew install postgresql postgis"
    exit 1
fi

# Verificar si la base de datos existe
if psql -lqt | cut -d \| -f 1 | grep -qw gemelos_digitales; then
    echo "⚠️  La base de datos 'gemelos_digitales' ya existe."
    read -p "¿Quieres recrearla? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        dropdb gemelos_digitales
        createdb gemelos_digitales
        echo "✅ Base de datos recreada."
    fi
else
    createdb gemelos_digitales
    echo "✅ Base de datos 'gemelos_digitales' creada."
fi

# Configurar PostGIS y esquemas
echo "🗺️  Configurando PostGIS..."
psql -d gemelos_digitales -c "CREATE EXTENSION IF NOT EXISTS postgis;"

echo "📊 Creando tablas..."
psql -d gemelos_digitales -f database/setup.sql

echo "🌱 Insertando datos iniciales..."
psql -d gemelos_digitales -f database/seeds/initial_data.sql

echo "✅ Configuración de base de datos completada!"
echo "📌 Conecta con: psql -d gemelos_digitales"
