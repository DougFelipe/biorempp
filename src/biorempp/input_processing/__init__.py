"""
Módulo de processamento e validação de dados de entrada para o BioRemPP.

Este subpacote contém funções e utilitários para:
    - Carregamento de arquivos FASTA-like
    - Validação de formato e conteúdo dos inputs
    - Decodificação de arquivos base64
    - Preparação de DataFrames para o pipeline de análise

Principais funções públicas:
    - validate_and_process_input: Valida e extrai amostras e KOs do input para DataFrame
"""

from .input_validator import validate_and_process_input

__all__ = [
    "validate_and_process_input",
]
