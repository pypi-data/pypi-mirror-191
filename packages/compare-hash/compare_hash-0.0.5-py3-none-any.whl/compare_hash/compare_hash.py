import os
import hashlib
import argparse
from datetime import datetime


def fill_string(string, length):
    return string.ljust(length)


def get_hash(file_path):
    """Get the hash of a file"""
    try:
        with open(file_path, 'rb') as file:
            return hashlib.sha256(file.read()).hexdigest()
    except FileNotFoundError:
        return None


def write_array_to_file(file_path, array):
    folder_name = os.path.dirname(file_path)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    with open(file_path, 'w') as file:
        for item in array:
            file.write(str(item) + "\n")


def main():
    # Define the command line arguments using argparse
    parser = argparse.ArgumentParser(description='Compare the contents of two folders')
    parser.add_argument('folder1', type=str,help='The path to the first folder')
    parser.add_argument('folder2', type=str,help='The path to the second folder')

    # Parse the command line arguments
    args = parser.parse_args()

    folder1 = args.folder1
    folder2 = args.folder2

    # Create an empty list to store the different files
    diff_files = []
    same_files = []
    try:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} :: Start comparison between {folder1} and {folder2}")
        # Iterate through all the files in both folders
        file_counter = 0
        total_files = sum([len(files) for r, d, files in os.walk(folder1)])
        for root, dirs, files in os.walk(folder1):
            for file in files:
                file_counter += 1
                # Get the full file path
                file_path1 = os.path.join(root, file)
                file_path2 = os.path.join(folder2, os.path.relpath(file_path1, folder1))
                # Compare the hashes of the files
                if get_hash(file_path1) != get_hash(file_path2) and get_hash(file_path2) != None:
                    diff_files.append(f"{fill_string(file_path1, 200)} => hash({get_hash(file_path1)}, {get_hash(file_path2)})")
                elif (get_hash(file_path1) == get_hash(file_path2) and get_hash(file_path2) != None):
                    same_files.append(f"{fill_string(file_path1, 200)} => hash({get_hash(file_path1)}, {get_hash(file_path2)})")
                print(f"{file_counter}/{total_files}", end='\r')
        print(f"""{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} :: End comparison""")
        write_array_to_file("./result/notsame.txt", diff_files)
        write_array_to_file("./result/same.txt", same_files)

        # Add summary information
        print(f"Total number of files: {total_files}")
        print(f"Number of different files: {len(diff_files)}")
        print(f"Number of same files: {len(same_files)}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        similarity_percent = (len(same_files) / total_files) * 100
        print(f"Percent of similarity: {similarity_percent:.2f}%")
        print(f"Finished")
    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
