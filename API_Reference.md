# BioRemPP API Reference Documentation

## Table of Contents

1. [Overview](#overview)
2. [Package Structure](#package-structure)
3. [Core API](#core-api)
4. [Pipeline Module](#pipeline-module)
5. [Input Processing Module](#input-processing-module)
6. [Application Module](#application-module)
7. [CLI Module](#cli-module)
8. [Commands Module](#commands-module)
9. [Utils Module](#utils-module)
10. [Integration Examples](#integration-examples)
11. [Error Handling](#error-handling)
12. [Best Practices](#best-practices)

## Overview

The BioRemPP (Bioremediation Potential Prediction) package provides a comprehensive Python API for analyzing biological data in the context of bioremediation processes. The API is designed with clean architecture principles, implementing dependency injection, command patterns, and modular design for enhanced maintainability and extensibility.

### API Design Principles

- **Modular Architecture**: Clear separation of concerns across functional domains
- **Dependency Injection**: Enhanced testability and configurability
- **Command Pattern**: Encapsulated operations with standardized execution flow
- **Error Resilience**: Comprehensive error handling with user-friendly messaging
- **Performance Optimization**: Memory-efficient data processing for large datasets

### Supported Data Sources

The API integrates with four specialized bioinformatics databases:

1. **BioRemPP Database**: Comprehensive bioremediation potential data
2. **KEGG Database**: Degradation pathway information
3. **HADEG Database**: Hydrocarbon degradation gene information
4. **ToxCSM Database**: Toxicity predictions and chemical properties

## Package Structure

```
biorempp/
├── __init__.py              # Package initialization and version management
├── main.py                  # CLI entry point with application orchestration
├── pipelines/               # High-level processing pipelines
├── input_processing/        # Data validation and database integration
├── app/                     # Application orchestration layer
├── cli/                     # Command-line interface components
├── commands/                # Command pattern implementations
└── utils/                   # Infrastructure utilities and support functions
```

## Core API

### Package Initialization

```python
import biorempp

# Package version access
print(biorempp.__version__)

# Silent logging setup (automatic)
# No explicit initialization required
```

**Key Features:**
- Automatic version detection using `importlib.metadata`
- Python 3.8+ compatibility with fallback handling
- Silent logging configuration for CLI applications
- Clean namespace with selective imports

### Main Entry Point

```python
from biorempp.main import main

# Run complete CLI application
main()
```

**Function:** `main()`
- **Purpose**: Primary entry point for CLI application
- **Returns**: None (designed for command-line usage)
- **Features**: Dependency injection, centralized error handling, silent logging

## Pipeline Module

The pipelines module provides high-level orchestration functions for complete data processing workflows.

### Core Pipeline Functions

```python
from biorempp.pipelines import biorempp, kegg, hadeg, toxcsm
```

#### BioRemPP Pipeline

```python
def biorempp(input_data: str, input_file: str, output_directory: str = None) -> tuple:
    """
    Complete BioRemPP database processing pipeline.

    Parameters:
    -----------
    input_data : str
        Raw input content with sample IDs and gene annotations
    input_file : str
        Input file path for reference and logging
    output_directory : str, optional
        Target directory for output files (default: current directory)

    Returns:
    --------
    tuple[pandas.DataFrame, str]
        Processed DataFrame with merged data and output file path

    Raises:
    -------
    ValidationError
        When input format is invalid
    DatabaseError
        When BioRemPP database integration fails
    """
```

#### KEGG Pipeline

```python
def kegg(input_data: str, input_file: str, output_directory: str = None) -> tuple:
    """
    KEGG pathway database processing pipeline.

    Parameters:
    -----------
    input_data : str
        Raw input content with KEGG identifiers
    input_file : str
        Input file path for reference and logging
    output_directory : str, optional
        Target directory for output files (default: current directory)

    Returns:
    --------
    tuple[pandas.DataFrame, str]
        Processed DataFrame with KEGG pathway data and output file path

    Features:
    ---------
    - Degradation pathway information integration
    - Memory optimization for large datasets
    - Comprehensive error handling with recovery suggestions
    """
```

#### HADEG Pipeline

```python
def hadeg(input_data: str, input_file: str, output_directory: str = None) -> tuple:
    """
    HADEG database processing pipeline for hydrocarbon degradation genes.

    Parameters:
    -----------
    input_data : str
        Raw input content with gene identifiers
    input_file : str
        Input file path for reference and logging
    output_directory : str, optional
        Target directory for output files (default: current directory)

    Returns:
    --------
    tuple[pandas.DataFrame, str]
        Processed DataFrame with HADEG data and output file path

    Specialization:
    --------------
    - Hydrocarbon degradation gene analysis
    - Environmental remediation focus
    - Gene function annotation and classification
    """
```

#### ToxCSM Pipeline

```python
def toxcsm(input_data: str, input_file: str, output_directory: str = None) -> tuple:
    """
    ToxCSM toxicity prediction pipeline.

    Parameters:
    -----------
    input_data : str
        Raw input content with chemical identifiers
    input_file : str
        Input file path for reference and logging
    output_directory : str, optional
        Target directory for output files (default: current directory)

    Returns:
    --------
    tuple[pandas.DataFrame, str]
        Processed DataFrame with toxicity predictions and output file path

    Capabilities:
    ------------
    - Chemical toxicity prediction
    - ADMET property analysis
    - Environmental impact assessment
    """
```

### Pipeline Usage Examples

```python
# Single database processing
from biorempp.pipelines import kegg

input_content = """
>Sample_1
K00001
K00002
>Sample_2
K00003
"""

result_df, output_path = kegg(input_content, "input.txt", "/output/directory")
print(f"Results saved to: {output_path}")
print(f"Processed {len(result_df)} records")

# Multi-database workflow
from biorempp.pipelines import biorempp, kegg, hadeg

datasets = {}
for pipeline_func in [biorempp, kegg, hadeg]:
    df, path = pipeline_func(input_content, "input.txt")
    datasets[pipeline_func.__name__] = df
```

## Input Processing Module

The input processing module handles data validation, parsing, and database integration operations.

### Main Processing Functions

```python
from biorempp.input_processing import (
    load_and_merge_input,
    validate_and_process_input
)
```

#### Complete Input Processing

```python
def load_and_merge_input(content: str, input_file: str, database_type: str = 'biorempp') -> tuple:
    """
    Complete input validation and database merge pipeline.

    Parameters:
    -----------
    content : str
        Raw input content or base64-encoded data
    input_file : str
        Input file path for reference
    database_type : str, optional
        Target database ('biorempp', 'kegg', 'hadeg', 'toxcsm')

    Returns:
    --------
    tuple[pandas.DataFrame, str]
        Merged DataFrame and error message (None if successful)

    Processing Steps:
    ----------------
    1. Base64 decoding detection and handling
    2. Input format validation
    3. Data parsing and structure verification
    4. Database-specific merging operations
    5. Memory optimization and type conversion
    """
```

#### Input Validation

```python
def validate_and_process_input(content: str, input_file: str) -> tuple:
    """
    Input validation and parsing without database integration.

    Parameters:
    -----------
    content : str
        Raw input content to validate
    input_file : str
        Input file path for error reporting

    Returns:
    --------
    tuple[pandas.DataFrame, str]
        Parsed DataFrame and error message (None if successful)

    Validation Features:
    -------------------
    - FASTA-like format validation
    - Sample ID uniqueness checking
    - Gene identifier format verification
    - Empty sample detection and handling
    """
```

### Database-Specific Merge Functions

```python
from biorempp.input_processing import (
    merge_input_with_biorempp,
    merge_input_with_kegg,
    merge_input_with_hadeg,
    merge_input_with_toxcsm
)
```

#### BioRemPP Database Integration

```python
def merge_input_with_biorempp(input_df: pandas.DataFrame) -> pandas.DataFrame:
    """
    Merge input data with BioRemPP comprehensive database.

    Parameters:
    -----------
    input_df : pandas.DataFrame
        Validated input DataFrame with Sample_ID and Gene_ID columns

    Returns:
    --------
    pandas.DataFrame
        Merged DataFrame with comprehensive bioremediation data

    Database Features:
    -----------------
    - Comprehensive gene annotation
    - Metabolic pathway information
    - Environmental context data
    - Bioremediation potential metrics
    """
```

#### KEGG Database Integration

```python
def merge_input_with_kegg(input_df: pandas.DataFrame) -> pandas.DataFrame:
    """
    Merge input data with KEGG pathway database.

    Parameters:
    -----------
    input_df : pandas.DataFrame
        Validated input DataFrame with KEGG identifiers

    Returns:
    --------
    pandas.DataFrame
        Merged DataFrame with KEGG pathway information

    KEGG Integration:
    ----------------
    - Degradation pathway mapping
    - Enzyme classification
    - Metabolic network analysis
    - Pathway enrichment data
    """
```

#### HADEG Database Integration

```python
def merge_input_with_hadeg(input_df: pandas.DataFrame) -> pandas.DataFrame:
    """
    Merge input data with HADEG hydrocarbon degradation database.

    Parameters:
    -----------
    input_df : pandas.DataFrame
        Validated input DataFrame with gene identifiers

    Returns:
    --------
    pandas.DataFrame
        Merged DataFrame with hydrocarbon degradation gene data

    HADEG Specialization:
    --------------------
    - Hydrocarbon degradation genes
    - Environmental remediation focus
    - Gene function classification
    - Substrate specificity information
    """
```

#### ToxCSM Database Integration

```python
def merge_input_with_toxcsm(input_df: pandas.DataFrame) -> pandas.DataFrame:
    """
    Merge input data with ToxCSM toxicity prediction database.

    Parameters:
    -----------
    input_df : pandas.DataFrame
        Validated input DataFrame with chemical identifiers

    Returns:
    --------
    pandas.DataFrame
        Merged DataFrame with toxicity predictions

    ToxCSM Capabilities:
    -------------------
    - Chemical toxicity prediction
    - ADMET property analysis
    - Environmental impact metrics
    - Risk assessment data
    """
```

### Memory Optimization Functions

```python
from biorempp.input_processing import (
    optimize_dtypes_biorempp,
    optimize_dtypes_kegg,
    optimize_dtypes_hadeg,
    optimize_dtypes_toxcsm
)
```

Each optimization function reduces memory usage through categorical data types and efficient storage formats:

```python
def optimize_dtypes_biorempp(df: pandas.DataFrame) -> pandas.DataFrame:
    """
    Optimize DataFrame memory usage for BioRemPP data.

    Optimization Strategies:
    -----------------------
    - Categorical data types for repeated values
    - Efficient numeric type selection
    - String interning for common identifiers
    - Memory usage reduction by 40-60%
    """
```

## Application Module

The application module provides high-level orchestration and factory components.

### Application Orchestrator

```python
from biorempp.app import BioRemPPApplication

class BioRemPPApplication:
    """
    Main application orchestrator implementing clean architecture principles.

    Features:
    ---------
    - Dependency injection for enhanced testability
    - Centralized error handling with user-friendly messages
    - Command pattern implementation for operation management
    - Professional user feedback and progress indication
    """

    def __init__(self):
        """Initialize application with dependency injection."""

    def run(self) -> None:
        """
        Execute complete application workflow.

        Execution Flow:
        --------------
        1. Argument parsing and validation
        2. Command factory instantiation
        3. Command execution with error handling
        4. Result presentation and user feedback
        """
```

### Command Factory

```python
from biorempp.app import CommandFactory

class CommandFactory:
    """
    Factory pattern implementation for command creation and routing.

    Supported Operations:
    --------------------
    - Database merger commands (single and multi-database)
    - Information display commands
    - Help and documentation access
    """

    @staticmethod
    def create_command(parsed_args) -> BaseCommand:
        """
        Create appropriate command instance based on CLI arguments.

        Parameters:
        -----------
        parsed_args : argparse.Namespace
            Parsed command-line arguments

        Returns:
        --------
        BaseCommand
            Configured command instance ready for execution
        """
```

## CLI Module

The CLI module provides command-line interface components with modern design principles.

### Argument Parser

```python
from biorempp.cli import BioRemPPArgumentParser

class BioRemPPArgumentParser:
    """
    Comprehensive argument parsing and validation engine.

    Supported Arguments:
    -------------------
    - Input file specifications
    - Database selection (single or multiple)
    - Output directory configuration
    - Information and help commands
    - Verbosity and logging control
    """

    def __init__(self):
        """Initialize argument parser with complete command structure."""

    def parse_args(self, args=None) -> argparse.Namespace:
        """
        Parse and validate command-line arguments.

        Returns:
        --------
        argparse.Namespace
            Validated argument namespace with type checking
        """
```

### Output Formatter

```python
from biorempp.cli import OutputFormatter

class OutputFormatter:
    """
    Result presentation and user feedback system.

    Formatting Features:
    -------------------
    - Structured result displays
    - Progress indicators for long operations
    - Error reporting with actionable guidance
    - Professional CLI design patterns
    """

    def format_results(self, results: dict) -> str:
        """
        Format processing results for user presentation.

        Parameters:
        -----------
        results : dict
            Processing results with metadata

        Returns:
        --------
        str
            Formatted output string for display
        """
```

## Commands Module

The commands module implements the Command Pattern architecture for operation encapsulation.

### Base Command

```python
from biorempp.commands import BaseCommand

class BaseCommand(ABC):
    """
    Abstract foundation implementing Template Method pattern.

    Template Method Flow:
    --------------------
    1. Input validation (file existence, permissions)
    2. Command-specific validation
    3. Command execution with error handling
    4. Result formatting and user feedback
    """

    @abstractmethod
    def run(self, parsed_args) -> dict:
        """
        Execute command with standardized flow.

        Parameters:
        -----------
        parsed_args : argparse.Namespace
            Validated command-line arguments

        Returns:
        --------
        dict
            Execution results with metadata
        """
```

### Database Merger Commands

```python
from biorempp.commands import DatabaseMergerCommand, AllDatabasesMergerCommand

class DatabaseMergerCommand(BaseCommand):
    """
    Single database processing command implementation.

    Supported Databases:
    -------------------
    - biorempp: Comprehensive bioremediation database
    - kegg: KEGG pathway database
    - hadeg: Hydrocarbon degradation gene database
    - toxcsm: Toxicity prediction database
    """

class AllDatabasesMergerCommand(BaseCommand):
    """
    Multi-database processing command for comprehensive analysis.

    Processing Features:
    -------------------
    - Parallel database processing
    - Consolidated result reporting
    - Cross-database correlation analysis
    - Memory-efficient large dataset handling
    """
```

### Information Command

```python
from biorempp.commands import InfoCommand

class InfoCommand(BaseCommand):
    """
    Information display and help functionality.

    Information Types:
    -----------------
    - Available databases and descriptions
    - System configuration and requirements
    - Usage examples and best practices
    - Version and dependency information
    """
```

## Utils Module

The utils module provides comprehensive infrastructure components for the entire package.

### I/O Utilities

```python
from biorempp.utils import (
    save_dataframe_output,
    get_project_root,
    resolve_output_path,
    generate_timestamped_filename
)
```

#### File Output Management

```python
def save_dataframe_output(df: pandas.DataFrame, base_filename: str,
                         suffix: str = None, output_dir: str = None) -> str:
    """
    Save DataFrame with standardized naming and format.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame to save
    base_filename : str
        Base name for output file
    suffix : str, optional
        Additional suffix for filename
    output_dir : str, optional
        Target directory (default: current directory)

    Returns:
    --------
    str
        Full path to saved file

    Features:
    ---------
    - Automatic timestamp generation
    - Directory creation if needed
    - Standardized CSV format with proper encoding
    - Conflict resolution for existing files
    """
```

#### Path Management

```python
def get_project_root() -> Path:
    """
    Locate project root directory automatically.

    Detection Strategy:
    ------------------
    - Search for marker files (pyproject.toml, setup.py)
    - Traverse directory hierarchy upward
    - Fallback to current directory if not found
    """

def resolve_output_path(base_path: str, output_dir: str = None) -> Path:
    """
    Resolve and validate output path with directory creation.

    Path Resolution:
    ---------------
    - Absolute path handling
    - Relative path resolution from project root
    - Directory creation with proper permissions
    - Path validation and error handling
    """
```

### Logging Configuration

```python
from biorempp.utils import (
    get_logger,
    setup_logging,
    configure_from_env,
    setup_silent_logging
)
```

#### Standard Logging

```python
def get_logger(name: str) -> logging.Logger:
    """
    Get configured logger instance for module.

    Logger Features:
    ---------------
    - File-based technical logging
    - Configurable log levels
    - Structured log formatting
    - Thread-safe operations
    """

def setup_logging(level: str = "INFO", log_file: str = None) -> None:
    """
    Configure comprehensive logging system.

    Configuration Options:
    ---------------------
    - Console and file output
    - Configurable log levels
    - Custom formatting patterns
    - Log rotation and archival
    """
```

#### Silent Logging for CLI

```python
def setup_silent_logging() -> None:
    """
    Configure silent logging for CLI applications.

    Silent Features:
    ---------------
    - Suppress console output
    - File-based technical logging only
    - User-friendly message display
    - Error logging with context
    """

def show_user_message(message: str, level: str = "info") -> None:
    """
    Display user-friendly messages without logging noise.

    Message Types:
    -------------
    - info: General information
    - warning: Important notices
    - error: Error conditions
    - success: Operation completion
    """
```

### Error Handling

```python
from biorempp.utils import EnhancedErrorHandler, get_error_handler
```

#### Enhanced Error Management

```python
class EnhancedErrorHandler:
    """
    Professional error handling with user-friendly messaging.

    Error Handling Features:
    -----------------------
    - Contextual error analysis
    - User-friendly error translation
    - Recovery suggestion generation
    - Technical detail logging
    """

    def handle_error(self, error: Exception, context: dict = None) -> str:
        """
        Process error with context and generate user-friendly message.

        Parameters:
        -----------
        error : Exception
            Original exception to handle
        context : dict, optional
            Additional context for error analysis

        Returns:
        --------
        str
            User-friendly error message with guidance
        """
```

### User Feedback Systems

```python
from biorempp.utils import (
    EnhancedFeedbackManager,
    UserFeedbackManager,
    ProgressIndicator,
    get_user_feedback,
    set_verbosity
)
```

#### Enhanced Feedback Management

```python
class EnhancedFeedbackManager:
    """
    Advanced user interaction and progress indication system.

    Feedback Features:
    -----------------
    - Visual progress tracking
    - Operation status indication
    - Performance metrics display
    - Memory usage monitoring
    """

    def show_progress(self, message: str, current: int = None,
                     total: int = None) -> None:
        """
        Display progress information with visual indicators.

        Progress Types:
        --------------
        - Indeterminate: Spinning indicator for unknown duration
        - Determinate: Progress bar with percentage completion
        - Status: Simple status message display
        """
```

#### Basic User Feedback

```python
class UserFeedbackManager:
    """
    Basic user feedback and progress indication.

    Core Features:
    -------------
    - Simple progress indicators
    - Verbosity level control
    - Basic status reporting
    - Error message display
    """

class ProgressIndicator:
    """
    Visual progress indicator for long-running operations.

    Indicator Types:
    ---------------
    - Spinner: Rotating animation for indeterminate progress
    - Bar: Progress bar with completion percentage
    - Dots: Animated dots for activity indication
    """
```

## Integration Examples

### Basic API Usage

```python
# High-level pipeline usage
from biorempp.pipelines import biorempp, kegg

# Process single sample
input_data = """
>Sample_001
K00001
K00002
K00003
"""

# BioRemPP analysis
biorempp_df, output_path = biorempp(input_data, "sample.txt")
print(f"BioRemPP results: {len(biorempp_df)} genes analyzed")

# KEGG pathway analysis
kegg_df, kegg_path = kegg(input_data, "sample.txt")
print(f"KEGG results: {len(kegg_df)} pathways identified")
```

### Advanced Workflow Integration

```python
# Multi-database comprehensive analysis
from biorempp.input_processing import validate_and_process_input
from biorempp.pipelines import biorempp, kegg, hadeg, toxcsm
from biorempp.utils import save_dataframe_output, get_logger

# Setup logging
logger = get_logger("analysis_workflow")

# Input validation
input_df, error = validate_and_process_input(input_data, "input.txt")
if error:
    logger.error(f"Input validation failed: {error}")
    raise ValueError(error)

# Multi-database processing
databases = [biorempp, kegg, hadeg, toxcsm]
results = {}

for db_func in databases:
    try:
        df, path = db_func(input_data, "input.txt", "output/")
        results[db_func.__name__] = {
            'dataframe': df,
            'output_path': path,
            'gene_count': len(df['Gene_ID'].unique()),
            'sample_count': len(df['Sample_ID'].unique())
        }
        logger.info(f"Completed {db_func.__name__} analysis: {len(df)} records")
    except Exception as e:
        logger.error(f"Failed {db_func.__name__} analysis: {e}")
        results[db_func.__name__] = {'error': str(e)}

# Generate summary report
summary_data = []
for db_name, result in results.items():
    if 'error' not in result:
        summary_data.append({
            'Database': db_name,
            'Records': len(result['dataframe']),
            'Genes': result['gene_count'],
            'Samples': result['sample_count'],
            'Output_File': result['output_path']
        })

summary_df = pd.DataFrame(summary_data)
summary_path = save_dataframe_output(summary_df, "analysis_summary")
print(f"Analysis summary saved to: {summary_path}")
```

### Custom Error Handling

```python
from biorempp.utils import EnhancedErrorHandler, EnhancedFeedbackManager
from biorempp.input_processing import load_and_merge_input

# Initialize components
error_handler = EnhancedErrorHandler()
feedback = EnhancedFeedbackManager()

try:
    feedback.show_progress("Processing input data...")

    result_df, error = load_and_merge_input(
        content=input_data,
        input_file="data.txt",
        database_type="biorempp"
    )

    if error:
        user_message = error_handler.handle_error(
            ValueError(error),
            context={'input_file': 'data.txt', 'database': 'biorempp'}
        )
        feedback.show_error(user_message)
    else:
        feedback.show_success(f"Successfully processed {len(result_df)} records")

except Exception as e:
    user_message = error_handler.handle_error(e)
    feedback.show_error(user_message)
```

### Memory Optimization for Large Datasets

```python
from biorempp.input_processing import (
    merge_input_with_biorempp,
    optimize_dtypes_biorempp
)
from biorempp.utils import get_logger

logger = get_logger("memory_optimization")

# Process large dataset with memory optimization
logger.info("Starting large dataset processing")
initial_memory = result_df.memory_usage(deep=True).sum()

# Apply memory optimization
optimized_df = optimize_dtypes_biorempp(result_df)
final_memory = optimized_df.memory_usage(deep=True).sum()

reduction = (initial_memory - final_memory) / initial_memory * 100
logger.info(f"Memory usage reduced by {reduction:.1f}%")
logger.info(f"Initial: {initial_memory / 1024**2:.1f} MB")
logger.info(f"Final: {final_memory / 1024**2:.1f} MB")
```

## Error Handling

### Exception Hierarchy

```python
# Input processing errors
ValidationError: Input format validation failures
DatabaseError: Database integration failures
FileError: File I/O and permission issues

# Application errors
ConfigurationError: Configuration and setup issues
CommandError: Command execution failures
DependencyError: Missing dependency issues
```

### Error Context and Recovery

```python
from biorempp.utils import EnhancedErrorHandler

error_handler = EnhancedErrorHandler()

# Error handling with context
try:
    result = some_operation()
except Exception as e:
    context = {
        'operation': 'database_merge',
        'input_file': 'data.txt',
        'database': 'biorempp',
        'stage': 'validation'
    }

    user_message = error_handler.handle_error(e, context)
    print(user_message)  # User-friendly error with recovery suggestions
```

### Common Error Patterns

```python
# Input validation errors
try:
    df, error = validate_and_process_input(content, filename)
    if error:
        print(f"Validation failed: {error}")
        # Error contains specific guidance for correction
except Exception as e:
    print(f"Unexpected error: {e}")

# Database integration errors
try:
    merged_df = merge_input_with_kegg(input_df)
except DatabaseError as e:
    print(f"Database integration failed: {e}")
    # Automatic retry logic or fallback suggestions
```

## Best Practices

### Performance Optimization

1. **Memory Management**
   ```python
   # Use memory optimization for large datasets
   optimized_df = optimize_dtypes_biorempp(large_dataframe)

   # Process data in chunks for very large files
   chunk_size = 10000
   for chunk in pd.read_csv(large_file, chunksize=chunk_size):
       process_chunk(chunk)
   ```

2. **Efficient Database Operations**
   ```python
   # Pre-validate input before expensive database operations
   input_df, error = validate_and_process_input(content, filename)
   if not error:
       result_df = merge_input_with_biorempp(input_df)
   ```

### Error Resilience

1. **Comprehensive Error Handling**
   ```python
   from biorempp.utils import EnhancedErrorHandler

   error_handler = EnhancedErrorHandler()

   try:
       # Operations that might fail
       result = complex_operation()
   except Exception as e:
       user_message = error_handler.handle_error(e, context)
       # Handle gracefully with user guidance
   ```

2. **Input Validation**
   ```python
   # Always validate input before processing
   df, error = validate_and_process_input(content, filename)
   if error:
       # Handle validation error with specific guidance
       return error_response(error)
   ```

### Logging and Monitoring

1. **Structured Logging**
   ```python
   from biorempp.utils import get_logger

   logger = get_logger("my_module")
   logger.info("Operation started", extra={'context': 'analysis'})
   ```

2. **User Feedback**
   ```python
   from biorempp.utils import EnhancedFeedbackManager

   feedback = EnhancedFeedbackManager()
   feedback.show_progress("Processing large dataset...")
   ```

### API Integration

1. **High-Level Pipeline Usage**
   ```python
   # Use pipeline functions for complete workflows
   from biorempp.pipelines import biorempp

   result_df, output_path = biorempp(input_data, "file.txt")
   ```

2. **Low-Level Component Usage**
   ```python
   # Use individual components for custom workflows
   from biorempp.input_processing import validate_and_process_input
   from biorempp.input_processing import merge_input_with_biorempp

   # Custom validation and processing
   df, error = validate_and_process_input(content, filename)
   if not error:
       merged_df = merge_input_with_biorempp(df)
   ```

### Testing and Development

1. **Unit Testing with Dependency Injection**
   ```python
   # Components are designed for testability
   from biorempp.app import CommandFactory

   # Mock dependencies for testing
   mock_args = create_mock_args()
   command = CommandFactory.create_command(mock_args)
   ```

2. **Integration Testing**
   ```python
   # Test complete workflows
   from biorempp.pipelines import kegg

   test_input = create_test_input()
   result_df, output_path = kegg(test_input, "test.txt")
   assert len(result_df) > 0
   assert output_path.exists()
   ```

---

*This API reference provides comprehensive documentation for integrating BioRemPP into bioinformatics workflows. For additional examples and advanced usage patterns, refer to the examples directory and test files in the package repository.*
