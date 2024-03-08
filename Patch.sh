export WORKSPACE_ID=<your_workspace_id>
export TOKEN=<your_api_token>
export NEW_TERRAFORM_VERSION="0.15.5"

curl -X PATCH \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/vnd.api+json" \
     -d "{\"data\":{\"type\":\"workspaces\",\"attributes\":{\"terraform-version\":\"$NEW_TERRAFORM_VERSION\"}}}" \
     https://app.terraform.io/api/v2/workspaces/$WORKSPACE_ID



export TOKEN=<your_api_token>

curl -X GET \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/vnd.api+json" \
     "https://app.terraform.io/api/v2/organizations/<organization_name>/workspaces?page[size]=100" \
     | jq '.data[] | select(.attributes.name | startswith("Azure-seia")) | .attributes.name'
