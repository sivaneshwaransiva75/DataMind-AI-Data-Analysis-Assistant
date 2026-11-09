
import os
from fpdf import FPDF


def generate_pdf_report(df, dataset_name, insights, output_path):

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    pdf = FPDF(orientation="P", unit="mm", format="A4")

    pdf.set_margins(12, 12, 12)
    pdf.set_auto_page_break(auto=False)
    pdf.add_page()
    LEFT = 12
    RIGHT = 12
    TOP = 15
    BOTTOM = 285
    MAX_WIDTH = pdf.w - LEFT - RIGHT
    LINE_HEIGHT = 6
    y = TOP
    def clean_text(value):
        return (
            str(value)
            .replace("\n", " ")
            .replace("\r", " ")
            .encode("latin-1", errors="replace")
            .decode("latin-1")
        )
    
    def wrap_text(value):

        value = clean_text(value)

        words = value.split(" ")
        lines = []
        current_line = ""

        for word in words:

            # Handle extremely long words
            if pdf.get_string_width(word) > MAX_WIDTH:

                if current_line:
                    lines.append(current_line)
                    current_line = ""

                chunk = ""

                for character in word:

                    candidate = chunk + character

                    if pdf.get_string_width(candidate) <= MAX_WIDTH:
                        chunk = candidate
                    else:
                        if chunk:
                            lines.append(chunk)

                        chunk = character

                if chunk:
                    current_line = chunk

                continue

            candidate = (
                current_line + " " + word
                if current_line
                else word
            )

            if pdf.get_string_width(candidate) <= MAX_WIDTH:
                current_line = candidate
            else:
                if current_line:
                    lines.append(current_line)

                current_line = word

        if current_line:
            lines.append(current_line)

        return lines or [""]

    def write_text(value, size=9, bold=False, gap=0):

        nonlocal y

        pdf.set_font(
            "Helvetica",
            "B" if bold else "",
            size
        )

        lines = wrap_text(value)

        for line in lines:

            if y + LINE_HEIGHT > BOTTOM:
                pdf.add_page()
                y = TOP

            pdf.text(LEFT, y, line)

            y += LINE_HEIGHT

        y += gap

    pdf.set_font("Helvetica", "B", 20)

    title = "DataMind AI Analysis Report"

    title_width = pdf.get_string_width(title)

    pdf.text(
        (pdf.w - title_width) / 2,
        y + 5,
        title
    )

    y += 18

    write_text("1. DATASET OVERVIEW", 14, True, 3)

    write_text(f"Dataset Name: {dataset_name}")
    write_text(f"Total Rows: {df.shape[0]}")
    write_text(f"Total Columns: {df.shape[1]}", gap=5)

    write_text("2. DATA QUALITY", 14, True, 3)

    missing = int(df.isnull().sum().sum())
    duplicates = int(df.duplicated().sum())

    write_text(f"Missing Values: {missing}")
    write_text(f"Duplicate Rows: {duplicates}", gap=5)

    write_text("3. STATISTICAL ANALYSIS", 14, True, 3)

    numeric_df = df.select_dtypes(include="number")

    if not numeric_df.empty:

        statistics = numeric_df.describe().round(2)

        for column in statistics.columns:

            write_text(f"Column: {column}", 10, True)

            for metric, value in statistics[column].items():
                write_text(f"{metric}: {value}", 9)

            y += 3

    else:
        write_text("No numerical columns found.")

    y += 3

    write_text("4. AI-GENERATED INSIGHTS", 14, True, 3)

    if insights:

        for number, insight in enumerate(insights, start=1):
            write_text(f"{number}. {insight}", 9, gap=2)

    else:
        write_text("No insights available.")

    y += 3

    write_text("5. DATASET PREVIEW", 14, True, 3)

    for number, (_, row) in enumerate(df.head(10).iterrows(), start=1):

        write_text(f"RECORD {number}", 10, True)

        for column in df.columns:

            write_text(
                f"{column}: {row[column]}",
                8
            )

        y += 3

    pdf.output(output_path)

    print("--------------------------------")
    print("PDF report generated successfully!")
    print("Saved at:", output_path)
    print("--------------------------------")

    return output_path


if __name__ == "__main__":
    print("DataMind FPDF2 Report Generator Ready!")
