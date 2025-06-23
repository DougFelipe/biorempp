"""
Configuração global de mocks e fixtures para testes do BioRemPP.

- Para saber mais sobre conftest.py:
    https://docs.pytest.org/en/stable/fixture.html
    https://docs.pytest.org/en/stable/writing_plugins.html
"""

import pandas as pd
import pytest

# ---------------------
# Mocks para arquivos de input
# ---------------------


@pytest.fixture
def fasta_like_input_txt():
    """
    Retorna um input do tipo FASTA-like com 5 amostras e 20 KOs variados.
    """
    return (
        ">SampleA\n"
        "K00001\nK00002\nK00003\nK00004\nK00005\n"
        ">SampleB\n"
        "K00006\nK00007\nK00008\nK00009\nK00010\n"
        ">SampleC\n"
        "K00011\nK00012\nK00013\nK00014\nK00015\n"
        ">SampleD\n"
        "K00016\nK00017\nK00018\n"
        ">SampleE\n"
        "K00019\nK00020\nK00001\nK00008\n"
    )


# ---------------------
# Mocks para o banco de dados BioRemPP
# ---------------------
@pytest.fixture
def mock_biorempp_db_csv(tmp_path):
    """
    Gera um CSV temporário com estrutura e conteúdo similar ao banco real BioRemPP.
    """
    data = [
        # Linhas para K00001
        [
            "K00001",
            "E1.1.1.1",
            "alcohol dehydrogenase",
            "C19302",
            "Nitrogen-containing",
            "IARC2B",
            "Thioacetamide",
            "dehydrogenase",
        ],
        [
            "K00001",
            "E1.1.1.1",
            "alcohol dehydrogenase",
            "C06696",
            "Metal",
            "ATSDR",
            "Lead",
            "dehydrogenase",
        ],
        [
            "K00001",
            "E1.1.1.1",
            "alcohol dehydrogenase",
            "C11344",
            "Aliphatic",
            "PSL",
            "Methyl tert-butyl ether",
            "dehydrogenase",
        ],
        [
            "K00001",
            "E1.1.1.1",
            "alcohol dehydrogenase",
            "C00084",
            "Aliphatic",
            "IARC1",
            "Acetaldehyde",
            "dehydrogenase",
        ],
        # Linhas para K00002
        [
            "K00002",
            "AKR1A1",
            "alcohol dehydrogenase (NADP+)",
            "C07434",
            "Nitrogen-containing",
            "IARC2B",
            "Phenobarbital",
            "dehydrogenase",
        ],
        [
            "K00002",
            "AKR1A1",
            "alcohol dehydrogenase (NADP+)",
            "C00038",
            "Metal",
            "ATSDR",
            "Zinc cation",
            "dehydrogenase",
        ],
        # Linhas para K00003, K00004, K00005, K00006,
        # K00007, K00008, K00009, K00010, etc.
        [
            "K00003",
            "GS3",
            "some gene",
            "C99999",
            "Aliphatic",
            "EPA",
            "Some Compound",
            "dehydrogenase",
        ],
        [
            "K00004",
            "BDH",
            "(R,R)-butanediol dehydrogenase",
            "C00038",
            "Metal",
            "ATSDR",
            "Zinc cation",
            "dehydrogenase",
        ],
        [
            "K00005",
            "gldA",
            "glycerol dehydrogenase",
            "C18676",
            "Aliphatic",
            "IARC2B",
            "alpha-Chlorohydrin",
            "dehydrogenase",
        ],
        [
            "K00006",
            "GPD1",
            "glycerol-3-phosphate dehydrogenase (NAD+)",
            "C00038",
            "Metal",
            "EPA",
            "Zinc cation",
            "dehydrogenase",
        ],
        [
            "K00007",
            "dalD",
            "D-arabinitol 4-dehydrogenase",
            "C00038",
            "Metal",
            "EPA",
            "Zinc cation",
            "dehydrogenase",
        ],
        [
            "K00008",
            "SORD",
            "L-iditol 2-dehydrogenase",
            "C13377",
            "Metal",
            "ATSDR",
            "Mercuric chloride",
            "dehydrogenase",
        ],
        [
            "K00009",
            "mtlD",
            "mannitol-1-phosphate 5-dehydrogenase",
            "C00038",
            "Metal",
            "EPA",
            "Zinc cation",
            "dehydrogenase",
        ],
        [
            "K00010",
            "G10",
            "test gene 10",
            "C10101",
            "Aliphatic",
            "EPA",
            "Test Compound",
            "dehydrogenase",
        ],
        [
            "K00011",
            "AKR1B",
            "aldehyde reductase",
            "C07443",
            "Nitrogen-containing",
            "IARC2B",
            "Phenytoin",
            "reductase",
        ],
        [
            "K00012",
            "AKR1B2",
            "aldehyde reductase",
            "C07675",
            "Aromatic",
            "IARC2A",
            "Pioglitazone",
            "reductase",
        ],
        [
            "K00013",
            "GEN13",
            "gene 13",
            "C13131",
            "Chlorinated",
            "ATSDR",
            "Compound 13",
            "dehydrogenase",
        ],
        [
            "K00014",
            "GEN14",
            "gene 14",
            "C14141",
            "Sulfur-containing",
            "EPA",
            "Compound 14",
            "dehydrogenase",
        ],
        [
            "K00015",
            "GEN15",
            "gene 15",
            "C15151",
            "Aromatic",
            "EPA",
            "Compound 15",
            "dehydrogenase",
        ],
        [
            "K00016",
            "GEN16",
            "gene 16",
            "C16161",
            "Inorganic",
            "PSL",
            "Compound 16",
            "dehydrogenase",
        ],
        [
            "K00017",
            "GEN17",
            "gene 17",
            "C17171",
            "Polyaromatic",
            "IARC2B",
            "Compound 17",
            "dehydrogenase",
        ],
        [
            "K00018",
            "GEN18",
            "gene 18",
            "C18181",
            "Metal",
            "ATSDR",
            "Compound 18",
            "dehydrogenase",
        ],
        [
            "K00019",
            "BDH1",
            "3-hydroxybutyrate dehydrogenase",
            "C07308",
            "Metal",
            "ATSDR",
            "Cacodylate",
            "dehydrogenase",
        ],
        [
            "K00020",
            "GEN20",
            "gene 20",
            "C20202",
            "Aromatic",
            "EPA",
            "Compound 20",
            "dehydrogenase",
        ],
    ]
    columns = [
        "ko",
        "genesymbol",
        "genename",
        "cpd",
        "compoundclass",
        "referenceAG",
        "compoundname",
        "enzyme_activity",
    ]
    df = pd.DataFrame(data, columns=columns)
    file_path = tmp_path / "biorempp_db.csv"
    df.to_csv(file_path, sep=";", index=False)
    return str(file_path)
