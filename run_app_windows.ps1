# =====================================
# Script universal para Windows PowerShell
# =====================================

Write-Host "Iniciando aplicação Streamlit no Windows..." -ForegroundColor Cyan

# Verifica se Docker está instalado
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Docker não encontrado. Instale o Docker Desktop." -ForegroundColor Red
    exit 1
}

# Caminho padrão do volume (exemplo: D:\data)
$volumePath = "D:\data"

# Cria o diretório se não existir
if (-not (Test-Path $volumePath)) {
    New-Item -ItemType Directory -Force -Path $volumePath | Out-Null
}

# Nome da imagem
$imageName = "app-streamlit"

Write-Host "Imagem: $imageName"
Write-Host "Volume montado: $volumePath"
Write-Host "Acesse em: http://localhost:8501"
Write-Host ""

# Executa o container
docker run --rm -it `
    -v "${volumePath}:${volumePath}" `
    -p 8501:8501 `
    $imageName
