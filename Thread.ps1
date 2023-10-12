# Import the PSThreadJob module
Import-Module PSThreadJob

# Define a function to make an asynchronous REST request
function Invoke-RestApiAsync {
    param (
        [string]$url,
        [string]$method,
        [object]$body,
        [string]$contentType
    )

    $scriptBlock = {
        param (
            $url,
            $method,
            $body,
            $contentType
        )

        # Convert the body to JSON
        $bodyJson = $body | ConvertTo-Json

        # Create an HTTP request with custom headers
        $headers = @{
            'Content-Type' = $contentType
        }

        $response = Invoke-RestMethod -Uri $url -Method $method -Body $bodyJson -Headers $headers
        $response
    }

    # Start the REST request as a thread job
    $job = Start-ThreadJob -ScriptBlock $scriptBlock -ArgumentList $url, $method, $body, $contentType

    return $job
}

# URL for the REST API request
$url = "https://jsonplaceholder.typicode.com/posts/1"
$method = "POST"  # Replace with the desired HTTP method
$body = @{ 'key' = 'value' }  # Replace with your request body
$contentType = "application/json"  # Customize the content type as needed

# Call the function asynchronously
$job = Invoke-RestApiAsync -url $url -method $method -body $body -contentType $contentType

# Continue with other tasks without waiting for the response

# Clean up the job when done
$job | Wait-ThreadJob
$result = $job | Receive-ThreadJob

# Process the response as needed
Write-Host "Response: $($result | ConvertTo-Json -Depth 1)"
$job | Remove-ThreadJob
