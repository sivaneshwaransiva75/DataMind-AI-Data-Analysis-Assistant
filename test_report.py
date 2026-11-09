import pandas as pd
from analysis.report_generator import generate_pdf_report

df = pd.DataFrame({
    "Name": ["Asha", "Ravi", "Kumar"],
    "Marks": [85, 72, 90],
    "Age": [21, 22, 23]
})

insights = [
    "The average marks are above 80.",
    "All students scored above 70."
]

generate_pdf_report(
    df,
    "test_dataset.csv",
    insights,
    "reports/test_report.pdf"
)

print("Test completed successfully!")