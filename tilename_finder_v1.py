# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 12:06:25 2023

@author: YektaCanUzundemir
"""

import boto3
import csv

s3 = boto3.client('s3', aws_access_key_id='AKIA5YDRE6HIULNGBRQ3', aws_secret_access_key='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')
bucket_name = 'doktar-classification'
folder_path = 'Turkey/2023/'

def get_tif_files_in_folder(bucket, folder):
    response = s3.list_objects_v2(Bucket=bucket, Prefix=folder)
    file_names = [obj['Key'] for obj in response.get('Contents', [])]

    tif_files = [file for file in file_names if file.lower().endswith('.tif')]
    return tif_files

def get_all_unique_tif_files(bucket, folder):
    unique_tif_files = set()
    folders_to_check = [folder]

    while len(folders_to_check) > 0:
        current_folder = folders_to_check.pop(0)
        tif_files = get_tif_files_in_folder(bucket, current_folder)

        for tif_file in tif_files:
            file_name = tif_file.split('/')[-1]
            unique_tif_files.add(file_name)

        response = s3.list_objects_v2(Bucket=bucket, Prefix=current_folder, Delimiter='/')
        subfolders = [prefix['Prefix'] for prefix in response.get('CommonPrefixes', [])]
        folders_to_check.extend(subfolders)

    return unique_tif_files

unique_files = get_all_unique_tif_files(bucket_name, folder_path)

csv_file_path = "C:/Users/YektaCanUzundemir/Desktop/deneme/tile_names.csv"

with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Unique_TIF_Names'])

    for file in unique_files:
        writer.writerow([file])

print(f"Unique tile isimleri {csv_file_path} konumuna CSV olarak kaydedildi.")


