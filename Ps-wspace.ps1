# Set your Terraform Cloud organization, API token, and workspace name
$orgName = "your-organization"
$apiToken = "your-api-token"
$workspaceName = "your-workspace-name"

# Set the variable name, value, and category (optional)
$variableKey = "new_variable"
$variableValue = "variable_value"
$variableCategory = "terraform" # Replace with "env" if needed

# Get the workspace ID
$headers = @{
    Authorization = "Bearer $apiToken"
}

$workspaceResponse = Invoke-RestMethod -Uri "https://app.terraform.io/api/v2/organizations/$orgName/workspaces" -Headers $headers
$workspace = $workspaceResponse.data | Where-Object { $_.attributes.name -eq $workspaceName }

if (!$workspace) {
    Write-Host "Workspace '$workspaceName' not found."
    exit 1
}

$workspaceId = $workspace.id

# Add the Terraform variable
$variableBody = @{
    data = @{
        type = "vars"
        attributes = @{
            key = $variableKey
            value = $variableValue
            category = $variableCategory
        }
    }
}

$addVariableResponse = Invoke-RestMethod -Uri "https://app.terraform.io/api/v2/workspaces/$workspaceId/vars" -Headers $headers -Method Post -ContentType "application/vnd.api+json" -Body ($variableBody | ConvertTo-Json)

if ($addVariableResponse.status -eq 201) {
    Write-Host "Terraform variable '$variableKey' added to workspace '$workspaceName'."
} else {
    Write-Host "Error adding Terraform variable:", $addVariableResponse.errors
}
