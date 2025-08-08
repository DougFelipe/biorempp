"""
input_validator.py
------------------
Valida e processa arquivos FASTA-like, extraindo dados para a próxima etapa do
pipeline BioRemPP.
"""

import base64
import logging
import re

import pandas as pd

# Technical logging (silent to console, file only)
logger = logging.getLogger("biorempp.input_processing.input_validator")


def validate_and_process_input(contents: str, filename: str):
    """
    Validate and process FASTA-like input files,
    returning a DataFrame or error message.

    Parameters
    ----------
    contents : str
        File content, plain text or base64.
    filename : str
        File name (to validate extension).

    Returns
    -------
    Tuple[pd.DataFrame | None, str | None]
        DataFrame ('sample', 'ko') or error.
    """
    logger.info(f"Processing file: {filename}")

    # 1. Validate extension
    if not filename.lower().endswith(".txt"):
        error = "Invalid file type. Only .txt files are supported."
        logger.error(error)
        return None, error

    # 2. Decode if necessary
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
    Decode if string is in base64 format (with data URI).
    """
    if contents.startswith("data"):
        try:
            _, content_string = contents.split(",", 1)
            decoded_bytes = base64.b64decode(content_string)
            decoded_str = decoded_bytes.decode("utf-8")
            # If decode results in empty string, raise explicit error
            if not decoded_str.strip():
                raise ValueError("Decoded content is empty.")
            return decoded_str
        except Exception as e:
            logger.exception("Failed to decode base64 content.")
            raise ValueError("Could not decode base64 content.") from e
    return contents


def process_content_lines(content: str):
    """
    Parse lines to extract sample IDs and KOs.
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
            # KO without sample before = format error
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
