import os
import pandas as pd

# Excel file path
excel_file = "datasets/EXIM_AI_Engineer_Simulated_Data.xlsx"

# Output folder
output_folder = "documents"

os.makedirs(output_folder, exist_ok=True)

# Read all sheets
excel = pd.ExcelFile(excel_file)

print(f"Found {len(excel.sheet_names)} sheets")

for sheet in excel.sheet_names:

    df = pd.read_excel(excel_file, sheet_name=sheet)

    output_file = os.path.join(output_folder, f"{sheet}.txt")

    with open(output_file, "w", encoding="utf-8") as f:

        f.write(f"Sheet Name: {sheet}\n\n")

        for _, row in df.iterrows():

            row_text = " | ".join(
                [f"{col}: {row[col]}" for col in df.columns]
            )

            f.write(row_text + "\n")

    print(f"Created: {output_file}")

print("Done!")