#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <zipfile>"
    exit 1
fi

ZIPFILE="$1"
TEMP_DIR=$(mktemp -d)
SUBMISSIONS_DIR="submissions"

# Extract zip to temp directory
unzip -q "$ZIPFILE" -d "$TEMP_DIR"

# Create submissions directory
mkdir -p "$SUBMISSIONS_DIR"

# Process each file
find "$TEMP_DIR" -type f | while read -r file; do
    filename=$(basename "$file")
    
    # Skip if filename doesn't match expected pattern
    if [[ ! "$filename" =~ ^[0-9]+-[0-9]+\ -\ (.+)\ -\ .+\ -\ (.+)$ ]]; then
        continue
    fi
    
    # Extract student name and actual filename
    student_name=$(echo "$filename" | sed 's/^[0-9]*-[0-9]* - \(.*\) - .* - .*/\1/')
    actual_filename=$(echo "$filename" | sed 's/^[0-9]*-[0-9]* - .* - .* - \(.*\)/\1/' | tr ' ' '_')
    
    # Create student directory
    student_dir="$SUBMISSIONS_DIR/$student_name"
    mkdir -p "$student_dir"
    
    # Copy file with actual filename
    cp "$file" "$student_dir/$actual_filename"
done

# Cleanup
rm -rf "$TEMP_DIR"

echo "Submissions organized in $SUBMISSIONS_DIR/"