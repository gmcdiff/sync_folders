import os
import shutil
import argparse
import time
from datetime import datetime

def log(log_file, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {message}"

    with open(log_file, "a") as lf:
        lf.write(log_entry + "\n")
        
def synchronize_folders(source_folder, replica_folder, log_file):
    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder)
        log(log_file, f"Created replica folder: {replica_folder}")
        print(f"Created replica folder: {replica_folder}")
        
    for root, dirs, files in os.walk(source_folder):
        relative_path = os.path.relpath(root, source_folder)
        replica_path = os.path.join(replica_folder, relative_path)

        if not os.path.exists(replica_path):
            os.makedirs(replica_path)

        for file in files:
            source_file_path = os.path.join(root, file)
            replica_file_path = os.path.join(replica_path, file)

            if os.path.exists(replica_file_path):
                source_mtime = os.path.getmtime(source_file_path)
                replica_mtime = os.path.getmtime(replica_file_path)

                if source_mtime > replica_mtime:
                    shutil.copy2(source_file_path, replica_file_path)
                    log(log_file, f"Copied: {source_file_path} to {replica_file_path}")
                    print(f"Copied: {source_file_path} to {replica_file_path}")
                else:
                    log(log_file, f"File already up to date: {replica_file_path}")
                    print(f"File is already up to date: {replica_file_path}")
            else:
                shutil.copy2(source_file_path, replica_file_path)
                log(log_file, f"Copied: {source_file_path} to {replica_file_path}")
                print(f"Copied: {source_file_path} to {replica_file_path}")

if __name__ == "__main__":
    print("Synchronization in process...")
    parser = argparse.ArgumentParser(description="Folder Synchronization")
    parser.add_argument("source", help="Path to the source folder")
    parser.add_argument("replica", help="Path to the replica folder")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("log", help="Path to the log file")

    args = parser.parse_args()

    while True:
        synchronize_folders(args.source, args.replica, args.log)
        time.sleep(args.interval)
