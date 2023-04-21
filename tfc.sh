#!/bin/bash

# Set repository and release name
owner=":owner"
repo=":repo"
release="v1.0.0"

# Get release ID
release_id=$(curl -s "https://api.github.com/repos/$owner/$repo/releases?q=name:$release" | jq -r '.[].id')

# Get list of asset IDs
asset_ids=$(curl -s "https://api.github.com/repos/$owner/$repo/releases/$release_id/assets" | jq -r '.[] | .id')

# Loop through asset IDs and download each asset
for asset_id in $asset_ids
do
    echo "Downloading asset $asset_id..."
    curl -LOJ "https://api.github.com/repos/$owner/$repo/releases/assets/$asset_id?access_token=$GITHUB_TOKEN"
done
