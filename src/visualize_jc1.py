"""
JC-1 Data Visualization
-----------------------

Generates a publication-style bar plot from the JC-1 group summary
produced by jc1_analysis.py.

Input:
    results/jc1_group_summary.csv

Output:
    results/jc1_normalized_membrane_potential.png

Author: Sharmistha Dutta
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_jc1_summary(summary_file, output_file):
    """Create a bar plot of normalized JC-1 membrane potential."""

    data = pd.read_csv(summary_file)

    groups = data["group"]
    means = data["mean_normalized_percent"]
    errors = data["sd"]

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(
        groups,
        means,
        yerr=errors,
        capsize=5
    )

    ax.set_ylabel("Normalized JC-1 red/green ratio (%)")
    ax.set_xlabel("Experimental group")

    ax.set_title(
        "Relative Mitochondrial Membrane Potential"
    )

    ax.axhline(
        y=100,
        linestyle="--",
        linewidth=1,
        label="Untreated control"
    )

    ax.tick_params(
        axis="x",
        rotation=25
    )

    ax.legend()

    fig.tight_layout()

    fig.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)


if __name__ == "__main__":

    summary_file = Path(
        "results/jc1_group_summary.csv"
    )

    output_file = Path(
        "results/jc1_normalized_membrane_potential.png"
    )

    plot_jc1_summary(
        summary_file,
        output_file
    )

    print(
        f"Visualization saved to: {output_file}"
    )
