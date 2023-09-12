function Send-JsonPayloadToAzureQueue {
    # Hardcoded parameters
    $StorageAccountName = "yourstorageaccountname"
    $QueueName = "yourqueuename"
    $JsonPayload = '{"key1": "value1", "key2": "value2"}'

    # Connect to your Azure account (you may need to log in)
    Connect-AzAccount

    # Get the storage account context
    $storageContext = (Get-AzStorageAccount -ResourceGroupName "yourResourceGroupName" -Name $StorageAccountName).Context

    # Create a message from the JSON payload
    $message = New-Object -TypeName Microsoft.WindowsAzure.Storage.Queue.CloudQueueMessage -ArgumentList $JsonPayload

    # Get the Azure Storage Queue
    $queue = Get-AzStorageQueue -Name $QueueName -Context $storageContext

    # Add the message to the queue
    $queue.CloudQueue.AddMessage($message)

    Write-Host "JSON payload added to the Azure Queue: $QueueName"
}

# Call the function
Send-JsonPayloadToAzureQueue
