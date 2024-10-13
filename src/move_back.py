import os
import shutil

# Paths to source, target, and base image folder
source_folder = "D:/gis_urbangrowth/dataset/source"
target_folder = "D:/gis_urbangrowth/dataset/target"
base_image_folder = "D:/gis_urbangrowth/cropped_images"

# Function to move files back to their original year folders
def move_files_back(folder, years):
    for img_file in os.listdir(folder):
        # Extract the year and OID_ from the file name
        file_name_parts = img_file.split('_')
        year = file_name_parts[0]
        OID_ = file_name_parts[1].split('.')[0]
        
        # Check if the image corresponds to the current year and move it back
        if year in years:
            destination_folder = os.path.join(base_image_folder, year)
            os.makedirs(destination_folder, exist_ok=True)  # Create the year folder if it doesn't exist
            shutil.move(os.path.join(folder, img_file), os.path.join(destination_folder, img_file))
            print(f"Moved {img_file} back to {destination_folder}")

# Move images from the source folder back to their respective years (2005–2014)
source_years = [str(year) for year in range(2005, 2015)]
move_files_back(source_folder, source_years)

# Move images from the target folder back to their respective years (2006–2015)
target_years = [str(year) for year in range(2006, 2016)]
move_files_back(target_folder, target_years)

print("Files have been moved back to their original folders.")
