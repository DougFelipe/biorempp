"""
input_validator.py
------------------
Valida e processa arquivos FASTA-like, extraindo dados para a próxima etapa do
pipeline BioRemPP.
"""

import base64
import re

import pandas as pd

from biorempp.utils.logging_config import get_logger

logger = get_logger("input_processing.input_validator")


def validate_and_process_input(contents: str, filename: str):
    """
    Valida e processa arquivos de input FASTA-like,
    retornando um DataFrame ou mensagem de erro.

    Parâmetros
    ----------
    contents : str
        Conteúdo do arquivo, texto puro ou base64.
    filename : str
        Nome do arquivo (para validar extensão).

    Retorna
    -------
    Tuple[pd.DataFrame | None, str | None]
        DataFrame ('sample', 'ko') ou erro.
    """
    logger.info(f"Processando arquivo: {filename}")

    # 1. Validar extensão
    if not filename.lower().endswith(".txt"):
        error = "Invalid file type. Only .txt files are supported."
        logger.error(error)
        return None, error

    # 2. Decodificar se necessário
    try:
        decoded_content = decode_content_if_base64(contents)
    except Exception as e:
        error = f"Failed to decode file content: {e}"
        logger.error(error)
        return None, error

    # 3. Parsing
    df, error = process_content_lines(decoded_content)
    if error:
        logger.error(error)
        return None, error
    return df, None


def decode_content_if_base64(contents: str) -> str:
    """
    Decodifica se a string estiver em base64 (com data URI).
    """
    if contents.startswith("data"):
        try:
            _, content_string = contents.split(",", 1)
            decoded_bytes = base64.b64decode(content_string)
            decoded_str = decoded_bytes.decode("utf-8")
            # Se decode resultar em string vazia, lança erro explícito
            if not decoded_str.strip():
                raise ValueError("Decoded content is empty.")
            return decoded_str
        except Exception as e:
            logger.exception("Failed to decode base64 content.")
            raise ValueError("Could not decode base64 content.") from e
    return contents


def process_content_lines(content: str):
    """
    Faz o parsing das linhas para extrair sample IDs e KOs.
    """
    lines = content.strip().split("\n")
    identifier_pattern = re.compile(r"^>([^\n]+)")
    ko_pattern = re.compile(r"^(K\d+)$")

    data = []
    current_sample = None

    for line_num, line in enumerate(lines, start=1):
        line = line.strip()
        if not line:
            continue
        id_match = identifier_pattern.match(line)
        ko_match = ko_pattern.match(line)
        if id_match:
            current_sample = id_match.group(1).strip()
        elif ko_match and current_sample:
            ko_value = ko_match.group(1).strip()
            data.append({"sample": current_sample, "ko": ko_value})
        elif ko_match and not current_sample:
            # KO sem sample antes = erro de formato
            return None, (
                f"Invalid format at line {line_num}: '{line}'. "
                "Expected '>' for sample ID before KO entry."
            )
        elif not id_match and not ko_match:
            return None, (
                f"Invalid format at line {line_num}: '{line}'. "
                "Expected '>' for sample ID or 'Kxxxxx' for KO entries."
            )
    if not data:
        return None, "No valid sample or KO entries found in the file."
    df = pd.DataFrame(data)
    return df, None
