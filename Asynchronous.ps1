# Define the REST API endpoint URL
$apiUrl = "https://example.com/api/your-endpoint"

# Define the JSON payload you want to send
$jsonPayload = @{
    "key1" = "value1"
    "key2" = "value2"
} | ConvertTo-Json

# Define the REST method (POST in this example) and any headers
$method = "POST"
$headers = @{
    "Authorization" = "Bearer YourAccessToken"
    "Content-Type" = "application/json"
}

# Create an instance of the HttpClient class
$httpClient = New-Object System.Net.Http.HttpClient

# Create a StringContent object for the JSON payload
$jsonContent = [System.Net.Http.StringContent]::new($jsonPayload, [System.Text.Encoding]::UTF8, "application/json")

# Add headers to the request
$headers.GetEnumerator() | ForEach-Object {
    $jsonContent.Headers.TryAddWithoutValidation($_.Key, $_.Value)
}

# Create a task to send the HTTP request asynchronously with the JSON payload
$task = $httpClient.PostAsync($apiUrl, $jsonContent)

# Continue with other tasks while the HTTP request is in progress
# ...

# Wait for the task to complete (this is optional)
# $task.Wait()

# Once the task is completed, you can access the response
$response = $task.Result

# Read the response content if needed
$responseContent = $response.Content.ReadAsStringAsync().Result

# Output or process the response content as necessary
# Write-Host $responseContent
