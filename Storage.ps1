function Upload-JsonPayloadToAzureStorage {
    param (
        [string]$StorageAccountName,
        [string]$ContainerName,
        [string]$BlobName,
        [string]$JsonPayload,
        [string]$ResourceGroupName
    )

    # Connect to your Azure account (you may need to log in)
    Connect-AzAccount

    # Convert the JSON payload to bytes
    $jsonBytes = [System.Text.Encoding]::UTF8.GetBytes($JsonPayload)

    # Create a new container (if it doesn't exist)
    $container = Get-AzStorageContainer -Name $ContainerName -Context (Get-AzStorageAccount -ResourceGroupName $ResourceGroupName -AccountName $StorageAccountName).Context
    if (!$container) {
        $container = New-AzStorageContainer -Name $ContainerName -Context (Get-AzStorageAccount -ResourceGroupName $ResourceGroupName -AccountName $StorageAccountName).Context
    }

    # Upload the JSON payload to the storage container
    $blob = Set-AzStorageBlobContent -Container $ContainerName -Blob $BlobName -BlobType Block -Context (Get-AzStorageAccount -ResourceGroupName $ResourceGroupName -AccountName $StorageAccountName).Context -InputObject $jsonBytes -Force

    # Output the URL to the uploaded JSON blob
    $blobUrl = $blob.ICloudBlob.Uri.AbsoluteUri
    Write-Host "Uploaded JSON blob URL: $blobUrl"
}

# Example usage:
# Upload-JsonPayloadToAzureStorage -StorageAccountName "yourstorageaccountname" -ContainerName "yourcontainername" -BlobName "yourblobname.json" -JsonPayload '{"key1": "value1", "key2": "value2"}' -ResourceGroupName "yourResourceGroupName"
