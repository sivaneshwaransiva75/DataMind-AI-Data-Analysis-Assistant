
import os
import pandas as pd

from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    send_file
)

from werkzeug.utils import secure_filename

from analysis.data_analyzer import analyze_dataset
from analysis.visualizer import generate_charts
from analysis.insight_generator import generate_insights
from analysis.data_explorer import prepare_explorer_data
from analysis.report_generator import generate_pdf_report

app = Flask(__name__)

BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_FOLDER, "uploads")

CHART_FOLDER = os.path.join(
    BASE_FOLDER, "static", "generated_charts"
)

REPORT_FOLDER = os.path.join(BASE_FOLDER, "reports")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CHART_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/charts/<path:filename>")
def show_chart(filename):
    return send_from_directory(CHART_FOLDER, filename)

@app.route("/upload", methods=["POST"])
def upload_dataset():

    file = request.files.get("dataset")

    if not file or file.filename == "":
        return render_template(
            "index.html",
            error="Please select a dataset."
        )

    filename = secure_filename(file.filename)
    extension = os.path.splitext(filename)[1].lower()

    if extension not in [".csv", ".xlsx", ".xls"]:
        return render_template(
            "index.html",
            error="Please upload a CSV or Excel file."
        )

    file_path = os.path.join(UPLOAD_FOLDER, filename)

    try:

        file.save(file_path)

        if extension == ".csv":
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        if df.empty:
            return render_template(
                "index.html",
                error="The uploaded dataset is empty."
            )

        total_rows = int(df.shape[0])
        total_columns = int(df.shape[1])

        column_names = df.columns.tolist()

        preview_data = df.head(5).to_html(
            classes="data-table",
            index=False
        )

        analysis = analyze_dataset(df)

        charts = generate_charts(df)

        insights = generate_insights(df)

        explorer_data = prepare_explorer_data(df)

        print("\n===================================")
        print("       DATAMIND ANALYTICS")
        print("===================================")

        print("Dataset:", filename)
        print("Rows:", total_rows)
        print("Columns:", total_columns)
        print("Missing Values:", analysis["total_missing"])
        print("Duplicate Rows:", analysis["duplicate_rows"])
        print("Charts Generated:", len(charts))
        print("Insights Generated:", len(insights))
        print("Explorer Records:", explorer_data["total_rows"])

        print("===================================\n")

        return render_template(
            "index.html",
            dataset_name=filename,
            total_rows=total_rows,
            total_columns=total_columns,
            column_names=column_names,
            preview_data=preview_data,
            analysis=analysis,
            charts=charts,
            insights=insights,
            explorer_data=explorer_data
        )

    except Exception as error:

        print("DATAMIND ERROR:", error)

        return render_template(
            "index.html",
            error=f"Dataset analysis failed: {error}"
        )

@app.route("/download-report/<filename>")
def download_report(filename):

    filename = secure_filename(filename)

    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.isfile(file_path):
        return "Dataset not found. Please upload it again.", 404

    try:

        extension = os.path.splitext(filename)[1].lower()

        if extension == ".csv":
            df = pd.read_csv(file_path)
        elif extension in [".xlsx", ".xls"]:
            df = pd.read_excel(file_path)
        else:
            return "Unsupported dataset format.", 400

        insights = generate_insights(df)

        report_filename = (
            os.path.splitext(filename)[0] + "_report.pdf"
        )

        report_path = os.path.join(
            REPORT_FOLDER,
            report_filename
        )

        generate_pdf_report(
            df,
            filename,
            insights,
            report_path
        )

        return send_file(
            report_path,
            as_attachment=True,
            download_name=report_filename
        )

    except Exception as error:

        print("PDF REPORT ERROR:", error)

        return f"PDF generation failed: {error}", 500

if __name__ == "__main__":

    print("\nDATAMIND AI ANALYTICS STARTING...")

    print(app.url_map)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )
