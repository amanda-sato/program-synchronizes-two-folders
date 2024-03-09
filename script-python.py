import os
import shutil
import time
import argparse
import logging
import sys
from datetime import datetime
import filecmp

def setup_logging(log_file):
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename=log_file
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    console_handler.setFormatter(console_formatter)

    logging.getLogger().addHandler(console_handler)


def list_dir_contents(directory_path):
    for dirpath, dirnames, filenames in os.walk(directory_path):
        print(
            f"Root: {dirpath}\n"
            f"Sub-directories: {dirnames}\n"
            f"Files: {filenames}\n\n"
        )

def copy_directory(source_path, destination_path):
    ''' 
        for each file in source path 
        if the file doesn't exist in destination path, copy.
        if the file exists in the destination path, but the content is different, overwrite.
        if the file exists in the destination path, but the content is the same, skip.
        for each file in the destination path, 
        if the file doesn't exist in the source path, remove.
    '''
    
    for dirpath, dirnames, filenames in os.walk(source_path):
        path = os.path.relpath(dirpath, start=source_path)
        
        for file in filenames:
            file_relpath = os.path.join(path, file)
            source_file_path = os.path.join(source_path, file_relpath)
            dest_file_path = os.path.join(destination_path, file_relpath)

            if not os.path.isfile(dest_file_path):
                print(f'Copying {file_relpath}...')
                # copy code
            elif not filecmp.cmp(source_file_path, dest_file_path, shallow=False):
                print(f'Overwriting {file_relpath}...')
                # copy code
            else:
                print(f'Skipping {file_relpath}')
        


    # if os.path.exists(destination_folder):
    #     logging.info("The destination folder already exists. Synchronizing...")
    #     shutil.rmtree(destination_folder)  

    # sync_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # try:
    #     shutil.copytree(source_folder, destination_folder)

    #     logging.info(f"{sync_timestamp} - Synced {source_folder} to {destination_folder}")

    #     logging.info(f"{sync_timestamp} - Pasta copiada.")
    
    # except Exception as e:
    #     logging.error(f"{sync_timestamp} - Error during synchronization: {str(e)}")

    # print("Pasta copiada.")


def main():
    parser = argparse.ArgumentParser(description="Folder synchronization program")
    parser.add_argument("source_path", help="Path to source folder")
    parser.add_argument("destination_path", help="Path to destination folder")
    parser.add_argument("log_file", help="Path to the log file")
    parser.add_argument('--period', '-p', default=30, help="Period in seconds")
    args = parser.parse_args()

    setup_logging(args.log_file)

    while True:
        list_dir_contents(args.source_path)
        copy_directory(args.source_path, args.destination_path)
        time.sleep(int(args.period))

if __name__ == "__main__":
    main()
