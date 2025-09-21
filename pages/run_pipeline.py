import streamlit as st
import subprocess
import sys
import os
import zipfile
import io
from pathlib import Path

IMAGE_PATH = Path("data/figures/comparison")
METADATA_PATH = Path("data/metadata")

# Usa session_state para guardar o status de execução da pipeline
# if "pipeline_concluida" not in st.session_state:
st.session_state.pipeline_concluida = False

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
            return

        progress_bar.progress(i / total)

    st.success("✅ Pipeline concluída com sucesso!")
    st.session_state.pipeline_concluida = True


def exibir_resultados_e_zip():
    """Exibe imagens e cria ZIP contendo figures + metadata."""
    if not IMAGE_PATH.exists():
        st.warning("⚠ Nenhuma pasta de figuras encontrada.")
        return

    imagens = list(IMAGE_PATH.glob("*.png"))
    if not imagens:
        st.warning("⚠ Nenhuma imagem encontrada no diretório.")
    else:
        st.subheader("📊 Resultados")
        for img_path in imagens:
            st.image(str(img_path), caption=img_path.name)

    # Cria ZIP em memória (figures + metadata)
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        # Adiciona figuras
        if IMAGE_PATH.exists():
            for file in IMAGE_PATH.rglob("*"):
                if file.is_file():
                    zip_file.write(file, arcname=str(file.relative_to(Path("data"))))

        # Adiciona metadata
        if METADATA_PATH.exists():
            for file in METADATA_PATH.rglob("*"):
                if file.is_file():
                    zip_file.write(file, arcname=str(file.relative_to(Path("data"))))

    zip_buffer.seek(0)

    st.download_button(
        label="📦 Baixar Figures + Metadata (ZIP)",
        data=zip_buffer,
        file_name="results_and_metadata.zip",
        mime="application/zip"
    )


# Página Streamlit
st.title("Pipeline de Experimentos")

if "diretorio_final_selecionado" not in st.session_state:
    st.warning("Por favor, selecione um diretório antes de executar a pipeline.")
else:
    st.info(f"📂 Diretório selecionado: {st.session_state.diretorio_final_selecionado}")

    if st.button("🚀 Executar Pipeline"):
        st.write("Esse processo pode durar alguns minutos para finalizar.")
        with st.spinner("Executando pipeline..."):
            run_pipeline()

# Exibe resultados se a pipeline foi concluída
if st.session_state.pipeline_concluida:
    exibir_resultados_e_zip()
