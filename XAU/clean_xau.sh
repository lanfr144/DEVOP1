#!/bin/bash
#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"

# Target directory is passed as the first argument, default to /app/XAU
TARGET_DIR="${1:-/app/XAU}"

cd "$TARGET_DIR" || { echo "Failed to cd to $TARGET_DIR"; exit 1; }

echo "Starting XAU cleanup. Organizing files in $TARGET_DIR into monthly zip files..."

# 1. Group files by YYYYMM so they go into the "right" zip file
find . -maxdepth 1 -name 'metaux-precieux_????????_??????.*' | sed 's|^\./||' | while read -r file; do
    # Extract the YYYYMM portion from the filename
    YYYYMM=$(echo "$file" | sed -E 's/metaux-precieux_([0-9]{6})[0-9]{2}_[0-9]{6}\..*/\1/')
    echo "$file" >> ".to_zip_${YYYYMM}.list"
done

# 2. Zip each group into its respective monthly zip file
for list_file in .to_zip_*.list; do
    # Check if files actually exist to avoid wildcard literal matching
    [ -e "$list_file" ] || continue
    
    YYYYMM=$(echo "$list_file" | sed -E 's/\.to_zip_([0-9]{6})\.list/\1/')
    ZIP_FILE="metaux-precieux_${YYYYMM}.zip"
    
    echo "Archiving to $ZIP_FILE..."
    cat "$list_file" | xargs zip -u "$ZIP_FILE"
    
    # Clean up the temporary list file
    rm -f "$list_file"
done

# 3. Verify zip integrity and remove original files that successfully zipped
echo "Verifying zip files younger than 4 days and removing archived files older than 1 day..."

# Find zip files younger than 4 days and check them
find . -maxdepth 1 -name 'metaux-precieux_??????.zip' -mtime -4 | sed 's|^\./||' | while read -r zip_file; do
    echo "Processing $zip_file..."
    unzip -t "$zip_file" 2>&1 | sed -e 's/^[ \t]*testing:[ \t]*//' -e 's/[ \t]*OK[ \t]*$//' | xargs -I {} find "{}" -type f -mtime +1 -print | xargs /bin/rm -f
done

echo "Cleanup completed."
