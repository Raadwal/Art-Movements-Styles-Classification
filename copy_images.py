import os
import shutil
from PIL import Image
import random
from concurrent.futures import ThreadPoolExecutor
import time

def process_image(src_file_path, dest_file_path):
    with Image.open(src_file_path) as img:
        resized_img = img.resize((224, 224))
        resized_img = resized_img.convert('RGB')
        resized_img.save(dest_file_path)

def process_folder(subdir, file_set, dest_subdir):
    for img_file in file_set:
        src_file_path = os.path.join(nested_subdir, img_file)
        dest_file_path = os.path.join(dest_subdir, img_file)
        process_image(src_file_path, dest_file_path)

# Set your source and destination directory paths
source_dir = "Original"
destination_dir = "Organized Images"

# Create train, dev, val, and test directories in the destination directory
train_dir = os.path.join(destination_dir, 'train')
dev_dir = os.path.join(destination_dir, 'dev')
val_dir = os.path.join(destination_dir, 'val')
test_dir = os.path.join(destination_dir, 'test')

os.makedirs(train_dir, exist_ok=True)
os.makedirs(dev_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# Set the ratios for splitting the data
train_ratio = 0.8
dev_ratio = 0.25
val_ratio = 0.1
test_ratio = 0.1

# Count the total numbers of the elements in each dataset
train_total = 0
dev_total = 0
val_total = 0
test_total = 0

# Iterate through the subdirectories in the source directory
for root, dirs, files in os.walk(source_dir):
    for subdir in dirs:
        # Get the start time of the current folder processing
        folder_start_time = time.time()
        
        # Replace '_' with ' ' in the subdir name
        subdir_renamed = subdir.replace("_", " ")

        # Define the path for the nested subdir (---)
        nested_subdir = os.path.join(root, subdir)
        
        # Create new directories in the train, dev, val, and test directories with the renamed subdir
        train_subdir = os.path.join(train_dir, subdir_renamed)
        dev_subdir = os.path.join(dev_dir, subdir_renamed)
        val_subdir = os.path.join(val_dir, subdir_renamed)
        test_subdir = os.path.join(test_dir, subdir_renamed)

        os.makedirs(train_subdir, exist_ok=True)
        os.makedirs(dev_subdir, exist_ok=True)
        os.makedirs(val_subdir, exist_ok=True)
        os.makedirs(test_subdir, exist_ok=True)

        # Get the list of files in the nested subdir and shuffle it
        nested_files = os.listdir(nested_subdir)
        random.shuffle(nested_files)

        # Calculate the number of files for each set
        num_files = len(nested_files)
        
        # Skip current loop if the current folder doesn't contain images
        if num_files == 1 and subdir in nested_files:
            continue
        
        train_count = int(num_files * train_ratio)
        dev_count = int(train_count * dev_ratio)
        val_count = int(num_files * val_ratio)
        test_count = num_files - train_count - val_count
        
        train_total += train_count
        dev_total += dev_count
        val_total += val_count
        test_total += test_count

        print(f'[{subdir_renamed}] Total size: {num_files}, '
                f'Train size: {train_count}, '
                f'dev size: {dev_count}, '
                f'val size: {val_count}, '
                f'test size: {test_count}')
        
        # Split the files into train (including dev), val, and test sets
        train_files = nested_files[:train_count]
        val_files = nested_files[train_count:train_count + val_count]
        test_files = nested_files[train_count + val_count:]

        # Get subset of train set as dev set
        random.shuffle(train_files)
        dev_files = train_files[:dev_count]
        
        folders_and_files = [
            (nested_subdir, train_files, train_subdir),
            (nested_subdir, dev_files, dev_subdir),
            (nested_subdir, val_files, val_subdir),
            (nested_subdir, test_files, test_subdir)
        ]
        
        with ThreadPoolExecutor() as executor:
            executor.map(lambda x: process_folder(*x), folders_and_files)
            
        # Calculate the time taken for the current folder
        folder_time = time.time() - folder_start_time

        # Print a message after completing each folder
        print(f"Folder '{subdir}' completed in {folder_time:.2f} seconds.")
        
print(f'[Total] Train size: {train_total}, '
                f'dev size: {dev_total}, '
                f'val size: {val_total}, '
                f'test size: {test_total}')