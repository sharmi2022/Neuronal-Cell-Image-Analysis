"""
JC-1 Mitochondrial Membrane Potential Analysis
-----------------------------------------------

Reproducible workflow for quantitative analysis of JC-1 fluorescence
measurements from neuronal cell imaging experiments.

The script:
1. Loads red and green fluorescence measurements from CSV
2. Calculates the JC-1 red/green fluorescence ratio
3. Normalizes ratios relative to the untreated control
4. Summarizes biological replicates
5. Exports processed results

Author: Sharmistha Dutta
"""

from pathlib import Path

import numpy as np
import pandas as pd


def calculate_jc1_ratio(red_intensity, green_intensity):
    """Calculate the JC-1 red/green fluorescence ratio."""
    if green_intensity <= 0:
        return np.nan

    return red_intensity / green_intensity


def normalize_to_control(ratios, control_ratio):
    """Normalize JC-1 ratios relative to untreated control (100%)."""
    return (ratios / control_ratio) * 100


def analyse_jc1(data):
    """Calculate JC-1 ratios and normalize measurements to control."""

    results = data.copy()

    results["jc1_ratio"] = results.apply(
        lambda row: calculate_jc1_ratio(
            row["red_intensity"],
            row["green_intensity"]
        ),
        axis=1,
    )

    control_ratio = results.loc[
        results["group"] == "Control",
        "jc1_ratio",
    ].mean()

    results["normalized_percent"] = normalize_to_control(
        results["jc1_ratio"],
        control_ratio,
    )

    return results


def summarize_groups(results):
    """Calculate group mean, standard deviation, and sample size."""

    summary = (
        results.groupby("group", sort=False)["normalized_percent"]
        .agg(["mean", "std", "count"])
        .reset_index()
    )

    summary.columns = [
        "group",
        "mean_normalized_percent",
        "sd",
        "n",
    ]

    return summary


if __name__ == "__main__":

    input_file = Path("data/sample_jc1_measurements.csv")
    output_directory = Path("results")

    output_directory.mkdir(exist_ok=True)

    data = pd.read_csv(input_file)

    results = analyse_jc1(data)
    summary = summarize_groups(results)

    results.to_csv(
        output_directory / "jc1_processed_results.csv",
        index=False,
    )

    summary.to_csv(
        output_directory / "jc1_group_summary.csv",
        index=False,
    )

    print("\nJC-1 processed measurements:")
    print(results)

    print("\nGroup summary:")
    print(summary)

    print("\nAnalysis completed successfully.")
