#!/bin/bash

# Define source and destination directories
src_dir="path/to/source/dir"
dest_dir="path/to/destination/dir"

# Ensure that both directories exist
if [ ! -d "$src_dir" ]; then
  echo "Source directory not found"
  exit 1
fi

if [ ! -d "$dest_dir" ]; then
  echo "Destination directory not found"
  exit 1
fi

# Change into the destination directory
cd "$dest_dir"

# Sync the two directories
rsync -av --exclude '.git' "$src_dir/" .

# Replace all occurrences of "automation.test.com" with "app.terraform.io"
find . -type f -exec sed -i 's/automation\.test\.com/app.terraform.io/g' {} \;

# Commit the changes to Git
git add .
git commit -m "Synced directories and replaced automation.test.com with app.terraform.io"
