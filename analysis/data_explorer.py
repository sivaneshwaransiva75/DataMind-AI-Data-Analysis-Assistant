
import pandas as pd


def prepare_explorer_data(df):

    columns = []

    for column in df.columns:
        columns.append(str(column))

    rows = []

    for _, record in df.iterrows():

        row_data = []

        for value in record:

            if pd.isna(value):
                row_data.append("")
            else:
                row_data.append(str(value))

        rows.append(row_data)

    return {
        "columns": columns,
        "rows": rows,
        "total_rows": len(df)
    }
