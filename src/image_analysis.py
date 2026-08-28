"""
Neuronal Cell Image Analysis
----------------------------
Basic fluorescence microscopy image analysis workflow.

This script:
1. Loads fluorescence microscopy images
2. Converts images to grayscale when required
3. Estimates background fluorescence
4. Performs background correction
5. Calculates mean fluorescence intensity
6. Exports quantitative measurements to CSV

Author: Sharmistha Dutta
"""

from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image


def load_image(image_path):
    """Load an image and convert it to a NumPy array."""
    image = Image.open(image_path).convert("L")
    return np.asarray(image, dtype=np.float32)


def estimate_background(image, percentile=10):
    """
    Estimate image background using a low-intensity percentile.

    Parameters
    ----------
    image : numpy.ndarray
        Grayscale fluorescence image.
    percentile : float
        Percentile used for background estimation.

    Returns
    -------
    float
        Estimated background intensity.
    """
    return np.percentile(image, percentile)


def background_correct(image, background):
    """Subtract background and prevent negative intensity values."""
    corrected = image - background
    return np.clip(corrected, 0, None)


def calculate_mean_intensity(image):
    """Calculate mean fluorescence intensity."""
    return float(np.mean(image))


def analyse_image(image_path):
    """Perform fluorescence intensity analysis on one image."""
    image = load_image(image_path)

    background = estimate_background(image)
    corrected_image = background_correct(image, background)
    mean_intensity = calculate_mean_intensity(corrected_image)

    return {
        "image": Path(image_path).name,
        "background": background,
        "mean_corrected_intensity": mean_intensity,
    }


def analyse_folder(folder_path):
    """Analyse all supported microscopy images in a folder."""

    folder = Path(folder_path)
    supported_formats = {".tif", ".tiff", ".png", ".jpg", ".jpeg"}

    results = []

    for image_path in folder.iterdir():
        if image_path.suffix.lower() in supported_formats:
            results.append(analyse_image(image_path))

    return pd.DataFrame(results)


if __name__ == "__main__":

    image_folder = Path("data/sample_images")

    results = analyse_folder(image_folder)

    output_folder = Path("results")
    output_folder.mkdir(exist_ok=True)

    results.to_csv(
        output_folder / "fluorescence_measurements.csv",
        index=False
    )

    print(results)
    print("\nAnalysis completed successfully.")
