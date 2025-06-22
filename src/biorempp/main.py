from biorempp.figures import generate_all_figures
from biorempp.pipeline import run_analysis_pipeline


def main():
    print("🚀 Executando BioRemPP via CLI")
    input_path = "src/biorempp/data/sample_data.txt"
    results = run_analysis_pipeline(input_path)
    figures = generate_all_figures(results)
    for name, fig in figures.items():
        fig.write_html(f"output/{name}.html")
        print(f"📊 Gráfico salvo: output/{name}.html")
