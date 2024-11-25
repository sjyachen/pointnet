import os
import random
import shutil

def copy_random_files_with_structure(src_folder, dest_folder, num_files=10):
    """Copy a specified number of random files from each subfolder to a new location while preserving the folder structure."""
    for dirpath, _, filenames in os.walk(src_folder):
        if filenames:
            # Randomly select up to num_files from the list of files
            selected_files = random.sample(filenames, min(num_files, len(filenames)))

            # Create the corresponding destination folder path
            relative_path = os.path.relpath(dirpath, src_folder)
            dest_subfolder = os.path.join(dest_folder, relative_path)

            # Create the destination subfolder if it doesn't exist
            os.makedirs(dest_subfolder, exist_ok=True)

            # Copy selected files to the corresponding destination subfolder
            for file in selected_files:
                src_file_path = os.path.join(dirpath, file)
                dest_file_path = os.path.join(dest_subfolder, file)
                shutil.copy(src_file_path, dest_file_path)
                print(f'Copied: {src_file_path} to {dest_file_path}')

if __name__ == '__main__':
    src_folder = '/etkon/data/off'
    dest_folder_training = './data/off/training'
    dest_folder_testing  = './data/off/testing'
    copy_random_files_with_structure(src_folder, dest_folder_training,num_files=20 )
    copy_random_files_with_structure(src_folder, dest_folder_testing,num_files=6)

    # src_folder = '/etkon/develop/pointnet-master/data/off/off_2048'
    # dest_folder_training_2048 = './data/off/training_2048'
    # dest_folder_testing_2048  = './data/off/testing_2048'
    # copy_random_files_with_structure(src_folder, dest_folder_training_2048,num_files=20 )
    # copy_random_files_with_structure(src_folder, dest_folder_testing_2048,num_files=6)

    #src_folder = '/etkon/hdd/data/nmdl_2023_06/nmdl'
    #dest_folder_man_testing = './data/off/man_testing'
    #dest_folder_nmdl = './data/off/nmdl'
    #copy_random_files_with_structure(src_folder, dest_folder_man_testing, num_files=3)
    #copy_random_files_with_structure(src_folder, dest_folder_nmdl, num_files=34200)

