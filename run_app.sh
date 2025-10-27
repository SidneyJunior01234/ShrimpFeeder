#!/bin/bash
# =====================================
# Script universal para Linux e macOS
# =====================================

echo "Iniciando aplicação Streamlit"

# Verifica se Docker está instalado
if ! command -v docker &> /dev/null
then
    echo "Docker não encontrado. Instale-o com:"
    echo "sudo apt install docker.io   # (Ubuntu/Debian)"
    echo "ou brew install --cask docker  # (macOS)"
    exit 1
fi

# Caminho padrão de dados
VOLUME_PATH="$HOME/data"

# Cria o diretório se não existir
mkdir -p "$VOLUME_PATH"

# Nome da imagem
IMAGE_NAME="app-streamlit"

# Exibe informações
echo "Imagem: $IMAGE_NAME"
echo "Volume montado: $VOLUME_PATH"
echo "Acesse em: http://localhost:8501"
echo ""

# Executa o container
docker run --rm -it \
    -v "$VOLUME_PATH:$VOLUME_PATH" \
    -p 8501:8501 \
    "$IMAGE_NAME"
