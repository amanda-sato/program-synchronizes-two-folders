import os

root = "/Users/amand/challange-python"

def list_all(path):
    files = os.listdir(path)
    print(path)
    for file in files:
        low_path = os.path.join(path, file)
        if os.path.isdir(low_path):
            list_all(low_path)
        else:
            print("\t", file)

list_all(root) 