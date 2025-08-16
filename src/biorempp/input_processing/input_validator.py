"""
    input_validator.py
------------------
Input File Validation and Processing Module

This module handles validation and processing of input biological data files
for the BioRemPP pipeline. It supports format with sample
identifiers and KEGG Orthology (KO) entries, including base64-encoded
content from web uploads.

The module provides robust validation, format checking, and data extraction
capabilities with comprehensive error reporting for user feedback and
debugging purposes.

Main Functions:
    - validate_and_process_input: Main validation and processing entry point
    - decode_content_if_base64: Base64 decoding for web upload support
    - process_content_lines: format parsing and validation

Input Format:
    Expected format follows structure:
    >Sample_ID_1
    K00001
    K00002
    >Sample_ID_2
    K00003

Supported Features:
    - Plain text and base64-encoded inputs
    - Multiple samples per file
    - Comprehensive format validation
    - Detailed error reporting with line numbers
"""

import base64
import logging
import re

import pandas as pd

# Technical logging (silent to console, file only)
logger = logging.getLogger("biorempp.input_processing.input_validator")


def validate_and_process_input(contents: str, filename: str):
    """
    Validate and process input files, returning DataFrame or error message.

    This function performs comprehensive validation of input biological data
    files, including format checking, content validation, and data extraction.
    It handles both plain text and base64-encoded inputs with detailed error
    reporting.

    Parameters
    ----------
    contents : str
        File content as string. Can be plain text or base64-encoded data URI
        in format: data:text/plain;base64,<encoded_content>
    filename : str
        Name of the input file. Used for extension validation and logging.
        Must have .txt extension.

    Returns
    -------
    tuple[pd.DataFrame | None, str | None]
        A tuple containing:
        - DataFrame: Validated data with 'sample' and 'ko' columns, or None
        if validation failed
        - str: Error message if validation failed, or None if successful

    Examples
    --------
    >>> contents = ">Sample1\\nK00001\\nK00002"
    >>> df, error = validate_and_process_input(contents, "input.txt")
    >>> if error is None:
    ...     print(df.columns.tolist())
    ['sample', 'ko']

    Notes
    -----
    - Only .txt files are supported
    - Input must follow format with > for sample IDs
    - KO entries must match pattern K followed by digits (e.g., K00001)
    - Base64 decoding is automatically handled
    - All validation errors include line numbers for debugging
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
    Decode base64-encoded content if present, otherwise return as-is.

    This function handles base64-encoded data URIs commonly used in web
    applications for file uploads. It automatically detects and decodes
    base64 content while preserving plain text inputs unchanged.

    Parameters
    ----------
    contents : str
        Input content string. Can be plain text or base64 data URI in
        format: data:text/plain;base64,<encoded_content>

    Returns
    -------
    str
        Decoded content as UTF-8 string.

    Raises
    ------
    ValueError
        If base64 decoding fails or results in empty content.biorempp_merge_processing
    Notes
    -----
    - Automatically detects data URI format by "data" prefix
    - Uses UTF-8 encoding for decoded content
    - Validates that decoded content is not empty
    - Preserves original content if not base64-encoded
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
    Parse and validate content lines to extract sample-KO pairs.

    This function processes the content line by line, extracting sample
    identifiers and their associated KEGG Orthology (KO) entries. It performs
    comprehensive format validation with detailed error reporting including
    line numbers.

    Parameters
    ----------
    content : str
        Input content as plain text string with newline-separated entries.

    Returns
    -------
    tuple[pd.DataFrame | None, str | None]
        A tuple containing:
        - DataFrame: Parsed data with 'sample' and 'ko' columns, or None
        if parsing failed
        - str: Error message with line number if parsing failed, or None
        if successful

    Format Requirements
    -------------------
    - Sample IDs: Lines starting with '>' followed by identifier
    - KO entries: Lines matching pattern 'K' + digits (e.g., K00001)
    - Each KO entry must be associated with a preceding sample ID
    - Empty lines are ignored

    Examples
    --------
    >>> content = ">Sample1\\nK00001\\nK00002\\n>Sample2\\nK00003"
    >>> df, error = process_content_lines(content)
    >>> if error is None:
    ...     print(df.to_dict('records'))
    [{'sample': 'Sample1', 'ko': 'K00001'},
    {'sample': 'Sample1', 'ko': 'K00002'},
    {'sample': 'Sample2', 'ko': 'K00003'}]

    Notes
    -----
    - Regex patterns: '^>([^\\n]+)' for samples, '^(K\\d+)$' for KO entries
    - Line numbers are 1-indexed in error messages
    - Sample IDs are stripped of leading/trailing whitespace
    - KO entries without preceding sample ID generate format errors
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
