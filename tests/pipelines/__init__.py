"""
Comprehensive test suite for BioRemPP processing pipelines.

This module contains extensive tests for all pipeline functions defined in
biorempp.pipelines.input_processing, covering the complete workflow from
input validation to output generation across all supported databases.

Test Coverage:
    - BioRemPP database processing pipeline
    - KEGG degradation pathways processing pipeline  
    - HADEG hydrocarbon degradation processing pipeline
    - ToxCSM toxicity prediction processing pipeline

The test suite validates:
    - Successful processing scenarios (happy path)
    - Error handling and edge cases
    - Parameter validation and customization
    - File I/O operations and path resolution
    - Database integration and merging logic
    - Output format consistency across pipelines
    - Memory optimization and performance features

Each pipeline is tested for:
    - Default parameter behavior
    - Custom configuration options
    - File not found error handling
    - Processing error scenarios
    - Empty result handling
    - Integration with underlying processing modules

Dependencies:
    - pytest for test framework
    - pandas for data structure testing
    - unittest.mock for mocking external dependencies
    - conftest.py fixtures for test data setup
"""
