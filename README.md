# sync_dirs.py

Syncs from source folder into a destination folder.
Doesn't handle symlinks.

Operations are logged to the console and to a file passed as parameter.

Requires python 3.

## How to run

```bash
# Control-C to exit the script.

# syncs from $source_path into $dest_path every 30s (default), 
# logs operations to $log_to and the console.
python sync_dirs.py $source_path $dest_path $log_to

# syncs from $source_path into $dest_path every 10s, 
# logs operations to $log_to and the console.
python sync_dirs.py --period 10 $source_path $dest_path $log_to
python sync_dirs.py -p 10 $source_path $dest_path $log_to
```