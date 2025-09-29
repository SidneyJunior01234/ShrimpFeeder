import streamlit as st
import os
from pathlib import Path

# --- Gerenciamento de Estado da Sessão ---
def iniciar_estado_sessao():
    """Inicializa as variáveis de estado da sessão."""
    if 'pasta_atual' not in st.session_state:
        st.session_state.pasta_atual = os.path.expanduser("~")  # Começa no home do usuário

    if 'diretorio_final_selecionado' not in st.session_state:
        st.session_state.diretorio_final_selecionado = None

    if 'redirecionar_para_app' not in st.session_state:
        st.session_state.redirecionar_para_app = False

    if 'nova_pasta_pendente' not in st.session_state:
        st.session_state.nova_pasta_pendente = st.session_state.pasta_atual

iniciar_estado_sessao()

# --- Funções de Callback ---
def selecionar_diretorio_atual():
    """Define a pasta atual como a seleção final e prepara para redirecionar."""
    caminho = Path(st.session_state.pasta_atual).resolve()
    # Remove a restrição de BASE_DIR
    st.session_state.diretorio_final_selecionado = str(caminho)
    st.session_state.redirecionar_para_app = True

def aplicar_caminho_manual():
    """Atualiza a pasta atual com base no input de texto manual."""
    caminho_do_input = st.session_state.input_caminho_manual
    if os.path.isdir(caminho_do_input):
        st.session_state.nova_pasta_pendente = os.path.abspath(caminho_do_input)
    else:
        st.error(f"O caminho inserido não é um diretório válido ou acessível: '{caminho_do_input}'")

# --- Layout da Aplicação Streamlit ---
if st.session_state.nova_pasta_pendente != st.session_state.pasta_atual:
    st.session_state.pasta_atual = st.session_state.nova_pasta_pendente
    st.rerun()

st.title("Seletor de Diretórios")
st.write("Selecione o diretório do experimento (qualquer caminho válido do sistema).")

# Campo de input para caminho manual
st.text_input(
    "Insira o caminho do diretório:",
    key='input_caminho_manual',
    on_change=aplicar_caminho_manual,
    help="Ex: /mnt/d/data/raw/Freq_Feeding",
    value=st.session_state.pasta_atual
)

# Botão de seleção final
st.button('✅ Selecionar Este Diretório', on_click=selecionar_diretorio_atual)

# Redirecionamento
if st.session_state.get('redirecionar_para_app'):
    st.success(f"Diretório selecionado com sucesso: `{st.session_state.diretorio_final_selecionado}`")
    st.info("Redirecionando para a página principal...")
    st.session_state.redirecionar_para_app = False
    st.switch_page("app.py")
