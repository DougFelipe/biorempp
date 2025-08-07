"""
Test refactored SampleCompoundInteractionProcessor.
"""

import pandas as pd

from biorempp.analysis.interaction_sample_compound_ import SampleCompoundInteraction


def test_refactored_functionality():
    """Test the refactored functionality."""
    print("Testing refactored SampleCompoundInteractionProcessor...")

    # Create test data with the expected structure
    test_data = pd.DataFrame(
        {
            "sample": [
                "Sample1",
                "Sample1",
                "Sample1",
                "Sample2",
                "Sample2",
                "Sample3",
            ],
            "compoundname": [
                "Ethanol",
                "Methanol",
                "Ethanol",
                "Ethanol",
                "Benzene",
                "Methanol",
            ],
            "compoundclass": [
                "Alcohols",
                "Alcohols",
                "Alcohols",
                "Alcohols",
                "Aromatics",
                "Alcohols",
            ],
            "ko": ["K00001", "K00002", "K00001", "K00001", "K00003", "K00002"],
        }
    )

    print("Input data:")
    print(test_data)
    print()

    # Initialize processor
    processor = SampleCompoundInteraction()

    print(f"Processor: {processor.name}")
    print(f"Required columns: {processor.required_columns}")
    print(f"Output columns: {processor.output_columns}")
    print()

    # Test process method
    result = processor.process(test_data, save_file=False)

    print("Processing completed!")
    print(f"Result shape: {result.shape}")
    print(f"Result columns: {list(result.columns)}")
    print()
    print("Sample-compound interactions found:")
    print(result)

    print("\nTest completed successfully!")


if __name__ == "__main__":
    test_refactored_functionality()
