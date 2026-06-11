#!/usr/bin/env python
#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import os
import shutil

# -----------------------------------------------------------------------------
# SCRATCH ARCHIVING UTILITY
# -----------------------------------------------------------------------------
# This script moves files from the local './scratch' folder to the user's home
# directory under '~/keep' to prevent local workspace pollution.
# It implements a versioning mechanism by suffixing files if they already exist
# in the archive directory (e.g. file.py -> file.py;001 -> file.py;002).
# -----------------------------------------------------------------------------
def archive_scratch():
    # A. Resolve absolute paths of target directories
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    scratch_dir = os.path.join(base_dir, "scratch")
    
    # Locate user home directory (supports Windows %USERPROFILE% and Unix/Linux ~ home path)
    user_profile = os.environ.get("USERPROFILE") or os.path.expanduser("~")
    keep_dir = os.path.join(user_profile, "keep")

    # B. Ensure the destination directory exists
    if not os.path.exists(keep_dir):
        os.makedirs(keep_dir)
        print(f"Created archive directory: {keep_dir}")

    # Check that local scratch directory exists before proceeding
    if not os.path.exists(scratch_dir):
        print(f"Scratch directory does not exist: {scratch_dir}")
        return

    # C. Loop through and move files in scratch directory
    files_moved = 0
    for filename in os.listdir(scratch_dir):
        src_path = os.path.join(scratch_dir, filename)
        
        # Skip directories to only archive files
        if not os.path.isfile(src_path):
            continue

        # D. Version resolution loop
        # We append a 3-digit version tag if the file already exists in keep_dir
        version = 1
        while True:
            # Format pattern: test.py -> test.py;001 -> test.py;002
            dest_filename = f"{filename};{version:03d}"
            dest_path = os.path.join(keep_dir, dest_filename)
            # Find the first available name that does not exist yet
            if not os.path.exists(dest_path):
                break
            version += 1

        # Move file using shutil.move
        shutil.move(src_path, dest_path)
        print(f"Moved: {filename} -> {dest_path}")
        files_moved += 1

    print(f"Scratch archiving completed. Total files archived: {files_moved}")

if __name__ == "__main__":
    archive_scratch()