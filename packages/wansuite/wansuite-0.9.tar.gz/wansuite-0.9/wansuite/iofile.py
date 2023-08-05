import pandas as pd

def listExcelSheets(file):
    return pd.ExcelFile(file).sheet_names