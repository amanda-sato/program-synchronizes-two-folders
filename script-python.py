import os
import shutil
import time

def list_dir_contents(directory_path):
    for dirpath, dirnames, filenames in os.walk(directory_path):
        print(
            f"Root: {dirpath}\n"
            f"Sub-directories: {dirnames}\n"
            f"Files: {filenames}\n\n"
        )

def copy_directory(source_path, destination_path):
    source_folder = os.path.join(source_path, "folder-test")
    destination_folder = os.path.join(destination_path, "backup-challange")

    if os.path.exists(destination_folder):
        print("A pasta de destino já existe. Sincronizando...")
        shutil.rmtree(destination_folder)  

    shutil.copytree(source_folder, destination_folder)
    print("Pasta copiada.")

while True:
    list_dir_contents("/Users/amand/challange-python/program-synchronizes-two-folders/folder-test")
    copy_directory("/Users/amand/challange-python/program-synchronizes-two-folders", "/Users/amand")
    time.sleep(30)

