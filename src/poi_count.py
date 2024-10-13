import os
import pandas as pd
import numpy as np

# Load the CSV file to inspect the data
file_path = r'D:\gis_urbangrowth\dataset_preparation\data\table_with_distance.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)

# Columns that represent POIs from Join_Cou_1 to Join_Cou_10
poi_columns = [
    'Join_Cou_1', 'Join_Cou_2', 'Join_Cou_3', 'Join_Cou_4', 'Join_Cou_5', 
    'Join_Cou_6', 'Join_Cou_7', 'Join_Cou_8', 'Join_Cou_9', 'Join_Co_10'
]

# Function to calculate POI number by summing the values in the POI columns
def calculate_poi_number(row):
    # Sum the values of the POI columns
    return row[poi_columns].sum()

# Function to calculate degree of POI mixture (Shannon diversity index)
def calculate_poi_mixture(row):
    poi_counts = row[poi_columns].value_counts(normalize=True)  # Get proportions (p_i)
    if len(poi_counts) == 0:
        return 0
    return -np.sum(poi_counts * np.log(poi_counts))

# Apply the POI number and degree of mixture calculations to each row
data['POI_Number'] = data.apply(calculate_poi_number, axis=1)
data['POI_Mixture'] = data.apply(calculate_poi_mixture, axis=1)

# Write the updated dataframe with the new columns back to the CSV
output_file_path = r'D:\gis_urbangrowth\dataset_preparation\data\poi_count.csv'  # Replace with your desired output file path
data.to_csv(output_file_path, index=False)

print(f'Updated CSV file written to {output_file_path}')
