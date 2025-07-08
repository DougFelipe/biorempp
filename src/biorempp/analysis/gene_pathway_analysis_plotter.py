"""
Gene pathway analysis plotter module for BioRemPP.

This module provides functionality for creating visualizations of gene and pathway
analysis results, specifically KO counts per sample data.
"""

from pathlib import Path
from typing import Union

import pandas as pd

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

try:
    import plotly.express as px
    import plotly.graph_objects as go
except ImportError:
    px = None
    go = None

from biorempp.utils.logging_config import get_logger

logger = get_logger("analysis.gene_pathway_analysis_plotter")


class GenePathwayPlotter:
    """
    Plotter for gene pathway analysis data from BioRemPP pipeline results.

    This class provides methods for creating visualizations of post-merge data
    including KO counts per sample and other analytical plots.

    Attributes
    ----------
    logger : logging.Logger
        Logger instance for this plotter.
    """

    def __init__(self):
        """Initialize the GenePathwayPlotter."""
        self.logger = logger
        self.logger.info("GenePathwayPlotter initialized")

    def _validate_dataframe(self, df: pd.DataFrame, required_columns: list) -> None:
        """
        Validate that DataFrame has required columns.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to validate.
        required_columns : list
            List of required column names.

        Raises
        ------
        ValueError
            If DataFrame is empty or missing required columns.
        TypeError
            If input is not a pandas DataFrame.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame")

        if df.empty:
            raise ValueError("DataFrame cannot be empty")

        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        self.logger.debug(f"DataFrame validation passed: {df.shape}")

    def plot_ko_counts_per_sample_matplotlib(self, df: pd.DataFrame):
        """
        Gera o gráfico de barras com grid horizontal e estilo limpo.

        Este método cria um gráfico de barras limpo e formatado mostrando a
        distribuição de contagens de KO entre amostras usando matplotlib.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame contendo colunas 'sample' e 'ko_count'.

        Returns
        -------
        matplotlib.figure.Figure
            Objeto figura do matplotlib pronto para exibição ou salvamento.

        Raises
        ------
        TypeError
            Se a entrada não for um pandas DataFrame.
        ValueError
            Se o DataFrame estiver vazio ou faltar colunas obrigatórias.

        Examples
        --------
        >>> plotter = GenePathwayPlotter()
        >>> df = pd.DataFrame({
        ...     'sample': ['Sample1', 'Sample2', 'Sample3'],
        ...     'ko_count': [150, 120, 180]
        ... })
        >>> fig = plotter.plot_ko_counts_per_sample_matplotlib(df)
        """
        self.logger.info("Generating matplotlib KO counts bar plot")

        # Validate input DataFrame
        required_columns = ["sample", "ko_count"]
        self._validate_dataframe(df, required_columns)

        # Definir estilo do matplotlib
        plt.style.use("ggplot")
        fig, ax = plt.subplots(figsize=(18, 9))

        # Criar gráfico de barras
        bars = ax.bar(df["sample"], df["ko_count"], color="steelblue")

        # Definir títulos e rótulos
        ax.set_title("KO Counts per Sample", fontsize=16)
        ax.set_xlabel("Samples", fontsize=12)
        ax.set_ylabel("KO Count", fontsize=12)

        # Rotacionar rótulos do eixo X
        for label in ax.get_xticklabels():
            label.set_rotation(45)
            label.set_horizontalalignment("right")

        # 🔳 Fundo branco
        ax.set_facecolor("white")
        fig.patch.set_facecolor("white")

        # 🟦 Ativar apenas grid horizontal (linhas do eixo Y)
        ax.grid(True, axis="y", linestyle="--", linewidth=0.5, color="gray")
        ax.grid(False, axis="x")  # Desativa o grid vertical

        # Anotar valores apenas se poucos dados
        if len(df) <= 80:
            for bar in bars:
                height = bar.get_height()
                ax.annotate(
                    f"{height}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                    fontsize=8,
                )

        plt.tight_layout()

        self.logger.info(
            f"Matplotlib plot generated successfully for {len(df)} samples"
        )
        return fig

    def plot_ko_counts_per_sample_plotly(self, df: pd.DataFrame):
        """
        Gera um gráfico de barras interativo Plotly de contagens de KO por amostra.

        Este método cria um gráfico de barras interativo mostrando a distribuição
        de contagens de KO entre amostras usando Plotly com estilo consistente
        com a versão matplotlib.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame contendo colunas 'sample' e 'ko_count'.

        Returns
        -------
        plotly.graph_objects.Figure
            Objeto figura do Plotly pronto para exibição ou salvamento.

        Raises
        ------
        TypeError
            Se a entrada não for um pandas DataFrame.
        ValueError
            Se o DataFrame estiver vazio ou faltar colunas obrigatórias.

        Examples
        --------
        >>> plotter = GenePathwayPlotter()
        >>> df = pd.DataFrame({
        ...     'sample': ['Sample1', 'Sample2', 'Sample3'],
        ...     'ko_count': [150, 120, 180]
        ... })
        >>> fig = plotter.plot_ko_counts_per_sample_plotly(df)
        """
        self.logger.info("Generating Plotly interactive KO counts bar plot")

        # Validate input DataFrame
        required_columns = ["sample", "ko_count"]
        self._validate_dataframe(df, required_columns)

        # Criar gráfico de barras simples com cor steelblue
        fig = go.Figure(
            data=[
                go.Bar(
                    x=df["sample"],
                    y=df["ko_count"],
                    marker_color="steelblue",
                    text=df["ko_count"] if len(df) <= 80 else None,
                    textposition="outside" if len(df) <= 80 else None,
                    textfont=dict(size=8),
                )
            ]
        )

        # Configurar layout para corresponder ao estilo matplotlib
        fig.update_layout(
            title={
                "text": "KO Counts per Sample",
                "x": 0.5,
                "xanchor": "center",
                "font": {"size": 16, "family": "Arial, sans-serif"},
            },
            xaxis_title="Samples",
            yaxis_title="KO Count",
            font=dict(size=12),
            plot_bgcolor="white",
            paper_bgcolor="white",
            width=1440,  # Equivalente a figsize=(18, 9) * 80 DPI
            height=720,
            showlegend=False,
        )

        # Rotacionar rótulos do eixo X para amostras múltiplas
        fig.update_layout(xaxis_tickangle=-45)

        # 🟦 Configurar grid: apenas horizontal (eixo Y)
        fig.update_yaxes(
            showgrid=True, gridwidth=0.5, gridcolor="gray", griddash="dash"
        )
        fig.update_xaxes(showgrid=False)

        self.logger.info(f"Plotly plot generated successfully for {len(df)} samples")
        return fig

    def save_plot(
        self, fig, filepath: Union[str, Path], format: str = "png", **kwargs
    ) -> str:
        """
        Save a plot figure to file.

        Parameters
        ----------
        fig : matplotlib.figure.Figure or plotly.graph_objects.Figure
            Figure object to save.
        filepath : str or Path
            Path where to save the figure.
        format : str, optional
            File format for saving ('png', 'pdf', 'svg', 'html' for Plotly).
        **kwargs
            Additional arguments passed to the save method.

        Returns
        -------
        str
            Path to the saved file.

        Raises
        ------
        ValueError
            If figure type is not supported or format is invalid.
        """
        filepath = Path(filepath)

        # Ensure directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)

        try:
            if plt and hasattr(fig, "savefig"):
                # Save matplotlib figure
                valid_formats = ["png", "pdf", "svg", "jpg", "jpeg"]
                if format.lower() not in valid_formats:
                    raise ValueError(
                        f"Format '{format}' not supported for matplotlib. "
                        f"Valid formats: {valid_formats}"
                    )

                filepath = filepath.with_suffix(f".{format}")
                fig.savefig(filepath, dpi=300, bbox_inches="tight", **kwargs)
                plt.close(fig)  # Close to free memory

            elif go and hasattr(fig, "write_html"):
                # Save plotly figure
                if format.lower() == "html":
                    filepath = filepath.with_suffix(".html")
                    fig.write_html(str(filepath), **kwargs)
                elif format.lower() in ["png", "pdf", "svg", "jpg", "jpeg"]:
                    filepath = filepath.with_suffix(f".{format}")
                    fig.write_image(str(filepath), **kwargs)
                else:
                    raise ValueError(f"Format '{format}' not supported for Plotly")
            else:
                raise ValueError("Figure must be matplotlib Figure or Plotly Figure")

            self.logger.info(f"Plot saved successfully to: {filepath}")
            return str(filepath)

        except Exception as e:
            self.logger.error(f"Error saving plot to {filepath}: {str(e)}")
            raise
