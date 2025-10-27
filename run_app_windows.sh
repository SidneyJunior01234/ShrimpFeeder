#!/bin/bash
# =====================================
# Script universal para Windows (WSL)
# =====================================

echo "Iniciando aplicação Streamlit no Windows (via WSL)..."

# Verifica se Docker está instalado
if ! command -v docker &> /dev/null
then
    echo "Docker não encontrado. Instale o Docker Desktop e habilite integração com WSL."
    exit 1
fi

# Caminho padrão do disco D no WSL (pode ajustar se desejar outro)
VOLUME_PATH="/mnt/d/data"

# Cria o diretório se não existir
mkdir -p "$VOLUME_PATH"

# Nome da imagem
IMAGE_NAME="app-streamlit"

# Exibe informações
echo "Imagem: $IMAGE_NAME"
echo "Volume montado: $VOLUME_PATH"
echo "Acesse em: http://localhost:8501"
echo ""

# Executa o container com o volume montado
docker run --rm -it \
    -v "$VOLUME_PATH:$VOLUME_PATH" \
    -p 8501:8501 \
    "$IMAGE_NAME"
