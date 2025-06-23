"""
Módulo de processamento e validação de dados de entrada para o BioRemPP.

Este subpacote contém funções e utilitários para:
    - Carregamento de arquivos FASTA-like
    - Validação de formato e conteúdo dos inputs
    - Decodificação de arquivos base64
    - Preparação e otimização de DataFrames para o pipeline de análise
    - Merge dos dados de entrada com bancos funcionais de referência

Principais funções públicas:
    - validate_and_process_input: Valida e extrai amostras e KOs do input
      para DataFrame
    - merge_input_with_biorempp: Realiza merge do input validado com banco
      BioRemPP (CSV)
    - optimize_dtypes_biorempp: Otimiza colunas categóricas para redução de
      memória
    - load_and_merge_input: Pipeline de validação e merge, pronto para uso em
      CLI ou interfaces
"""

from .biorempp_merge_processing import (
    merge_input_with_biorempp,
    optimize_dtypes_biorempp,
)
from .input_loader import load_and_merge_input
from .input_validator import validate_and_process_input

__all__ = [
    "validate_and_process_input",
    "merge_input_with_biorempp",
    "optimize_dtypes_biorempp",
    "load_and_merge_input",
]
