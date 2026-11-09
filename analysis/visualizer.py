
import os
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


BASE_FOLDER = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

CHART_FOLDER = os.path.join(
    BASE_FOLDER,
    "static",
    "generated_charts"
)

os.makedirs(CHART_FOLDER, exist_ok=True)


def generate_charts(df):

    charts = []

    # Remove previous generated charts
    for filename in os.listdir(CHART_FOLDER):

        if filename.endswith(".png"):
            file_path = os.path.join(CHART_FOLDER, filename)
            os.remove(file_path)

    # Identify column types
    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()


    # 1. HISTOGRAMS
    for index, column in enumerate(numeric_columns[:3]):

        values = df[column].dropna()

        if values.empty:
            continue

        plt.figure(figsize=(8, 5))

        plt.hist(
            values,
            bins=15,
            edgecolor="black"
        )

        plt.title(f"Distribution of {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.grid(axis="y", alpha=0.3)

        filename = f"histogram_{index + 1}.png"

        plt.tight_layout()

        plt.savefig(
            os.path.join(CHART_FOLDER, filename),
            dpi=120
        )

        plt.close()

        charts.append({
            "title": f"Histogram - {column}",
            "filename": filename
        })


    # 2. BAR CHARTS
    for index, column in enumerate(categorical_columns[:3]):

        values = df[column].dropna().astype(str)

        if values.empty:
            continue

        counts = values.value_counts().head(10)

        plt.figure(figsize=(8, 5))

        plt.bar(
            counts.index,
            counts.values
        )

        plt.title(f"Category Comparison - {column}")
        plt.xlabel(column)
        plt.ylabel("Count")
        plt.xticks(rotation=30, ha="right")
        plt.grid(axis="y", alpha=0.3)

        filename = f"bar_chart_{index + 1}.png"

        plt.tight_layout()

        plt.savefig(
            os.path.join(CHART_FOLDER, filename),
            dpi=120
        )

        plt.close()

        charts.append({
            "title": f"Bar Chart - {column}",
            "filename": filename
        })


    # 3. CORRELATION HEATMAP
    if len(numeric_columns) >= 2:

        correlation = df[numeric_columns].corr()

        plt.figure(figsize=(8, 6))

        image = plt.imshow(
            correlation,
            cmap="coolwarm",
            vmin=-1,
            vmax=1
        )

        plt.colorbar(image)

        plt.xticks(
            range(len(numeric_columns)),
            numeric_columns,
            rotation=45,
            ha="right"
        )

        plt.yticks(
            range(len(numeric_columns)),
            numeric_columns
        )

        plt.title("Correlation Heatmap")

        plt.tight_layout()

        filename = "correlation_heatmap.png"

        plt.savefig(
            os.path.join(CHART_FOLDER, filename),
            dpi=120
        )

        plt.close()

        charts.append({
            "title": "Correlation Heatmap",
            "filename": filename
        })


    return charts
