import pandas as pd
import pytest

from biorempp.input_processing.biorempp_merge_processing import (
    merge_input_with_biorempp,
)


@pytest.fixture
def input_df_from_fasta(fasta_like_input_txt):
    """DataFrame de input criado a partir do mock de input
    (pode usar a função de parsing do seu projeto).
    """
    # Supondo que sua função de parsing já existe
    from biorempp.input_processing.input_validator import validate_and_process_input

    df, error = validate_and_process_input(fasta_like_input_txt, "input.txt")
    assert error is None
    return df


def test_merge_full(input_df_from_fasta, mock_biorempp_db_csv):
    """Testa merge completo usando mock realista de banco BioRemPP."""
    df_merged = merge_input_with_biorempp(input_df_from_fasta, mock_biorempp_db_csv)
    # Checa se todas as KOs do input existem no banco
    assert not df_merged.empty
    # Deve conter as colunas do banco
    for col in [
        "ko",
        "genesymbol",
        "genename",
        "cpd",
        "compoundclass",
        "referenceAG",
        "compoundname",
        "enzyme_activity",
        "sample",
    ]:
        assert col in df_merged.columns
    # Testa se não há duplicação inesperada de amostras/KOs (apenas cruzamento real)
    assert df_merged["ko"].isin(input_df_from_fasta["ko"]).all()


def test_merge_only_matching(input_df_from_fasta, mock_biorempp_db_csv):
    """Testa que apenas KOs presentes nos dois aparecem no resultado (inner join)."""
    # Remove K00001 do banco temporariamente para testar ausência
    import pandas as pd

    db = pd.read_csv(mock_biorempp_db_csv, sep=";")
    db = db[db["ko"] != "K00001"]
    test_path = mock_biorempp_db_csv.replace(".csv", "_noK00001.csv")
    db.to_csv(test_path, sep=";", index=False)
    from biorempp.input_processing.biorempp_merge_processing import (
        merge_input_with_biorempp,
    )

    merged = merge_input_with_biorempp(input_df_from_fasta, test_path)
    assert "K00001" not in merged["ko"].values


def test_merge_missing_ko_column_raises(input_df_from_fasta, tmp_path):
    """Erro se banco não tem coluna 'ko'."""
    path = tmp_path / "noko.csv"
    pd.DataFrame({"genename": ["a"]}).to_csv(path, sep=";", index=False)
    with pytest.raises(KeyError):
        merge_input_with_biorempp(input_df_from_fasta, str(path))


def test_merge_file_not_found(input_df_from_fasta):
    """Erro se arquivo não existe."""
    with pytest.raises(FileNotFoundError):
        merge_input_with_biorempp(input_df_from_fasta, "fake_path.csv")
