# ANKIIT ERP Development Startup Script
Write-Host "🚀 Starting ANKIIT ERP Development Environment..." -ForegroundColor Green

# Check if Docker is running
Write-Host "Checking Docker status..." -ForegroundColor Yellow
try {
    docker info | Out-Null
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Start the development environment
Write-Host "Starting services with Docker Compose..." -ForegroundColor Yellow
docker-compose up -d

Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check service status
Write-Host "Checking service status..." -ForegroundColor Yellow
docker-compose ps

Write-Host ""
Write-Host "🎉 ANKIIT ERP is starting up!" -ForegroundColor Green
Write-Host ""
Write-Host "📱 Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "🔧 Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "🗄️  Database: localhost:5432" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 To stop services, run: docker-compose down" -ForegroundColor Yellow
Write-Host "💡 To view logs, run: docker-compose logs -f" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to open the frontend in your browser..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Open frontend in browser
Start-Process "http://localhost:3000"
