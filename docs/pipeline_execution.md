# Pipeline Execution Documentation

## Post-Merge Analysis Integration

This document describes the automated analytical routines in the BioRemPP post-merge processing pipeline.

### Automated Analytical Methods

The BioRemPP pipeline includes automated analytical methods specifically designed for KEGG data processing:

#### 1. `analyze_ko_per_pathway_per_sample`
- **Purpose**: Counts KO (KEGG Orthology) occurrences per pathway per sample
- **Input**: KEGG DataFrame with 'sample', 'pathname', 'ko' columns
- **Output**: Tab-separated TXT file with KO counts per pathway per sample
- **Location**: `outputs/analysis_results/ko_per_pathway_per_sample_YYYYMMDD_HHMMSS.txt`

#### 2. `analyze_ko_per_sample_for_pathway` (Automatic Top Pathways)
- **Purpose**: Counts KO occurrences per sample for the top 3 most frequent pathways
- **Input**: KEGG DataFrame automatically processes top pathways
- **Output**: Tab-separated TXT files for each top pathway
- **Location**: `outputs/analysis_results/ko_per_sample_for_{pathway_name}_YYYYMMDD_HHMMSS.txt`

### Pipeline Integration

These methods are automatically executed when:
1. Pipeline type is set to "kegg"
2. Post-merge analysis is enabled (default behavior)
3. KEGG data is successfully processed
4. Required columns ('sample', 'pathname', 'ko') are present in the data

### Command Line Interface

#### Basic Usage
```bash
python main.py --input data.txt --pipeline-type kegg
```

#### Disable Post-Merge Analysis
```bash
python main.py --input data.txt --pipeline-type kegg --disable-post-merge
```

### Automatic Pathway Selection

The pipeline automatically:
- Identifies the top 3 most frequent pathways in the dataset
- Generates detailed KO analysis for each of these pathways
- Sanitizes pathway names for filesystem compatibility
- Creates separate output files for each pathway analysis

### Output Structure

The analysis results are saved in the following structure:
```
outputs/
└── analysis_results/
    ├── ko_counts_YYYYMMDD_HHMMSS.txt
    ├── ko_per_pathway_per_sample_YYYYMMDD_HHMMSS.txt
    ├── ko_per_sample_for_{top_pathway_1}_YYYYMMDD_HHMMSS.txt
    ├── ko_per_sample_for_{top_pathway_2}_YYYYMMDD_HHMMSS.txt
    └── ko_per_sample_for_{top_pathway_3}_YYYYMMDD_HHMMSS.txt
```

### File Formats

All output files use tab-separated format (.txt) for easy integration with external analysis tools and visualization software.

### Error Handling

The pipeline includes comprehensive error handling:
- Missing required columns in KEGG data
- Invalid pathway names (automatically sanitized)
- File I/O errors
- Empty datasets
- Pathway identification failures

### Integration Points

1. **Processing Pipeline**: `src/biorempp/pipelines/processing_post_merge.py`
   - Automatically detects KEGG data
   - Executes all analytical methods automatically
   - Identifies top 3 pathways for detailed analysis
   - Handles file saving and error logging

2. **Main Entry Point**: `src/biorempp/main.py`
   - Triggers post-merge analysis automatically
   - Provides user feedback on analysis completion
   - Integrates with existing pipeline workflow

3. **Analytical Core**: `src/biorempp/analysis/gene_pathway_analysis_processing.py`
   - Contains the analytical logic
   - Handles data validation and processing
   - Generates formatted output DataFrames
   - Supports automatic pathway identification

### Automatic Features

- **Top Pathway Detection**: Automatically identifies the 3 most frequent pathways
- **Filename Sanitization**: Pathway names are cleaned for filesystem compatibility
- **Timestamp Integration**: All files include timestamp for versioning
- **Comprehensive Logging**: Detailed progress and error reporting

### Dependencies

- pandas >= 1.0.0
- Standard Python logging
- BioRemPP core utilities

### Future Enhancements

- Support for configurable number of top pathways
- Additional pathway-specific analyses
- Integration with external visualization tools
- Batch processing for multiple pathways
- Statistical summaries and quality metrics
