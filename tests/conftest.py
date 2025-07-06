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


# ---------------------
# Mocks para KEGG degradation pathways
# ---------------------
@pytest.fixture
def mock_kegg_degradation_pathways_csv(tmp_path):
    """
    Gera um CSV temporário com estrutura e conteúdo similar ao banco
    KEGG degradation pathways real.
    """
    data = [
        # K00001 - Multiplos pathways
        ["K00001", "Naphthalene", "E1.1.1.1"],
        ["K00001", "Cytochrome P450", "E1.1.1.1"],
        ["K00001", "Aromatic", "E1.1.1.1"],
        ["K00001", "Cl. alkane and Cl.alkene", "E1.1.1.1"],
        # K00002 - Diferentes pathways
        ["K00002", "Aromatic", "AKR1A1"],
        ["K00002", "Caprolactam", "AKR1A1"],
        # K00003-K00020 - Dados para testes diversos
        ["K00003", "Benzoate", "GS3"],
        ["K00004", "Toluene", "BDH"],
        ["K00005", "Xylene", "gldA"],
        ["K00006", "Styrene", "GPD1"],
        ["K00007", "Aminobenzoate", "dalD"],
        ["K00008", "Fluorobenzoate", "SORD"],
        ["K00009", "Nitrotoluene", "mtlD"],
        ["K00010", "Cl. cyclohexane and Cl. benzene", "G10"],
        ["K00011", "Cytochrome P450", "AKR1B"],
        ["K00012", "Aromatic", "AKR1B2"],
        ["K00013", "Naphthalene", "GEN13"],
        ["K00014", "Benzoate", "GEN14"],
        ["K00015", "Toluene", "GEN15"],
        ["K00016", "Xylene", "GEN16"],
        ["K00017", "Styrene", "GEN17"],
        ["K00018", "Aromatic", "GEN18"],
        ["K00019", "Caprolactam", "BDH1"],
        ["K00020", "Cytochrome P450", "GEN20"],
        # Alguns KOs adicionais para testes de cobertura
        ["K00022", "Caprolactam", "HADH"],
        ["K00055", "Xylene", "E1.1.1.90"],
        ["K00055", "Toluene", "E1.1.1.90"],
        ["K00055", "Aromatic", "E1.1.1.90"],
        ["K00074", "Benzoate", "paaH"],
        ["K00078", "Cytochrome P450", "DHDH"],
        ["K00079", "Cytochrome P450", "CBR1"],
        ["K00081", "Cytochrome P450", "CBR2"],
        ["K00084", "Cytochrome P450", "CBR3"],
        ["K00114", "Cl. alkane and Cl.alkene", "exaA"],
        ["K00121", "Aromatic", "frmA"],
        ["K00121", "Naphthalene", "frmA"],
        ["K00121", "Cytochrome P450", "frmA"],
        ["K00121", "Cl. alkane and Cl.alkene", "frmA"],
        ["K00128", "Cl. alkane and Cl.alkene", "ALDH"],
        ["K00129", "Cytochrome P450", "ALDH3"],
        ["K00141", "Aromatic", "xylC"],
        ["K00141", "Toluene", "xylC"],
        ["K00141", "Aminobenzoate", "xylC"],
        ["K00141", "Xylene", "xylC"],
        ["K00146", "Styrene", "feaB"],
        ["K00148", "Cl. alkane and Cl.alkene", "fdhA"],
        ["K00151", "Aromatic", "hpaE"],
        ["K00152", "Aromatic", "nahF"],
        ["K00152", "Naphthalene", "nahF"],
    ]

    columns = ["ko", "pathname", "genesymbol"]
    df = pd.DataFrame(data, columns=columns)
    file_path = tmp_path / "kegg_degradation_pathways.csv"
    df.to_csv(file_path, sep=";", index=False)
    return str(file_path)


@pytest.fixture
def mock_kegg_degradation_pathways_dataframe():
    """
    Retorna um DataFrame com dados de mock do KEGG degradation pathways
    para testes que não precisam de arquivo.
    """
    data = [
        # K00001 - Multiplos pathways
        ["K00001", "Naphthalene", "E1.1.1.1"],
        ["K00001", "Cytochrome P450", "E1.1.1.1"],
        ["K00001", "Aromatic", "E1.1.1.1"],
        ["K00001", "Cl. alkane and Cl.alkene", "E1.1.1.1"],
        # K00002 - Diferentes pathways
        ["K00002", "Aromatic", "AKR1A1"],
        ["K00002", "Caprolactam", "AKR1A1"],
        # Dados para testes diversos
        ["K00003", "Benzoate", "GS3"],
        ["K00008", "Fluorobenzoate", "SORD"],
        ["K00011", "Cytochrome P450", "AKR1B"],
        ["K00020", "Cytochrome P450", "GEN20"],
    ]

    columns = ["ko", "pathname", "genesymbol"]
    return pd.DataFrame(data, columns=columns)
