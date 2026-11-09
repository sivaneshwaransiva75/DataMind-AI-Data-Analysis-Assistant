
import pandas as pd


def generate_insights(df):

    insights = []
    total_rows = len(df)
    total_columns = len(df.columns)

    insights.append({
        "title": "Dataset Overview",
        "message": f"Your dataset contains {total_rows} records and {total_columns} features.",
        "type": "info"
    })

    total_missing = int(df.isnull().sum().sum())

    if total_missing > 0:
        insights.append({
            "title": "Missing Values",
            "message": f"Your dataset contains {total_missing} missing values. Consider cleaning them.",
            "type": "warning"
        })
    else:
        insights.append({
            "title": "Data Quality",
            "message": "No missing values were detected.",
            "type": "success"
        })

    total_duplicates = int(df.duplicated().sum())

    if total_duplicates > 0:
        insights.append({
            "title": "Duplicate Records",
            "message": f"{total_duplicates} duplicate records were found.",
            "type": "warning"
        })
    else:
        insights.append({
            "title": "Duplicate Records",
            "message": "No duplicate records were detected.",
            "type": "success"
        })

    numeric_columns = df.select_dtypes(
        include=["number"]
    ).columns

    for column in numeric_columns[:5]:

        values = df[column].dropna()

        if len(values) == 0:
            continue

        average = float(values.mean())
        highest = float(values.max())
        lowest = float(values.min())

        insights.append({
            "title": str(column) + " Analysis",
            "message": (
                f"Average: {average:.2f} | "
                f"Highest: {highest:.2f} | "
                f"Lowest: {lowest:.2f}"
            ),
            "type": "info"
        })

    categorical_columns = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns

    for column in categorical_columns[:3]:

        values = df[column].dropna().astype(str)

        if values.empty:
            continue

        most_common = values.value_counts().index[0]

        frequency = int(
            values.value_counts().iloc[0]
        )

        insights.append({
            "title": str(column) + " Category Insight",
            "message": (
                f"{most_common} is the most frequent category, "
                f"appearing {frequency} times."
            ),
            "type": "info"
        })

    return insights
