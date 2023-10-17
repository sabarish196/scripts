# Import Azure PowerShell module
Import-Module Az

# Sign in to your Azure account
Connect-AzAccount

# Replace with the name of your AKS cluster and resource group
$resourceGroupName = "<YourResourceGroupName>"
$clusterName = "<YourClusterName>"

# Check the current state of the AKS cluster
$aksCluster = Get-AzAks -ResourceGroupName $resourceGroupName -Name $clusterName

# Check if the cluster is in a running state
if ($aksCluster.ProvisioningState -eq "Succeeded" -and $aksCluster.AgentPoolProfiles[0].PowerState -eq "Running") {
    # The cluster is already running, so we'll stop it
    Stop-AzAks -ResourceGroupName $resourceGroupName -Name $clusterName
    Write-Host "Stopping AKS cluster..."
} else {
    # The cluster is not running, so we'll start it
    Start-AzAks -ResourceGroupName $resourceGroupName -Name $clusterName
    Write-Host "Starting AKS cluster..."
}

# Get the current state of the AKS cluster
$aksCluster = Get-AzAks -ResourceGroupName $resourceGroupName -Name $clusterName

# Display the status of the AKS cluster
Write-Host "AKS Cluster Status: $($aksCluster.ProvisioningState)"
