import logging
import os

import pandas as pd

logger = logging.getLogger("biorempp.biorempp_merge_processing")


def merge_input_with_biorempp(
    input_data: pd.DataFrame, database_filepath: str = None, optimize_types: bool = True
) -> pd.DataFrame:
    """
    Realiza o merge do input com um banco de referência BioRemPP em formato CSV.

    Parameters
    ----------
    input_data : pd.DataFrame
        DataFrame de input contendo ao menos a coluna 'ko'.
    database_filepath : str, optional
        Caminho para o arquivo do banco (.csv). Default: 'data/database.csv'
    optimize_types : bool, optional
        Otimiza tipos com optimize_dtypes_biorempp. Default: True

    Returns
    -------
    pd.DataFrame
        DataFrame com o merge pelo campo 'ko', pronto para análise.

    Raises
    ------
    FileNotFoundError
        Se o arquivo do banco não existir.
    ValueError
        Se o arquivo não for .csv.
    KeyError
        Se faltar a coluna 'ko' em input ou banco.
    """
    if database_filepath is None:
        database_filepath = os.path.join("data", "database.csv")
    logger.info(f"Usando arquivo de banco: {database_filepath}")

    # Checa existência do arquivo
    if not os.path.exists(database_filepath):
        logger.error(f"Database file not found: {database_filepath}")
        raise FileNotFoundError(f"Database file not found: {database_filepath}")

    # Apenas .csv aceito
    if not database_filepath.lower().endswith(".csv"):
        logger.error("Formato de arquivo não suportado. Use .csv")
        raise ValueError("Unsupported file format. Use .csv")

    # Load database
    try:
        database_df = pd.read_csv(database_filepath, encoding="utf-8", sep=";")
        logger.info(
            "Database loaded (%d rows, %d columns)",
            database_df.shape[0],
            database_df.shape[1],
        )
    except Exception:
        logger.exception("Error loading database CSV.")
        raise

    # Otimiza tipos se solicitado
    if optimize_types:
        database_df = optimize_dtypes_biorempp(database_df)
        input_data = optimize_dtypes_biorempp(input_data.copy())
        logger.info("Tipos otimizados com optimize_dtypes_biorempp.")

    # Valida presença da coluna 'ko'
    for df_name, df in {"input_data": input_data, "database_df": database_df}.items():
        if "ko" not in df.columns:
            logger.error(f"Missing 'ko' column in {df_name}.")
            raise KeyError(
                "Column 'ko' must be present in both input and database DataFrames."
            )

    # Realiza merge pelo campo 'ko'
    merged_df = pd.merge(input_data, database_df, on="ko", how="inner")

    if optimize_types:
        merged_df = optimize_dtypes_biorempp(merged_df)

    logger.info(f"Merge realizado. Shape final: {merged_df.shape}")
    return merged_df


def optimize_dtypes_biorempp(df: pd.DataFrame) -> pd.DataFrame:
    """
    Otimiza tipos de colunas recorrentes no projeto (transforma em categorical).

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame de entrada.

    Returns
    -------
    pd.DataFrame
        DataFrame com tipos otimizados.
    """
    if not isinstance(df, pd.DataFrame):
        logger.error("Input must be a pandas DataFrame.")
        raise TypeError("Input must be a pandas DataFrame.")

    categorical_columns = [
        "ko",
        "genesymbol",
        "genename",
        "cpd",
        "compoundclass",
        "referenceAG",
        "compoundname",
        "enzyme_activity",
        "sample",
    ]

    for col in categorical_columns:
        if col in df.columns:
            logger.debug(f"Convertendo coluna '{col}' para categorical.")
            df[col] = df[col].astype("category")
    logger.info("Otimização de dtypes concluída.")
    return df
