# BioRemPP: Bioremediation Potential Profile

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE.txt)
[![GitHub](https://img.shields.io/badge/github-DougFelipe%2Fbiorempp-blue.svg)](https://github.com/DougFelipe/biorempp)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/DougFelipe/biorempp)

## Table of Contents

1. [Overview](#overview)
2. [Database Specifications](#database-specifications)
3. [Installation](#installation)
4. [Command-Line Interface](#command-line-interface)
5. [Input Data Format](#input-data-format)
6. [Output Data Format](#output-data-format)
7. [Usage Examples](#usage-examples)
8. [Python API](#python-api)
9. [System Architecture](#system-architecture)
10. [Pipeline Integration](#pipeline-integration)
11. [Troubleshooting](#troubleshooting)
12. [Contributing](#contributing)

---

## Overview

BioRemPP (Bioremediation Potential Profile) is a sophisticated command-line bioinformatics tool designed for comprehensive assessment of biological systems' bioremediation potential. The software enables systematic analysis of genomic, metagenomic, and transcriptomic data against curated databases to predict biotechnological capabilities for environmental remediation applications.

The system employs a Command Pattern architecture with intelligent factory instantiation, ensuring robust, reproducible, and methodologically rigorous analytical workflows suitable for high-throughput bioinformatics applications and publication-quality research outputs.

### Core Capabilities

- **Multi-Database Integration**: Simultaneous analysis against four specialized bioremediation databases
- **Metabolic Pathway Analysis**: Comprehensive assessment of degradation pathways for environmental contaminants
- **Toxicity Prediction**: Advanced modeling for chemical safety assessment and biological impact evaluation
- **High-Throughput Processing**: Optimized algorithms for large-scale genomic dataset analysis
- **Extensible Architecture**: Modular design supporting integration of additional databases and analytical modules

### Technical Features

- ✅ **Command Pattern Implementation**: Robust CLI architecture with factory-based command instantiation
- ✅ **Multi-Level Verbosity Control**: Configurable output detail from silent to comprehensive debug mode
- ✅ **Structured Output Generation**: Standards-compliant data formats with customizable delimiters
- ✅ **Advanced Error Handling**: Comprehensive exception management with diagnostic recommendations
- ✅ **Type-Optimized Processing**: Memory-efficient data handling for large-scale analyses
- ✅ **Reproducible Workflows**: Deterministic processing ensuring consistent results across environments

---

## Database Specifications

BioRemPP integrates four specialized databases optimized for comprehensive bioremediation potential assessment. Each database provides distinct analytical capabilities and complementary biological insights:

| Database | Records | File Size | Primary Function | Unique Features |
|----------|---------|-----------|------------------|-----------------|
| **BioRemPP Core** | 6,623 | 0.69 MB | Bioremediation Potential Profiling | 986 KO identifiers, 323 compounds, 12 chemical classes |
| **HADEG** | 1,168 | 0.04 MB | Hydrocarbon Aerobic Degradation | 339 KO identifiers, 71 pathways, 5 compound categories |
| **KEGG Pathways** | 871 | 0.02 MB | Xenobiotic Biodegradation | 517 KO identifiers, 20 degradation pathways |
| **ToxCSM** | 323 | 0.18 MB | Toxicity Prediction & Safety Assessment | 314 SMILES structures, 66 toxicity endpoints |

### Database-Specific Analytical Features

**BioRemPP Core Database**:
- **Scope**: Comprehensive bioremediation potential across diverse environmental contaminants
- **Coverage**: 986 unique KEGG Orthology identifiers mapped to 978 enzyme gene symbols
- **Chemical Diversity**: 323 unique compounds spanning 12 distinct chemical classes
- **Functional Annotation**: 150 different enzyme activities with detailed biochemical characterization
- **Applications**: Primary screening for bioremediation potential assessment and pathway identification

**HADEG (Hydrocarbon Aerobic Degradation Enzymes and Genes)**:
- **Scope**: Specialized focus on aerobic hydrocarbon degradation mechanisms
- **Coverage**: 323 unique genes across 339 KEGG Orthology identifiers
- **Pathway Organization**: 71 distinct metabolic pathways organized into 5 major compound categories
- **Specificity**: Expert-curated dataset for petroleum hydrocarbon and aromatic compound degradation
- **Applications**: Specialized analysis for oil spill bioremediation and industrial contamination assessment

**KEGG Pathways Database**:
- **Scope**: Xenobiotic biodegradation pathway analysis with metabolic context
- **Coverage**: 517 unique KO identifiers mapped to 513 gene symbols
- **Pathway Focus**: 20 curated degradation pathways including naphthalene, aromatic compounds, and toluene
- **Integration**: Direct linkage to KEGG metabolic pathway maps and enzymatic annotations
- **Applications**: Mechanistic understanding of biodegradation processes and metabolic network analysis

**ToxCSM (Comprehensive Small Molecule Toxicity)**:
- **Scope**: Predictive toxicology and chemical safety assessment
- **Coverage**: 314 unique SMILES molecular structures with ChEBI standardization
- **Toxicity Endpoints**: 66 distinct toxicity categories spanning nuclear receptors, genotoxicity, and organ-specific effects
- **Prediction Categories**: Environmental toxicity, stress response pathways, and bioaccumulation potential
- **Applications**: Risk assessment, safety evaluation, and environmental impact prediction

### Input Compatibility and Data Standards

All databases utilize **KEGG Orthology (KO) identifiers** as primary keys, ensuring:
- **Standardized Integration**: Consistent annotation framework across all analytical modules
- **Cross-Database Compatibility**: Seamless multi-database analysis with unified identifier space
- **International Standards Compliance**: Adherence to established bioinformatics annotation protocols
- **Version Control**: Synchronized updates with KEGG database releases for current annotations

---

## Installation

### System Requirements

- **Python**: 3.8 or higher (recommended: 3.10+)
- **Operating System**: Cross-platform (Linux, macOS, Windows)
- **Memory**: Minimum 4GB RAM (recommended: 8GB+ for large datasets)
- **Storage**: 50MB for core installation, additional space for analysis outputs

### Production Installation via PyPI

```bash
pip install biorempp
```

### Development Installation for Beta Testing

Access pre-release versions through TestPyPI:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ biorempp
```

### Development Environment Setup

For contributors and advanced users:

```bash
git clone https://github.com/DougFelipe/biorempp.git
cd biorempp
pip install -e .
```

### Conda Environment Installation

Create isolated environment with all dependencies:

```bash
# Create environment from provided configuration
conda env create -f environment.yml
conda activate biorempp

# Alternative: manual environment creation
conda create -n biorempp python=3.10 pandas numpy tqdm click
conda activate biorempp
pip install biorempp
```

### Core Dependencies

BioRemPP requires the following essential packages:

- **pandas** (≥2.0.0): High-performance data manipulation and analysis
- **numpy** (≥1.21.0): Fundamental numerical computing capabilities
- **tqdm**: Progress visualization for long-running analyses
- **click**: Advanced command-line interface framework

### Optional Dependencies for Development

```bash
pip install biorempp[dev]  # Includes development tools
pip install biorempp[testing]  # Testing framework components
```

Development dependencies include:
- **pytest**: Comprehensive testing framework
- **pytest-cov**: Code coverage analysis
- **black**: Code formatting standardization
- **pre-commit**: Git hooks for code quality
- **sphinx**: Documentation generation
- **jupyterlab**: Interactive analysis environment

---

## Command-Line Interface

### General Usage Pattern

BioRemPP implements a hierarchical command structure with logical argument grouping:

```bash
biorempp [INPUT_OPTIONS] [DATABASE_OPTIONS] [OUTPUT_OPTIONS] [VERBOSITY_OPTIONS]
```

Alternative information discovery mode:

```bash
biorempp [INFORMATION_COMMANDS] [VERBOSITY_OPTIONS]
```

### Available Commands and Options

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `--input` | filepath | Input data file (required for processing) | `--input data/sample_data.txt` |
| `--database` | choice | Single database analysis | `--database biorempp` |
| `--all-databases` | flag | Multi-database comprehensive analysis | `--all-databases` |
| `--output-dir` | directory | Custom output directory | `--output-dir results/` |
| `--list-databases` | flag | Display available databases | `--list-databases` |
| `--database-info` | choice | Detailed database information | `--database-info kegg` |
| `--quiet` | flag | Silent mode (errors only) | `--quiet` |
| `--verbose` | flag | Detailed progress information | `--verbose` |
| `--debug` | flag | Comprehensive diagnostic output | `--debug` |
| `--help` | flag | Display usage information | `--help` |

### Database Selection Options

- **biorempp**: Core bioremediation potential database with comprehensive enzymatic coverage
- **hadeg**: Specialized hydrocarbon aerobic degradation enzyme and gene analysis
- **kegg**: KEGG pathway-based xenobiotic biodegradation analysis
- **toxcsm**: Toxicity prediction and chemical safety assessment

### Verbosity Control System

BioRemPP implements a three-tier verbosity system with mutually exclusive options:

**Silent Mode (`--quiet`)**: Minimal output for automated processing
- Error messages and critical warnings only
- Final processing summaries
- Optimal for scripting and batch processing

**Verbose Mode (`--verbose`)**: Detailed progress tracking
- Real-time progress indicators with timing information
- Step-by-step processing updates
- Database connection and matching statistics
- Recommended for interactive analysis

**Debug Mode (`--debug`)**: Comprehensive diagnostic information
- All verbose mode features plus technical details
- Internal processing state information
- File logging activation with detailed timestamps
- Memory usage and performance metrics
- Essential for troubleshooting and development

---

## Input Data Format

### Standard Input Format

BioRemPP processes biological data in FASTA-like format with sample-based organization:

```text
>Sample_Identifier_1
K00031
K00032
K00090
K00042
K00052
>Sample_Identifier_2
K00031
K00033
K00091
K00043
K00053
>Sample_Identifier_3
K00034
K00035
K00092
K00044
K00054
```

### Input Format Requirements

**File Structure**:
- **Sample Headers**: Lines beginning with `>` followed by unique sample identifier
- **KO Identifiers**: KEGG Orthology identifiers (format: K##### where # = digits)
- **Line Organization**: One KO identifier per line under each sample header
- **Encoding**: UTF-8 text encoding (standard for most systems)

**Supported Identifier Formats**:
- Standard KO format: `K00001`, `K12345`
- Zero-padded variations automatically handled
- Case-insensitive processing (k00001 → K00001)

**File Format Guidelines**:
- Empty lines are automatically ignored during processing
- Comment lines starting with `#` are filtered out
- Trailing whitespace is automatically trimmed
- Duplicate identifiers within samples are deduplicated

### Example Input Data

The package includes sample data demonstrating proper format:

```bash
# View sample data structure
head src/biorempp/data/sample_data.txt

# Example content:
>Acinetobacter_baumanii_acb
K01704
K10773
K14682
K07462
K03643
```

### Data Validation

BioRemPP performs comprehensive input validation:
- **Format Verification**: Ensures proper FASTA-like structure
- **Identifier Validation**: Confirms KO identifier format compliance
- **Sample Integrity**: Verifies presence of valid identifiers under each sample
- **Encoding Check**: Validates UTF-8 encoding and character compatibility

---

## Output Data Format

### Output File Structure

BioRemPP generates structured results in delimited text format optimized for bioinformatics workflows:

```text
# Example output structure (semicolon-separated)
KO_ID;Gene_Symbol;Enzyme_Name;EC_Number;Pathway;Chemical_Class;Compound_Name;...
K00001;ADH1;Alcohol dehydrogenase;EC:1.1.1.1;Methane metabolism;Alcohols;Methanol;...
K00002;AKR1A1;Aldo-keto reductase;EC:1.1.1.2;Xenobiotic metabolism;Aldehydes;Formaldehyde;...
```

### Database-Specific Output Files

**Single Database Analysis**:
- `BioRemPP_Results.txt`: Core bioremediation potential matches
- `KEGG_Results.txt`: Pathway-based degradation analysis
- `HADEG_Results.txt`: Hydrocarbon degradation enzymes
- `ToxCSM_Results.txt`: Toxicity predictions and safety assessments

**Multi-Database Analysis**:
All four files generated simultaneously in specified output directory with comprehensive cross-referencing capabilities.

### Output Directory Structure

```
outputs/results_tables/
├── BioRemPP_Results.txt
├── KEGG_Results.txt
├── HADEG_Results.txt
├── ToxCSM_Results.txt
└── processing_summary.log
```

### Processing Statistics and Metadata

Each analysis provides comprehensive statistics:

```text
🎉 Processing completed successfully!
   📊 Results: 1,247 total matches across databases
   📁 Output Files Generated:
      - BioRemPP_Results.txt (156 matches, 89KB)
      - KEGG_Results.txt (423 matches, 134KB)
      - HADEG_Results.txt (89 matches, 34KB)
      - ToxCSM_Results.txt (579 matches, 267KB)
   ⏱️  Processing Time: 4.2 seconds
   💾 Total Output Size: 524KB
```

### Data Export Options

**Customizable Delimiters**:
- Default: Semicolon (`;`) for Excel compatibility
- Alternative: Comma (`,`), tab (`\t`), or custom separators
- Configurable through API parameters

**Output Format Features**:
- **Headers**: Descriptive column names for immediate data interpretation
- **Timestamps**: Optional timestamp inclusion for version control
- **Type Optimization**: Efficient data types for memory management
- **Cross-References**: Database-specific identifiers for integration workflows

---

## Usage Examples

### Information Discovery Commands

**List all available databases with metadata:**
```bash
biorempp --list-databases
```

**Get detailed information about specific databases:**
```bash
biorempp --database-info biorempp --verbose
biorempp --database-info kegg
biorempp --database-info hadeg
biorempp --database-info toxcsm
```

### Single Database Analysis

**Core bioremediation potential assessment:**
```bash
biorempp --input data/sample_data.txt --database biorempp
```

**Hydrocarbon degradation analysis with custom output:**
```bash
biorempp --input ko_identifiers.txt --database hadeg --output-dir hydrocarbon_analysis/
```

**KEGG pathway-based analysis with verbose feedback:**
```bash
biorempp --input biological_data.txt --database kegg --verbose
```

**Toxicity prediction and safety assessment:**
```bash
biorempp --input compound_data.txt --database toxcsm --debug
```

### Comprehensive Multi-Database Analysis

**Standard comprehensive analysis:**
```bash
biorempp --input data/sample_data.txt --all-databases
```

**Custom output directory with verbose reporting:**
```bash
biorempp --input ko_data.txt --all-databases --output-dir comprehensive_results/ --verbose
```

**Silent mode for automated processing:**
```bash
biorempp --input batch_data.txt --all-databases --output-dir automated_results/ --quiet
```

### Advanced Usage Scenarios

**High-throughput batch processing:**
```bash
#!/bin/bash
for sample in samples/*.txt; do
    output_name=$(basename "$sample" .txt)
    biorempp --input "$sample" --all-databases --output-dir "results/$output_name/" --quiet
done
```

**Pipeline integration with error handling:**
```bash
#!/bin/bash
# Preprocessing
preprocess_ko_data.sh input_raw.txt > ko_identifiers.txt

# BioRemPP Analysis
biorempp --input ko_identifiers.txt --all-databases --output-dir analysis_results/ --quiet

# Conditional post-processing
if [ $? -eq 0 ]; then
    echo "Analysis completed successfully"
    postprocess_results.sh analysis_results/
else
    echo "BioRemPP analysis failed" >&2
    exit 1
fi
```

**Memory-optimized processing for large datasets:**
```bash
biorempp --input large_dataset.txt --database biorempp --quiet --output-dir optimized_results/
```

---

## Python API

### Core Module Imports

```python
from biorempp.pipelines import (
    run_biorempp_processing_pipeline,
    run_kegg_processing_pipeline,
    run_hadeg_processing_pipeline,
    run_toxcsm_processing_pipeline,
    run_all_processing_pipelines
)
```

### Single Database Processing

**BioRemPP Core Database Analysis:**
```python
result = run_biorempp_processing_pipeline(
    input_path="data/sample_data.txt",
    output_dir="results/",
    optimize_types=True
)

print(f"Matches found: {result['matches']}")
print(f"Output file: {result['output_path']}")
print(f"Processing time: {result['processing_time']:.2f} seconds")
```

**KEGG Pathway Analysis:**
```python
result = run_kegg_processing_pipeline(
    input_path="pathway_data.txt",
    output_dir="kegg_analysis/",
    output_filename="custom_kegg_results.txt",
    sep=",",  # Custom delimiter
    add_timestamp=True
)
```

**HADEG Hydrocarbon Degradation Analysis:**
```python
result = run_hadeg_processing_pipeline(
    input_path="hydrocarbon_genes.txt",
    output_dir="hadeg_results/",
    optimize_types=False  # Disable memory optimization
)
```

**ToxCSM Toxicity Prediction:**
```python
result = run_toxcsm_processing_pipeline(
    input_path="toxicity_data.txt",
    output_dir="safety_assessment/",
    sep="\t"  # Tab-separated output
)
```

### Comprehensive Multi-Database Analysis

```python
# Process against all databases simultaneously
results = run_all_processing_pipelines(
    input_path="comprehensive_data.txt",
    output_dir="multi_database_results/",
    optimize_types=True
)

# Analyze results across databases
for database, result in results.items():
    print(f"{database.upper()}:")
    print(f"  Matches: {result['matches']}")
    print(f"  File size: {result['file_size_mb']:.2f} MB")
    print(f"  Processing time: {result['processing_time']:.2f}s")
```

### Advanced Configuration Options

```python
# Custom configuration with all parameters
result = run_biorempp_processing_pipeline(
    input_path="advanced_data.txt",
    output_dir="custom_analysis/",
    output_filename="specialized_results.csv",
    sep=",",                    # Comma-separated values
    add_timestamp=True,         # Include processing timestamp
    optimize_types=True,        # Enable memory optimization
    custom_headers=True,        # Include detailed column headers
    validate_input=True         # Comprehensive input validation
)

# Error handling and validation
if result['status'] == 'success':
    print(f"Analysis completed: {result['matches']} matches")
else:
    print(f"Analysis failed: {result['error_message']}")
```

### Integration with Data Analysis Workflows

```python
import pandas as pd
from biorempp.pipelines import run_all_processing_pipelines

# Process data and load results for analysis
results = run_all_processing_pipelines(
    input_path="metagenome_data.txt",
    output_dir="analysis_output/"
)

# Load and combine results for integrated analysis
biorempp_df = pd.read_csv(results['biorempp']['output_path'], sep=';')
kegg_df = pd.read_csv(results['kegg']['output_path'], sep=';')
hadeg_df = pd.read_csv(results['hadeg']['output_path'], sep=';')
toxcsm_df = pd.read_csv(results['toxcsm']['output_path'], sep=';')

# Perform comparative analysis
print(f"Total unique KO identifiers across databases: {
    len(set(biorempp_df['KO_ID'].tolist() +
            kegg_df['KO_ID'].tolist() +
            hadeg_df['KO_ID'].tolist()))
}")
```

---

## System Architecture

### Modular Design Pattern

BioRemPP implements a sophisticated modular architecture optimized for extensibility and maintainability:

```
biorempp/
├── 📁 pipelines/          # High-level processing orchestration
│   ├── biorempp_pipeline.py
│   ├── kegg_pipeline.py
│   ├── hadeg_pipeline.py
│   └── toxcsm_pipeline.py
├── 📁 input_processing/   # Data validation and preprocessing
│   ├── validators.py
│   └── parsers.py
├── 📁 cli/               # Command-line interface implementation
│   ├── argument_parser.py
│   └── command_handlers.py
├── 📁 commands/          # Command Pattern implementation
│   ├── base_command.py
│   ├── info_command.py
│   └── merger_commands.py
├── 📁 app/               # Application core and factory patterns
│   ├── command_factory.py
│   └── main_application.py
├── 📁 utils/             # Utility functions and helpers
│   ├── file_operations.py
│   ├── logging_config.py
│   └── path_resolution.py
└── 📁 data/              # Embedded database files
    ├── biorempp_core.csv
    ├── kegg_pathways.csv
    ├── hadeg_enzymes.csv
    └── toxcsm_profiles.csv
```

### Design Pattern Implementation

**Command Pattern**: Encapsulates CLI operations as objects, enabling:
- Flexible command composition and extension
- Standardized error handling across all operations
- Simplified testing and validation procedures
- Clean separation of concerns between interface and logic

**Template Method Pattern**: Standardizes processing pipelines while allowing:
- Database-specific customization of analysis workflows
- Consistent error handling and logging across all databases
- Uniform output formatting with database-specific content
- Extensible architecture for additional database integration

**Factory Pattern**: Manages command instantiation with:
- Intelligent command selection based on argument patterns
- Centralized validation and error handling
- Simplified addition of new command types
- Consistent interface across all operational modes

### Processing Workflow Architecture

1. **Input Validation Phase**:
   - File existence and accessibility verification
   - Format compliance checking (FASTA-like structure)
   - KO identifier validation and standardization
   - Encoding verification and character set validation

2. **Database Loading Phase**:
   - Optimized CSV parsing with type inference
   - Memory-efficient data structure initialization
   - Index creation for rapid lookup operations
   - Database integrity verification

3. **Matching and Analysis Phase**:
   - Vectorized matching operations for performance
   - Statistical analysis and result quantification
   - Cross-reference generation between databases
   - Memory optimization during large dataset processing

4. **Output Generation Phase**:
   - Structured data formatting with customizable delimiters
   - Comprehensive metadata inclusion (timestamps, statistics)
   - File writing with atomic operations for data integrity
   - Processing summary generation and display

5. **Logging and Reporting Phase**:
   - Multi-level logging with configurable verbosity
   - Performance metrics collection and reporting
   - Error tracking with diagnostic recommendations
   - User feedback with progress visualization

---

## Pipeline Integration

### Bioinformatics Workflow Integration

BioRemPP is architected for seamless integration into existing bioinformatics pipelines and automated workflows:

### Standard Pipeline Integration Patterns

**Preprocessing Integration:**
```bash
#!/bin/bash
# Example preprocessing pipeline integration
set -euo pipefail

# Input validation and preprocessing
validate_input_format.sh "$INPUT_FILE"
preprocess_ko_data.sh "$INPUT_FILE" > processed_identifiers.txt

# BioRemPP analysis with error handling
biorempp --input processed_identifiers.txt \
         --all-databases \
         --output-dir "$OUTPUT_DIR" \
         --quiet || {
    echo "ERROR: BioRemPP analysis failed" >&2
    cleanup_temp_files
    exit 1
}

# Post-processing and result integration
integrate_results.sh "$OUTPUT_DIR"
generate_summary_report.sh "$OUTPUT_DIR"
```

**High-Throughput Batch Processing:**
```bash
#!/bin/bash
# Parallel processing for multiple samples
SAMPLE_DIR="samples/"
RESULTS_DIR="batch_results/"
MAX_PARALLEL=4

find "$SAMPLE_DIR" -name "*.txt" | \
xargs -n 1 -P "$MAX_PARALLEL" -I {} bash -c '
    sample_name=$(basename "{}" .txt)
    output_dir="'$RESULTS_DIR'/$sample_name"

    biorempp --input "{}" \
             --all-databases \
             --output-dir "$output_dir" \
             --quiet

    echo "Completed: $sample_name"
'
```

### Computational Resource Optimization

**Memory Management for Large Datasets:**
- **Streaming Processing**: Input files processed in chunks to minimize memory footprint
- **Type Optimization**: Automatic data type optimization reduces memory usage by 40-60%
- **Garbage Collection**: Explicit memory cleanup during processing phases
- **Resource Monitoring**: Built-in memory and CPU usage tracking

**Performance Characteristics:**
- **Processing Speed**: 1,000-10,000 KO identifiers per second (system-dependent)
- **Memory Usage**: 200-800MB base memory + 50MB per 1,000 input identifiers
- **Scalability**: Linear scaling with input size, tested up to 1M+ identifiers
- **Disk I/O**: Optimized buffered reading/writing for large result sets

### Integration with Analysis Frameworks

**R Integration Example:**
```r
# R script for post-processing BioRemPP results
library(readr)
library(dplyr)

# Load BioRemPP results
biorempp_results <- read_delim("results/BioRemPP_Results.txt",
                              delim = ";",
                              col_types = cols())

# Perform statistical analysis
pathway_summary <- biorempp_results %>%
  group_by(Pathway) %>%
  summarise(
    enzyme_count = n(),
    unique_compounds = n_distinct(Compound_Name),
    .groups = "drop"
  )

# Generate publication-quality plots
library(ggplot2)
ggplot(pathway_summary, aes(x = enzyme_count, y = unique_compounds)) +
  geom_point(size = 3, alpha = 0.7) +
  labs(title = "Bioremediation Pathway Analysis",
       x = "Number of Enzymes",
       y = "Unique Compounds") +
  theme_minimal()
```

**Python Data Science Integration:**
```python
import pandas as pd
import numpy as np
from biorempp.pipelines import run_all_processing_pipelines

# Automated analysis pipeline
def comprehensive_bioremediation_analysis(input_file, output_base_dir):
    """
    Comprehensive bioremediation potential analysis with statistical summary.
    """
    # Run BioRemPP analysis
    results = run_all_processing_pipelines(
        input_path=input_file,
        output_dir=f"{output_base_dir}/biorempp_output/"
    )

    # Load and integrate results
    combined_results = {}
    for database, result_info in results.items():
        df = pd.read_csv(result_info['output_path'], sep=';')
        combined_results[database] = df

    # Generate integrated analysis
    analysis_summary = {
        'total_matches': sum(len(df) for df in combined_results.values()),
        'unique_ko_ids': len(set().union(*[df['KO_ID'].tolist()
                                          for df in combined_results.values()])),
        'database_coverage': {db: len(df) for db, df in combined_results.items()},
        'processing_time': sum(r['processing_time'] for r in results.values())
    }

    return combined_results, analysis_summary

# Usage example
results, summary = comprehensive_bioremediation_analysis(
    "metagenome_ko_data.txt",
    "comprehensive_analysis_output"
)
print(f"Analysis completed: {summary['total_matches']} total matches")
```

### Container and Cloud Deployment

**Docker Integration:**
```dockerfile
FROM python:3.10-slim

# Install BioRemPP and dependencies
RUN pip install biorempp

# Set up analysis environment
WORKDIR /analysis
COPY data/ ./data/
COPY scripts/ ./scripts/

# Default command for containerized analysis
CMD ["biorempp", "--input", "data/input.txt", "--all-databases", "--output-dir", "results/"]
```

**Nextflow Workflow Integration:**
```nextflow
#!/usr/bin/env nextflow

process BIOREMPP_ANALYSIS {
    publishDir "${params.outdir}/biorempp", mode: 'copy'

    input:
    path input_file

    output:
    path "biorempp_results/*"

    script:
    """
    biorempp --input ${input_file} \
             --all-databases \
             --output-dir biorempp_results/ \
             --quiet
    """
}

workflow {
    input_files = Channel.fromPath(params.input_pattern)
    BIOREMPP_ANALYSIS(input_files)
}
```

---

## Troubleshooting

### Common Error Scenarios and Solutions

#### Input File Issues

**Error: Input file not found**
```bash
❌ Error: Input file not found: data.txt

💡 Solutions:
- Verify file path is correct and accessible
- Use absolute path if relative path fails
- Check file permissions and read access
- Ensure file exists in specified location
```

**Error: Invalid input format**
```bash
❌ Error: Invalid input format detected

💡 Solutions:
- Ensure file follows FASTA-like format (>Sample_ID followed by KO identifiers)
- Verify KO identifiers follow K##### format
- Check file encoding (should be UTF-8)
- Remove special characters or non-standard formatting
- Validate sample headers begin with '>' character
```

**Error: Empty or corrupted input file**
```bash
❌ Error: No valid KO identifiers found in input file

💡 Solutions:
- Verify file contains valid KO identifiers (K00001, K12345, etc.)
- Check for empty lines or missing content
- Ensure sample sections contain identifiers under headers
- Validate file is not corrupted or truncated
```

#### Database and Processing Errors

**Error: Database selection conflicts**
```bash
❌ Error: Cannot specify both --database and --all-databases

💡 Solutions:
- Use either --database <name> for single database analysis
- Use --all-databases for comprehensive multi-database analysis
- Remove conflicting arguments from command line
```

**Error: Invalid database name**
```bash
❌ Error: Invalid database choice: 'invalid_db'
Valid options: biorempp, hadeg, kegg, toxcsm

💡 Solutions:
- Use only supported database names: biorempp, hadeg, kegg, toxcsm
- Check spelling and capitalization (case-sensitive)
- Use --list-databases to view available options
```

#### Output and Permission Issues

**Error: Output directory permissions**
```bash
❌ Error: Permission denied for output directory

💡 Solutions:
- Choose different output directory with write permissions
- Create output directory manually with appropriate permissions
- Run with elevated privileges if necessary (not recommended)
- Use home directory or user-writable location
```

**Error: Insufficient disk space**
```bash
❌ Error: Insufficient disk space for output generation

💡 Solutions:
- Free disk space in target output directory
- Choose output location with adequate space (typically 10-100MB per analysis)
- Use disk cleanup utilities to remove temporary files
- Consider using external storage or different partition
```

#### Performance and Memory Issues

**Error: Memory allocation failure**
```bash
❌ Error: Cannot allocate memory for dataset processing

💡 Solutions:
- Close unnecessary applications to free memory
- Process smaller input files or split large datasets
- Enable type optimization: use optimize_types=True in Python API
- Increase system virtual memory if possible
- Use streaming processing for very large datasets
```

### Diagnostic Tools and Commands

**System compatibility check:**
```bash
biorempp --list-databases --debug
```

**Input validation test:**
```bash
biorempp --input src/biorempp/data/sample_data.txt --database biorempp --verbose
```

**Memory usage monitoring:**
```bash
biorempp --input large_file.txt --database biorempp --debug
# Monitor output for memory usage statistics
```

### Debug Mode Information

When using `--debug` flag, BioRemPP provides comprehensive diagnostic information:

**Debug Output Structure:**
```text
biorempp --debug --input "data/sample_data.txt" --database biorempp

[BIOREMPP] Processing with BIOREMPP Database
===================================================================
🔧 [DEBUG] Verbosity level: DEBUG
🔧 [DEBUG] Target database: biorempp
🔧 [DEBUG] Display name: BioRemPP

[LOAD] Loading input data...        OK 23,653 identifiers loaded
🔧 [DEBUG] Input file processing completed
🔧 [DEBUG] File path: data/sample_data.txt
🔧 [DEBUG] Total identifiers parsed: 23,653

[CONNECT] Connecting to BIOREMPP...    OK Database available
🔧 [DEBUG] Database connection established
🔧 [DEBUG] Database type: biorempp
[PROCESS] Processing data...          #################### 100%
🔧 [DEBUG] Processing completed successfully
🔧 [DEBUG] Output file: BioRemPP_Results.txt

[SUCCESS] Processing completed successfully!
   [RESULTS] Results: 7,613 matches found
   [OUTPUT] Output: BioRemPP_Results.txt (921KB)
   [TIME] Time: 0.2 seconds
🔧 [DEBUG] ===== TECHNICAL SUMMARY =====
🔧 [DEBUG] Total processing time: 0.169 seconds
🔧 [DEBUG] Database: biorempp (BioRemPP)
🔧 [DEBUG] File size: 921KB
🔧 [DEBUG] Processing rate: 44918.8 matches/second
```

**Log File Location:**
Debug logs are automatically saved to: `outputs/logs/biorempp_YYYYMMDD_HHMMSS.log`

### Performance Optimization Guidelines

**For Large Datasets (>100,000 KO identifiers):**
- Use `--quiet` mode to reduce output overhead
- Enable type optimization in Python API
- Process in smaller batches if memory is limited
- Use SSD storage for better I/O performance

**For Automated/Production Environments:**
- Always use `--quiet` flag for cleaner log output
- Implement proper error handling in wrapper scripts
- Monitor disk space before processing
- Use absolute paths to avoid working directory issues

**For Development and Testing:**
- Use `--debug` mode for comprehensive diagnostic information
- Test with sample data first: `src/biorempp/data/sample_data.txt`
- Validate input format before large-scale processing
- Monitor memory usage patterns for optimization

### Getting Additional Support

**Documentation Resources:**
- [Complete CLI Reference](CLI_Reference.md)
- [GitHub Issues](https://github.com/DougFelipe/biorempp/issues)
- [API Documentation](https://biorempp.readthedocs.io)

**Reporting Issues:**
When reporting issues, please include:
- Complete command line used
- Input file format example (first 10-20 lines)
- Full error message output
- System information (OS, Python version, available memory)
- Debug log file if available

**Contact Information:**
- **Technical Support**: [biorempp@gmail.com](mailto:biorempp@gmail.com)
- **GitHub Repository**: [https://github.com/DougFelipe/biorempp](https://github.com/DougFelipe/biorempp)
- **Bug Reports**: [GitHub Issues](https://github.com/DougFelipe/biorempp/issues)

---

## Contributing

Contributions to BioRemPP are welcome and encouraged. The project follows established open-source contribution guidelines and maintains high standards for code quality, documentation, and testing.

### Development Environment Setup

```bash
# Clone repository
git clone https://github.com/DougFelipe/biorempp.git
cd biorempp

# Create development environment
python -m venv biorempp-dev
source biorempp-dev/bin/activate  # Linux/macOS
# or
biorempp-dev\Scripts\activate     # Windows

# Install development dependencies
pip install -e .[dev]
pip install -e .[testing]

# Install pre-commit hooks
pre-commit install
```

### Contribution Areas

**Database Extensions:**
- Addition of new KO-based databases for specialized applications
- Enhancement of existing database coverage and annotation quality
- Integration of complementary biological databases (UniProt, MetaCyc, etc.)

**CLI Enhancements:**
- New command-line options and functionality
- Improved user experience and interface design
- Enhanced output formatting and visualization options

**Performance Optimizations:**
- Algorithm improvements for faster processing
- Memory usage optimization for large datasets
- Parallel processing implementation

**Feature Development:**
- Statistical analysis modules for result interpretation
- Visualization tools for pathway and network analysis
- Integration with popular bioinformatics frameworks

**Documentation and Testing:**
- Comprehensive test suite expansion
- Documentation improvements and examples
- Tutorial development for specific use cases

### Contribution Process

1. **Fork the Repository**: Create a personal fork on GitHub
2. **Create Feature Branch**: `git checkout -b feature/new-functionality`
3. **Implement Changes**: Follow coding standards and include tests
4. **Run Quality Checks**: Ensure all tests pass and code meets standards
5. **Submit Pull Request**: Provide detailed description of changes and motivation

### Code Quality Standards

- **Python Style**: Black formatting with 88-character line limit
- **Type Hints**: Comprehensive type annotations for all public APIs
- **Documentation**: Docstrings following Google/NumPy style conventions
- **Testing**: pytest-based testing with >90% code coverage requirement
- **Linting**: flake8 compliance with project-specific configuration

### Testing Requirements

All contributions must include appropriate tests:

```bash
# Run complete test suite
pytest tests/ --cov=biorempp

# Run specific test categories
pytest tests/test_pipelines.py
pytest tests/test_cli.py
pytest tests/test_databases.py
```

For detailed contribution guidelines, code of conduct, and development workflows, see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Citation and License

### Academic Citation

If you use BioRemPP in your research, please cite:

```bibtex
@software{biorempp2025,
  title={BioRemPP: Bioremediation Potential Profile Analysis Tool},
  author={Felipe, Douglas},
  year={2025},
  url={https://github.com/DougFelipe/biorempp},
  version={0.5.0}
}
```

### License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for complete details.

### Acknowledgments

- **KEGG Database**: Kanehisa Laboratories for metabolic pathway annotations
- **Scientific Community**: Contributors and users providing feedback and improvements
- **Open Source Ecosystem**: Python scientific computing libraries enabling this work

### Project Statistics

- **Current Version**: v0.5.0 (Beta Release)
- **Development Status**: Active development with regular updates
- **Code Quality**: >90% test coverage, comprehensive type annotations
- **Performance**: Optimized for datasets up to 1M+ KO identifiers
- **Database Records**: 9,000+ curated entries across four specialized databases
- **Supported Platforms**: Cross-platform (Linux, macOS, Windows)

---

**BioRemPP**: Advancing environmental bioremediation through computational biology and systematic bioinformatics analysis.

## 🔧 Solução de Problemas

### Problemas Comuns

#### 1. Arquivo de Entrada Não Encontrado

```bash
❌ Error: Input file not found: dados.txt

💡 Solutions:
- Check if the file path is correct
- Ensure the file exists in the specified location
- Use absolute path if necessary
```

**Solução**: Verificar se o caminho do arquivo está correto.

#### 2. Formato de Entrada Inválido

```bash
❌ Error: Invalid input format

💡 Solutions:
- Ensure file is in FASTA-like format
- Check that identifiers start with '>'
- Verify file encoding is UTF-8
```

**Solução**: Converter arquivo para formato FASTA-like correto.

#### 3. Problemas de Permissão

```bash
❌ Error: Permission denied for output directory

💡 Solutions:
- Choose a different output directory
- Check write permissions for the directory
- Try running with administrator privileges
```

**Solução**: Verificar permissões de escrita no diretório de saída.


TODO: FALE MAIS SOBRE ESSA PARTE MAS NAO CITE O COMANDO E SIM A ESTRUTURA DO SEU OUTPUT
### Logs de Debug



Os logs são salvos em `outputs/logs/biorempp_YYYYMMDD.log`.

### Suporte

- 📧 **Email**: [suporte@biorempp.org](mailto:suporte@biorempp.org)
- 🐛 **Issues**: [GitHub Issues](https://github.com/DougFelipe/biorempp/issues)
- 📖 **Documentação**: [biorempp.readthedocs.io](https://biorempp.readthedocs.io)

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 🙏 Agradecimentos

- Equipe de desenvolvimento BioRemPP
- Contribuidores da comunidade
- Bancos de dados KEGG, HAdeg e ToxCSM
- Bibliotecas Python utilizadas

---

## 📊 Estatísticas do Projeto

- **Versão**: v0.5.0
- **Linhas de Código**: ~15.000
- **Módulos**: 25+
- **Testes**: 95% cobertura
- **Bancos Integrados**: 4
- **Registros Totais**: ~9.000

---

**🧬 BioRemPP - Transformando dados biológicos em insights para remediação ambiental.**
