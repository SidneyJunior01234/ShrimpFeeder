import streamlit as st

diretorio_estrutura_texto = """
raw
└───Freq_Feeding
    ├───8x_Rep01
    │       ├───audio_file_01.wav
    │       ├───audio_file_02.wav
    │       ├───audio_file_03.wav
    │       └───audio_file_04.wav
    ├───8x_Rep02
    │       ├───audio_file_01.wav
    │       ├───audio_file_02.wav
    │       ├───audio_file_03.wav
    │       └───audio_file_04.wav
    ├───8x_Rep03
    │       ├───audio_file_01.wav
    │       ├───audio_file_02.wav
    │       ├───audio_file_03.wav
    │       └───audio_file_04.wav
    └───8x_Rep04
            ├───audio_file_01.wav
            ├───audio_file_02.wav
            ├───audio_file_03.wav
            └───audio_file_04.wav
"""

# st.set_page_config(
#     initial_sidebar_state="collapsed"
# )

# with st.sidebar:
#     st.page_link('./app.py', label='Início', icon='🏚️')
#     st.page_link('pages/load_path.py', label='Carregar Diretório', icon='📁')

caminho_selecionado = st.session_state.get('diretorio_final_selecionado')

if caminho_selecionado:
    st.success(f"O diretório foi selecionado.")
    st.markdown(f"O caminho selecionado é: `{caminho_selecionado}`")

    st.markdown('### ')

    st.sidebar.markdown('# Processing')
    st.sidebar.slider('short_term_duration (seconds)', min_value=0.0, max_value=0.1, value=0.005, step=0.001, format="%.3f")
    st.sidebar.slider('mid_term_duration (seconds)', min_value=0.1, max_value=2.0, value=1.0, step=0.01)

    st.sidebar.markdown('# Detection')
    st.sidebar.slider('threshold', min_value=0.0, max_value=0.1, value=0.005, step=0.001, format="%.3f")
    st.sidebar.slider('frequency_band (low)', min_value=0, max_value=44100, value=5000, step=1)
    st.sidebar.slider('frequency_band (high)', min_value=0, max_value=44100, value=22050, step=1)

    st.sidebar.markdown('# Aggregation')
    st.sidebar.slider('window_size (seconds)', min_value=0.0, max_value=2.0, value=1.0, step=0.01)

    if st.button('Executar'):
        st.switch_page('pages/run_pipeline.py')

    
            
else:
    exibir_instrucoes = st.checkbox('Exibir instruções?')
    if exibir_instrucoes:
        st.markdown("# Instruções Iniciais")

        st.markdown('Para a realização dos esperimentos, faz-se necessário a organização dos diretórios dos dados (arquivos de audio *.wav).')
        st.markdown('Abaixo temos como exemplo de referência onde temos a organização dos diretórios e arquivos.')
        st.markdown('*raw* refere-se ao diretório onde os experimentos se encontram e *Freq_Feeding* é a pasta do experimento selecionado.')
        
        st.code(diretorio_estrutura_texto, language='text')

    if st.button('Carregar Caminho'):
        st.switch_page('pages/load_path.py')
