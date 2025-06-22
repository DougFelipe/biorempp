import pandas as pd

from biorempp.input_processing.input_validator import validate_and_process_input


def extract_ko_records(txt):
    """
    Extrai tuplas (sample, ko) de um input FASTA-like
    para comparar com o DataFrame.
    """
    records = []
    current_sample = None
    for line in txt.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            current_sample = line[1:].strip()
        elif line.startswith("K") and current_sample:
            records.append((current_sample, line))
    return records


def test_valid_txt_input(fasta_like_input_txt):
    df, error = validate_and_process_input(fasta_like_input_txt, "input.txt")
    assert error is None
    assert isinstance(df, pd.DataFrame)
    expected_records = extract_ko_records(fasta_like_input_txt)
    assert len(df) == len(expected_records)
    tuples_in_df = set(zip(df["sample"], df["ko"]))
    tuples_expected = set(expected_records)
    assert tuples_in_df == tuples_expected


def test_valid_base64_input(fasta_like_input_txt):
    import base64

    base64_bytes = base64.b64encode(fasta_like_input_txt.encode()).decode()
    encoded = f"data:text/plain;base64,{base64_bytes}"
    df, error = validate_and_process_input(encoded, "input.txt")
    assert error is None
    assert isinstance(df, pd.DataFrame)
    expected_records = extract_ko_records(fasta_like_input_txt)
    assert len(df) == len(expected_records)
    tuples_in_df = set(zip(df["sample"], df["ko"]))
    tuples_expected = set(expected_records)
    assert tuples_in_df == tuples_expected


def test_invalid_extension(fasta_like_input_txt):
    df, error = validate_and_process_input(fasta_like_input_txt, "input.csv")
    assert df is None
    assert error is not None
    assert "invalid file type" in error.lower()


def test_bad_base64_input():
    bad = "data:text/plain;base64,@@@"
    df, error = validate_and_process_input(bad, "input.txt")
    assert df is None
    assert error is not None
    # Aceita qualquer mensagem de erro relevante
    error_l = error.lower()
    assert (
        "decode" in error_l
        or "could not decode" in error_l
        or "no valid sample" in error_l
        or "error" in error_l
    )


def test_invalid_line_format():
    # KO antes de qualquer sample
    bad_content = "K00001\n>SampleX\nK00002"
    df, error = validate_and_process_input(bad_content, "input.txt")
    assert df is None
    assert error is not None
    assert "invalid format" in error.lower()


def test_empty_file():
    df, error = validate_and_process_input("", "input.txt")
    assert df is None
    assert error is not None
    assert "no valid sample" in error.lower() or "no valid" in error.lower()


def test_sample_without_ko():
    content = ">Sample1\n>Sample2\nK00005"
    df, error = validate_and_process_input(content, "input.txt")
    assert error is None
    assert len(df) == 1
    assert df.iloc[0]["sample"] == "Sample2"
    assert df.iloc[0]["ko"] == "K00005"
