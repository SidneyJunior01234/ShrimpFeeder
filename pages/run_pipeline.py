import streamlit as st
import subprocess
import sys
import os

IMAGE_PATH = 'data/figures/comparison'
sucess = False

def run_pipeline():
    steps = [
        ("[1/4] Detecting clicks in raw WAV files...",
         [sys.executable, "src/detection/click_detection_batch.py", st.session_state.diretorio_final_selecionado]),
        ("[2/4] Aggregating detections for reference...",
         [sys.executable, "src/aggregation/aggregate_detections_batch.py", "reference_detections"]),
        ("[2/4] Aggregating detections for model...",
         [sys.executable, "src/aggregation/aggregate_detections_batch.py", "model_detections"]),
        ("[3/4] Concatenating aggregated results for reference...",
         [sys.executable, "src/aggregation/join_aggregated_files.py", "reference_detections"]),
        ("[3/4] Concatenating aggregated results for model...",
         [sys.executable, "src/aggregation/join_aggregated_files.py", "model_detections"]),
        ("[4/4] Generating comparison plots...",
         [sys.executable, "src/visualization/plot_detection_comparison.py"]),
    ]

    progress_bar = st.progress(0)
    total = len(steps)

    for i, (msg, cmd) in enumerate(steps, start=1):
        st.write(msg)
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            st.error(f"❌ Erro ao executar: {msg}")
            st.exception(e)
            return  # para a pipeline em caso de erro

        progress_bar.progress(i / total)

    st.success("✅ Pipeline concluída com sucesso!")

# Página Streamlit
st.title("Pipeline de Experimentos")

if "diretorio_final_selecionado" not in st.session_state:
    st.warning("Por favor, selecione um diretório antes de executar a pipeline.")
else:
    st.info(f"📂 Diretório selecionado: {st.session_state.diretorio_final_selecionado}")
    if sucess == False:
        if st.button("🚀 Executar Pipeline"):
            st.write("Esse processo pode durar alguns minutos para finalizar.")
            with st.spinner("Executando pipeline..."):
                run_pipeline()
                sucess = True
if sucess:
    st.title('Visualização dos Resultados')
    imagens = os.listdir(IMAGE_PATH)
    print(imagens)
    for imagem in imagens:
        try:
            st.image(os.path.join(IMAGE_PATH, imagem), caption=imagem)
        except FileNotFoundError:
            st.error(f"Erro: O arquivo não foi encontrado no caminho: {os.path.join(IMAGE_PATH, imagem)}")