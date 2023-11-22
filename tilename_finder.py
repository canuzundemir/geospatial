# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 11:16:02 2023

@author: YektaCanUzundemir
"""

import boto3
import os


s3 = boto3.client('s3', aws_access_key_id='AKI*****', aws_secret_access_key='IQW****')


bucket_name = 'doktar-classification'


folder_path = 'Turkey/2023/Zone_1'


response = s3.list_objects(Bucket=bucket_name, Prefix=folder_path)
file_names = [obj['Key'] for obj in response.get('Contents', [])]


tif_files = [os.path.basename(file) for file in file_names if file.lower().endswith('.tif')]


for tif_file in tif_files:
    print(tif_file)
    
file_names = [...]

file_path = "C:/Users/YektaCanUzundemir/Desktop/deneme/tile_names.txt"  

with open(file_path, "w") as file:
    for tif_file in tif_files:
        file.write(tif_file + "\n")

print(f".tif uzantılı dosya isimleri {file_path} konumuna kaydedildi.")

