# Script de setup para Windows PowerShell
Write-Host "🚀 Configurando base de datos para Gemelos Digitales..." -ForegroundColor Green

# Verificar si PostgreSQL está instalado
try {
    $postgresPath = Get-Command psql -ErrorAction Stop
    Write-Host "✅ PostgreSQL encontrado" -ForegroundColor Green
} catch {
    Write-Host "❌ PostgreSQL no está instalado" -ForegroundColor Red
    Write-Host "   Descarga desde: https://www.postgresql.org/download/windows/" -ForegroundColor Yellow
    exit 1
}

# Verificar/Crear base de datos
$dbExists = & psql -lqt | Select-String "gemelos_digitales"
if ($dbExists) {
    $response = Read-Host "⚠️  La base de datos 'gemelos_digitales' ya existe. ¿Quieres recrearla? (y/n)"
    if ($response -eq 'y') {
        & dropdb gemelos_digitales
        & createdb gemelos_digitales
        Write-Host "✅ Base de datos recreada" -ForegroundColor Green
    }
} else {
    & createdb gemelos_digitales
    Write-Host "✅ Base de datos 'gemelos_digitales' creada" -ForegroundColor Green
}

# Configurar PostGIS y esquemas
Write-Host "🗺️  Configurando PostGIS..." -ForegroundColor Cyan
& psql -d gemelos_digitales -c "CREATE EXTENSION IF NOT EXISTS postgis;"

Write-Host "📊 Creando tablas..." -ForegroundColor Cyan
& psql -d gemelos_digitales -f database/setup.sql

Write-Host "🌱 Insertando datos iniciales..." -ForegroundColor Cyan
& psql -d gemelos_digitales -f database/seeds/initial_data.sql

Write-Host "✅ Configuración de base de datos completada!" -ForegroundColor Green
Write-Host "📌 Conecta con: psql -d gemelos_digitales" -ForegroundColor Yellow
