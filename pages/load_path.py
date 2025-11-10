import streamlit as st
from pathlib import Path
import re

# -------------------------------
# Configuração do Ponto de Partida (Foco WSL/Windows)
# -------------------------------
# Define o ponto de partida padrão como o disco C: do Windows, 
# acessível via /mnt/c no WSL.
START_DIR = Path("/mnt/c").resolve()

# -------------------------------
# Gerenciamento de Estado da Sessão
# -------------------------------
def iniciar_estado_sessao():
    r"""Inicializa as variáveis de estado de sessão necessárias."""
    if 'pasta_atual' not in st.session_state:
        # Define o diretório inicial como /mnt/c para facilitar o acesso ao Windows
        st.session_state.pasta_atual = str(START_DIR)
    if 'diretorio_final_selecionado' not in st.session_state:
        st.session_state.diretorio_final_selecionado = None
    if 'redirecionar_para_app' not in st.session_state:
        st.session_state.redirecionar_para_app = False
    if 'nova_pasta_pendente' not in st.session_state:
        st.session_state.nova_pasta_pendente = st.session_state.pasta_atual

iniciar_estado_sessao()

# -------------------------------
# Função de Utilitário Central
# -------------------------------
def converter_sintaxe_para_wsl_linux(caminho_digitado: str) -> str:
    r"""
    Converte um caminho no formato Windows (ex: C:\dir\file)
    para o formato Linux/WSL (ex: /mnt/c/dir/file).
    Se for um caminho Linux/WSL, retorna como está.
    """
    caminho_digitado = caminho_digitado.strip()

    # 1. Detecta caminho Windows (ex: D:\data\raw)
    match = re.match(r'^([A-Za-z]):\\(.*)$', caminho_digitado)
    if match:
        drive = match.group(1).lower()
        # Substitui barras invertidas por barras normais e remove barra inicial extra se houver
        rest = match.group(2).replace("\\", "/").lstrip("/")
        caminho_convertido_str = f"/mnt/{drive}/{rest}"
        st.info(f"💡 Windows path detected and converted to WSL/Linux format: `{caminho_convertido_str}`")
        return caminho_convertido_str
    
    # 2. Retorna o caminho como está se já for um formato Linux/WSL
    return caminho_digitado


# -------------------------------
# Callbacks
# -------------------------------
def selecionar_diretorio_atual():
    r"""Define a pasta atual como a seleção final e redireciona para a página principal."""
    caminho = Path(st.session_state.pasta_atual).resolve()

    # No WSL, a única validação é garantir que o caminho exista e seja um diretório.
    try:
        if caminho.exists() and caminho.is_dir():
            st.session_state.diretorio_final_selecionado = str(caminho)
            st.session_state.redirecionar_para_app = True
        else:
            st.error(f"⚠️ The selected directory does not exist or is not a valid folder: `{st.session_state.pasta_atual}`")
    except Exception as e:
        st.error(f"⚠️ Error validating path: {e}. Please check if the path is correct and accessible.")


def aplicar_caminho_manual():
    r"""Atualiza a pasta atual com base no input de texto manual, aplicando a conversão de sintaxe."""
    caminho_digitado = st.session_state.input_caminho_manual.strip()
    
    # Converte a sintaxe (Windows -> WSL/Linux)
    caminho_convertido_str = converter_sintaxe_para_wsl_linux(caminho_digitado)
    
    # Cria objeto Path
    caminho_convertido = Path(caminho_convertido_str)
    
    # Valida o diretório (checa se existe e é um diretório no ambiente de execução)
    try:
        if caminho_convertido.exists() and caminho_convertido.is_dir():
            # Apenas atualiza o estado pendente, o re-run fará a atualização final
            st.session_state.nova_pasta_pendente = str(caminho_convertido)
        else:
            st.error(f"The entered path is not a valid or accessible directory: '{caminho_digitado}'")
    except Exception as e:
        # Captura erros de FileNotFoundError ou PermissionError
        st.error(f"Error accessing directory: {e}. Please check if the path is correct and accessible.")

# -------------------------------
# Layout Streamlit
# -------------------------------
# Lógica de re-run para forçar a atualização do valor de input após a aplicação manual
if st.session_state.nova_pasta_pendente != st.session_state.pasta_atual:
    st.session_state.pasta_atual = st.session_state.nova_pasta_pendente
    st.rerun()

st.title("Directory Selector")
st.markdown(r"Select the working directory. You can use Windows paths (C:\...) or WSL paths (/mnt/c/...).")

# Campo de input
st.text_input(
    "Enter the directory path:",
    key='input_caminho_manual',
    on_change=aplicar_caminho_manual,
    help="Ex: D:\\data\\raw\\Freq_Feeding (Windows) ou /mnt/d/data/raw/Freq_Feeding (Linux/WSL)",
    value=st.session_state.pasta_atual
)

# Botão de seleção final
st.button('✅ Select This Directory', on_click=selecionar_diretorio_atual)

# Exibe o caminho atualmente definido
st.markdown(f"**Current Path:** `{st.session_state.pasta_atual}`")


# Redirecionamento (simulação)
if st.session_state.get('redirecionar_para_app'):
    st.success(f"Directory selected successfully: `{st.session_state.diretorio_final_selecionado}`")
    st.switch_page('app.py')
    # Apenas limpa o estado para permitir nova seleção
    st.session_state.redirecionar_para_app = False
