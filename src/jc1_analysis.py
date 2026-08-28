"""
JC-1 Mitochondrial Membrane Potential Analysis
----------------------------------------------

Quantitative analysis of JC-1 fluorescence measurements from
neuronal cell imaging experiments.

JC-1 mitochondrial membrane potential is represented using the
ratio of red (JC-1 aggregates) to green (JC-1 monomers)
fluorescence.

Author: Sharmistha Dutta
"""

import pandas as pd
import numpy as np


def background_correct(signal, background):
    """Subtract background fluorescence from measured intensity."""
    corrected = signal - background
    return np.maximum(corrected, 0)


def calculate_jc1_ratio(red_intensity, green_intensity):
    """
    Calculate JC-1 red/green fluorescence ratio.

    A higher red/green ratio is generally associated with
    greater mitochondrial membrane polarization.
    """
    if green_intensity <= 0:
        return np.nan

    return red_intensity / green_intensity


def normalize_to_control(ratios, control_ratio):
    """
    Normalize JC-1 ratios relative to the untreated control.

    Untreated control is expressed as 100%.
    """
    return (ratios / control_ratio) * 100


def analyse_jc1_dataframe(data):
    """
    Calculate JC-1 ratios for fluorescence measurements.

    Required columns:
        group
        red_intensity
        green_intensity
    """

    results = data.copy()

    results["jc1_ratio"] = results.apply(
        lambda row: calculate_jc1_ratio(
            row["red_intensity"],
            row["green_intensity"]
        ),
        axis=1
    )

    return results


if __name__ == "__main__":

    # Example data only.
    # Replace with measurements obtained from image analysis.
    example_data = pd.DataFrame({
        "group": [
            "Control",
            "Oxidative_stress",
            "Positive_control",
            "Treatment_A",
            "Treatment_B"
        ],
        "red_intensity": [250, 80, 190, 175, 150],
        "green_intensity": [100, 180, 120, 125, 135]
    })

    results = analyse_jc1_dataframe(example_data)

    control_ratio = results.loc[
        results["group"] == "Control",
        "jc1_ratio"
    ].mean()

    results["normalized_percent"] = normalize_to_control(
        results["jc1_ratio"],
        control_ratio
    )

    print(results)
