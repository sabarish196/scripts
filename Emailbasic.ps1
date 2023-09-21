# Define the API endpoint URL
$apiUrl = "https://example.com/api/endpoint"

# Create a Hashtable for the FormData payload
$formData = @{
    "key1" = "value1"
    "key2" = "value2"
}

# Define your Basic Authentication credentials (username and password)
$username = "your_username"
$password = "your_password"

# Convert the credentials to Base64
$base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("${username}:${password}")))

# Create headers with Basic Authentication
$headers = @{
    "Authorization" = "Basic $base64AuthInfo"
}

# Send the POST request with the FormData payload and Basic Authentication
$response = Invoke-RestMethod -Uri $apiUrl -Method Post -Headers $headers -FormData $formData

# Output the response (optional)
$response
