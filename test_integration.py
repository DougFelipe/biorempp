"""
Simple integration test for SampleCompoundInteractionProcessor.
"""

import tempfile

import pandas as pd

from biorempp.analysis.interaction_sample_compound_ import SampleCompoundInteraction


def test_basic_functionality():
    """Test basic functionality of the processor."""
    print("Testing SampleCompoundInteractionProcessor...")

    # Create test data
    test_data = pd.DataFrame(
        {
            "sample": ["Sample1", "Sample1", "Sample2", "Sample2", "Sample3"],
            "compoundclass": [
                "Alkaloids",
                "Flavonoids",
                "Alkaloids",
                "Terpenes",
                "Flavonoids",
            ],
            "protein": ["P1", "P2", "P3", "P4", "P5"],
            "ko": ["K00001", "K00002", "K00001", "K00003", "K00002"],
        }
    )

    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Initialize processor
        processor = SampleCompoundInteraction(
            output_dir=temp_dir, output_file="test_compounds.txt"
        )

        print(f"Processor initialized: {processor.name}")
        print(f"Required columns: {processor.required_columns}")
        print(f"Output columns: {processor.output_columns}")

        # Test process method
        result = processor.process(test_data, save_file=True)

        print(f"Processing completed. Result shape: {result.shape}")
        print(f"Result columns: {list(result.columns)}")
        print(f"Unique compound classes found: {len(result)}")
        print("Compound classes:")
        for _, row in result.iterrows():
            print(f"  - {row['compound_class']}")

        # Test legacy method
        legacy_result = processor.extract_compound_classes(test_data)
        print(f"Legacy method result: {legacy_result}")

    print("Test completed successfully!")


if __name__ == "__main__":
    test_basic_functionality()
