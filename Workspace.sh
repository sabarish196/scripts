#!/bin/bash

# Set your TFC organization and API token
ORG_NAME="your-organization"
API_TOKEN="your-api-token"

# Set the workspace name
WORKSPACE_NAME="your-workspace-name"

# Set the variable names and values to add/update
SECRET_KEY="my_secret"
SECRET_VALUE="my_secret_value"
ENV_VARIABLE_KEY="MY_ENV_VARIABLE"
ENV_VARIABLE_VALUE="new_value"

# Get the workspace ID
WORKSPACE_ID=$(curl -s -H "Authorization: Bearer $API_TOKEN" \
    "https://app.terraform.io/api/v2/organizations/$ORG_NAME/workspaces" | \
    jq -r ".data[] | select(.attributes.name == \"$WORKSPACE_NAME\") | .id")

if [[ -z $WORKSPACE_ID ]]; then
    echo "Workspace '$WORKSPACE_NAME' not found."
    exit 1
fi

# Add secret variable
curl -s -X POST -H "Authorization: Bearer $API_TOKEN" \
    -H "Content-Type: application/vnd.api+json" \
    -d '{
        "data": {
            "type": "vars",
            "attributes": {
                "key": "'$SECRET_KEY'",
                "value": "'$SECRET_VALUE'",
                "category": "env"
            }
        }
    }' \
    "https://app.terraform.io/api/v2/workspaces/$WORKSPACE_ID/vars"

# Update environment variable
curl -s -X PATCH -H "Authorization: Bearer $API_TOKEN" \
    -H "Content-Type: application/vnd.api+json" \
    -d '{
        "data": {
            "type": "vars",
            "attributes": {
                "key": "'$ENV_VARIABLE_KEY'",
                "value": "'$ENV_VARIABLE_VALUE'"
            }
        }
    }' \
    "https://app.terraform.io/api/v2/workspaces/$WORKSPACE_ID/vars/environment"

echo "Secret variable and environment variable updated for workspace '$WORKSPACE_NAME'."
