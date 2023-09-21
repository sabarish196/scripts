function Invoke-ApiWithFormData {
    param(
        [string]$ApiUrl,
        [string]$ToEmails,  # Comma-separated list of email addresses
        [string]$Subject,
        [string]$HtmlBody  # HTML content for the email body
    )

    # Create a hashtable to store headers (including content type)
    $headers = @{
        'Content-Type' = 'application/x-www-form-urlencoded'
    }

    # Create a hashtable to store the form data
    $formData = @{
        'toEmails' = $ToEmails
        'subject' = $Subject
        'htmlBody' = $HtmlBody
    }

    # Convert the form data hashtable to a query string
    $formDataQueryString = $formData | ForEach-Object {
        [uri]::EscapeDataString($_.Key) + '=' + [uri]::EscapeDataString($_.Value)
    } -join '&'

    # Invoke the API with the form-data payload
    $response = Invoke-RestMethod -Uri $ApiUrl -Method Post -Headers $headers -Body $formDataQueryString

    return $response
}

# Example usage:
$apiUrl = 'https://example.com/send-email-api'
$toEmails = 'email1@example.com,email2@example.com,email3@example.com'
$subject = 'Test Subject'
$htmlBody = '<html><body><h1>This is an HTML email</h1><p>Hello, World!</p></body></html>'

$response = Invoke-ApiWithFormData -ApiUrl $apiUrl -ToEmails $toEmails -Subject $subject -HtmlBody $htmlBody
