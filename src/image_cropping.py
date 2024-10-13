import os
from PIL import Image

# Optionally increase the maximum image size limit
Image.MAX_IMAGE_PIXELS = None  # Set to None to disable the limit, or set to a specific value

def crop_images(input_folder, base_output_folder, crop_size=(1024, 1024), grid_size=(22, 17)):
    for year in os.listdir(input_folder):
        if year.isdigit() and 1985 <= int(year) <= 2024:  # Check if the folder name is a valid year
            year_path = os.path.join(input_folder, year)
            if os.path.isdir(year_path):
                # Create a specific output folder for the current year
                output_folder = os.path.join(base_output_folder, year)
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)

                for img_file in os.listdir(year_path):
                    img_path = os.path.join(year_path, img_file)
                    try:
                        with Image.open(img_path) as img:
                            img_width, img_height = img.size
                            
                            # Increase the size threshold to 500 million pixels
                            if img_width * img_height > 500_000_000:  # New threshold
                                print(f"Skipping {img_path}: Image size exceeds limit of 500 million pixels.")
                                continue

                            for row in range(grid_size[1]):
                                for col in range(grid_size[0]):
                                    left = col * crop_size[0]
                                    upper = img_height - (row + 1) * crop_size[1]
                                    right = left + crop_size[0]
                                    lower = upper + crop_size[1]

                                    if right <= img_width and upper >= 0:
                                        cropped_img = img.crop((left, upper, right, lower))
                                        cropped_img_name = f"{year}_{row * grid_size[0] + col}.jpg"
                                        cropped_img.save(os.path.join(output_folder, cropped_img_name))
                    except Exception as e:
                        print(f"Error processing {img_path}: {e}")

input_folder = r'D:\gis_urbangrowth\dataset_preparation\data\color patch'  # Adjust this path as needed
base_output_folder = r'D:\gis_urbangrowth\dataset_preparation\data\cropped_images'  # Base output path
crop_images(input_folder, base_output_folder)
