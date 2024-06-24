import os
import hashlib
import json
import argparse


def calculate_md5(file_path):
    """Calculate MD5 checksum of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_files_in_directory(directory):
    """Get all file paths in the specified directory and its subdirectories."""
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths


def calculate_md5_for_directory(directory):
    """Calculate MD5 checksums for all files in the specified directory."""
    files = get_files_in_directory(directory)
    md5_dict = {}
    for file in files:
        md5_dict[file] = calculate_md5(file)
    return md5_dict


def save_md5_to_json(md5_dict, json_file):
    """Save the MD5 checksums dictionary to a JSON file."""
    with open(json_file, "w") as f:
        json.dump(md5_dict, f, indent=4)


def main(directory, json_file):
    md5_dict = calculate_md5_for_directory(directory)
    save_md5_to_json(md5_dict, json_file)
    print(f"MD5 checksums saved to {json_file}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Calculate MD5 checksums for all files in a directory and save to a JSON file."
    )
    parser.add_argument("directory", type=str, help="Directory to scan for files")
    parser.add_argument(
        "json_file", type=str, help="JSON file to save the MD5 checksums"
    )
    args = parser.parse_args()

    main(args.directory, args.json_file)
