$infobloxServer = "https://infoblox.example.com" # Replace with your Infoblox server URL
$username = "admin" # Replace with your Infoblox username
$password = "password" # Replace with your Infoblox password

$filePath = "path/to/file.txt" # Replace with the actual file path

# Read the file content
$fileContent = Get-Content -Path $filePath

# Process non-empty lines
$fileContent | ForEach-Object {
    $line = $_

    # Skip empty lines or lines with only whitespace
    if (![string]::IsNullOrWhiteSpace($line)) {
        # Split the line using regular expression to handle multiple spaces
        $lineData = $line -split '\s+'
        $hostname = $lineData[0]
        $ip = $lineData[1]
        $newIP = $lineData[2]

        # Construct the REST API endpoint for A record
        $endpoint = "$infobloxServer/wapi/v2.11/record:a"

        # Construct the JSON payload for the A record
        $recordData = @{
            "name" = $hostname
            "ipv4addr" = $newIP
        } | ConvertTo-Json

        try {
            # Send HTTP request to create/update A record
            if (Test-Path "$endpoint/$hostname") {
                # Update A record
                Invoke-RestMethod -Uri "$endpoint/$hostname" -Method Put -Headers @{ "Content-Type" = "application/json" } -Credential (Get-Credential -UserName $username -Password $password) -Body $recordData
                Write-Host "Updated A record for $hostname with IP $newIP"
            } else {
                # Create A record
                Invoke-RestMethod -Uri $endpoint -Method Post -Headers @{ "Content-Type" = "application/json" } -Credential (Get-Credential -UserName $username -Password $password) -Body $recordData
                Write-Host "Created A record for $hostname with IP $newIP"
            }
        } catch {
            Write-Host "Error occurred while creating/updating A record for $hostname: $_"
        }
    }
}
