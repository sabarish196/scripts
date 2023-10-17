# Import Azure PowerShell module
Import-Module Az

# Sign in to your Azure account
Connect-AzAccount

# Replace these with your VMSS details
$resourceGroupName = "<ResourceGroupName>"
$vmssName = "<VMSSName>"

# Get the VMSS instance details
$vmss = Get-AzVmss -ResourceGroupName $resourceGroupName -VMScaleSetName $vmssName

# Get the VMSS instances
$vmssInstances = Get-AzVmssVM -ResourceGroupName $resourceGroupName -VMScaleSetName $vmssName

# Initialize variables to count running and total instances
$runningInstances = 0
$totalInstances = $vmssInstances.Count

# Check each instance for its power state
foreach ($instance in $vmssInstances) {
    if ($instance.PowerState -eq "VM running") {
        $runningInstances++
    }
}

# Determine if the VMSS is started or stopped
if ($runningInstances -eq $totalInstances) {
    Write-Host "VMSS is started. All instances are running."
} elseif ($runningInstances -eq 0) {
    Write-Host "VMSS is stopped. No instances are running."
} else {
    Write-Host "VMSS is partially started. $runningInstances out of $totalInstances instances are running."
}
