# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 14:28:50 2023

@author: YektaCanUzundemir
"""

import geopandas as gpd
import pandas as pd

df = gpd.read_file(r"C:\Users\YektaCanUzundemir\Downloads\bursa_csi.gpkg")

ilceler = ['Kestel', 'Gursu', 'Karacabey']

subset = df[df['DistrictName'].isin(ilceler)]

# Yeni bir liste oluşturun
export_data = []

for index, row in subset.iterrows():
    City = row['CityName']
    District = row['DistrictName']
    centroid = row['geometry'].centroid
    latitude = centroid.y
    longitude = centroid.x
    
    # Yeni veriyi listeye ekleyin
    export_data.append({'CityName': City, 'DistrictName': District, 'geometry': f'POINT ({latitude} {longitude})'})

# Liste üzerinden bir DataFrame oluşturun
export_df = pd.DataFrame(export_data)

# Excel'e export edin
export_df.to_excel(r"C:\Users\YektaCanUzundemir\Downloads\output4.xlsx", index=False)


    