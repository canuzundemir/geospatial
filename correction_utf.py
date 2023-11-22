# -*- coding: utf-8 -*-

import pandas as pd
from openpyxl import load_workbook
import unicodedata
import geopandas as gpd 

df_excel = gpd.read_file(r"C:\Users\YektaCanUzundemir\Downloads\Zone_7.gpkg")

# Define a function to remove diacritical marks
def remove_diacritics(x):
    if isinstance(x, str):
        return ''.join(
            c for c in unicodedata.normalize('NFKD', x)
            if not unicodedata.combining(c)
        )
    return x

# Apply the function to the specific column(s) with the desired format
df_excel['CityName'] = df_excel['CityName'].apply(remove_diacritics)
df_excel['DistrictName'] = df_excel['DistrictName'].apply(remove_diacritics)
df_excel['RegionName'] = df_excel['RegionName'].apply(remove_diacritics)

df_excel.to_file(r"C:\Users\YektaCanUzundemir\Downloads\Zone_7_v1.gpkg", driver="GPKG")


#df_excel.to_excel(r"C:\HASAN\2023\Turkey\Reports\BASF\Doktar_BASF_Turkey_Plantation_Area_2023_v20231106.xlsx", engine = 'openpyxl', index = False)
