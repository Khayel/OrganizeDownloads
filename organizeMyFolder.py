# Create subfolders based on all filetypes and place files in folders

import sys
import os
import time


def get_file_extension(filepath):
    return filepath[filepath.rfind('.')+1:]


def organize_my_folder(path):
    dir_items = os.listdir(path)
    files = [file for file in dir_items if os.path.isfile(f'{path}\{file}')]

    file_types = set([get_file_extension(file)
                      for file in files])
    print(files, file_types)

    for file_type in file_types:
        try:
            os.makedirs(f'{path}\{file_type}', exist_ok=True)
        except OSError:
            print(f"Error Creating {file_type} Directory")

    for file in files:
        try:
            os.rename(f'{path}\{file}',
                      f'{path}\{get_file_extension(file)}\{file}')
            while os.path.exists(f'{path}\{file}'):
                time.sleep(0.2)
        except FileExistsError:
            pass


if __name__ == "__main__":
    path_to_watch = sys.argv[1] if len(sys.argv) > 1 else '.'
    print(path_to_watch)
    print(f"Organizing {path_to_watch} into file folders")
    organize_my_folder(path_to_watch)
