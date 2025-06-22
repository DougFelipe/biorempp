"""
Configuração global de mocks e fixtures para testes do BioRemPP.

- Para saber mais sobre conftest.py:
    https://docs.pytest.org/en/stable/fixture.html
    https://docs.pytest.org/en/stable/writing_plugins.html
"""

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
