$infobloxServer = "https://infoblox.example.com" # Replace with your Infoblox server URL
$username = "admin" # Replace with your Infoblox username
$password = "password" # Replace with your Infoblox password

$hostname = "example.com" # Replace with the desired hostname

# Construct the REST API endpoint for the A record
$endpoint = "$infobloxServer/wapi/v2.11/record:a"

try {
    # Send HTTP GET request to retrieve the A record
    $record = Invoke-RestMethod -Uri "$endpoint?name=$hostname" -Method Get -Credential (Get-Credential -UserName $username -Password $password)

    # Extract the relevant information from the response
    $ipAddress = $record.ipv4addr
    $canonicalName = $record.canonical

    # Display the retrieved A record information
    Write-Host "Hostname: $hostname"
    Write-Host "IP Address: $ipAddress"
    Write-Host "Canonical Name: $canonicalName"
} catch {
    Write-Host "Error occurred while retrieving the A record for $hostname: $_"
}
