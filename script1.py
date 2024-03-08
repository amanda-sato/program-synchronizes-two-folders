import os

for dirpath, dirnames, filenames in os.walk(r"/Users/amand/challange-python"):
    print(
        f"Root: {dirpath}\n"
        f"Sub-directories: {dirnames}\n"
        f"Files: {filenames}\n\n"
    )