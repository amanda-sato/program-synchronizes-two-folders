import os
import shutil
import time
import argparse
import logging
import sys
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


def sync_directory(source_path, destination_path):
    ''' 
    Algorithm details:
    ---
    for each empty dir in source path
        if the dir doesn't exist in destination path, create
        else skip
    for each file in source path 
        if the file doesn't exist in destination path, copy.
        if the file exists in the destination path, but the content is different, overwrite.
        if the file exists in the destination path, but the content is the same, skip.
    for each empty dir in destination path
        if the dir doesn't exist in source path, remove.
    for each file in the destination path, 
        if the file doesn't exist in the source path, remove.
    '''
    
    logging.info(f'Syncing from={source_path} to={destination_path}')

    for dirpath, _, filenames in os.walk(source_path):
        path = os.path.relpath(dirpath, start=source_path)

        if not filenames and not os.path.isdir(os.path.join(destination_path, path)):
            logging.info(f'Creating directory {path}')
            os.makedirs(os.path.join(destination_path, path))
        
        for file in filenames:
            file_relpath = os.path.join(path, file)
            source_file_path = os.path.join(source_path, file_relpath)
            dest_file_path = os.path.join(destination_path, file_relpath)

            if not os.path.isfile(dest_file_path):
                logging.info(f'Copying {file_relpath}...')
                os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
                shutil.copy2(source_file_path, dest_file_path)
            elif not filecmp.cmp(source_file_path, dest_file_path, shallow=False):
                logging.info(f'Overwriting {file_relpath}...')
                os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
                shutil.copy2(source_file_path, dest_file_path)
            else:
                logging.info(f'Skipping {file_relpath}')
        
    for dirpath, _, filenames in os.walk(destination_path):
        path = os.path.relpath(dirpath, start=destination_path)

        for file in filenames:
            file_relpath = os.path.join(path, file)
            source_file_path = os.path.join(source_path, file_relpath)
            dest_file_path = os.path.join(destination_path, file_relpath)

            if not os.path.isfile(source_file_path):
                logging.info(f'Removing {file_relpath}')
                os.remove(dest_file_path)

    # Last loop will only remove files, leaving empty dirs behind, 
    # These are then handled separately here.
    # Using os.walk default topdown approach would try to delete empty dirs
    # with other (empty) subdirs on them, erroring out. 
    # This is solved by doing it bottom up (topdown=False)
    for dirpath, _, filenames in os.walk(destination_path, topdown=False):
        path = os.path.relpath(dirpath, start=destination_path)

        if not filenames and not os.path.isdir(os.path.join(source_path, path)):
            logging.info(f'Removing directory {path}')
            os.rmdir(os.path.join(destination_path, path))


def main():
    parser = argparse.ArgumentParser(description="Syncs a source folder into a destination one.")
    parser.add_argument("source_path", help="Path to source folder")
    parser.add_argument("destination_path", help="Path to destination folder")
    parser.add_argument("log_file", help="Path to the log file")
    parser.add_argument('--period', '-p', default=30, help="Period in seconds")
    args = parser.parse_args()

    setup_logging(args.log_file)

    while True:
        sync_directory(args.source_path, args.destination_path)
        time.sleep(int(args.period))


if __name__ == "__main__":
    main()
