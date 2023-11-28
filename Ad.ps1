# Import the Active Directory module
Import-Module ActiveDirectory

# Specify the Organizational Unit (OU) path for Service Accounts
$ouPath = "OU=Service Account,DC=yourdomain,DC=com"

# Get all service accounts within the specified OU
$serviceAccounts = Get-ADUser -Filter * -SearchBase $ouPath -SearchScope OneLevel -Properties *

# Loop through each service account
foreach ($account in $serviceAccounts) {
    # Check if login shell is "/bin/bash" (replace 'LoginShellAttribute' with the actual attribute)
    $loginShell = $account.LoginShellAttribute

    if ($loginShell -eq "/bin/bash") {
        # Display account name if the login shell is "/bin/bash"
        Write-Host "Account with /bin/bash: $($account.Name)"
    }
}
