import os
import argparse
from dotenv import dotenv_values

def main():
    parser = argparse.ArgumentParser(
        description="Validate files from the list in text file againt a source directory"
    )
    parser.add_argument("filename", type=str, help="The log file to parse")
    args = parser.parse_args()

    # Path to the text file containing the file list
    file_list_path = args.filename

    # load configuration
    config = dotenv_values("config.txt")

    # Path to the source directory
    source_directory_path = config["TIFF_PATH"]

    # Read the file list from the text file
    file_list = {}
    with open(file_list_path, 'r') as file:
        for line in file.readlines():
            parts = line.split()
            file_path = parts[0]
            file_size = int(parts[1])
            file_list[file_path] = file_size

    # Get the list of files and their sizes in the source directory
    source_files = {}
    for root, dirs, files in os.walk(source_directory_path):
        for name in files:
            file_path = os.path.join(root, name)
            file_size = os.path.getsize(file_path)
            source_files[file_path] = file_size

    # Compare the two lists
    missing_files = [file for file in file_list if file not in source_files]
    extra_files = [file for file in source_files if file not in file_list]
    size_mismatches = {file: (file_list[file], source_files[file]) for file in file_list if file in source_files and file_list[file] != source_files[file]}

    # Print the results
    print("Files listed in text file but not in source directory:")
    for file in missing_files:
        print(file)

    print("\nFiles in source directory but not listed in text file:")
    for file in extra_files:
        print(file)

    print("\nFiles with size mismatches:")
    for file, sizes in size_mismatches.items():
        print(f"{file}: Listed size = {sizes[0]}, Source size = {sizes[1]}")

if __name__ == "__main__":
    main()