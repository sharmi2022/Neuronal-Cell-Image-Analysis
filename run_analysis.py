"""
Run complete JC-1 analysis workflow.

This script:
1. Loads the synthetic JC-1 dataset
2. Calculates JC-1 red/green ratios
3. Normalizes values to untreated control
4. Generates group summary statistics
5. Creates a publication-style visualization

Author: Sharmistha Dutta
"""

from pathlib import Path
import sys

# Add src folder to Python path
sys.path.append(str(Path(__file__).parent / "src"))

from jc1_analysis import analyse_jc1, summarize_groups
from visualize_jc1 import plot_jc1_summary

import pandas as pd


def main():

    data_file = Path("data/sample_jc1_measurements.csv")
    results_dir = Path("results")

    results_dir.mkdir(exist_ok=True)

    print("Loading JC-1 sample dataset...")

    data = pd.read_csv(data_file)

    print("Calculating JC-1 ratios and normalization...")

    results = analyse_jc1(data)

    summary = summarize_groups(results)

    processed_file = results_dir / "jc1_processed_results.csv"
    summary_file = results_dir / "jc1_group_summary.csv"
    figure_file = results_dir / "jc1_normalized_membrane_potential.png"

    results.to_csv(processed_file, index=False)
    summary.to_csv(summary_file, index=False)

    print("Generating visualization...")

    plot_jc1_summary(
        summary_file,
        figure_file
    )

    print("\nAnalysis completed successfully.")
    print(f"Processed data: {processed_file}")
    print(f"Group summary:  {summary_file}")
    print(f"Figure:         {figure_file}")


if __name__ == "__main__":
    main()
