"""
Unit tests for the biorempp.pipelines.input_processing module.

This module contains comprehensive tests for all processing pipelines
implemented in the BioRemPP system, including:

1. BioRemPP Pipeline (run_biorempp_processing_pipeline)
   - Primary bioremediation gene-compound database processing
   - Complete workflow from input validation to output generation
   - Memory optimization and categorical type conversion testing

2. KEGG Pipeline (run_kegg_processing_pipeline)
   - Degradation pathway analysis using KEGG database
   - Pathway-specific gene annotation and enrichment
   - Environmental degradation process identification

3. HADEG Pipeline (run_hadeg_processing_pipeline)
   - Hydrocarbon degradation gene database processing
   - Specialized for petroleum contamination analysis
   - Multi-pathway gene classification (Alkanes, Alkenes, Aromatics, etc.)

4. ToxCSM Pipeline (run_toxcsm_processing_pipeline)
   - Two-stage toxicity prediction processing
   - Integration of BioRemPP and ToxCSM databases
   - Chemical safety assessment and SMILES representation

Test Categories:
    - Success scenarios: Validate normal operation with expected inputs
    - Parameter validation: Test custom configurations and options
    - Error handling: Verify proper exception raising and error messages
    - File operations: Test input/output file handling and path resolution
    - Integration: Verify pipeline interactions and data flow
    - Performance: Test memory optimization and processing efficiency

Each test class follows the pattern:
    - Setup: Prepare test data and mock dependencies
    - Act: Execute the pipeline function under test
    - Assert: Verify expected outcomes and side effects

Mock Strategy:
    - External file operations are mocked to avoid filesystem dependencies
    - Database loading functions are mocked with controlled test data
    - Output generation is mocked to focus on pipeline logic testing
    
Test Data:
    - Uses fixtures from conftest.py for consistent test data
    - Temporary files and directories for isolation
    - Representative data covering all supported database formats
"""

import os
from unittest.mock import patch

import pandas as pd
import pytest

from biorempp.pipelines.input_processing import (
    run_biorempp_processing_pipeline,
    run_kegg_processing_pipeline,
    run_hadeg_processing_pipeline,
    run_toxcsm_processing_pipeline,
)


class TestRunBioremppProcessingPipeline:
    """Test suite for run_biorempp_processing_pipeline function."""

    def test_biorempp_pipeline_success_default_params(
        self, tmp_path, fasta_like_input_txt, mock_biorempp_db_csv
    ):
        """
        Test successful execution of BioRemPP pipeline with default parameters.
        
        Verifies that the pipeline correctly processes valid input
        and returns expected results.
        """
        # Arrange
        input_file = tmp_path / "test_input.txt"
        input_file.write_text(fasta_like_input_txt, encoding="utf-8")
        output_dir = tmp_path / "outputs"
        
        # Act
        result = run_biorempp_processing_pipeline(
            input_path=str(input_file),
            database_path=mock_biorempp_db_csv,
            output_dir=str(output_dir),
        )
        
        # Assert
        assert isinstance(result, dict)
        assert "output_path" in result
        assert "matches" in result
        assert "filename" in result
        assert result["matches"] > 0
        assert result["filename"] == "BioRemPP_Results.txt"
        assert os.path.exists(result["output_path"])

    def test_biorempp_pipeline_success_custom_params(
        self, tmp_path, fasta_like_input_txt, mock_biorempp_db_csv
    ):
        """
        Test BioRemPP pipeline execution with custom parameters.
        
        Verifies custom configurations such as filename,
        separator and type optimization.
        """
        # Arrange
        input_file = tmp_path / "custom_input.txt"
        input_file.write_text(fasta_like_input_txt, encoding="utf-8")
        output_dir = tmp_path / "custom_outputs"
        custom_filename = "Custom_BioRemPP.csv"
        
        # Act
        result = run_biorempp_processing_pipeline(
            input_path=str(input_file),
            database_path=mock_biorempp_db_csv,
            output_dir=str(output_dir),
            output_filename=custom_filename,
            sep=",",
            optimize_types=False,
            add_timestamp=True,
        )
        
        # Assert
        assert result["filename"].startswith("Custom_BioRemPP")
        assert result["filename"].endswith(".csv")
        assert os.path.exists(result["output_path"])
        
        # Verifica se o arquivo foi criado com o separador correto
        with open(result["output_path"], "r", encoding="utf-8") as f:
            header = f.readline()
            assert "," in header  # Verifica separador personalizado

    def test_biorempp_pipeline_file_not_found_error(self, mock_biorempp_db_csv):
        """
        Test error handling when input file does not exist.
        
        Verifies that FileNotFoundError is raised with appropriate message.
        """
        # Arrange
        non_existent_file = "/path/to/non/existent/file.txt"
        
        # Act & Assert
        with pytest.raises(FileNotFoundError) as exc_info:
            run_biorempp_processing_pipeline(
                input_path=non_existent_file,
                database_path=mock_biorempp_db_csv,
            )
        
        assert "Input file not found" in str(exc_info.value)
        assert non_existent_file in str(exc_info.value)

    def test_biorempp_pipeline_default_database_path(
        self, tmp_path, fasta_like_input_txt
    ):
        """
        Test usage of default BioRemPP database path.
        
        Verifies that the pipeline correctly uses the default path
        when database_path is None.
        """
        # Arrange
        input_file = tmp_path / "test_input.txt"
        input_file.write_text(fasta_like_input_txt, encoding="utf-8")
        
        # Mock do banco de dados padrão
        mock_df = pd.DataFrame({
            "ko": ["K00001", "K00002"],
            "genesymbol": ["gene1", "gene2"],
            "genename": ["Gene 1", "Gene 2"]
        })
        
        # Act & Assert
        with patch(
            "biorempp.pipelines.input_processing.load_and_merge_input"
        ) as mock_load:
            mock_load.return_value = (mock_df, None)
            
            with patch(
                "biorempp.pipelines.input_processing.save_dataframe_output"
            ) as mock_save:
                mock_save.return_value = "/fake/output/path.txt"
                
                run_biorempp_processing_pipeline(
                    input_path=str(input_file),
                    database_path=None,  # Testa caminho padrão
                )
                
                # Verifica se load_and_merge_input foi chamado
                mock_load.assert_called_once()
                call_args = mock_load.call_args
                
                # Verifica se o caminho do banco de dados padrão foi usado
                assert call_args[1]["database_filepath"] is not None
                assert "database_biorempp.csv" in call_args[1]["database_filepath"]

    @patch("biorempp.pipelines.input_processing.load_and_merge_input")
    def test_biorempp_pipeline_processing_error(
        self, mock_load, tmp_path, fasta_like_input_txt
    ):
        """
        Testa tratamento de erro durante processamento dos dados.
        
        Verifica se RuntimeError é levantada quando ocorre erro
        na função load_and_merge_input.
        """
        # Arrange
        input_file = tmp_path / "test_input.txt"
        input_file.write_text(fasta_like_input_txt, encoding="utf-8")
        
        mock_load.return_value = (None, "Erro de processamento")
        
        # Act & Assert
        with pytest.raises(RuntimeError) as exc_info:
            run_biorempp_processing_pipeline(
                input_path=str(input_file),
                database_path="/fake/db/path.csv",
            )
        
        assert "Pipeline error" in str(exc_info.value)
        assert "Erro de processamento" in str(exc_info.value)

    def test_biorempp_pipeline_empty_dataframe(
        self, tmp_path, fasta_like_input_txt, mock_biorempp_db_csv
    ):
        """
        Testa pipeline com DataFrame vazio (sem matches).
        
        Verifica se o pipeline lida corretamente com casos
        onde não há correspondências no banco de dados.
        """
        # Arrange
        input_file = tmp_path / "test_input.txt"
        input_file.write_text(fasta_like_input_txt, encoding="utf-8")
        
        empty_df = pd.DataFrame(columns=["ko", "genesymbol", "sample"])
        
        # Act
        with patch(
            "biorempp.pipelines.input_processing.load_and_merge_input"
        ) as mock_load:
            mock_load.return_value = (empty_df, None)
            
            with patch(
                "biorempp.pipelines.input_processing.save_dataframe_output"
            ) as mock_save:
                mock_save.return_value = "/fake/output/path.txt"
                
                result = run_biorempp_processing_pipeline(
                    input_path=str(input_file),
                    database_path=mock_biorempp_db_csv,
                )
        
        # Assert
        assert result["matches"] == 0
        assert isinstance(result["output_path"], str)


class TestRunKeggProcessingPipeline:
    """Test suite for run_kegg_processing_pipeline function."""

    def test_kegg_pipeline_success_default_params(
        self, tmp_path, fasta_like_input_txt, mock_kegg_degradation_pathways_csv
    ):
        """
        Test successful execution of KEGG pipeline with default parameters.
        
        Verifies that the pipeline correctly processes degradation pathways
        from KEGG and returns expected results.
        """
        # Arrange
        input_file = tmp_path / "kegg_input.txt"
        input_file.write_text(fasta_like_input_txt, encoding="utf-8")
        output_dir = tmp_path / "kegg_outputs"
        
        # Act
        result = run_kegg_processing_pipeline(
            input_path=str(input_file),
            kegg_database_path=mock_kegg_degradation_pathways_csv,
            output_dir=str(output_dir),
        )
        
        # Assert
        assert isinstance(result, dict)
        assert "output_path" in result
        assert "matches" in result
        assert "filename" in result
        assert result["matches"] > 0
        assert result["filename"] == "KEGG_Results.txt"
        assert os.path.exists(result["output_path"])

    def test_kegg_pipeline_custom_filename_and_separator(
        self, tmp_path, fasta_like_input_txt, mock_kegg_degradation_pathways_csv
    ):
        """
        Testa pipeline KEGG com configurações personalizadas.
        
        Verifica configurações customizadas de arquivo e separador.
        """
        # Arrange
        input_file = tmp_path / "kegg_custom.txt"
        input_file.write_text(fasta_like_input_txt, encoding="utf-8")
        output_dir = tmp_path / "kegg_custom_outputs"
        custom_filename = "Pathways_Analysis.tsv"
        
        # Act
        result = run_kegg_processing_pipeline(
            input_path=str(input_file),
            kegg_database_path=mock_kegg_degradation_pathways_csv,
            output_dir=str(output_dir),
            output_filename=custom_filename,
            sep="\t",  # Tab character correto
            add_timestamp=True,
        )
        
        # Assert
        assert result["filename"].startswith("Pathways_Analysis")
        assert result["filename"].endswith(".tsv")
        
        # Verifica se o arquivo foi criado com separador tab
        with open(result["output_path"], "r", encoding="utf-8") as f:
            header = f.readline()
            assert "\t" in header

    def test_kegg_pipeline_file_not_found_error(
        self, mock_kegg_degradation_pathways_csv
    ):
        """
        Testa tratamento de erro quando arquivo de input não existe.
        """
        # Arrange
        non_existent_file = "/path/to/non/existent/kegg_file.txt"
        
        # Act & Assert
        with pytest.raises(FileNotFoundError) as exc_info:
            run_kegg_processing_pipeline(
                input_path=non_existent_file,
                kegg_database_path=mock_kegg_degradation_pathways_csv,
            )
        
        assert "Input file not found" in str(exc_info.value)

    def test_kegg_pipeline_default_database_path(
        self, tmp_path, fasta_like_input_txt
    ):
        """
        Testa uso do caminho padrão do banco KEGG.
        """
        # Arrange
        input_file = tmp_path / "test_input.txt"
        input_file.write_text(fasta_like_input_txt, encoding="utf-8")
        
        mock_df = pd.DataFrame({
            "ko": ["K00001"],
            "pathname": ["Aromatic"],
            "genesymbol": ["gene1"],
            "sample": ["SampleA"]
        })
        
        # Act
        with patch(
            "biorempp.input_processing.input_validator.validate_and_process_input"
        ) as mock_validate:
            mock_validate.return_value = (mock_df, None)
            
            with patch(
                "biorempp.pipelines.input_processing.merge_input_with_kegg"
            ) as mock_merge:
                mock_merge.return_value = mock_df
                
                with patch(
                    "biorempp.pipelines.input_processing.save_dataframe_output"
                ) as mock_save:
                    mock_save.return_value = "/fake/kegg/output.txt"
                    
                    run_kegg_processing_pipeline(
                        input_path=str(input_file),
                        kegg_database_path=None,  # Testa caminho padrão
                    )
                    
                    # Verifica se merge foi chamado com caminho padrão
                    mock_merge.assert_called_once()
                    call_args = mock_merge.call_args
                    assert "kegg_degradation_pathways.csv" in call_args[1][
                        "kegg_filepath"
                    ]

    @patch("biorempp.input_processing.input_validator.validate_and_process_input")
    def test_kegg_pipeline_validation_error(
        self, mock_validate, tmp_path, fasta_like_input_txt
    ):
        """
        Testa tratamento de erro durante validação de input.
        """
        # Arrange
        input_file = tmp_path / "test_input.txt"
        input_file.write_text(fasta_like_input_txt, encoding="utf-8")
        
        mock_validate.return_value = (None, "Erro de validação KEGG")
        
        # Act & Assert
        with pytest.raises(RuntimeError) as exc_info:
            run_kegg_processing_pipeline(
                input_path=str(input_file),
                kegg_database_path="/fake/kegg/db.csv",
            )
        
        assert "KEGG pipeline validation error" in str(exc_info.value)
        assert "Erro de validação KEGG" in str(exc_info.value)


class TestRunHadegProcessingPipeline:
    """Test suite for run_hadeg_processing_pipeline function."""

    def test_hadeg_pipeline_success_default_params(
        self, tmp_path, fasta_like_input_txt, mock_hadeg_database_csv
    ):
        """
        Test successful execution of HADEG pipeline with default parameters.
        
        Verifies processing of hydrocarbon degradation genes.
        """
        # Arrange
        input_file = tmp_path / "hadeg_input.txt"
        input_file.write_text(fasta_like_input_txt, encoding="utf-8")
        output_dir = tmp_path / "hadeg_outputs"
        
        # Act
        result = run_hadeg_processing_pipeline(
            input_path=str(input_file),
            hadeg_database_path=mock_hadeg_database_csv,
            output_dir=str(output_dir),
        )
        
        # Assert
        assert isinstance(result, dict)
        assert "output_path" in result
        assert "matches" in result
        assert "filename" in result
        assert result["matches"] >= 0
        assert result["filename"] == "HADEG_Results.txt"
        assert os.path.exists(result["output_path"])

    def test_hadeg_pipeline_hydrocarbon_specific_analysis(
        self, tmp_path, mock_hadeg_database_csv
    ):
        """
        Test HADEG pipeline with hydrocarbon-specific data.
        
        Verifies that the pipeline correctly identifies genes related
        to different types of hydrocarbons.
        """
        # Arrange - Hydrocarbon-specific input
        hydrocarbon_input = (
            ">OilSampleA\n"
            "K00496\nK24119\nK00128\n"  # Genes alkB, ahpC, alkH
            ">OilSampleB\n"
            "K00549\nK16242\nK00354\n"  # Genes etnE, isoA, abmA
        )
        
        input_file = tmp_path / "hydrocarbon_input.txt"
        input_file.write_text(hydrocarbon_input, encoding="utf-8")
        output_dir = tmp_path / "hydrocarbon_analysis"
        
        # Act
        result = run_hadeg_processing_pipeline(
            input_path=str(input_file),
            hadeg_database_path=mock_hadeg_database_csv,
            output_dir=str(output_dir),
            output_filename="Hydrocarbon_Degradation.txt",
        )
        
        # Assert
        assert result["matches"] > 0
        assert result["filename"] == "Hydrocarbon_Degradation.txt"
        
        # Verifies file contains data from different categories
        with open(result["output_path"], "r", encoding="utf-8") as f:
            content = f.read()
            # Verifies presence of different pathway types
            pathway_types = ["Alkanes", "Alkenes", "Aromatics"]
            assert any(keyword in content for keyword in pathway_types)

    def test_hadeg_pipeline_default_database_path(
        self, tmp_path, fasta_like_input_txt
    ):
        """
        Testa uso do caminho padrão do banco HADEG.
        """
        # Arrange
        input_file = tmp_path / "test_input.txt"
        input_file.write_text(fasta_like_input_txt, encoding="utf-8")
        
        mock_df = pd.DataFrame({
            "ko": ["K00001"],
            "Gene": ["alkB"],
            "Pathway": ["A_Terminal_oxidation"],
            "compound_pathway": ["Alkanes"],
            "sample": ["SampleA"]
        })
        
        # Act
        with patch(
            "biorempp.pipelines.input_processing.load_and_merge_input"
        ) as mock_load:
            mock_load.return_value = (mock_df, None)
            
            with patch(
                "biorempp.pipelines.input_processing.save_dataframe_output"
            ) as mock_save:
                mock_save.return_value = "/fake/hadeg/output.txt"
                
                run_hadeg_processing_pipeline(
                    input_path=str(input_file),
                    hadeg_database_path=None,  # Testa caminho padrão
                )
                
                # Verifica se load_and_merge_input foi chamado com caminho padrão
                mock_load.assert_called_once()
                call_args = mock_load.call_args
                assert "database_hadeg.csv" in call_args[1]["database_filepath"]

    def test_hadeg_pipeline_file_not_found_error(self, mock_hadeg_database_csv):
        """
        Testa tratamento de erro quando arquivo de input não existe.
        """
        # Arrange
        non_existent_file = "/path/to/non/existent/hadeg_file.txt"
        
        # Act & Assert
        with pytest.raises(FileNotFoundError) as exc_info:
            run_hadeg_processing_pipeline(
                input_path=non_existent_file,
                hadeg_database_path=mock_hadeg_database_csv,
            )
        
        assert "Input file not found" in str(exc_info.value)

    @patch("biorempp.pipelines.input_processing.load_and_merge_input")
    def test_hadeg_pipeline_processing_error(
        self, mock_load, tmp_path, fasta_like_input_txt
    ):
        """
        Testa tratamento de erro durante processamento HADEG.
        """
        # Arrange
        input_file = tmp_path / "test_input.txt"
        input_file.write_text(fasta_like_input_txt, encoding="utf-8")
        
        mock_load.return_value = (None, "Erro de processamento HADEG")
        
        # Act & Assert
        with pytest.raises(RuntimeError) as exc_info:
            run_hadeg_processing_pipeline(
                input_path=str(input_file),
                hadeg_database_path="/fake/hadeg/db.csv",
            )
        
        assert "HADEG Pipeline error" in str(exc_info.value)
        assert "Erro de processamento HADEG" in str(exc_info.value)


class TestRunToxcsmProcessingPipeline:
    """Test suite for run_toxcsm_processing_pipeline function."""

    def test_toxcsm_pipeline_success_two_stage_processing(
        self, tmp_path, fasta_like_input_txt, mock_biorempp_db_csv
    ):
        """
        Test successful execution of ToxCSM pipeline with two-stage processing.
        
        Verifies that the pipeline correctly executes:
        1. Processing through BioRemPP
        2. Merge with ToxCSM database
        """
        # Arrange
        input_file = tmp_path / "toxcsm_input.txt"
        input_file.write_text(fasta_like_input_txt, encoding="utf-8")
        output_dir = tmp_path / "toxcsm_outputs"
        
        # Mock DataFrame com coluna 'cpd' para segunda etapa
        biorempp_df = pd.DataFrame({
            "ko": ["K00001", "K00002"],
            "cpd": ["C19302", "C07434"],
            "sample": ["SampleA", "SampleA"],
            "genesymbol": ["gene1", "gene2"]
        })
        
        toxcsm_df = pd.DataFrame({
            "ko": ["K00001", "K00002"],
            "cpd": ["C19302", "C07434"],
            "sample": ["SampleA", "SampleA"],
            "SMILES": ["C1=CC=CC=C1", "C2=CC=CC=C2"],
            "ChEBI": ["CHEBI:1234", "CHEBI:5678"],
            "value_ames": [0.2, 0.8],
            "label_ames": ["Non-toxic", "Toxic"]
        })
        
        # Act
        with patch(
            "biorempp.pipelines.input_processing.load_and_merge_input"
        ) as mock_load:
            mock_load.return_value = (biorempp_df, None)
            
            with patch(
                "biorempp.pipelines.input_processing.merge_input_with_toxcsm"
            ) as mock_toxcsm:
                mock_toxcsm.return_value = toxcsm_df
                
                with patch(
                    "biorempp.pipelines.input_processing.save_dataframe_output"
                ) as mock_save:
                    mock_save.return_value = str(output_dir / "ToxCSM.txt")
                    
                    result = run_toxcsm_processing_pipeline(
                        input_path=str(input_file),
                        toxcsm_database_path="/fake/toxcsm/db.csv",
                        output_dir=str(output_dir),
                    )
        
        # Assert
        assert isinstance(result, dict)
        assert "output_path" in result
        assert "matches" in result
        assert "filename" in result
        assert result["matches"] == 2
        assert result["filename"] == "ToxCSM.txt"
        
        # Verifies that both stages were called
        mock_load.assert_called_once()
        mock_toxcsm.assert_called_once()

    def test_toxcsm_pipeline_custom_parameters(
        self, tmp_path, fasta_like_input_txt
    ):
        """
        Testa pipeline ToxCSM com parâmetros personalizados.
        """
        # Arrange
        input_file = tmp_path / "toxcsm_custom.txt"
        input_file.write_text(fasta_like_input_txt, encoding="utf-8")
        output_dir = tmp_path / "toxcsm_custom_outputs"
        custom_filename = "Toxicity_Assessment.csv"
        
        mock_df = pd.DataFrame({
            "ko": ["K00001"],
            "cpd": ["C19302"],
            "SMILES": ["C1=CC=CC=C1"],
            "value_ames": [0.3]
        })
        
        # Act
        with patch(
            "biorempp.pipelines.input_processing.load_and_merge_input"
        ) as mock_load:
            mock_load.return_value = (mock_df, None)
            
            with patch(
                "biorempp.pipelines.input_processing.merge_input_with_toxcsm"
            ) as mock_toxcsm:
                mock_toxcsm.return_value = mock_df
                
                with patch(
                    "biorempp.pipelines.input_processing.save_dataframe_output"
                ) as mock_save:
                    mock_save.return_value = str(output_dir / custom_filename)
                    
                    result = run_toxcsm_processing_pipeline(
                        input_path=str(input_file),
                        toxcsm_database_path="/fake/toxcsm/db.csv",
                        output_dir=str(output_dir),
                        output_filename=custom_filename,
                        sep=",",
                        optimize_types=False,
                        add_timestamp=True,
                    )
        
        # Assert
        assert custom_filename in result["filename"]
        
        # Verifies that parameters were passed correctly
        mock_toxcsm.assert_called_once()
        call_args = mock_toxcsm.call_args
        assert call_args[1]["optimize_types"] is False

    def test_toxcsm_pipeline_default_database_paths(
        self, tmp_path, fasta_like_input_txt
    ):
        """
        Testa uso de caminhos padrão para ambos os bancos de dados.
        """
        # Arrange
        input_file = tmp_path / "test_input.txt"
        input_file.write_text(fasta_like_input_txt, encoding="utf-8")
        
        mock_df = pd.DataFrame({
            "ko": ["K00001"],
            "cpd": ["C19302"],
            "sample": ["SampleA"]
        })
        
        # Act
        with patch(
            "biorempp.pipelines.input_processing.load_and_merge_input"
        ) as mock_load:
            mock_load.return_value = (mock_df, None)
            
            with patch(
                "biorempp.pipelines.input_processing.merge_input_with_toxcsm"
            ) as mock_toxcsm:
                mock_toxcsm.return_value = mock_df
                
                with patch(
                    "biorempp.pipelines.input_processing.save_dataframe_output"
                ) as mock_save:
                    mock_save.return_value = "/fake/toxcsm/output.txt"
                    
                    run_toxcsm_processing_pipeline(
                        input_path=str(input_file),
                        toxcsm_database_path=None,  # Testa caminho padrão
                    )
                    
                    # Verifica chamadas com caminhos padrão
                    mock_load.assert_called_once()
                    mock_toxcsm.assert_called_once()
                    
                    # Verifica parâmetros de chamada
                    load_call_args = mock_load.call_args
                    toxcsm_call_args = mock_toxcsm.call_args
                    
                    # O BioRemPP path é definido automaticamente quando ToxCSM é None
                    assert load_call_args[1]["database_filepath"] is not None
                    db_path = toxcsm_call_args[1]["database_filepath"]
                    assert "database_toxcsm.csv" in db_path

    def test_toxcsm_pipeline_file_not_found_error(self):
        """
        Testa tratamento de erro quando arquivo de input não existe.
        """
        # Arrange
        non_existent_file = "/path/to/non/existent/toxcsm_file.txt"
        
        # Act & Assert
        with pytest.raises(FileNotFoundError) as exc_info:
            run_toxcsm_processing_pipeline(
                input_path=non_existent_file,
                toxcsm_database_path="/fake/toxcsm/db.csv",
            )
        
        assert "Input file not found" in str(exc_info.value)

    @patch("biorempp.pipelines.input_processing.load_and_merge_input")
    def test_toxcsm_pipeline_biorempp_stage_error(
        self, mock_load, tmp_path, fasta_like_input_txt
    ):
        """
        Testa tratamento de erro na primeira etapa (BioRemPP).
        """
        # Arrange
        input_file = tmp_path / "test_input.txt"
        input_file.write_text(fasta_like_input_txt, encoding="utf-8")
        
        mock_load.return_value = (None, "Erro BioRemPP para ToxCSM")
        
        # Act & Assert
        with pytest.raises(RuntimeError) as exc_info:
            run_toxcsm_processing_pipeline(
                input_path=str(input_file),
                toxcsm_database_path="/fake/toxcsm/db.csv",
            )
        
        assert "BioRemPP processing error" in str(exc_info.value)
        assert "Erro BioRemPP para ToxCSM" in str(exc_info.value)

    def test_toxcsm_pipeline_empty_results(
        self, tmp_path, fasta_like_input_txt
    ):
        """
        Testa pipeline ToxCSM com resultados vazios.
        """
        # Arrange
        input_file = tmp_path / "test_input.txt"
        input_file.write_text(fasta_like_input_txt, encoding="utf-8")
        
        empty_df = pd.DataFrame(columns=["ko", "cpd", "sample", "SMILES"])
        
        # Act
        with patch(
            "biorempp.pipelines.input_processing.load_and_merge_input"
        ) as mock_load:
            mock_load.return_value = (empty_df, None)
            
            with patch(
                "biorempp.pipelines.input_processing.merge_input_with_toxcsm"
            ) as mock_toxcsm:
                mock_toxcsm.return_value = empty_df
                
                with patch(
                    "biorempp.pipelines.input_processing.save_dataframe_output"
                ) as mock_save:
                    mock_save.return_value = "/fake/empty/output.txt"
                    
                    result = run_toxcsm_processing_pipeline(
                        input_path=str(input_file),
                        toxcsm_database_path="/fake/toxcsm/db.csv",
                    )
        
        # Assert
        assert result["matches"] == 0
        assert isinstance(result["output_path"], str)


class TestPipelineIntegration:
    """Integration tests between different pipelines."""

    def test_all_pipelines_consistent_return_format(
        self, tmp_path, fasta_like_input_txt, mock_biorempp_db_csv,
        mock_kegg_degradation_pathways_csv, mock_hadeg_database_csv
    ):
        """
        Test that all pipelines return consistent format.
        
        Verifies that all pipelines return the same data structure
        in the result.
        """
        # Arrange
        input_file = tmp_path / "integration_test.txt"
        input_file.write_text(fasta_like_input_txt, encoding="utf-8")
        
        # List of pipelines to test
        pipelines = [
            (
                run_biorempp_processing_pipeline,
                {"database_path": mock_biorempp_db_csv}
            ),
            (
                run_kegg_processing_pipeline,
                {"kegg_database_path": mock_kegg_degradation_pathways_csv}
            ),
            (
                run_hadeg_processing_pipeline,
                {"hadeg_database_path": mock_hadeg_database_csv}
            ),
        ]
        
        # Act & Assert
        for pipeline_func, extra_kwargs in pipelines:
            result = pipeline_func(
                input_path=str(input_file),
                output_dir=str(tmp_path / f"test_{pipeline_func.__name__}"),
                **extra_kwargs
            )
            
            # Verifies consistent format
            assert isinstance(result, dict)
            assert "output_path" in result
            assert "matches" in result
            assert "filename" in result
            assert isinstance(result["matches"], int)
            assert isinstance(result["output_path"], str)
            assert isinstance(result["filename"], str)

    def test_pipelines_output_directory_creation(
        self, tmp_path, fasta_like_input_txt, mock_biorempp_db_csv
    ):
        """
        Testa se os pipelines criam diretórios de output automaticamente.
        
        Verifica se diretórios não-existentes são criados pelos pipelines.
        """
        # Arrange
        input_file = tmp_path / "test_dir_creation.txt"
        input_file.write_text(fasta_like_input_txt, encoding="utf-8")
        
        non_existent_dir = tmp_path / "new_output_directory" / "subdirectory"
        
        # Act
        result = run_biorempp_processing_pipeline(
            input_path=str(input_file),
            database_path=mock_biorempp_db_csv,
            output_dir=str(non_existent_dir),
        )
        
        # Assert
        assert os.path.exists(non_existent_dir)
        assert os.path.exists(result["output_path"])

    @pytest.mark.parametrize("sep,extension", [
        (";", ".txt"),
        (",", ".csv"),
        ("\t", ".tsv"),
        ("|", ".psv"),
    ])
    def test_pipelines_different_separators(
        self, tmp_path, fasta_like_input_txt, mock_biorempp_db_csv, sep, extension
    ):
        """
        Testa pipelines com diferentes separadores de campo.
        
        Verifica se os pipelines funcionam com diversos separadores.
        """
        # Arrange
        input_file = tmp_path / "test_separators.txt"
        input_file.write_text(fasta_like_input_txt, encoding="utf-8")
        
        filename = f"test_output{extension}"
        
        # Act
        result = run_biorempp_processing_pipeline(
            input_path=str(input_file),
            database_path=mock_biorempp_db_csv,
            output_dir=str(tmp_path),
            output_filename=filename,
            sep=sep,
        )
        
        # Assert
        assert os.path.exists(result["output_path"])
        
        # Verifica se o arquivo foi criado com o separador correto
        with open(result["output_path"], "r", encoding="utf-8") as f:
            header = f.readline()
            assert sep in header
