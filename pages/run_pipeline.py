import streamlit as st
import subprocess
import sys
import os
import zipfile
import io
from pathlib import Path
from src.data.report import gerar_relatorio_pdf
import yaml

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
            st.error(f"❌ Error during execution: {msg}")
            st.exception(e)
            return

        progress_bar.progress(i / total)

    st.success("✅ Pipeline completed successfully!")
    st.session_state.pipeline_concluida = True


def exibir_resultados_e_zip():
    """Exibe imagens em layout 2x2 e cria ZIP contendo figures + metadata."""
    if not IMAGE_PATH.exists():
        st.warning("⚠ No figures folder found.")
        return

    imagens = list(IMAGE_PATH.glob("*.png"))
    if not imagens:
        st.warning("⚠ No image found in the directory.")
    else:
        st.subheader("📊 Results")
        st.markdown("Visualization of the generated graphs:")

        # Mostra as imagens em duas colunas
        cols = st.columns(2)
        for i, img_path in enumerate(imagens):
            with cols[i % 2]:
                st.image(str(img_path), caption=img_path.name, width='stretch')

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

    # Botão para download do ZIP
    st.download_button(
        label="📦 Download Figures + Metadata (ZIP)",
        data=zip_buffer,
        file_name="results_and_metadata.zip",
        mime="application/zip"
    )

# Página Streamlit
st.title("Experiment Pipeline")

if "diretorio_final_selecionado" not in st.session_state:
    st.warning("Please select a directory before executing the pipeline.")
else:
    st.info(f"📂 Directory selected: {st.session_state.diretorio_final_selecionado}")

    if st.button("🚀 Run Pipeline"):
        st.write("This process may take a few minutes to complete.")
        with st.spinner("Running pipeline..."):
            run_pipeline()

# Exibe resultados se a pipeline foi concluída
if st.session_state.pipeline_concluida:
    exibir_resultados_e_zip()

    config_file = Path("config/config.yaml")
    with open(config_file, "r") as f:
        config_data = yaml.safe_load(f)
    pdf_file = gerar_relatorio_pdf(config_data)
    st.success(f"📄 PDF report generated: {pdf_file}")
    st.download_button(
        label="📥 Download PDF Report",
        data=open(pdf_file, "rb").read(),
        file_name="pipeline_report.pdf",
        mime="application/pdf"
    )