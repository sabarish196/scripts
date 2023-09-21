# Get the current date and time
$currentDateTime = Get-Date
$currentDay = $currentDateTime.DayOfWeek
$currentTime = $currentDateTime.ToString("HH:mm:ss")

# Check if it's a weekend (Saturday or Sunday)
if ($currentDay -eq "Saturday" -or $currentDay -eq "Sunday") {
    # Check if it's after Friday 6:00 PM (18:00)
    if ($currentDay -eq "Sunday" -or ($currentDay -eq "Friday" -and $currentTime -ge "18:00:00")) {
        Write-Output "Starting VMs for the week"
        # Add logic to start VMs here
    } else {
        Write-Output "Weekend: Skipping start-stop actions"
    }
} else {
    # Check if it's before Monday 4:00 AM (04:00)
    if ($currentTime -lt "04:00:00") {
        Write-Output "Stopping VMs for the weekend"
        # Add logic to stop VMs here
    } else {
        Write-Output "Weekday: Skipping start-stop actions"
    }
}
