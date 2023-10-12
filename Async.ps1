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

# Load necessary .NET libraries
Add-Type -TypeDefinition @"
using System;
using System.Net.Http;
using System.Threading.Tasks;
"@

# Define an asynchronous function
function InvokeRestMethodAsync {
    param (
        [string]$url
    )

    $httpClient = New-Object System.Net.Http.HttpClient

    $task = [System.Threading.Tasks.Task]::Run({
        $response = $httpClient.GetAsync($url)
        $content = $response.Result.Content.ReadAsStringAsync().Result
        Write-Host "Request to $url succeeded. Response: $content"
    })

    $task.Wait()
}

# URL to make the HTTP GET request
$url = "https://jsonplaceholder.typicode.com/posts/1"  # Replace with your desired URL

# Call the asynchronous function
InvokeRestMethodAsync -url $url
