#!/bin/bash

# Set your Terraform Cloud organization, API token, and workspace name
ORG_NAME="your-organization"
API_TOKEN="your-api-token"
WORKSPACE_NAME="your-workspace-name"

# Set the variable name and updated value
VARIABLE_NAME="variable_name"
UPDATED_VALUE="new_value"

# Get the workspace ID
WORKSPACE_ID=$(curl -s -H "Authorization: Bearer $API_TOKEN" \
    "https://app.terraform.io/api/v2/organizations/$ORG_NAME/workspaces" | \
    grep -o "\"id\":\"[^\"]*\"" | grep -o "[^\"]*" | paste - - | grep "$WORKSPACE_NAME" | cut -f 2)

if [[ -z $WORKSPACE_ID ]]; then
    echo "Workspace '$WORKSPACE_NAME' not found."
    exit 1
fi

# Get the variable ID
VARIABLE_ID=$(curl -s -H "Authorization: Bearer $API_TOKEN" \
    "https://app.terraform.io/api/v2/workspaces/$WORKSPACE_ID/vars" | \
    grep -o "\"id\":\"[^\"]*\",\"key\":\"$VARIABLE_NAME\"" | grep -o "\"id\":\"[^\"]*\"" | grep -o "[^\"]*")

if [[ -z $VARIABLE_ID ]]; then
    echo "Variable '$VARIABLE_NAME' not found in workspace '$WORKSPACE_NAME'."
    exit 1
fi

# Update the variable value
curl -s -X PATCH -H "Authorization: Bearer $API_TOKEN" \
    -H "Content-Type: application/vnd.api+json" \
    -d '{
        "data": {
            "type": "vars",
            "attributes": {
                "value": "'$UPDATED_VALUE'"
            }
        }
    }' \
    "https://app.terraform.io/api/v2/workspaces/$WORKSPACE_ID/vars/$VARIABLE_ID"

echo "Terraform variable '$VARIABLE_NAME' updated to '$UPDATED_VALUE' in workspace '$WORKSPACE_NAME'."
