import pandas as pd

from biorempp.input_processing.input_loader import load_and_merge_input


# Caminho feliz: tudo certo (input + banco OK)
def test_load_and_merge_input_success(fasta_like_input_txt, mock_biorempp_db_csv):
    df, error = load_and_merge_input(
        fasta_like_input_txt, "input.txt", database_filepath=mock_biorempp_db_csv
    )
    assert error is None
    assert isinstance(df, pd.DataFrame)
    # Deve haver pelo menos uma coluna do banco e do input
    assert "sample" in df.columns
    assert "ko" in df.columns
    assert "genesymbol" in df.columns
    # Todos os samples e KOs do input devem aparecer (se presentes no banco)
    assert (
        df["sample"].isin(["SampleA", "SampleB", "SampleC", "SampleD", "SampleE"]).any()
    )
    assert (
        df["ko"]
        .isin(
            [
                "K00001",
                "K00002",
                "K00003",
                "K00004",
                "K00005",
                "K00006",
                "K00007",
                "K00008",
                "K00009",
                "K00010",
                "K00011",
                "K00012",
                "K00013",
                "K00014",
                "K00015",
                "K00016",
                "K00017",
                "K00018",
                "K00019",
                "K00020",
            ]
        )
        .all()
    )


# Input: extensão errada
def test_load_and_merge_input_invalid_extension(
    fasta_like_input_txt, mock_biorempp_db_csv
):
    df, error = load_and_merge_input(
        fasta_like_input_txt, "input.csv", database_filepath=mock_biorempp_db_csv
    )
    assert df is None
    assert error is not None
    assert "file type" in error or "extension" in error.lower()


# Input: formato inválido (KO sem sample)
def test_load_and_merge_input_invalid_format(mock_biorempp_db_csv):
    invalid_txt = "K00001\n>SampleA\nK00002"
    df, error = load_and_merge_input(
        invalid_txt, "input.txt", database_filepath=mock_biorempp_db_csv
    )
    assert df is None
    assert error is not None
    assert "format" in error.lower() or "Expected '>'" in error


# Input: arquivo vazio
def test_load_and_merge_input_empty(mock_biorempp_db_csv):
    df, error = load_and_merge_input(
        "", "input.txt", database_filepath=mock_biorempp_db_csv
    )
    assert df is None
    assert error is not None
    assert "No valid sample or KO entries" in error or "empty" in error.lower()


# Banco não encontrado
def test_load_and_merge_input_db_not_found(fasta_like_input_txt):
    df, error = load_and_merge_input(
        fasta_like_input_txt, "input.txt", database_filepath="not_a_real_file.csv"
    )
    assert df is None
    assert error is not None
    assert "Database merge error" in error or "not found" in error


# Input válido, KO não está no banco (deve retornar DataFrame vazio)
def test_load_and_merge_input_ko_not_in_db(tmp_path):
    input_txt = ">SampleZ\nK99999\n"
    # Banco só com K00001
    db = pd.DataFrame(
        [["K00001", "GEN", "test", "C001", "class", "ref", "cmp", "act"]],
        columns=[
            "ko",
            "genesymbol",
            "genename",
            "cpd",
            "compoundclass",
            "referenceAG",
            "compoundname",
            "enzyme_activity",
        ],
    )
    db_path = tmp_path / "testdb.csv"
    db.to_csv(db_path, sep=";", index=False)
    df, error = load_and_merge_input(
        input_txt, "input.txt", database_filepath=str(db_path)
    )
    assert error is None
    assert isinstance(df, pd.DataFrame)
    # DataFrame deve estar vazio pois não há KO em comum
    assert df.empty
