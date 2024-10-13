import os
import shutil
import pandas as pd
import json

# Folder paths for images and CSV
source_folder = "D:/gis_urbangrowth/dataset/source"
target_folder = "D:/gis_urbangrowth/dataset/target"
base_image_folder = "D:/gis_urbangrowth/cropped_images"
csv_file_path = r'D:\gis_urbangrowth\dataset_preparation\data\poi_count.csv'

# Load the CSV data
csv_data = pd.read_csv(csv_file_path)

# Create source and target folders if they don't exist
os.makedirs(source_folder, exist_ok=True)
os.makedirs(target_folder, exist_ok=True)

# Years to consider for moving images
source_years = list(range(2005, 2015))
target_years = list(range(2006, 2016))

# Copy images from source years to the source folder, if not already copied
for year in source_years:
    year_folder = os.path.join(base_image_folder, str(year))
    if os.path.exists(year_folder):
        for img_file in os.listdir(year_folder):
            source_img_path = os.path.join(source_folder, img_file)
            # Only copy if the image does not already exist in the source folder
            if not os.path.exists(source_img_path):
                shutil.copy(os.path.join(year_folder, img_file), source_img_path)

# Copy images from target years to the target folder, if not already copied
for year in target_years:
    year_folder = os.path.join(base_image_folder, str(year))
    if os.path.exists(year_folder):
        for img_file in os.listdir(year_folder):
            target_img_path = os.path.join(target_folder, img_file)
            # Only copy if the image does not already exist in the target folder
            if not os.path.exists(target_img_path):
                shutil.copy(os.path.join(year_folder, img_file), target_img_path)

# Function to generate the prompt based on the CSV row data
def generate_prompt(row):
    prompt_parts = ["White is city growth, Red is road, Blue is water, Green is green space"]
    
    # Append relevant POI values only if they are non-zero
    if row['Join_Co_11'] != 0:
        prompt_parts.append(f"Train_{int(row['Join_Co_11'])}")
    if row['Join_Co_12'] != 0:
        prompt_parts.append(f"Subway_{int(row['Join_Co_12'])}")
    if row['Join_Co_13'] != 0:
        prompt_parts.append(f"Bus_{int(row['Join_Co_13'])}")
    if row['Join_Co_14'] != 0:
        prompt_parts.append(f"Airport_{int(row['Join_Co_14'])}")
    if row['Join_Co_15'] != 0:
        prompt_parts.append(f"Public Infrastructure_{int(row['Join_Co_15'])}")
    
    # Add POI number and POI mixture (multiplied by 100)
    poi_number = int(row['POI_Number'])
    poi_mixture = int(row['POI_Mixture'] * 100)
    prompt_parts.append(f"POI_{poi_number}")
    prompt_parts.append(f"POI_Mixture_{poi_mixture}")
    
    return ', '.join(prompt_parts)

# Generate the JSON file
json_output_file = r"D:\gis_urbangrowth\dataset\prompt.json"  # Replace with your desired output path

# Open the file in write mode (without the square brackets)
with open(json_output_file, 'w') as f:
    # Iterate over each row in the CSV and create the corresponding JSON entry
    for _, row in csv_data.iterrows():
        OID_ = int(row['OID_'])  # Cast OID_ to integer
        
        # Debugging: Print the current OID_ being processed
        print(f"Processing OID_: {OID_}")
        
        # Iterate over years 2005 to 2014 for source images
        for year in range(2005, 2015):
            next_year = year + 1  # the corresponding target year
            
            source_img = f"{year}_{OID_}.jpg"
            target_img = f"{next_year}_{OID_}.jpg"
            
            # Check if both source and target images exist in the folders
            source_img_path = os.path.join(source_folder, source_img)
            target_img_path = os.path.join(target_folder, target_img)
            
            if os.path.exists(source_img_path) and os.path.exists(target_img_path):
                # Debugging: Print the image paths
                print(f"Found source image: {source_img_path}")
                print(f"Found target image: {target_img_path}")
                
                # Generate the prompt from the CSV row
                prompt = generate_prompt(row)
                
                # Create the JSON entry
                json_entry = {
                    "source": f"source/{source_img}",
                    "target": f"target/{target_img}",
                    "prompt": prompt
                }
                
                # Write each JSON entry as a new line (independent JSON object)
                json.dump(json_entry, f, separators=(',', ':'), ensure_ascii=False)
                f.write('\n')  # Add newline after each entry
            else:
                # Debugging: If images are not found
                print(f"Images not found for OID {OID_}: {source_img}, {target_img}")

print(f"JSON file created at {json_output_file}")
