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

# Sync the "module" directory
rsync -av --exclude '.git' "$src_dir/module/" "$dest_dir/module/"

# Replace all occurrences of "automation.humana.com" with "app.terraform.io" in the "module" directory
find "$dest_dir/module" -type f -exec sed -i 's/automation\.humana\.com/app.terraform.io/g' {} \;

# Sync the "template" directory
rsync -av --exclude '.git' "$src_dir/template/" "$dest_dir/template/"

# Replace all occurrences of "automation.humana.com" with "app.terraform.io" in the "template" directory
find "$dest_dir/template" -type f -exec sed -i 's/automation\.humana\.com/app.terraform.io/g' {} \;

# Commit the changes to Git
git add .
git commit -m "Synced 'module' and 'template' directories and replaced automation.humana.com with app.terraform.io"
