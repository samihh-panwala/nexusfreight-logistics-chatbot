import pandas as pd
import os

excel_file = "datasets/EXIM_AI_Engineer_Simulated_Data.xlsx"
output_folder = "datasets/supabase_csv"

os.makedirs(output_folder, exist_ok=True)

xls = pd.ExcelFile(excel_file)

for sheet in xls.sheet_names:

    if sheet == "README":
        continue

    df = pd.read_excel(excel_file, sheet_name=sheet)

    filename = os.path.join(output_folder, f"{sheet}.csv")

    df.to_csv(filename, index=False)

    print(f"Saved {filename}")

print("\nDone!")