function Invoke-ApiWithFormDataAndBasicAuth {
    param(
        [string]$ApiUrl,
        [string]$ToEmails,  # Comma-separated list of email addresses
        [string]$Subject,
        [string]$HtmlBody,  # HTML content for the email body
        [string]$Username,
        [securestring]$Password
    )

    # Create a hashtable to store headers (including content type)
    $headers = @{
        'Content-Type' = 'multipart/form-data'
    }

    # Create a hashtable to store the form data
    $formData = @{
        'toEmails' = $ToEmails
        'subject' = $Subject
        'htmlBody' = $HtmlBody
    }

    # Create a boundary for the multipart form-data
    $boundary = [System.Guid]::NewGuid().ToString()

    # Create the multipart form-data content
    $formDataContent = $formData.GetEnumerator() | ForEach-Object {
        "--$boundary`r`n"
        "Content-Disposition: form-data; name=`"$($_.Key)`"`r`n"
        "`r`n$($_.Value)`r`n"
    }

    # Add a closing boundary
    $formDataContent += "--$boundary--"

    # Convert the form-data content to bytes
    $formDataBytes = [System.Text.Encoding]::UTF8.GetBytes($formDataContent)

    # Create a credential object for Basic Authentication
    $credential = New-Object System.Management.Automation.PSCredential ($Username, $Password)

    # Invoke the API with Basic Authentication and the form-data payload
    $response = Invoke-RestMethod -Uri $ApiUrl -Method Post -Headers $headers -ContentType "multipart/form-data; boundary=$boundary" -InFile $formDataBytes -Credential $credential

    return $response
}

# Example usage:
$apiUrl = 'https://example.com/send-email-api'
$toEmails = 'email1@example.com,email2@example.com,email3@example.com'
$subject = 'Test Subject'
$username = 'your_username'
$password = ConvertTo-SecureString 'your_password' -AsPlainText -Force

# Define HTML body with variables
$htmlBody = @"
<html>
<body>
<h1>$subject</h1>
<p>Hello, World! Sending this email to: $toEmails</p>
</body>
</html>
"@

$response = Invoke-ApiWithFormDataAndBasicAuth -ApiUrl $apiUrl -ToEmails $toEmails -Subject $subject -HtmlBody $htmlBody -Username $username -Password $password
