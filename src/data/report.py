from fpdf import FPDF
from pathlib import Path
import datetime

def gerar_relatorio_pdf(config_data, image_dir=Path("data/figures/comparison"), output_dir=Path("data/report")):

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Página de título
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Pipeline Experiment Report", ln=True, align='C')
    pdf.ln(5)
    
    # Data e hora
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 8, f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(5)
    
    # Algoritmo usado
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "Algorithm Used:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 7, "Click Detection -> Aggregation -> Comparison Plots")
    pdf.ln(5)
    
    # Parâmetros
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "Parameters Used:", ln=True)
    pdf.set_font("Arial", '', 12)
    for section, params in config_data.items():
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(0, 6, section.capitalize(), ln=True)
        pdf.set_font("Arial", '', 11)
        if isinstance(params, dict):
            for k, v in params.items():
                if isinstance(v, dict):
                    pdf.cell(0, 5, f"  {k}: ", ln=True)
                    for kk, vv in v.items():
                        pdf.cell(0, 5, f"    {kk}: {vv}", ln=True)
                else:
                    pdf.cell(0, 5, f"  {k}: {v}", ln=True)
        else:
            pdf.cell(0, 5, str(params), ln=True)
        pdf.ln(2)
    
    # Gráficos
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "Generated Graphs:", ln=True)
    
    imagens = list(image_dir.glob("*.png"))
    for img_path in imagens:
        pdf.ln(3)
        # Mantendo a largura da página, com margem
        pdf.image(str(img_path), w=180)
    
    # Salvar PDF
    pdf_path = output_dir / "pipeline_report.pdf"
    pdf.output(str(pdf_path))
    
    return pdf_path
