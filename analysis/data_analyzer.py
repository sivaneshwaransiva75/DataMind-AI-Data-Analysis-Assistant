
import pandas as pd


def analyze_dataset(df):

    # Dataset dimensions
    total_rows = int(df.shape[0])
    total_columns = int(df.shape[1])

    # Missing values
    total_missing = int(df.isnull().sum().sum())

    missing_values = []

    for column in df.columns:
        missing_values.append({
            "column": str(column),
            "missing": int(df[column].isnull().sum())
        })

    # Duplicate records
    duplicate_rows = int(df.duplicated().sum())

    # Column data types
    data_types = []

    for column in df.columns:
        data_types.append({
            "column": str(column),
            "data_type": str(df[column].dtype)
        })

    # Statistical summary
    summary = df.describe(include="all").transpose()
    summary.index.name = "Column"
    summary = summary.reset_index()
    summary = summary.fillna("-")

    summary_html = summary.to_html(
        classes="data-table",
        index=False
    )

    return {
        "total_rows": total_rows,
        "total_columns": total_columns,
        "total_missing": total_missing,
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "data_types": data_types,
        "summary_html": summary_html
    }
