import os
import shutil
import time
import argparse
import logging
import sys
from datetime import datetime

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
    source_folder = source_path
    destination_folder = destination_path

    if os.path.exists(destination_folder):
        logging.info("The destination folder already exists. Synchronizing...")
        shutil.rmtree(destination_folder)  

    sync_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        shutil.copytree(source_folder, destination_folder)

        logging.info(f"{sync_timestamp} - Synced {source_folder} to {destination_folder}")

        logging.info(f"{sync_timestamp} - Pasta copiada.")
    
    except Exception as e:
        logging.error(f"{sync_timestamp} - Error during synchronization: {str(e)}")

    print("Pasta copiada.")


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
