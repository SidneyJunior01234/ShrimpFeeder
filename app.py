import streamlit as st
import os
import sys
import yaml
from pathlib import Path
import base64

# O bloco BASE_DIR e a correção de caminho foram removidos, 
# pois o 'directory_selector.py' já fornece o caminho absoluto (/mnt/...)

if "input_caminho_manual" not in st.session_state:
    st.session_state.input_caminho_manual = ""
    
# Tenta encontrar a logo no caminho relativo (ajuste conforme a estrutura do seu projeto)
logo_path = Path("pages/images/logo.jpg")

if logo_path.exists():
    with open(logo_path, "rb") as f:
        logo_bytes = f.read()
        logo_b64 = base64.b64encode(logo_bytes).decode()

    # Centraliza e exibe no topo
    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src="data:image/png;base64,{logo_b64}" width="200">
        </div>
        """,
        unsafe_allow_html=True,
    )

# Configuração padrão para ser usada como fallback ou como opção
DEFAULT_CONFIG = {
    "processing": {
        "short_term_duration": 0.005,
        "mid_term_duration": 1.0
    },
    "detection": {
        "threshold": 0.005,
        "frequency_band": {
            "low": 5000,
            "high": 22050
        }
    },
    "aggregation": {
        "window_size": 1.0
    }
}

def write_config_file(config_data):
    """
    Writes a config file to the project's config directory.
    """
    # Encontra a raiz do projeto para criar o diretório 'config'
    # Esta lógica depende da estrutura do seu projeto (assumindo que app.py está em pages/ ou na raiz)
    project_root = Path(__file__).resolve().parents[1]
    config_path = project_root / "config"
    config_path.mkdir(exist_ok=True) # Garante que o diretório existe
    
    config_file = config_path / "config.yaml"
    with open(config_file, 'w') as file:
        yaml.dump(config_data, file, default_flow_style=False, sort_keys=False)
    st.success(f"Settings saved in: `{config_file}`")


# ==============================================================================
# --- Lógica principal da página ---
# ==============================================================================

st.set_page_config(
    page_title="Main Application",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Renderiza os page_links na sidebar
with st.sidebar:
    st.page_link('./app.py', label='Home Page', icon='🏚️')
    # Renomeando para refletir o nome real do arquivo no seu projeto
    st.page_link('pages/load_path.py', label='Load Directory', icon='📁')

# Estrutura de texto para exibição
diretorio_estrutura_texto = """
raw
└───Freq_Feeding
    ├───8x_Rep01
    │       ├───audio_file_01.wav
    │       ├───audio_file_02.wav
    │       ├───audio_file_03.wav
    │       └───audio_file_04.wav
    ├───8x_Rep02
    │       ├───audio_file_01.wav
    │       ├───audio_file_02.wav
    │       ├───audio_file_03.wav
    │       └───audio_file_04.wav
    ├───8x_Rep03
    │       ├───audio_file_01.wav
    │       ├───audio_file_02.wav
    │       ├───audio_file_03.wav
    │       └───audio_file_04.wav
    └───8x_Rep04
            ├───audio_file_01.wav
            ├───audio_file_02.wav
            ├───audio_file_03.wav
            └───audio_file_04.wav
"""

# Obtém o caminho selecionado do estado da sessão
caminho_selecionado = st.session_state.get('diretorio_final_selecionado')

if caminho_selecionado:
    st.success(f"O diretório foi selecionado com sucesso.")
    st.markdown(f"O caminho selecionado é: `{caminho_selecionado}`")
    st.markdown(f"Use a barra lateral para configurar os parâmetros do algoritmo.")
    
    # 🚨 PONTO CRÍTICO: Aqui você usaria 'caminho_selecionado' para carregar seus dados
    # Exemplo: all_files = list(Path(caminho_selecionado).rglob('*.wav'))
    
    st.markdown('### ')
    
    # Checkbox para usar a configuração padrão
    use_default_config = st.sidebar.checkbox('Use default settings', value=True)

    # Lógica para mostrar sliders ou caixas de texto
    if not use_default_config:
        use_sliders = st.sidebar.checkbox('Use sliders for editing', value=True)
        
    st.sidebar.markdown('# Processing')
    if use_default_config or use_sliders:
        short_term_duration = st.sidebar.slider('short_term_duration (seconds)', min_value=0.0, max_value=0.1, value=DEFAULT_CONFIG["processing"]["short_term_duration"], step=0.001, format="%.3f", key='short_term_duration_slider', disabled=use_default_config)
        mid_term_duration = st.sidebar.slider('mid_term_duration (seconds)', min_value=0.1, max_value=2.0, value=DEFAULT_CONFIG["processing"]["mid_term_duration"], step=0.01, key='mid_term_duration_slider', disabled=use_default_config)
    else:
        short_term_duration = st.sidebar.text_input('short_term_duration (seconds)', value=str(DEFAULT_CONFIG["processing"]["short_term_duration"]), key='short_term_duration_text')
        mid_term_duration = st.sidebar.text_input('mid_term_duration (seconds)', value=str(DEFAULT_CONFIG["processing"]["mid_term_duration"]), key='mid_term_duration_text')

    st.sidebar.markdown('# Detection')
    if use_default_config or use_sliders:
        threshold = st.sidebar.slider('threshold', min_value=0.0, max_value=0.1, value=DEFAULT_CONFIG["detection"]["threshold"], step=0.001, format="%.3f", key='threshold_slider', disabled=use_default_config)
        low_freq = st.sidebar.slider('frequency_band (low)', min_value=0, max_value=44100, value=DEFAULT_CONFIG["detection"]["frequency_band"]["low"], step=1, key='low_freq_slider', disabled=use_default_config)
        high_freq = st.sidebar.slider('frequency_band (high)', min_value=0, max_value=44100, value=DEFAULT_CONFIG["detection"]["frequency_band"]["high"], step=1, key='high_freq_slider', disabled=use_default_config)
    else:
        threshold = st.sidebar.text_input('threshold', value=str(DEFAULT_CONFIG["detection"]["threshold"]), key='threshold_text')
        low_freq = st.sidebar.text_input('frequency_band (low)', value=str(DEFAULT_CONFIG["detection"]["frequency_band"]["low"]), key='low_freq_text')
        high_freq = st.sidebar.text_input('frequency_band (high)', value=str(DEFAULT_CONFIG["detection"]["frequency_band"]["high"]), key='high_freq_text')

    st.sidebar.markdown('# Aggregation')
    if use_default_config or use_sliders:
        window_size = st.sidebar.slider('window_size (seconds)', min_value=0.0, max_value=2.0, value=DEFAULT_CONFIG["aggregation"]["window_size"], step=0.01, key='window_size_slider', disabled=use_default_config)
    else:
        window_size = st.sidebar.text_input('window_size (seconds)', value=str(DEFAULT_CONFIG["aggregation"]["window_size"]), key='window_size_text')
    
    # Botão de execução
    if st.button('Execute'):
        st.info("O pipeline está em execução...")

        # 1. Constrói o dicionário de configurações com base na escolha do usuário
        if use_default_config:
            config_data = DEFAULT_CONFIG
        else:
            # Converte os valores de texto para os tipos corretos
            try:
                if use_sliders:
                    final_short_term_duration = short_term_duration
                    final_mid_term_duration = mid_term_duration
                    final_threshold = threshold
                    final_low_freq = low_freq
                    final_high_freq = high_freq
                    final_window_size = window_size
                else:
                    final_short_term_duration = float(short_term_duration)
                    final_mid_term_duration = float(mid_term_duration)
                    final_threshold = float(threshold)
                    final_low_freq = int(low_freq)
                    final_high_freq = int(high_freq)
                    final_window_size = float(window_size)

                config_data = {
                    "processing": {
                        "short_term_duration": final_short_term_duration,
                        "mid_term_duration": final_mid_term_duration
                    },
                    "detection": {
                        "threshold": final_threshold,
                        "frequency_band": {
                            "low": final_low_freq,
                            "high": final_high_freq
                        }
                    },
                    "aggregation": {
                        "window_size": final_window_size
                    }
                }
            except ValueError:
                st.error("Erro: Por favor, insira valores numéricos válidos.")
                st.stop()
        
        # 2. Salva o arquivo de configuração antes de executar a pipeline
        write_config_file(config_data)

        # 3. Redireciona para a página de execução da pipeline
        st.switch_page('pages/run_pipeline.py')

else:
    exibir_instrucoes = st.checkbox('Display instructions?')
    if exibir_instrucoes:
        st.markdown("# Initial Instructions")
        st.markdown('For the realization of the experiments, it is necessary to organize the data directories (audio files *.wav).')
        st.markdown('Below is a reference example showing the organization of the directories and files.')
        st.markdown('*raw* refers to the directory where the experiments are located and Freq_Feeding is the folder for the selected experiment.')
        
        st.code(diretorio_estrutura_texto, language='text')

    # Altera o nome do arquivo referenciado para o nome atualizado
    if st.button('Load Path'):
        st.switch_page('pages/load_path.py')
