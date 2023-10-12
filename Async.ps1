async function InvokeRestMethodAsync {
    param (
        [string]$url
    )

    try {
        $response = await Invoke-RestMethod -Uri $url -Method Get
        Write-Host "Request to $url succeeded. Response: $($response | ConvertTo-Json -Depth 1)"
    } catch {
        Write-Host "Request to $url failed. Error: $($_.Exception.Message)"
    }
}

# Example usage
$url = "https://jsonplaceholder.typicode.com/posts/1" # Replace with your desired URL
InvokeRestMethodAsync -url $url
