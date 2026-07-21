import pandas as pd

xls = pd.ExcelFile("datasets/EXIM_AI_Engineer_Simulated_Data.xlsx")

for sheet in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet)
    print(sheet, len(df))