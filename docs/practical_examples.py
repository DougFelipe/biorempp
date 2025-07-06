#!/usr/bin/env python3
"""
Exemplos Práticos de Uso do BioRemPP com Comportamento Padrão

Este script demonstra como utilizar o sistema BioRemPP com o novo comportamento
padrão que executa automaticamente ambos os merges (BioRemPP e KEGG).
"""

import os
import subprocess
import sys


def run_command(cmd, description):
    """Execute um comando e mostra o resultado."""
    print(f"\n{'='*60}")
    print(f"EXEMPLO: {description}")
    print(f"{'='*60}")
    print(f"Comando: {cmd}")
    print("-" * 60)

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ SUCESSO!")
            print(f"Saída:\n{result.stdout}")
        else:
            print("❌ ERRO!")
            print(f"Erro: {result.stderr}")
    except Exception as e:
        print(f"❌ EXCEÇÃO: {e}")


def main():
    """Demonstra diferentes formas de usar o BioRemPP."""

    print("🧬 BioRemPP - Exemplos Práticos do Comportamento Padrão")
    print("=" * 80)

    # Verificar se estamos no diretório correto
    if not os.path.exists("src/biorempp/main.py"):
        print("❌ Erro: Execute este script no diretório raiz do BioRemPP")
        sys.exit(1)

    # Verificar se arquivo de entrada existe
    input_file = "docs/exemple_input.txt"
    if not os.path.exists(input_file):
        print(f"❌ Erro: Arquivo de entrada não encontrado: {input_file}")
        sys.exit(1)

    # Exemplo 1: Comportamento padrão (executa ambos os pipelines)
    run_command(
        f"python -m src.biorempp.main --input {input_file}",
        "Comportamento Padrão - Executa BioRemPP + KEGG",
    )

    # Exemplo 2: Especificar explicitamente o pipeline "all"
    run_command(
        f"python -m src.biorempp.main --input {input_file} --pipeline-type all",
        "Pipeline 'all' Explícito - Mesmo comportamento do padrão",
    )

    # Exemplo 3: Personalizar diretório de saída
    run_command(
        f"python -m src.biorempp.main --input {input_file} "
        f"--output-dir results/custom_analysis",
        "Diretório de Saída Personalizado",
    )

    # Exemplo 4: Personalizar nomes dos arquivos
    run_command(
        f"python -m src.biorempp.main --input {input_file} "
        f"--biorempp-output-filename Custom_BioRemPP_Results.txt "
        f"--kegg-output-filename Custom_KEGG_Results.txt",
        "Nomes de Arquivo Personalizados",
    )

    # Exemplo 5: Pipeline individual - apenas BioRemPP
    run_command(
        f"python -m src.biorempp.main --input {input_file} --pipeline-type biorempp",
        "Pipeline Individual - Apenas BioRemPP",
    )

    # Exemplo 6: Pipeline individual - apenas KEGG
    run_command(
        f"python -m src.biorempp.main --input {input_file} --pipeline-type kegg",
        "Pipeline Individual - Apenas KEGG",
    )

    # Exemplo 7: Separador personalizado
    run_command(
        f"python -m src.biorempp.main --input {input_file} --sep ,",
        "Separador Personalizado (vírgula)",
    )

    # Mostrar estrutura de arquivos gerada
    print(f"\n{'='*60}")
    print("ESTRUTURA DE ARQUIVOS GERADA")
    print(f"{'='*60}")

    output_dirs = ["outputs", "results"]
    for base_dir in output_dirs:
        if os.path.exists(base_dir):
            print(f"\n📁 {base_dir}/")
            for root, dirs, files in os.walk(base_dir):
                level = root.replace(base_dir, "").count(os.sep)
                indent = " " * 2 * level
                print(f"{indent}📁 {os.path.basename(root)}/")
                subindent = " " * 2 * (level + 1)
                for file in files:
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    print(f"{subindent}📄 {file} ({file_size:,} bytes)")

    print(f"\n{'='*60}")
    print("VERIFICAR CONTEÚDO DOS ARQUIVOS")
    print(f"{'='*60}")

    # Mostrar primeiras linhas dos arquivos de resultado
    result_files = [
        "outputs/biorempp/BioRemPP_Results.txt",
        "outputs/kegg/KEGG_Results.txt",
    ]

    for file_path in result_files:
        if os.path.exists(file_path):
            print(f"\n📄 {file_path} (primeiras 3 linhas):")
            print("-" * 40)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    for i, line in enumerate(f):
                        if i < 3:
                            print(f"{i+1:2d}: {line.rstrip()}")
                        else:
                            break
            except Exception as e:
                print(f"❌ Erro ao ler arquivo: {e}")

    print(f"\n{'='*60}")
    print("RESUMO DOS COMPORTAMENTOS")
    print(f"{'='*60}")
    print(
        """
🎯 COMPORTAMENTO PADRÃO:
   • Executa automaticamente ambos os pipelines (BioRemPP + KEGG)
   • Salva resultados em: outputs/biorempp/BioRemPP_Results.txt
   • Salva resultados em: outputs/kegg/KEGG_Results.txt
   • Não precisa especificar --pipeline-type (padrão = "all")

🔧 PERSONALIZAÇÃO:
   • --output-dir: Personalizar diretório base
   • --biorempp-output-filename: Nome do arquivo BioRemPP
   • --kegg-output-filename: Nome do arquivo KEGG
   • --sep: Separador personalizado (padrão = ";")

🚀 PIPELINES INDIVIDUAIS:
   • --pipeline-type biorempp: Apenas BioRemPP
   • --pipeline-type kegg: Apenas KEGG
   • --pipeline-type all: Ambos (padrão)

✅ VANTAGENS:
   • Análise abrangente por padrão
   • Estrutura organizada de saída
   • Flexibilidade para personalização
   • Logs detalhados para monitoramento
    """
    )


if __name__ == "__main__":
    main()
